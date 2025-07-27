from backend import db
from backend.models.user import User
from flask import Blueprint, request, jsonify, make_response
from flask_jwt_extended import (
    create_access_token, set_access_cookies, unset_jwt_cookies,
    jwt_required, get_jwt,get_jwt_identity
)
from backend.models.vehicles import Vehicle  
from datetime import timedelta
import traceback

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    try:
        claims = get_jwt()
        user_id = claims.get('sub', {}).get('id') if isinstance(claims.get('sub'), dict) else claims.get('sub')

        user = User.query.get(user_id)
        if not user:
            return jsonify({'msg': 'User not found'}), 404

        return jsonify({
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "is_admin": user.is_admin
        }), 200

    except Exception as e:
        traceback.print_exc()
        return jsonify({'msg': 'Error fetching user', 'error': str(e)}), 500


@auth_bp.route('/register', methods=['POST'])
def register():
    try:
        data = request.json or {}
        required_fields = ('username', 'email', 'password', 'address', 'pin_code')
        missing_fields = [field for field in required_fields if not data.get(field) or not str(data[field]).strip()]
        if missing_fields:
            return jsonify({'msg': f'Missing or empty fields: {", ".join(missing_fields)}'}), 400

        if User.query.filter_by(email=data['email'].strip()).first():
            return jsonify({'msg': 'User already exists'}), 409

        user = User(
            username=data['username'].strip(),
            email=data['email'].strip(),
            is_admin=False,
            address=data['address'].strip(),
            pin_code=data['pin_code'].strip()
        )
        user.set_password(data['password'].strip())
        db.session.add(user)
        db.session.flush()  

        vehicle_list = data.get('vehicles', [])
        if not isinstance(vehicle_list, list) or len(vehicle_list) > 3:
            return jsonify({'msg': 'You can register up to 3 vehicles only.'}), 400

        for v in vehicle_list:
            if not v.get('vehicle_number') or not v['vehicle_number'].strip():
                return jsonify({'msg': 'Each vehicle must have a valid vehicle_number'}), 400
            vehicle = Vehicle(
                vehicle_number=v['vehicle_number'].strip(),
                vehicle_type=v.get('vehicle_type', '').strip() or None,
                brand=v.get('brand', '').strip() or None,
                color=v.get('color', '').strip() or None,
                user_id=user.id
            )
            db.session.add(vehicle)

        db.session.commit()
        return jsonify({'msg': 'User registered successfully'}), 201

    except Exception as e:
        traceback.print_exc()
        return jsonify({'msg': 'Error during registration', 'error': str(e)}), 500


@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.json or {}
        if not data.get('email') or not data.get('password'):
            return jsonify({'msg': 'Missing email or password'}), 400

        user = User.query.filter_by(email=data['email'].strip()).first()
        if not user or not user.check_password(data['password'].strip()):
            return jsonify({'msg': 'Invalid credentials'}), 401

        access_token = create_access_token(
            identity=str(user.id),  
            additional_claims={
                "username": user.username,
                "is_admin": user.is_admin
            },
            expires_delta=timedelta(days=1)
        )

        resp = make_response(jsonify({"msg": "Login successful", "is_admin": user.is_admin}))
        set_access_cookies(resp, access_token)
        return resp, 200

    except Exception as e:
        traceback.print_exc()
        return jsonify({'msg': 'Login failed', 'error': str(e)}), 500


@auth_bp.route('/logout', methods=['POST'])
def logout():
    try:
        resp = make_response(jsonify({"msg": "Logout successful"}))
        unset_jwt_cookies(resp)
        return resp, 200
    except Exception as e:
        traceback.print_exc()
        return jsonify({'msg': 'Logout failed', 'error': str(e)}), 500



@auth_bp.route("/profile", methods=["PUT"])
@jwt_required()
def update_profile():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user:
        return jsonify({"msg": "User not found"}), 404

    data = request.json

    user.username = data.get("username", user.username)
    user.email = data.get("email", user.email)
    user.address = data.get("address", user.address)
    user.pin_code = data.get("pin_code", user.pin_code)

    # Optional: replace vehicles
    if "vehicles" in data:
        user.vehicles.clear()
        for v in data["vehicles"]:
            if "vehicle_number" in v:
                vehicle = Vehicle(
                    user_id=user.id,
                    vehicle_number=v["vehicle_number"],
                    vehicle_type=v.get("vehicle_type"),
                    brand=v.get("brand"),
                    color=v.get("color")
                )
                user.vehicles.append(vehicle)

    try:
        db.session.commit()
        return jsonify({
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "address": user.address,
            "pin_code": user.pin_code,
            "is_admin": user.is_admin,
            "created_at": user.created_at.isoformat() if user.created_at else None,
            "vehicles": [
                {
                    "vehicle_number": v.vehicle_number,
                    "vehicle_type": v.vehicle_type,
                    "brand": v.brand,
                    "color": v.color
                } for v in user.vehicles
            ]
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({"msg": "Update failed", "error": str(e)}), 500





@auth_bp.route("/profile", methods=["GET"])
@jwt_required()
def get_profile():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user:
        return jsonify({"msg": "User not found"}), 404

    vehicle_list = [
        {
            "vehicle_number": v.vehicle_number,
            "vehicle_type": v.vehicle_type,
            "brand": v.brand,
            "color": v.color,
        }
        for v in user.vehicles
    ]

    return jsonify({
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "is_admin": user.is_admin,
        "address": user.address,
        "pin_code": user.pin_code,
        "created_at": user.created_at.isoformat() if user.created_at else None,
        "vehicles": vehicle_list
    })
