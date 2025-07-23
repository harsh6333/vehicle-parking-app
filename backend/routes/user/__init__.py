from flask import Blueprint
from .reservation import reservation_bp
from .spots import spot_bp
from .stats import stats_bp
from .exports import export_bp

user_bp = Blueprint('user', __name__)
user_bp.register_blueprint(reservation_bp, url_prefix='')
user_bp.register_blueprint(spot_bp, url_prefix='')
user_bp.register_blueprint(stats_bp, url_prefix='')
user_bp.register_blueprint(export_bp, url_prefix='')