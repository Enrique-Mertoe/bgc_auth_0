import os
from pathlib import Path

BASE_PATH = Path(os.path.dirname(os.path.abspath(__file__))).resolve()
database_config = {
    "user": "root",
    "password": "",
    "host": "localhost",
    "name": "bgc_accounts",
}


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'jnckjz787dsklajshd87a8sdja'
    FLASKY_MAIL_SUBJECT_PREFIX = '[Flasky]'
    FLASKY_MAIL_SENDER = 'Flasky Admin <flasky@example.com>'
    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')
    _DB_USER = database_config["user"]
    _DB_PASSWORD = database_config["password"]
    _DB_HOST = database_config["host"]
    _DB_NAME = database_config["name"]
    _DB_PORT = database_config.get("port")
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{_DB_USER}:{_DB_PASSWORD}@{_DB_HOST}/{_DB_NAME}"

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    THREADED = True
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')


class TestingConfig(Config):
    TESTING = True


class ProductionConfig(Config): ...


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig,
    "base_path": os.path.dirname(os.path.abspath(__file__))
}
