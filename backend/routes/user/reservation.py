from flask import Blueprint
from controllers.user.reservation_controller import ReservationController
from middleware.decorators import user_required
from extensions import cache

reservation_bp = Blueprint('user_reservation', __name__)
controller = ReservationController()

@reservation_bp.route("/reserve", methods=["POST"])
@user_required
def reserve_spot():
    return controller.reserve_spot()

@reservation_bp.route("/occupy/<int:spot_id>", methods=["PUT"])
@user_required
def occupy_spot(spot_id):
    return controller.occupy_spot(spot_id)

@reservation_bp.route("/release/<int:spot_id>", methods=["PUT"])
@user_required
def release_spot(spot_id):
    return controller.release_spot(spot_id)