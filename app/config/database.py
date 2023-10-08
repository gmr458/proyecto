import pymysql
import pymysql.cursors
from dotenv import load_dotenv
import os


def get_mysql_connection():
    load_dotenv()

    connection = pymysql.connect(
        user=os.environ.get("MYSQL_USER", "root"),
        password=os.environ.get("MYSQL_PASSWORD", "password"),
        host=os.environ.get("MYSQL_HOST", "localhost"),
        port=int(os.environ.get("MYSQL_PORT", "3306")),
        database=os.environ.get("MYSQL_DBNAME", "proyecto"),
        cursorclass=pymysql.cursors.DictCursor,
        ssl=None,
        ssl_verify_identity=None,
    )

    return connection
