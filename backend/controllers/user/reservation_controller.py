from flask import request, jsonify
from flask_jwt_extended import get_jwt_identity
from datetime import datetime, timedelta, timezone
from app import db
from models.parking_spot import ParkingSpot
from models.reservation import Reservation
from utils.datetimeformate import parse_iso_datetime
from extensions import cache
from sqlalchemy.exc import SQLAlchemyError


class ReservationController:
    # Reserve Spot
    def reserve_spot(self):
        try:
            data = request.json
            spot_id = data.get("spot_id")
            start_time_str = data.get("start_time")
            duration_hours = int(data.get("duration_hours", 1))
            user_id = get_jwt_identity()

            if not spot_id or not start_time_str:
                return jsonify({"error": "Missing spot_id or start_time"}), 400

            try:
                start_time = parse_iso_datetime(start_time_str)
            except ValueError:
                return jsonify({"error": "Invalid start_time format"}), 400

            end_time = start_time + timedelta(hours=duration_hours)

            # Overlap check
            overlapping = Reservation.query.filter(
                Reservation.spot_id == spot_id,
                Reservation.reserved_at < end_time,
                Reservation.reserved_till > start_time,
                Reservation.leaving_timestamp == None
            ).first()

            if overlapping:
                return jsonify({"error": "Spot already reserved during this time"}), 409

            spot = ParkingSpot.query.get_or_404(spot_id)
            lot = spot.lot
            price_per_hour = lot.price
            cost = price_per_hour * duration_hours

            new_res = Reservation(
                user_id=user_id,
                spot_id=spot_id,
                reserved_at=start_time,
                reserved_till=end_time,
                parking_cost=cost
            )

            db.session.add(new_res)
            db.session.commit()

            cache.delete(f"user_history_{user_id}")
            cache.delete(f"user_stats_{user_id}")
            cache.delete(f"user_lot_{spot.lot_id}_spots_{start_time.date().isoformat()}")

            return jsonify({
                "reservation_id": new_res.id,
                "spot_id": spot_id,
                "reserved_at": new_res.reserved_at.isoformat() + "Z",
                "reserved_till": new_res.reserved_till.isoformat() + "Z",
                "parking_cost": new_res.parking_cost
            }), 200

        except SQLAlchemyError as e:
            db.session.rollback()
            return jsonify({"error": "Database error", "details": str(e)}), 500
        except Exception as e:
            return jsonify({"error": "Internal server error", "details": str(e)}), 500

    # Occupy Spot

    def occupy_spot(self, spot_id):
        try:
            user_id = int(get_jwt_identity())
            data = request.json
            reserved_at_str = data.get("reserved_at")

            if not reserved_at_str:
                return jsonify({"msg": "Missing reserved_at"}), 400

            try:
                reserved_at = parse_iso_datetime(reserved_at_str)
            except ValueError:
                return jsonify({"msg": "Invalid reserved_at format"}), 400

            # Make reserved_at timezone-aware if not already
            if reserved_at.tzinfo is None:
                reserved_at = reserved_at.replace(tzinfo=timezone.utc)

            reservation = Reservation.query.filter_by(
                user_id=user_id,
                spot_id=spot_id,
                reserved_at=reserved_at
            ).first()

            if not reservation:
                return jsonify({"msg": "No reservation found for this user and time"}), 404

            now = datetime.now(timezone.utc)

            # Ensure reservation times are timezone-aware
            if reservation.reserved_at.tzinfo is None:
                reservation.reserved_at = reservation.reserved_at.replace(tzinfo=timezone.utc)

            if reservation.reserved_till and reservation.reserved_till.tzinfo is None:
                reservation.reserved_till = reservation.reserved_till.replace(tzinfo=timezone.utc)

            if now < reservation.reserved_at:
                return jsonify({"msg": "Reservation time has not started yet"}), 400

            if now > reservation.reserved_till:
                return jsonify({"msg": "Reservation window has already ended"}), 400

            if reservation.parking_timestamp is not None:
                return jsonify({"msg": "Spot already marked as occupied"}), 400

            reservation.parking_timestamp = now
            db.session.commit()

            cache.delete(f"user_history_{user_id}")
            cache.delete(f"user_stats_{user_id}")
            cache.delete(f"user_lot_{spot_id}_spots_{reservation.reserved_at.date().isoformat()}")

            return jsonify({
                "msg": "Spot marked as occupied",
                "occupied_at": now.isoformat() + "Z"
            }), 200

        except SQLAlchemyError as e:
            db.session.rollback()
            return jsonify({"error": "Database error", "details": str(e)}), 500
        except Exception as e:
            return jsonify({"error": "Internal server error", "details": str(e)}), 500


    # Release Spot
    def release_spot(self, spot_id):
        try:
            user_id = get_jwt_identity()
            data = request.json
            reserved_at_str = data.get("reserved_at")

            if not reserved_at_str:
                return jsonify({"msg": "Missing reserved_at"}), 400

            try:
                reserved_at = parse_iso_datetime(reserved_at_str)
                print(reserved_at)
            except ValueError:
                return jsonify({"msg": "Invalid reserved_at format"}), 400
            

            reservation = Reservation.query.filter_by(
                spot_id=spot_id, reserved_at=reserved_at
            ).first()

            if not reservation:
                return jsonify({"msg": "Reservation not found"}), 404

            if reservation.leaving_timestamp is not None:
                return jsonify({"msg": "Spot already released"}), 400

            now = datetime.now(timezone.utc)
            reservation.leaving_timestamp = now
            db.session.commit()

            cache.delete(f"user_history_{user_id}")
            cache.delete(f"user_stats_{user_id}")
            cache.delete(f"user_lot_{spot_id}_spots_{reservation.reserved_at.date().isoformat()}")

            return jsonify({"message": "Spot released", "time": now.isoformat() + "Z"}), 200

        except SQLAlchemyError as e:
            db.session.rollback()
            return jsonify({"error": "Database error", "details": str(e)}), 500
        except Exception as e:
            return jsonify({"error": "Internal server error", "details": str(e)}), 500
