import os

from dotenv import load_dotenv
import pymysql
import pymysql.cursors

load_dotenv()

user = os.environ.get("MYSQL_USER") or "user"
password = os.environ.get("MYSQL_PASSWORD") or "password"
host = os.environ.get("MYSQL_HOST") or "127.0.0.1"
port = int(os.environ.get("MYSQL_PORT") or "3306")
dbname = os.environ.get("MYSQL_DBNAME") or "dbname"


def get_mysql_url():
    return f"mysql+pymysql://{user}:{password}@{host}:{port}/{dbname}"


def get_mysql_connection():
    connection = pymysql.connect(
        user=user,
        password=password,
        host=host,
        port=port,
        database=dbname,
        cursorclass=pymysql.cursors.DictCursor,
        ssl=None,
        ssl_verify_identity=None,
    )

    return connection
