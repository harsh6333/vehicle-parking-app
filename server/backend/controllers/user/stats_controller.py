from collections import defaultdict
from flask import jsonify
from flask_jwt_extended import get_jwt_identity
from backend.models.parking_lot import ParkingLot
from backend.models.parking_spot import ParkingSpot
from backend.models.reservation import Reservation
from sqlalchemy.exc import SQLAlchemyError


class StatsController:
    # Get User Reservation History
    def get_history(self):
        try:
            user_id = get_jwt_identity()

            reservations = Reservation.query.filter_by(user_id=user_id)\
                .order_by(Reservation.reserved_at.desc())\
                .all()

            history = []
            for r in reservations:
                try:
                    history.append({
                        "id": r.id,
                        "spot_id": r.spot_id,
                        "reserved_at": r.reserved_at.isoformat() + "Z" if r.reserved_at else None,
                        "reserved_till": r.reserved_till.isoformat() + "Z" if r.reserved_till else None,
                        "parking_timestamp": r.parking_timestamp.isoformat() + "Z" if r.parking_timestamp else None,
                        "leaving_timestamp": r.leaving_timestamp.isoformat() + "Z" if r.leaving_timestamp else None,
                        "hourlyrate": r.parking_cost if r.parking_cost is not None else 0.0,
                        "address": (
                            f"{r.spot.lot.prime_location_name}, {r.spot.lot.address}"
                            if r.spot and r.spot.lot else None
                        )
                    })
                except Exception as e:
                    # Log partial entry failure but continue others
                    continue

            return jsonify(history), 200

        except SQLAlchemyError as db_err:
            return jsonify({"error": "Database error while fetching reservation history.", "details": str(db_err)}), 500
        except Exception as e:
            return jsonify({"error": "Unexpected error in get_history", "details": str(e)}), 500

    # Get Daily User Stats (Revenue + Duration)
    def get_user_stats(self):
        try:
            user_id = get_jwt_identity()

            reservations = Reservation.query.filter_by(user_id=user_id)\
                .join(ParkingSpot)\
                .join(ParkingLot)\
                .order_by(Reservation.reserved_at.asc())\
                .all()

            dates = []
            hours = []
            revenue = []

            for res in reservations:
                try:
                    if res.reserved_at and res.reserved_till and res.spot and res.spot.lot:
                        duration = (res.reserved_till - res.reserved_at).total_seconds() / 3600
                        amount = duration * res.spot.lot.price

                        dates.append(res.reserved_at.date().isoformat())
                        hours.append(round(duration, 2))
                        revenue.append(round(amount, 2))
                except Exception:
                    continue  # skip if invalid

            return jsonify({
                "dates": dates,
                "hours": hours,
                "revenue": revenue
            }), 200

        except SQLAlchemyError as db_err:
            return jsonify({"error": "Database error while computing stats.", "details": str(db_err)}), 500
        except Exception as e:
            return jsonify({"error": "Unexpected error in get_user_stats", "details": str(e)}), 500
