from flask import jsonify
from backend.models.parking_spot import ParkingSpot
from backend.models.user import User
from backend.models.reservation import Reservation
# from backend.models.vehicles import Vehicle
from sqlalchemy.orm import joinedload
from backend import db


class UserController:
    # User List with Stats + Vehicle Details
    def list_users(self):
        try:
            users = User.query.options(
                joinedload(User.reservations)
                .joinedload(Reservation.spot)
                .joinedload(ParkingSpot.lot),
                joinedload(User.vehicles)
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

                vehicles = []
                for v in u.vehicles:
                    vehicles.append({
                        "vehicle_number": v.vehicle_number,
                        "vehicle_type": v.vehicle_type,
                        "brand": v.brand,
                        "color": v.color,
                        "created_at": v.created_at.isoformat() + "Z" if v.created_at else None
                    })

                result.append({
                    "username": u.username,
                    "email": u.email,
                    "is_admin": u.is_admin,
                    "total_reservations": len(u.reservations),
                    "total_parked_hours": round(total_hours, 2),
                    "total_parking_cost": round(total_cost, 2),
                    "vehicles": vehicles
                })

            return jsonify(result), 200

        except Exception as e:
            db.session.rollback()
            return jsonify({"msg": "Error fetching user data", "error": str(e)}), 500
