from dotenv import load_dotenv
import datetime as dt
import os

load_dotenv()


class Config:
    SECRET_KEY = os.getenv('FLASK_SECRET_KEY')

    SQLALCHEMY_DATABASE_URI = os.getenv('POSTGRES_URL_WORK')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_SECRET_KEY = os.getenv('FLASK_JWT_SECRET_KEY')
    JWT_TOKEN_LOCATION = ["headers", 'cookies']
    JWT_REFRESH_COOKIE_NAME = "refresh_token_cookie"
    JWT_COOKIE_SECURE = True
    JWT_ACCESS_TOKEN_EXPIRES = dt.timedelta(minutes=20)
    JWT_REFRESH_TOKEN_EXPIRES = dt.timedelta(days=30)

    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
