from flask import Flask
from config import Config
from extensions import db, jwt, cache
from routes.auth import auth_bp
from routes.admin import admin_bp
from routes.user import user_bp
from models.user import User
from flask_cors import CORS
import os
from utils.redisping import ping_bp
import logging

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    jwt.init_app(app)
    cache.init_app(app)  # Initialize caching
    CORS(app, origins=["http://localhost:8080"], supports_credentials=True)

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(admin_bp, url_prefix='/api/admin')
    app.register_blueprint(user_bp, url_prefix='/api/user')
    app.register_blueprint(ping_bp, url_prefix='/try')

    # logging 
    app.logger.setLevel(logging.INFO)

    with app.app_context():
        if not os.path.exists("instance/parking_app.db"):
            app.logger.info(" Creating database...")
            db.create_all()

        # Seed admin user if not present
        if not User.query.filter_by(email="admin@example.com").first():
            app.logger.info(" Seeding admin user...")
            admin = User(
                username="admin",
                email="admin@example.com",
                is_admin=True
            )
            admin.set_password("admin123")
            db.session.add(admin)
            db.session.commit()
            app.logger.info(" Admin seeded: admin@example.com / admin123")
        else:
            app.logger.info("Admin already exists.")

        # ✅ Redis connection test
        try:
            cache.set("redis_test_key", "connected", timeout=5)
            if cache.get("redis_test_key") == "connected":
                app.logger.info(" Redis cache connected successfully.")
            else:
                app.logger.warning(" Redis cache set/get failed.")
        except Exception as e:
            app.logger.error(f" Redis connection failed: {e}")

    return app
