import os
import logging
from celery import Celery
from flask import Flask, jsonify
from config import Config
from extensions import db, jwt, cache
from flask_cors import CORS

def create_app(test_config=None):
    """Application factory with improved Celery support"""
    app = Flask(__name__, instance_relative_config=True)
    # Configure the application
    if test_config is None:
        app.config.from_object(Config)
    else:
        app.config.from_mapping(test_config)
    
    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app)
    jwt.init_app(app)
    cache.init_app(app)
    CORS(app, origins=["http://localhost:8080"], supports_credentials=True)

    register_blueprints(app)

    configure_logging(app)

    # database and admin user
    with app.app_context():
        initialize_database(app)
        test_redis_connection(app)

    return app

def register_blueprints(app):
    """Register all blueprints with the application"""
    from routes.auth import auth_bp
    from routes.admin import admin_bp
    from routes.user import user_bp
    from utils.redisping import ping_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(admin_bp, url_prefix='/api/admin')
    app.register_blueprint(user_bp, url_prefix='/api/user')
    app.register_blueprint(ping_bp, url_prefix='/try')

def configure_logging(app):
    """Configure application logging"""
    app.logger.setLevel(logging.INFO)
    if not app.debug:
        handler = logging.StreamHandler()
        handler.setLevel(logging.INFO)
        app.logger.addHandler(handler)

def initialize_database(app):
    """Initialize database and create admin user if needed"""
    from models.user import User
    
    if not os.path.exists(os.path.join(app.instance_path, "parking_app.db")):
        app.logger.info("Creating database...")
        db.create_all()

    if not User.query.filter_by(email="admin@example.com").first():
        app.logger.info("Seeding admin user...")
        admin = User(
            username="admin",
            email="admin@example.com",
            is_admin=True
        )
        admin.set_password("admin123")
        db.session.add(admin)
        db.session.commit()
        app.logger.info("Admin seeded: admin@example.com / admin123")
    else:
        app.logger.info("Admin already exists.")

def test_redis_connection(app=None):
    """Test Redis connection"""
    try:
        cache.set("redis_test_key", "connected", timeout=5)
        if cache.get("redis_test_key") == "connected":
            app.logger.info("Redis cache connected successfully.")
        else:
            app.logger.warning("Redis cache set/get failed.")
    except Exception as e:
        app.logger.error(f"Redis connection failed: {e}")





# from flask import Flask, jsonify
# from celery import Celery
# import ssl

# app = Flask(__name__)

# # Aiven Redis over SSL
# REDIS_URL = "redis....."

# app.config["CELERY_BROKER_URL"] = REDIS_URL
# app.config["CELERY_RESULT_BACKEND"] = REDIS_URL

# # Secure Redis SSL options
# ssl_options = {
#     "ssl_cert_reqs": ssl.CERT_NONE,  
# }

# celery = Celery(app.name, broker=REDIS_URL, backend=REDIS_URL)
# celery.conf.update(
#     task_serializer="json",
#     result_serializer="json",
#     accept_content=["json"],
#     broker_use_ssl=ssl_options,
#     redis_backend_use_ssl=ssl_options,
# )

# @celery.task()
# def add(x, y):
#     return x + y

# @app.route('/')
# def add_task():
#     print('hello')
#     for i in range(100):
#         add.delay(i, i)
#     return jsonify({'status': 'ok'})

