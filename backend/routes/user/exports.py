from flask import Blueprint
from controllers.user.export_controller import ExportController
from middleware.decorators import user_required

export_bp = Blueprint('user_export', __name__)
controller = ExportController()

@export_bp.route('/export/csv', methods=['GET'])
# @user_required
def trigger_user_export():
    return controller.trigger_user_export()