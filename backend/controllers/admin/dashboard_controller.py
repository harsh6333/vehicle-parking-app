from flask import jsonify
from models.parking_lot import ParkingLot
from models.parking_spot import ParkingSpot
from models.user import User
from models.reservation import Reservation
from app import db
from sqlalchemy import func, and_
from datetime import datetime, timedelta, timezone


class DashboardController:

    # Dashboard Summary
    def admin_dashboard_summary(self):
        try:
            latest_lots = ParkingLot.query.order_by(ParkingLot.id.desc()).limit(5).all()
            lots_data = [{
                "id": lot.id,
                "prime_location_name": lot.prime_location_name,
                "address": lot.address,
                "price": lot.price,
                "number_of_spots": lot.number_of_spots
            } for lot in latest_lots]

            latest_reservations = Reservation.query.order_by(Reservation.reserved_at.desc()).limit(5).all()
            reservation_data = [{
                "reservation_id": r.id,
                "user_id": r.user_id,
                "spot_id": r.spot_id,
                "reserved_at": r.reserved_at.astimezone(timezone.utc).isoformat() if r.reserved_at else None,
                "reserved_till": r.reserved_till.astimezone(timezone.utc).isoformat() if r.reserved_till else None,
                "parking_timestamp": r.parking_timestamp.astimezone(timezone.utc).isoformat() if r.parking_timestamp else None,
                "leaving_timestamp": r.leaving_timestamp.astimezone(timezone.utc).isoformat() if r.leaving_timestamp else None,
            } for r in latest_reservations]

            latest_users = User.query.order_by(User.id.desc()).limit(5).all()
            users_data = [{
                "id": u.id,
                "username": u.username,
                "email": u.email,
                "is_admin": u.is_admin
            } for u in latest_users]

            total_lots = db.session.query(func.count(ParkingLot.id)).scalar()
            total_spots = db.session.query(func.count(ParkingSpot.id)).scalar()
            total_users = db.session.query(func.count(User.id)).scalar()

            reservations = Reservation.query.all()
            total_earnings = 0.0

            for r in reservations:
                if r.reserved_at and r.reserved_till and r.spot and r.spot.lot:
                    duration = (r.reserved_till - r.reserved_at).total_seconds() / 3600
                    total_earnings += duration * r.spot.lot.price

            return jsonify({
                "latest_lots": lots_data,
                "latest_reservations": reservation_data,
                "latest_users": users_data,
                "stats": {
                    "total_lots": total_lots,
                    "total_spots": total_spots,
                    "total_users": total_users,
                    "total_earnings": round(total_earnings, 2)
                }
            }), 200

        except Exception as e:
            db.session.rollback()
            return jsonify({"msg": "Error fetching dashboard data", "error": str(e)}), 500


    # Weekly Trends & Totals
    def get_admin_stats(self):
        try:
            today = datetime.utcnow().date()
            labels = []
            parking_counts = []
            revenue_sums = []

            for i in range(7):
                day = today - timedelta(days=6 - i)
                start = datetime.combine(day, datetime.min.time())
                end = start + timedelta(days=1)

                labels.append(day.strftime('%b %d'))

                count = db.session.query(func.count(Reservation.id)).filter(
                    Reservation.reserved_at.between(start, end)
                ).scalar()

                revenue = db.session.query(
                    func.coalesce(func.sum(Reservation.parking_cost), 0)
                ).filter(
                    Reservation.reserved_at.between(start, end)
                ).scalar()

                parking_counts.append(count)
                revenue_sums.append(float(revenue))

            totals = {
                'users': db.session.query(func.count(User.id)).scalar(),
                'lots': db.session.query(func.count(ParkingLot.id)).scalar(),
                'spots': db.session.query(func.count(ParkingSpot.id)).scalar(),
                'activeReservations': db.session.query(func.count(Reservation.id)).filter(
                    and_(
                        Reservation.reserved_at <= datetime.utcnow(),
                        Reservation.reserved_till >= datetime.utcnow()
                    )
                ).scalar()
            }

            return jsonify({
                "parking": {"labels": labels, "values": parking_counts},
                "revenue": {"labels": labels, "values": revenue_sums},
                "totals": totals
            }), 200

        except Exception as e:
            db.session.rollback()
            return jsonify({"msg": "Error fetching statistics", "error": str(e)}), 500
