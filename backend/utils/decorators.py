from flask_jwt_extended import verify_jwt_in_request, get_jwt
from functools import wraps
from flask import jsonify, request

def user_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if request.method == 'OPTIONS':
            return '', 200

        try:
            verify_jwt_in_request()
            claims = get_jwt()
            if claims.get("is_admin", False):  
                return jsonify({"msg": "User access only"}), 403
        except Exception as e:
            return jsonify({"msg": "Authorization error", "error": str(e)}), 401

        return fn(*args, **kwargs)

    return wrapper


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