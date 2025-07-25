from flask import request, jsonify
from datetime import datetime, timedelta, timezone
from backend import db
from backend.models.parking_lot import ParkingLot
from backend.models.parking_spot import ParkingSpot
from sqlalchemy.orm import joinedload
from zoneinfo import ZoneInfo
import logging

IST = timezone(timedelta(hours=5, minutes=30))
KOLKATA = ZoneInfo("Asia/Kolkata")

class SpotController:
    # Get all lots with optional date-based reservations
    def get_lots(self):
        date_str = request.args.get("date")
        selected_date = None

        if date_str:
            try:
                selected_date = datetime.strptime(date_str, "%Y-%m-%d").date()
            except ValueError:
                return jsonify({"msg": "Invalid date format. Use YYYY-MM-DD"}), 400

        try:
            lots = ParkingLot.query.all()
        except Exception as e:
            logging.exception("Failed to fetch parking lots")
            return jsonify({"msg": "Internal server error while fetching lots."}), 500

        response = []
        for lot in lots:
            lot_data = {
                "id": lot.id,
                "prime_location_name": lot.prime_location_name,
                "address": lot.address,
                "pin_code": lot.pin_code,
                "price": float(lot.price),
                "total_spots": lot.number_of_spots,
            }

            if selected_date:
                lot_data["spots"] = []
                for spot in lot.spots:
                    reservations_on_date = []
                    for r in spot.reservations:
                        try:
                            reserved_at = r.reserved_at
                            if reserved_at.tzinfo is None:
                                reserved_at = reserved_at.replace(tzinfo=timezone.utc)

                            if reserved_at.astimezone(KOLKATA).date() == selected_date:
                                reservations_on_date.append({
                                    "reserved_at": r.reserved_at.isoformat() + "Z",
                                    "reserved_till": r.reserved_till.isoformat() + "Z",
                                    "parking_timestamp": r.parking_timestamp.isoformat() + "Z" if r.parking_timestamp else None,
                                    "leaving_timestamp": r.leaving_timestamp.isoformat() + "Z" if r.leaving_timestamp else None,
                                })
                        except Exception as e:
                            logging.warning(f"Skipping malformed reservation (ID: {r.id}): {e}")
                            continue

                    lot_data["spots"].append({
                        "spot_id": spot.id,
                        "reservations": reservations_on_date
                    })

            response.append(lot_data)

        return jsonify(response), 200

    # Get spot details for a specific lot and date
    def spot_details(self, lot_id):
        date_str = request.args.get("date")
        selected_date = datetime.now(KOLKATA).date()

        if date_str:
            try:
                selected_date = datetime.strptime(date_str, "%Y-%m-%d").date()
            except ValueError:
                return jsonify({"msg": "Invalid date format. Use YYYY-MM-DD"}), 400

        try:
            lot = ParkingLot.query.get(lot_id)
        except Exception as e:
            logging.exception("Error fetching parking lot")
            return jsonify({"msg": "Internal server error while fetching parking lot."}), 500

        if not lot:
            return jsonify({"msg": "Parking lot not found"}), 404

        try:
            spots = ParkingSpot.query.filter_by(lot_id=lot_id).options(
                joinedload(ParkingSpot.reservations)
            ).all()
        except Exception as e:
            logging.exception("Error fetching spots")
            return jsonify({"msg": "Internal server error while fetching spots."}), 500

        lot_data = {
            "id": lot.id,
            "prime_location_name": lot.prime_location_name,
            "address": lot.address,
            "pin_code": lot.pin_code,
            "price": float(lot.price),
            "total_spots": lot.number_of_spots,
        }

        result = []
        for spot in spots:
            reservations = []
            for r in spot.reservations:
                try:
                    reserved_at = r.reserved_at
                    if reserved_at.tzinfo is None:
                        reserved_at = reserved_at.replace(tzinfo=timezone.utc)

                    reserved_ist = reserved_at.astimezone(KOLKATA)
                    if reserved_ist.date() == selected_date:
                        reservations.append({
                            "id": r.id,
                            "user_id": r.user_id,
                            "reserved_at": r.reserved_at.isoformat() + "Z",
                            "reserved_till": r.reserved_till.isoformat() + "Z",
                            "parking_timestamp": r.parking_timestamp.isoformat() + "Z" if r.parking_timestamp else None,
                            "leaving_timestamp": r.leaving_timestamp.isoformat() + "Z" if r.leaving_timestamp else None,
                            "status": "occupied" if r.parking_timestamp else "reserved"
                        })
                except Exception as e:
                    logging.warning(f"Skipping invalid reservation (ID: {r.id}): {e}")
                    continue

            result.append({
                "id": spot.id,
                "status": "available" if not reservations else "reserved",
                "reservations": reservations
            })

        return jsonify({
            "lot": lot_data,
            "spots": result,
            "date": selected_date.isoformat()
        }), 200
