from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity
from datetime import datetime, timedelta
from app import db
from models.parking_lot import ParkingLot
from models.parking_spot import ParkingSpot
from models.reservation import Reservation
from utils.decorators import user_required
from sqlalchemy.orm import joinedload


user_bp = Blueprint("user", __name__)



@user_bp.route("/lots", methods=["GET"])
@user_required
def get_lots():
    date_str = request.args.get("date")  

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

        if date_str:
            print(date_str)
            try:
                selected_date = datetime.strptime(date_str, "%Y-%m-%d").date()
            except ValueError:
                return jsonify({"msg": "Invalid date format. Use YYYY-MM-DD"}), 400

            lot_data["spots"] = []

            for spot in lot.spots:
                reservations_on_date = []
                for r in spot.reservations:
                    if r.reserved_at.date() == selected_date:
                        reservations_on_date.append({
                            # "reservation_id": r.id,
                            # "user_id": r.user_id,
                            "reserved_at": r.reserved_at.isoformat(),
                            "reserved_till": r.reserved_till.isoformat(),
                            "parking_timestamp": r.parking_timestamp.isoformat() if r.parking_timestamp else None,
                            "leaving_timestamp": r.leaving_timestamp.isoformat() if r.leaving_timestamp else None,
                        })

                lot_data["spots"].append({
                    "spot_id": spot.id,
                   
                    "reservations": reservations_on_date
                })

        response.append(lot_data)

    return jsonify(response), 200



@user_bp.route('/lots/<int:lot_id>/spots', methods=['GET'])
@user_required
def spot_details(lot_id):
    # optional date parameter with default today
    date_str = request.args.get("date", datetime.utcnow().date().isoformat())
    
    try:
        selected_date = datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        return jsonify({"msg": "Invalid date format. Use YYYY-MM-DD"}), 400

    # Validate lot exists
    lot = ParkingLot.query.get(lot_id)
    if not lot:
        return jsonify({"msg": "Parking lot not found"}), 404

    # Get all spots for this lot with reservations for the selected date
    spots = ParkingSpot.query.filter_by(lot_id=lot_id).options(
        joinedload(ParkingSpot.reservations)
    ).all()

    # Prepare response data
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
        reservations = [
            {
                "id": r.id,
                "user_id": r.user_id,
                "reserved_at": r.reserved_at.isoformat(),
                "reserved_till": r.reserved_till.isoformat(),
                "parking_timestamp": r.parking_timestamp.isoformat() if r.parking_timestamp else None,
                "leaving_timestamp": r.leaving_timestamp.isoformat() if r.leaving_timestamp else None,
                "status": "occupied" if r.parking_timestamp else "reserved"
            }
            for r in spot.reservations 
            if r.reserved_at.date() == selected_date
        ]

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


@user_bp.route("/reserve", methods=["POST"])
@user_required
def reserve_specific_spot():
    from datetime import datetime, timedelta

    data = request.json
    user_id = int(get_jwt_identity())

    spot_id = data.get("spot_id")
    duration_hours = data.get("duration_hours", 1)
    start_time_str = data.get("start_time")  

    if not spot_id or not start_time_str:
        return jsonify({"msg": "Missing spot_id or start_time"}), 400
    if duration_hours <= 0:
        return jsonify({"msg": "Invalid duration"}), 400

    try:
        start_time = datetime.fromisoformat(start_time_str)
    except ValueError:
        return jsonify({"msg": "Invalid start_time format. Use ISO 8601."}), 400

    end_time = start_time + timedelta(hours=duration_hours)

    # Validate spot
    spot = ParkingSpot.query.get(spot_id)
    if not spot:
        return jsonify({"msg": "Invalid spot ID"}), 404

    # Correct overlap check
    overlapping = Reservation.query.filter(
        Reservation.spot_id == spot_id,
        Reservation.reserved_at < end_time,
        Reservation.reserved_till > start_time
    ).first()

    if overlapping:
        return jsonify({"msg": "Spot is already reserved in the selected time range"}), 409

    cost = round(duration_hours * spot.lot.price, 2)

    reservation = Reservation(
        user_id=user_id,
        spot_id=spot_id,
        reserved_at=start_time,
        reserved_till=end_time,
        parking_cost=cost
    )

    db.session.add(reservation)
    db.session.commit()

    return jsonify({
        "msg": "Spot reserved",
        "spot_id": spot.id,
        "reserved_at": reservation.reserved_at.isoformat(),
        "reserved_till": reservation.reserved_till.isoformat(),
        "parking_timestamp": reservation.parking_timestamp.isoformat() if reservation.parking_timestamp else None,
        "leaving_timestamp": reservation.leaving_timestamp.isoformat() if reservation.leaving_timestamp else None,
        "duration": duration_hours,
        "price": cost,
        "lot_name": spot.lot.prime_location_name
    }), 200




@user_bp.route("/occupy/<int:spot_id>", methods=["PUT"])
@user_required
def occupy_spot(spot_id):
    user_id = int(get_jwt_identity())
    data = request.json
    reserved_at_str = data.get('reserved_at')
    spot = ParkingSpot.query.get_or_404(spot_id)

    if not reserved_at_str:
        return jsonify({"msg": "Missing reserved_at"}), 400

    try:
        reserved_at = datetime.fromisoformat(reserved_at_str)
    except ValueError:
        return jsonify({"msg": "Invalid reserved_at format"}), 400

    #  matching reservation
    reservation = Reservation.query.filter_by(
        user_id=user_id,
        spot_id=spot_id,
        reserved_at=reserved_at
    ).first()
    if not reservation:
        return jsonify({"msg": "No reservation found"}), 404

    if datetime.utcnow() < reservation.reserved_at:
        return jsonify({"msg": "Reservation not yet started"}), 400
    reservation.parking_timestamp = datetime.utcnow()
    db.session.commit()

    return jsonify({"msg": "Spot marked as occupied"}), 200


@user_bp.route("/release/<int:spot_id>", methods=["PUT"])
@user_required
def release_spot(spot_id):

    user_id = int(get_jwt_identity())
    data = request.json
    reserved_at_str = data.get('reserved_at')

    if not reserved_at_str:
        return jsonify({"msg": "Missing reserved_at"}), 400

    try:
        reserved_at = datetime.fromisoformat(reserved_at_str)
    except ValueError:
        return jsonify({"msg": "Invalid reserved_at format"}), 400

    # matching reservation
    reservation = Reservation.query.filter_by(
        user_id=user_id,
        spot_id=spot_id,
        reserved_at=reserved_at
    ).first()

    if not reservation:
        return jsonify({"msg": "No matching reservation found"}), 404

    # leaving time
    reservation.leaving_timestamp = datetime.utcnow()
    db.session.commit()

    return jsonify({"msg": "Spot released"}), 200




# Parking history for logged-in user
@user_bp.route("/history", methods=["GET"])
@user_required
def parking_history():
    user_id = int(get_jwt_identity())

    history = Reservation.query.filter_by(user_id=user_id).order_by(Reservation.reserved_at.desc()).all()
    return jsonify([{
        "spot_id": r.spot_id,
        "reserved_at": r.reserved_at,
        "address": f"{r.spot.lot.address}, {r.spot.lot.prime_location_name}",
        "reserved_till": r.reserved_till.isoformat(),
        "parking_timestamp": r.parking_timestamp.isoformat() if r.parking_timestamp else None,
        "leaving_timestamp": r.leaving_timestamp.isoformat() if r.leaving_timestamp else None,
        "hourlyrate":r.spot.lot.price
    } for r in history]), 200
