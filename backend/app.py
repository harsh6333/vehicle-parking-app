from flask import Flask
from config import Config
from extensions import db, jwt
from routes.auth import auth_bp
from flask_cors import CORS
from models.user import User  
import os

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    jwt.init_app(app)
    CORS(app)

    app.register_blueprint(auth_bp, url_prefix='/api/auth')

    with app.app_context():
        if not os.path.exists("instance/parking_app.db"): 
            print("Creating database...")
        db.create_all()

        if not User.query.filter_by(email="admin@example.com").first():
            print("Seeding admin user...")
            admin = User(
                username="admin",
                email="admin@example.com",
                is_admin=True
            )
            admin.set_password("admin123")
            db.session.add(admin)
            db.session.commit()
            print("Admin seeded: admin@example.com / admin123")
        else:
            print("Admin already exists.")

    return app
