from flask import Blueprint, jsonify
# from backend.controllers.user.export_controller import ExportController
from backend.middleware.decorators import user_required
from flask_jwt_extended import get_jwt_identity
export_bp = Blueprint('user_export', __name__)
# controller = ExportController()

@export_bp.route('/export/csv', methods=['POST'])
@user_required
def trigger_user_export():
    user_id =get_jwt_identity()
    from backend.services.tasks import generate_csv_export  # ⬅ moved inside
    generate_csv_export.delay(user_id)
    return jsonify({"message": "CSV export job started"}), 202




