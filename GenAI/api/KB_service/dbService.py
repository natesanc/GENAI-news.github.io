import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def create_connection():
# Connect to PostgreSQL
    conn = psycopg2.connect(
        dbname=os.getenv('POSTGRES_DB'),
        user=os.getenv('POSTGRES_USER'),
        password=os.getenv('POSTGRES_PASSWORD'),
        host=os.getenv('POSTGRES_HOST'),
        port=os.getenv('POSTGRES_PORT')
    )

    print(conn)
    return conn
# cur = conn.cursor()