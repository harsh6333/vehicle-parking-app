from app import create_app, db
import models  # important to import to register models

app = create_app()

with app.app_context():
    db.create_all()
    print("✅ Database and tables created successfully.")
