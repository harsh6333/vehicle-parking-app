from flask import Blueprint
from backend.controllers.admin.user_controller import UserController
from backend.middleware.decorators import admin_required
from backend.extensions import cache

user_bp = Blueprint('admin_user', __name__)
controller = UserController()

@user_bp.route('/users', methods=['GET'])
@admin_required
@cache.cached(timeout=60, key_prefix="admin_users_list")
def list_users():
    return controller.list_users()