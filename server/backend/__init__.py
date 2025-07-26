import os
import logging
import ssl
from celery import Celery
from celery.schedules import crontab
from flask import Flask, jsonify
from backend.config import Config
from backend.extensions import db, jwt, cache
from flask_cors import CORS
from dotenv import load_dotenv
load_dotenv()


celery = Celery(
    "backend",
    broker=os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0"),
    backend=os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/1"),
    include=["backend.tasks.tasks"],
)
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



    class ContextTask(celery.Task):
            def __call__(self, *args, **kwargs):
                with app.app_context():
                    return self.run(*args, **kwargs)

    celery.Task = ContextTask
    # Configure Celery
    celery.conf.update(
        enable_utc=False,
        timezone="Asia/Kolkata",
        broker_connection_retry_on_startup=True,
        task_track_started=True,
        task_ignore_result=False,
        beat_schedule={
            "daily-reminder": {
                "task": "backend.tasks.tasks.send_daily_reminders",
                "schedule": crontab(
                    hour=18,
                    minute=18,
                ),
            },
            "monthly-report": {
                "task": "backend.tasks.tasks.send_monthly_reports",
                "schedule": crontab(hour=22, minute=57, day_of_month="4"),
            },
           
        },
       
    )

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
    from backend.routes.auth import auth_bp
    from backend.routes.admin import admin_bp
    from backend.routes.user import user_bp
    from backend.utils.redisping import ping_bp
    
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
    from backend.models.user import User
    
    if not os.path.exists(os.path.join(app.instance_path, "parking_app.db")):
        app.logger.info("Creating database...")
        db.create_all()

    if not User.query.filter_by(email="theoneharsh2003@gmail.com").first():
        app.logger.info("Seeding admin user...")
        admin = User(
            username="admin",
            email="theoneharsh2003@gmail.com",
            is_admin=True
        )
        admin.set_password("admin123")
        db.session.add(admin)
        db.session.commit()
        app.logger.info("Admin seeded: theoneharsh2003@gmail.com / admin123")
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




