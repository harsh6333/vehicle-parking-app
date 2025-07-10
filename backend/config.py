import os
class Config:
    SECRET_KEY=os.getenv("SECRET_KEY","MAD2_PROJECT")
    SQLALCHEMY_DATABASE_URI = 'sqlite:///parking_app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False