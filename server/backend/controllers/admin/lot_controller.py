from flask import request, jsonify
from backend.models.parking_lot import ParkingLot
from backend.models.parking_spot import ParkingSpot
from backend import db
from backend.extensions import cache
from sqlalchemy.exc import SQLAlchemyError

class LotController:
    # Create Lot
    def create_lot(self):
        try:
            data = request.get_json()
            required_fields = ["prime_location_name", "price", "number_of_spots"]
            missing_fields = [field for field in required_fields if field not in data]

            if missing_fields:
                return jsonify({"msg": f"Missing fields: {', '.join(missing_fields)}"}), 400

            lot = ParkingLot(
                prime_location_name=data["prime_location_name"],
                address=data.get("address", ""),
                pin_code=data.get("pin_code", ""),
                price=float(data["price"]),
                number_of_spots=int(data["number_of_spots"])
            )

            db.session.add(lot)
            db.session.flush()

            for _ in range(lot.number_of_spots):
                spot = ParkingSpot(lot_id=lot.id)
                db.session.add(spot)

            db.session.commit()
            cache.delete("admin_lots")

            return jsonify({"msg": "Lot and spots created"}), 201

        except (ValueError, TypeError) as ve:
            db.session.rollback()
            return jsonify({"msg": "Invalid input type", "error": str(ve)}), 400

        except SQLAlchemyError as db_err:
            db.session.rollback()
            return jsonify({"msg": "Database error", "error": str(db_err)}), 500

        except Exception as e:
            db.session.rollback()
            return jsonify({"msg": "Internal Server Error", "error": str(e)}), 500

    # Update Lot
    def update_lot(self, lot_id):
        try:
            if request.method == 'OPTIONS':
                return '', 200

            data = request.get_json()
            lot = ParkingLot.query.get_or_404(lot_id)

            lot.prime_location_name = data.get("prime_location_name", lot.prime_location_name)
            lot.address = data.get("address", lot.address)
            lot.pin_code = data.get("pin_code", lot.pin_code)
            lot.price = float(data.get("price", lot.price))

            new_spot_count = int(data.get("number_of_spots", lot.number_of_spots))
            current_spot_count = len(lot.spots)

            if new_spot_count > current_spot_count:
                for _ in range(new_spot_count - current_spot_count):
                    db.session.add(ParkingSpot(lot_id=lot.id))
            elif new_spot_count < current_spot_count:
                removable_spots = ParkingSpot.query.filter_by(lot_id=lot.id)\
                    .order_by(ParkingSpot.id.desc())\
                    .limit(current_spot_count - new_spot_count).all()
                for spot in removable_spots:
                    db.session.delete(spot)

            lot.number_of_spots = new_spot_count
            db.session.commit()

            cache.delete("admin_lots")
            cache.delete(f"lot_spots_status_{lot_id}")

            return jsonify({"msg": "Lot updated"}), 200

        except (ValueError, TypeError) as ve:
            db.session.rollback()
            return jsonify({"msg": "Invalid input type", "error": str(ve)}), 400

        except SQLAlchemyError as db_err:
            db.session.rollback()
            return jsonify({"msg": "Database error", "error": str(db_err)}), 500

        except Exception as e:
            db.session.rollback()
            return jsonify({"msg": "Internal Server Error", "error": str(e)}), 500

    # Delete Lot
    def delete_lot(self, lot_id):
        try:
            lot = ParkingLot.query.get_or_404(lot_id)

            db.session.delete(lot)
            db.session.commit()

            cache.delete("admin_lots")
            cache.delete(f"lot_spots_status_{lot_id}")

            return jsonify({"msg": "Lot deleted"}), 200

        except SQLAlchemyError as db_err:
            db.session.rollback()
            return jsonify({"msg": "Database error", "error": str(db_err)}), 500

        except Exception as e:
            db.session.rollback()
            return jsonify({"msg": "Internal Server Error", "error": str(e)}), 500

    # Get Lots
    def get_lots(self):
        try:
            lots = ParkingLot.query.all()
            response = []

            for lot in lots:
                lot_data = {
                    "id": lot.id,
                    "prime_location_name": lot.prime_location_name,
                    "address": lot.address,
                    "pin_code": lot.pin_code,
                    "price": lot.price,
                    "total_spots": lot.number_of_spots,
                }
                response.append(lot_data)

            return jsonify(response), 200

        except Exception as e:
            return jsonify({"msg": "Failed to fetch lots", "error": str(e)}), 500
