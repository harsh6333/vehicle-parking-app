from app import db
from models.user import User
from flask import Blueprint, request, jsonify, make_response
from flask_jwt_extended import (
    create_access_token, set_access_cookies, unset_jwt_cookies,
    jwt_required, get_jwt, get_jwt_identity
)
from datetime import timedelta

auth_bp = Blueprint('auth', __name__)


from flask_jwt_extended import jwt_required, get_jwt


@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
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


@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    if not data or not all(k in data for k in ('username', 'email', 'password')):
        return jsonify({'msg': 'Missing required fields'}), 400

    if User.query.filter_by(email=data['email']).first():
        return jsonify({'msg': 'User already exists'}), 409

    user = User(
        username=data['username'],
        email=data['email'],
        is_admin=False
    )
    user.set_password(data['password'])
    db.session.add(user)
    db.session.commit()
    return jsonify({'msg': 'User registered successfully'}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'msg': 'Missing email or password'}), 400

    user = User.query.filter_by(email=data['email']).first()
    if not user or not user.check_password(data['password']):
        return jsonify({'msg': 'Invalid credentials'}), 401

    access_token = create_access_token(
    identity=str(user.id),  # ✅ must be string
    additional_claims={
        "username": user.username,
        "is_admin": user.is_admin
    },
    expires_delta=timedelta(days=1)
)
    resp = make_response(jsonify({"msg": "Login successful", "is_admin": user.is_admin}))
    set_access_cookies(resp, access_token)
    return resp, 200

@auth_bp.route('/logout', methods=['POST'])
def logout():
    resp = make_response(jsonify({"msg": "Logout successful"}))
    unset_jwt_cookies(resp)
    return resp, 200
