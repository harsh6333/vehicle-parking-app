import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "MAD2_PROJECT")
    SQLALCHEMY_DATABASE_URI = 'sqlite:///parking_app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = '121_YAB_DTC'

    JWT_TOKEN_LOCATION = ['cookies']
    JWT_COOKIE_SECURE = True
    JWT_COOKIE_SAMESITE = "None"
    JWT_COOKIE_CSRF_PROTECT = False

    CACHE_TYPE = "redis"
    CACHE_REDIS_URL =os.getenv('REDIS_URL')
