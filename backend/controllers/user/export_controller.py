# backend/controllers/user/exports.py
from flask import jsonify
from flask_jwt_extended import get_jwt_identity
from extensions import cache


class ExportController:
    def trigger_user_export(self):
        try:
            from services.tasks import generate_csv_export
            # user_id = get_jwt_identity()
            generate_csv_export.delay(user_id=3)
            return jsonify({"msg": "Export started"}), 202
        except Exception as e:
            return jsonify({"error": str(e)}), 500