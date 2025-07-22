from flask import Blueprint, jsonify
from extensions import cache


ping_bp = Blueprint("ping", __name__)

@ping_bp.route('/api/ping', methods=['GET'])
def ping():
    try:
        cache.set("ping_test_key", "pong", timeout=5)
        result = cache.get("ping_test_key")
        if result == "pong":
            return jsonify({"redis": "up"}), 200
        else:
            return jsonify({"redis": "down", "error": "Unexpected cache result"}), 500
    except Exception as e:
        return jsonify({"redis": "down", "error": str(e)}), 500
    

@ping_bp.route('/test-cache')
def test_cache():
    from extensions import cache
    cache.set("foo", "bar", timeout=60)
    return cache.get("foo") or "None"
