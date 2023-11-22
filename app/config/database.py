import os

from dotenv import load_dotenv
import pymysql
import pymysql.cursors

load_dotenv()

USER = os.environ.get("MYSQL_USER") or "user"
PASSWORD = os.environ.get("MYSQL_PASSWORD") or "password"
HOST = os.environ.get("MYSQL_HOST") or "127.0.0.1"
PORT = int(os.environ.get("MYSQL_PORT") or "3306")
DBNAME = os.environ.get("MYSQL_DBNAME") or "dbname"
APP_ENV = os.environ.get("APP_ENV") or "development"


def get_mysql_url():
    return f"mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}"


def get_mysql_connection():
    ssl = None
    ssl_verify_identity = None

    if APP_ENV != "development":
        ssl = {"ca": "/etc/ssl/cert.pem"}
        ssl_verify_identity = True

    connection = pymysql.connect(
        user=USER,
        password=PASSWORD,
        host=HOST,
        port=PORT,
        database=DBNAME,
        cursorclass=pymysql.cursors.DictCursor,
        ssl=ssl,
        ssl_verify_identity=ssl_verify_identity,
    )

    return connection
