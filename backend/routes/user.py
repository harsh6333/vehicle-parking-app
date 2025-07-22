from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity
from datetime import datetime, timedelta,timezone
from app import db
from models.parking_lot import ParkingLot
from models.parking_spot import ParkingSpot
from models.reservation import Reservation
from utils.decorators import user_required
from sqlalchemy.orm import joinedload
from utils.datetimeformate import parse_iso_datetime
from zoneinfo import ZoneInfo 
from extensions import cache


user_bp = Blueprint("user", __name__)


@user_bp.route("/lots", methods=["GET"])
@user_required
@cache.cached(timeout=60, key_prefix=lambda: f"user_lots_{request.args.get('date', 'all')}")
def get_lots():
    date_str = request.args.get("date")
    ist = ZoneInfo("Asia/Kolkata")

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
            try:
                selected_date = datetime.strptime(date_str, "%Y-%m-%d").date()
            except ValueError:
                return jsonify({"msg": "Invalid date format. Use YYYY-MM-DD"}), 400

            lot_data["spots"] = []

            for spot in lot.spots:
                reservations_on_date = []
                for r in spot.reservations:
                    
                    if r.reserved_at.astimezone(ist).date() == selected_date:
                        reservations_on_date.append({
                            "reserved_at": r.reserved_at.isoformat() + "Z",
                            "reserved_till": r.reserved_till.isoformat() + "Z",
                            "parking_timestamp": r.parking_timestamp.isoformat() + "Z" if r.parking_timestamp else None,
                            "leaving_timestamp": r.leaving_timestamp.isoformat() + "Z" if r.leaving_timestamp else None,
                        })

                lot_data["spots"].append({
                    "spot_id": spot.id,
                    "reservations": reservations_on_date
                })

        response.append(lot_data)

    return jsonify(response), 200


IST = timezone(timedelta(hours=5, minutes=30))

@user_bp.route('/lots/<int:lot_id>/spots', methods=['GET'])
@user_required
@cache.cached(timeout=60, key_prefix=lambda: f"user_lot_{request.view_args['lot_id']}_spots_{request.args.get('date', 'today')}")
def spot_details(lot_id):
    # Use today's date in IST by default
    now_ist = datetime.now(IST)
    selected_date = now_ist.date()
    print(selected_date)

    date_str = request.args.get("date")
    if date_str:
        try:
            selected_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            return jsonify({"msg": "Invalid date format. Use YYYY-MM-DD"}), 400

    # Validate lot exists
    lot = ParkingLot.query.get(lot_id)
    if not lot:
        return jsonify({"msg": "Parking lot not found"}), 404

    # Get all spots with reservations
    spots = ParkingSpot.query.filter_by(lot_id=lot_id).options(
        joinedload(ParkingSpot.reservations)
    ).all()

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
            reserved_at = r.reserved_at
            if reserved_at.tzinfo is None:
                reserved_at = reserved_at.replace(tzinfo=timezone.utc)

            reserved_ist = reserved_at.astimezone(IST)
            reserved_date_ist = reserved_ist.date()

            if reserved_date_ist == selected_date:
                reservations.append({
                    "id": r.id,
                    "user_id": r.user_id,
                    "reserved_at": r.reserved_at.isoformat() + "Z",
                    "reserved_till": r.reserved_till.isoformat() + "Z",
                    "parking_timestamp": r.parking_timestamp.isoformat() + "Z" if r.parking_timestamp else None,
                    "leaving_timestamp": r.leaving_timestamp.isoformat() + "Z" if r.leaving_timestamp else None,
                    "status": "occupied" if r.parking_timestamp else "reserved"
                })

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
def reserve_spot():
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

    # Overlap check (excluding released reservations)
    overlapping = Reservation.query.filter(
        Reservation.spot_id == spot_id,
        Reservation.reserved_at < end_time,
        Reservation.reserved_till > start_time,
        Reservation.leaving_timestamp == None
    ).first()

    if overlapping:
        return jsonify({"error": "Spot already reserved during this time"}), 409

    # Fetch spot and its lot to calculate cost
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






@user_bp.route("/occupy/<int:spot_id>", methods=["PUT"])
@user_required
def occupy_spot(spot_id):
    user_id = int(get_jwt_identity())
    data = request.json
    reserved_at_str = data.get("reserved_at")

    if not reserved_at_str:
        return jsonify({"msg": "Missing reserved_at"}), 400

    try:
        reserved_at = parse_iso_datetime(reserved_at_str)
    except ValueError:
        return jsonify({"msg": "Invalid reserved_at format"}), 400

    reservation = Reservation.query.filter_by(
        user_id=user_id,
        spot_id=spot_id,
        reserved_at=reserved_at
    ).first()

    if not reservation:
        return jsonify({"msg": "No reservation found for this user and time"}), 404

    now = datetime.now(timezone.utc)

    # Check if current time is within reservation window
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


@user_bp.route("/release/<int:spot_id>", methods=["PUT"])
@user_required
def release_spot(spot_id):
    user_id = get_jwt_identity()
    data = request.json
    reserved_at = parse_iso_datetime(data.get("reserved_at"))

    reservation = Reservation.query.filter_by(
        spot_id=spot_id, reserved_at=reserved_at
    ).first_or_404()

    now = datetime.now(timezone.utc)
    reservation.leaving_timestamp = now
    db.session.commit()
    cache.delete(f"user_history_{user_id}")
    cache.delete(f"user_stats_{user_id}")
    cache.delete(f"user_lot_{spot_id}_spots_{reservation.reserved_at.date().isoformat()}")

    return jsonify({"message": "Spot released", "time": now.isoformat() + "Z"}), 200

# @user_bp.route("/occupy/<int:spot_id>", methods=["PUT"])
# @user_required
# def occupy_spot(spot_id):
#     user_id = int(get_jwt_identity())
#     data = request.json
#     reserved_at_str = data.get('reserved_at')
#     spot = ParkingSpot.query.get_or_404(spot_id)

#     if not reserved_at_str:
#         return jsonify({"msg": "Missing reserved_at"}), 400

#     try:
#         reserved_at = parse_iso_datetime(reserved_at_str)
#     except ValueError:
#         return jsonify({"msg": "Invalid reserved_at format"}), 400

#     reservation = Reservation.query.filter_by(
#         user_id=user_id,
#         spot_id=spot_id,
#         reserved_at=reserved_at
#     ).first()

#     if not reservation:
#         return jsonify({"msg": "No reservation found"}), 404

#     ist = ZoneInfo("Asia/Kolkata")
#     now_ist = datetime.now(ist)
#     reserved_till_ist = reservation.reserved_till.astimezone(ist) if reservation.reserved_till else None

#     # Check if current time is within reservation window
#     if now_ist < reservation.reserved_at.astimezone(ist):
#         return jsonify({"msg": "Reservation not yet started"}), 400

#     if reserved_till_ist and now_ist > reserved_till_ist:
#         return jsonify({"msg": "Reservation time window has passed"}), 400

#     if reservation.parking_timestamp is not None:
#         return jsonify({"msg": "Spot already marked as occupied"}), 400

#     # Store timestamp in UTC
#     reservation.parking_timestamp = datetime.now(timezone.utc)
#     db.session.commit()

#     return jsonify({"msg": "Spot marked as occupied"}), 200






# @user_bp.route("/release/<int:spot_id>", methods=["PUT"])
# @user_required
# def release_spot(spot_id):

#     user_id = int(get_jwt_identity())
#     data = request.json
#     reserved_at_str = data.get('reserved_at')

#     if not reserved_at_str:
#         return jsonify({"msg": "Missing reserved_at"}), 400

#     try:
#         reserved_at = parse_iso_datetime(reserved_at_str)
#     except ValueError:
#         return jsonify({"msg": "Invalid reserved_at format"}), 400

#     # matching reservation
#     reservation = Reservation.query.filter_by(
#         user_id=user_id,
#         spot_id=spot_id,
#         reserved_at=reserved_at
#     ).first()

#     if not reservation:
#         return jsonify({"msg": "No matching reservation found"}), 404

#     # leaving time
#     reservation.leaving_timestamp = datetime.utcnow()
#     db.session.commit()

#     return jsonify({"msg": "Spot released"}), 200




# Parking history for logged-in user
@user_bp.route("/history", methods=["GET"])
@user_required
@cache.cached(timeout=60, key_prefix=lambda: f"user_history_{get_jwt_identity()}")
def get_history():
    user_id = get_jwt_identity()
    reservations = Reservation.query.filter_by(user_id=user_id).order_by(Reservation.reserved_at.desc()).all()
    return jsonify([
        {
            "id": r.id,
            "spot_id": r.spot_id,
            "reserved_at": r.reserved_at.isoformat() + "Z" if r.reserved_at else None,
            "reserved_till": r.reserved_till.isoformat() + "Z" if r.reserved_till else None,
            "parking_timestamp": r.parking_timestamp.isoformat() + "Z" if r.parking_timestamp else None,
            "leaving_timestamp": r.leaving_timestamp.isoformat() + "Z" if r.leaving_timestamp else None,
            "hourlyrate":r.parking_cost,
           "address": f"{r.spot.lot.prime_location_name},{r.spot.lot.address}," if r.spot and r.spot.lot else None,
        }
        for r in reservations
    ])



@user_bp.route("/stats", methods=["GET"])
@user_required
@cache.cached(timeout=120, key_prefix=lambda: f"user_stats_{get_jwt_identity()}")
def get_user_stats():
    user_id = get_jwt_identity()

    reservations = Reservation.query.filter_by(user_id=user_id).all()

    from collections import defaultdict
    from datetime import datetime

    stats = defaultdict(lambda: {"hours": 0, "revenue": 0})

    for res in reservations:
        if res.reserved_at and res.reserved_till:
            date = res.reserved_at.date().isoformat()
            duration = (res.reserved_till - res.reserved_at).total_seconds() / 3600
            stats[date]["hours"] += duration
            stats[date]["revenue"] += duration * res.spot.lot.price

    return jsonify({
        "dates": list(stats.keys()),
        "hours": [round(v["hours"], 2) for v in stats.values()],
        "revenue": [round(v["revenue"], 2) for v in stats.values()]
    })
