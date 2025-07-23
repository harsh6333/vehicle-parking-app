from flask import Blueprint,  request
from controllers.admin.spot_controller import SpotController
from middleware.decorators import admin_required
from extensions import cache

spot_bp = Blueprint('admin_spot', __name__)
controller = SpotController()

@spot_bp.route('/lots/<int:lot_id>/spots/current', methods=['GET'])
@admin_required
@cache.cached(timeout=60, key_prefix=lambda: f"lot_spots_status_{request.view_args['lot_id']}")
def current_spot_status(lot_id):
    return controller.current_spot_status(lot_id)

@spot_bp.route('/spots/<int:spot_id>/history', methods=['GET'])
@cache.cached(timeout=60, key_prefix=lambda: f"spot_history_{request.view_args['spot_id']}")
@admin_required
def get_spot_history(spot_id):
    return controller.get_spot_history(spot_id)