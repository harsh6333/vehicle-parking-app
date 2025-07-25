from flask import Blueprint
from .lots import lot_bp
from .spots import spot_bp
from .users import user_bp
from .dashboard import dashboard_bp
from .exports import export_bp

admin_bp = Blueprint('admin', __name__)
admin_bp.register_blueprint(lot_bp, url_prefix='')
admin_bp.register_blueprint(spot_bp, url_prefix='')
admin_bp.register_blueprint(user_bp, url_prefix='')
admin_bp.register_blueprint(dashboard_bp, url_prefix='')
admin_bp.register_blueprint(export_bp, url_prefix='')