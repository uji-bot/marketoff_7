import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

database_url = os.environ.get("DATABASE_URL")
if database_url and database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key")
    SQLALCHEMY_DATABASE_URI = database_url or f"sqlite:///{os.path.join(BASE_DIR, 'instance', 'market_off.db')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


import os

class Config:
    # process.env ашиглаж .env файлаас DATABASE_URL-г уншина
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')