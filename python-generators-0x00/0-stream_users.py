#!/usr/bin/python3
import psycopg2
from psycopg2.extras import RealDictCursor

def stream_users():
    """Generator that streams rows from user_data table one by one"""
    connection = psycopg2.connect(
        host="localhost",
        user="postgres",         # your PostgreSQL username
        password="Myart@2023!",     # your PostgreSQL password
        dbname="ALX_prodev"      # your PostgreSQL database
    )
    cursor = connection.cursor(cursor_factory=RealDictCursor)

    cursor.execute("SELECT * FROM user_data")
    for row in cursor:
        yield row  # ✅ generator yields one row at a time

    cursor.close()
    connection.close()
