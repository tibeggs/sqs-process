import psycopg2
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD

def get_db():
    connection = psycopg2.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        dbname=DB_NAME,
        port=int(DB_PORT)
    )
    return connection
