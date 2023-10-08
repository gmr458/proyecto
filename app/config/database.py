import pymysql
import pymysql.cursors
from dotenv import load_dotenv
import os


def get_mysql_connection():
    load_dotenv()

    connection = pymysql.connect(
        user=os.environ.get("MYSQL_USER"),
        password=os.environ.get("MYSQL_PASSWORD"),
        host=os.environ.get("MYSQL_HOST"),
        port=int(os.environ.get("MYSQL_PORT")),
        database=os.environ.get("MYSQL_DBNAME"),
        cursorclass=pymysql.cursors.DictCursor,
        ssl=None,
        ssl_verify_identity=None,
    )

    return connection
