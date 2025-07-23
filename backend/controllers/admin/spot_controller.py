from flask import jsonify
from models.parking_spot import ParkingSpot
from models.user import User
from models.reservation import Reservation
from datetime import datetime, timezone
from app import db


class SpotController:

    # Current Spot Status
    def current_spot_status(self, lot_id):
        try:
            now = datetime.now(timezone.utc)
            spots = ParkingSpot.query.filter_by(lot_id=lot_id).all()
            result = []

            for spot in spots:
                current_reservation = next(
                    (r for r in spot.reservations if r.reserved_at and r.reserved_till and r.reserved_at <= now <= r.reserved_till),
                    None
                )

                reservation_info = None
                if current_reservation:
                    reservation_info = {
                        "user_id": current_reservation.user_id,
                        "reserved_at": current_reservation.reserved_at.astimezone(timezone.utc).isoformat(),
                        "reserved_till": current_reservation.reserved_till.astimezone(timezone.utc).isoformat(),
                    }

                result.append({
                    "spot_id": spot.id,
                    "status": "Reserved" if current_reservation else "Available",
                    "reservation": reservation_info,
                })

            return jsonify({"spots": result}), 200

        except Exception as e:
            db.session.rollback()
            return jsonify({"msg": "Failed to fetch spot status", "error": str(e)}), 500


    # Spot Reservation History
    def get_spot_history(self, spot_id):
        try:
            spot = ParkingSpot.query.get_or_404(spot_id)
            reservations = Reservation.query.filter_by(spot_id=spot_id).order_by(Reservation.reserved_at.desc()).all()

            history = []
            for reservation in reservations:
                user = User.query.get(reservation.user_id)
                if not user:
                    continue  # skip if user data is not found

                reserved_at = reservation.reserved_at.astimezone(timezone.utc).isoformat() if reservation.reserved_at else None
                reserved_till = reservation.reserved_till.astimezone(timezone.utc).isoformat() if reservation.reserved_till else None
                parking_ts = reservation.parking_timestamp.astimezone(timezone.utc).isoformat() if reservation.parking_timestamp else None
                leaving_ts = reservation.leaving_timestamp.astimezone(timezone.utc).isoformat() if reservation.leaving_timestamp else None

                if reservation.leaving_timestamp:
                    status = "Completed"
                elif reservation.parking_timestamp:
                    status = "In Progress"
                else:
                    status = "Reserved"

                duration_minutes = None
                if reservation.reserved_at and reservation.reserved_till:
                    duration_minutes = (reservation.reserved_till - reservation.reserved_at).total_seconds() / 60

                history.append({
                    "reservation_id": reservation.id,
                    "user_id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "reserved_at": reserved_at,
                    "reserved_till": reserved_till,
                    "parking_timestamp": parking_ts,
                    "leaving_timestamp": leaving_ts,
                    "status": status,
                    "duration_minutes": round(duration_minutes, 2) if duration_minutes else None
                })

            return jsonify({
                "spot_id": spot.id,
                "lot_id": spot.lot_id,
                "history": history
            }), 200

        except Exception as e:
            db.session.rollback()
            return jsonify({"msg": "Failed to fetch spot history", "error": str(e)}), 500
