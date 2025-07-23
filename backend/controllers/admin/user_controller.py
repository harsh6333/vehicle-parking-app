from flask import jsonify
from models.parking_spot import ParkingSpot
from models.user import User
from models.reservation import Reservation
from sqlalchemy.orm import joinedload
from app import db


class UserController:
    # User List with Stats
    def list_users(self):
        try:
            users = User.query.options(
                joinedload(User.reservations)
                .joinedload(Reservation.spot)
                .joinedload(ParkingSpot.lot)
            ).all()

            result = []

            for u in users:
                total_hours = 0
                total_cost = 0

                for r in u.reservations:
                    start = r.parking_timestamp or r.reserved_at
                    end = r.leaving_timestamp or r.reserved_till

                    if start and end and end > start:
                        duration_hours = (end - start).total_seconds() / 3600
                        total_hours += duration_hours

                        if r.spot and r.spot.lot and r.spot.lot.price is not None:
                            total_cost += duration_hours * float(r.spot.lot.price)

                result.append({
                    "username": u.username,
                    "email": u.email,
                    "is_admin": u.is_admin,
                    "total_reservations": len(u.reservations),
                    "total_parked_hours": round(total_hours, 2),
                    "total_parking_cost": round(total_cost, 2),
                })

            return jsonify(result), 200

        except Exception as e:
            db.session.rollback()
            return jsonify({"msg": "Error fetching user data", "error": str(e)}), 500
