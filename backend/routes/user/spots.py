from flask import Blueprint, request
from controllers.user.spot_controller import SpotController
from middleware.decorators import user_required
from extensions import cache

spot_bp = Blueprint('user_spot', __name__)
controller = SpotController()

@spot_bp.route("/lots", methods=["GET"])
@user_required
@cache.cached(timeout=60, key_prefix=lambda: f"user_lots_{request.args.get('date', 'all')}")
def get_lots():
    return controller.get_lots()

@spot_bp.route('/lots/<int:lot_id>/spots', methods=['GET'])
@user_required
@cache.cached(timeout=60, key_prefix=lambda: f"user_lot_{request.view_args['lot_id']}_spots_{request.args.get('date', 'today')}")
def spot_details(lot_id):
    return controller.spot_details(lot_id)