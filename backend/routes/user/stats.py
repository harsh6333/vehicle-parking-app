from flask import Blueprint
from flask_jwt_extended import get_jwt_identity
from controllers.user.stats_controller import StatsController
from middleware.decorators import user_required
from extensions import cache

stats_bp = Blueprint('user_stats', __name__)
controller = StatsController()

@stats_bp.route("/history", methods=["GET"])
@user_required
@cache.cached(timeout=60, key_prefix=lambda: f"user_history_{get_jwt_identity()}")
def get_history():
    return controller.get_history()

@stats_bp.route("/stats", methods=["GET"])
@user_required
@cache.cached(timeout=120, key_prefix=lambda: f"user_stats_{get_jwt_identity()}")
def get_user_stats():
    return controller.get_user_stats()