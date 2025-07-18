import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "MAD2_PROJECT")
    SQLALCHEMY_DATABASE_URI = 'sqlite:///parking_app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = '121_YAB_DTC'

    # Cookie-related for cross-site (localhost:5173 <-> localhost:5000)
    JWT_TOKEN_LOCATION = ['cookies']
    JWT_COOKIE_SECURE = True      
    JWT_COOKIE_SAMESITE = "None"
    JWT_COOKIE_CSRF_PROTECT = False 
