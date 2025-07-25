from flask import Blueprint, jsonify
from backend.controllers.admin.dashboard_controller import DashboardController
from backend.middleware.decorators import admin_required
from backend.extensions import cache

dashboard_bp = Blueprint('admin_dashboard', __name__)
controller = DashboardController()

@dashboard_bp.route('/dashboard', methods=['GET'])
@cache.cached(timeout=60, key_prefix="admin_dashboard_summary")
@admin_required
def admin_dashboard_summary():
    return controller.admin_dashboard_summary()

@dashboard_bp.route("/stats", methods=["GET"])
@cache.cached(timeout=120, key_prefix="admin_weekly_stats")
@admin_required
def get_admin_stats():
    return controller.get_admin_stats()