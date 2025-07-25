from backend import db
from backend.models.user import User
from flask import Blueprint, request, jsonify, make_response
from flask_jwt_extended import (
    create_access_token, set_access_cookies, unset_jwt_cookies,
    jwt_required, get_jwt
)
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
        required_fields = ('username', 'email', 'password')
        missing_fields = [field for field in required_fields if not data.get(field) or not str(data[field]).strip()]
        if missing_fields:
            return jsonify({'msg': f'Missing or empty fields: {", ".join(missing_fields)}'}), 400

        if User.query.filter_by(email=data['email'].strip()).first():
            return jsonify({'msg': 'User already exists'}), 409

        user = User(
            username=data['username'].strip(),
            email=data['email'].strip(),
            is_admin=False
        )
        user.set_password(data['password'].strip())

        db.session.add(user)
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
