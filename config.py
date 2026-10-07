from dotenv import load_dotenv
import os
from urllib.parse import quote_plus

load_dotenv()


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "change-this-in-production")
    MYSQL_USER = os.getenv("MYSQL_USER", "root").strip()
    MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "").strip()
    MYSQL_HOST = os.getenv("MYSQL_HOST", "127.0.0.1").strip()
    MYSQL_PORT = os.getenv("MYSQL_PORT", "3306").strip()
    MYSQL_DB = os.getenv("MYSQL_DB", "asset_intelligence").strip()

    _db_user = quote_plus(MYSQL_USER)
    _db_password = quote_plus(MYSQL_PASSWORD)
    _db_name = quote_plus(MYSQL_DB)
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        f"mysql+pymysql://{_db_user}:{_db_password}@{MYSQL_HOST}:{MYSQL_PORT}/{_db_name}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {"pool_pre_ping": True, "pool_recycle": 280}
