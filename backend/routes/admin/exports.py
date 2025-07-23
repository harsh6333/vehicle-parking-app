from flask import Blueprint
from controllers.admin.export_controller import ExportController
from middleware.decorators import admin_required

export_bp = Blueprint('admin_export', __name__)
controller = ExportController()

@export_bp.route('/export/csv', methods=['POST'])
@admin_required
def trigger_admin_export():
    return controller.trigger_admin_export()