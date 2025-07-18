from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt,verify_jwt_in_request
from functools import wraps
from flask import jsonify
from models.parking_lot import ParkingLot
from models.parking_spot import ParkingSpot
from models.user import User
from models.reservation import Reservation
from app import db

admin_bp = Blueprint('admin', __name__)




def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if request.method == 'OPTIONS':
            return '', 200  

        try:
            verify_jwt_in_request()
            claims = get_jwt()
            if not claims.get("is_admin", False):
                return jsonify({"msg": "Admin access required"}), 403
        except Exception as e:
            return jsonify({"msg": "Authorization error", "error": str(e)}), 401

        return fn(*args, **kwargs)

    return wrapper





@admin_bp.route('/lots', methods=['POST'])
@admin_required
def create_lot():
    try:
        data = request.json
        print("Incoming data:", data)

        lot = ParkingLot(
            prime_location_name=data["prime_location_name"],
            address=data.get("address", ""),
            pin_code=data.get("pin_code", ""),
            price=data["price"],
            number_of_spots=data["number_of_spots"]
        )
        db.session.add(lot)
        db.session.flush()  
        print("Created lot with ID:", lot.id)

        for i in range(lot.number_of_spots):
            spot = ParkingSpot(status='A', lot_id=lot.id)
            db.session.add(spot)
        print(f"Added {lot.number_of_spots} spots")

        db.session.commit()
        print("Commit successful")

        return jsonify({"msg": "Lot and spots created"}), 201

    except Exception as e:
        db.session.rollback()
        print("Error during DB operation:", str(e))
        return jsonify({"msg": "Internal Server Error", "error": str(e)}), 500



@admin_bp.route('/lots/<int:lot_id>', methods=['PUT', 'OPTIONS'])
@admin_required
def update_lot(lot_id):
    if request.method == 'OPTIONS':
        return '', 200

    data = request.json
    lot = ParkingLot.query.get_or_404(lot_id)

    lot.prime_location_name = data.get("prime_location_name", lot.prime_location_name)
    lot.address = data.get("address", lot.address)
    lot.pin_code = data.get("pin_code", lot.pin_code)
    lot.price = data.get("price", lot.price)

    new_spot_count = data.get("number_of_spots", lot.number_of_spots)
    current_spot_count = len(lot.spots)

    # Update number of spots if changed
    if new_spot_count > current_spot_count:
        # Add new spots
        for _ in range(new_spot_count - current_spot_count):
            db.session.add(ParkingSpot(status='A', lot_id=lot.id))
    elif new_spot_count < current_spot_count:
        # Remove excess spots — only unoccupied ones
        removable_spots = ParkingSpot.query.filter_by(lot_id=lot.id, status='A').limit(current_spot_count - new_spot_count).all()
        for spot in removable_spots:
            db.session.delete(spot)

    lot.number_of_spots = new_spot_count

    db.session.commit()
    return jsonify({"msg": "Lot updated"}), 200





@admin_bp.route('/lots/<int:lot_id>', methods=['DELETE'])
@admin_required
def delete_lot(lot_id):
    lot = ParkingLot.query.get_or_404(lot_id)
    db.session.delete(lot)
    db.session.commit()
    return jsonify({"msg": "Lot deleted"}), 200


@admin_bp.route('/lots', methods=['GET'])
@admin_required
def list_lots():
    lots = ParkingLot.query.all()
    result = []
    for lot in lots:
        spots = ParkingSpot.query.filter_by(lot_id=lot.id).all()
        total = len(spots)
        occupied = len([s for s in spots if s.status == 'O'])
        result.append({
            "id": lot.id,
            "address": lot.prime_location_name,
            "pin_code":lot.pin_code,
            "price": lot.price,
            "number_of_spots": total,
            "occupied_spots": occupied
        })
    return jsonify(result), 200



@admin_bp.route('/lots/<int:lot_id>/spots', methods=['GET'])
@admin_required
def spot_details(lot_id):
    spots = ParkingSpot.query.filter_by(lot_id=lot_id).all()
    return jsonify([
        {"id": s.id, "status": s.status}
        for s in spots
    ]), 200



@admin_bp.route('/users', methods=['GET'])
@admin_required
def list_users():
    users = User.query.all()
    result = []
    for u in users:
        result.append({
            "username": u.username,
            "email": u.email,
            "is_admin": u.is_admin,
            "reservations": [{
                "spot_id": r.spot_id,
                "from": r.parking_timestamp,
                "to": r.leaving_timestamp
            } for r in u.reservations]
        })
    return jsonify(result), 200
