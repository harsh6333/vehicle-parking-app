from flask import Blueprint, jsonify, request
from backend.controllers.admin.search_controller import SearchController
from backend.middleware.decorators import admin_required
from backend.extensions import cache

search_bp = Blueprint('admin_search', __name__)
controller = SearchController()

@search_bp.route("/search/lots", methods=["GET"])
@admin_required
def search_lots():
    query = request.args.get("q", "")
    page = int(request.args.get("page", 1))
    per_page = int(request.args.get("per_page", 10))
    sort_by = request.args.get("sort_by", "prime_location_name")
    sort_order = request.args.get("sort_order", "asc")
    return controller.search_lots(query, page, per_page, sort_by, sort_order)

@search_bp.route("/search/spots", methods=["GET"])
@admin_required
def search_spots():
    status = request.args.get("status")
    lot_id = request.args.get("lot_id")
    return controller.search_spots(status, lot_id)

@search_bp.route("/search/users", methods=["GET"])
@admin_required
def search_users():
    query = request.args.get("q", "")
    page = int(request.args.get("page", 1))
    per_page = int(request.args.get("per_page", 10))
    return controller.search_users(query, page, per_page)
