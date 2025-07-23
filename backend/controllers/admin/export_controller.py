from flask import jsonify
from flask_jwt_extended import get_jwt_identity
from services.tasks import generate_csv_export

class ExportController:
    def trigger_admin_export(self):
        admin_id = get_jwt_identity()
        generate_csv_export.delay(admin_id=admin_id)
        return jsonify({"msg": "Export started. You will receive an email when ready."}), 201