from flask import Blueprint, request, jsonify
from backend.controllers.admin.lot_controller import LotController
from backend.middleware.decorators import admin_required
from backend.extensions import cache

lot_bp = Blueprint('admin_lot', __name__)
controller = LotController()

@lot_bp.route('/lots', methods=['POST'])
@admin_required
def create_lot():
    return controller.create_lot()

@lot_bp.route('/lots/<int:lot_id>', methods=['PUT', 'OPTIONS'])
@admin_required
def update_lot(lot_id):
    return controller.update_lot(lot_id)

@lot_bp.route('/lots/<int:lot_id>', methods=['DELETE'])
@admin_required
def delete_lot(lot_id):
    return controller.delete_lot(lot_id)

@lot_bp.route("/lots", methods=["GET"])
@admin_required
@cache.cached(timeout=60, key_prefix="admin_lots")
def get_lots():
    return controller.get_lots()