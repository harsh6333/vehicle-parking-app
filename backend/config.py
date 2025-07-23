import os
from celery.schedules import crontab

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
    CACHE_REDIS_URL = os.getenv('REDIS_URL')
    beat_schedule = {
        'send-daily-reminders': {
            'task': 'services.celery_worker.send_daily_reminders',
            'schedule': crontab(hour=8, minute=0),
        },
        'send-monthly-reports': {
            'task': 'services.celery_worker.send_monthly_reports',
            'schedule': crontab(day_of_month=1, hour=9, minute=0),
        }
    }

    MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.getenv('MAIL_PORT', 587))
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', 'true').lower() in ['true', 'on', '1']
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER', MAIL_USERNAME)

    
