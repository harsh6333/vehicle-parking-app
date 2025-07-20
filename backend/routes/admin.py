from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt, verify_jwt_in_request
from functools import wraps
from models.parking_lot import ParkingLot
from models.parking_spot import ParkingSpot
from models.user import User
from models.reservation import Reservation
from datetime import datetime, timezone
from utils.decorators import admin_required
from app import db
from sqlalchemy import func
from sqlalchemy.orm import joinedload
from pytz import timezone as timezeone2

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/lots', methods=['POST'])
@admin_required
def create_lot():
    try:
        data = request.json
        lot = ParkingLot(
            prime_location_name=data["prime_location_name"],
            address=data.get("address", ""),
            pin_code=data.get("pin_code", ""),
            price=data["price"],
            number_of_spots=data["number_of_spots"]
        )
        db.session.add(lot)
        db.session.flush()

        for i in range(lot.number_of_spots):
            spot = ParkingSpot(lot_id=lot.id)
            db.session.add(spot)

        db.session.commit()
        return jsonify({"msg": "Lot and spots created"}), 201

    except Exception as e:
        db.session.rollback()
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

    if new_spot_count > current_spot_count:
        for _ in range(new_spot_count - current_spot_count):
            db.session.add(ParkingSpot(lot_id=lot.id))
    elif new_spot_count < current_spot_count:
        removable_spots = ParkingSpot.query.filter_by(lot_id=lot.id).limit(current_spot_count - new_spot_count).all()
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


@admin_bp.route("/lots", methods=["GET"])
@admin_required
def get_lots():
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


@admin_bp.route('/lots/<int:lot_id>/spots/current', methods=['GET'])
@admin_required
def current_spot_status(lot_id):
    now = datetime.now(timezone.utc)
    spots = ParkingSpot.query.filter_by(lot_id=lot_id).all()
    result = []

    for spot in spots:
        current_reservation = next(
            (
                r for r in spot.reservations
                if r.reserved_at <= now <= r.reserved_till
            ),
            None
        )
        result.append({
            "spot_id": spot.id,
            "status": "Reserved" if current_reservation else "Available",
            "reservation": {
                "user_id": current_reservation.user_id,
                "reserved_at": current_reservation.reserved_at.astimezone(timezone.utc).isoformat(),
                "reserved_till": current_reservation.reserved_till.astimezone(timezone.utc).isoformat(),
            } if current_reservation else None,
        })

    return jsonify({"spots": result}), 200





@admin_bp.route('/users', methods=['GET'])
@admin_required
def list_users():
    users = User.query.options(joinedload(User.reservations).joinedload(Reservation.spot).joinedload(ParkingSpot.lot)).all()
    result = []

    for u in users:
        total_hours = 0
        total_cost = 0

        for r in u.reservations:
            # Fallback to reserved_at/till if parking timestamps are missing
            start = r.parking_timestamp or r.reserved_at
            end = r.leaving_timestamp or r.reserved_till

            if start and end and end > start:
                duration_hours = (end - start).total_seconds() / 3600
                total_hours += duration_hours
                if r.spot and r.spot.lot:
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



@admin_bp.route('/dashboard', methods=['GET'])
@admin_required
def admin_dashboard_summary():
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
            "reserved_at": r.reserved_at.astimezone(timezone.utc).isoformat(),
            "reserved_till": r.reserved_till.astimezone(timezone.utc).isoformat(),
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
        return jsonify({"msg": "Error fetching dashboard data", "error": str(e)}), 500


@admin_bp.route('/spots/<int:spot_id>/history', methods=['GET'])
@admin_required
def get_spot_history(spot_id):
    spot = ParkingSpot.query.get_or_404(spot_id)
    reservations = Reservation.query.filter_by(spot_id=spot_id).order_by(Reservation.reserved_at.desc()).all()

    result = {
        "spot_id": spot.id,
        "lot_id": spot.lot_id,
        "history": []
    }

    for reservation in reservations:
        user = User.query.get(reservation.user_id)
        result["history"].append({
            "reservation_id": reservation.id,
            "user_id": user.id,
            "username": user.username,
            "email": user.email,
            "reserved_at": reservation.reserved_at.astimezone(timezone.utc).isoformat(),
            "reserved_till": reservation.reserved_till.astimezone(timezone.utc).isoformat(),
            "parking_timestamp": reservation.parking_timestamp.astimezone(timezone.utc).isoformat() if reservation.parking_timestamp else None,
            "leaving_timestamp": reservation.leaving_timestamp.astimezone(timezone.utc).isoformat() if reservation.leaving_timestamp else None,
            "status": "Completed" if reservation.leaving_timestamp else "In Progress" if reservation.parking_timestamp else "Reserved",
            "duration_minutes": ((reservation.reserved_till - reservation.reserved_at).total_seconds() / 60) if reservation.reserved_till and reservation.reserved_at else None
        })

    return jsonify(result), 200
