#!/usr/bin/python3

import psycopg2
import psycopg2.extras

def connect_to_prodev():
    """Connect to ALX_prodev database and return the connection or None"""
    try:
        connection = psycopg2.connect(
            host="localhost",
            user="postgres",
            password="Myart@2023!",
            database="ALX_prodev"
        )
        return connection
    except:
        pass  # skip if connection fails

def stream_users_in_batches(batch_size):
    """
    Generator that yields batches of users from user_data.
    Each batch is a list of rows (dicts).
    """
    connection = connect_to_prodev()
    if connection:
        cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        offset = 0
        while True:
            cursor.execute(
                "SELECT user_id, name, email, age FROM user_data ORDER BY user_id LIMIT %s OFFSET %s;",
                (batch_size, offset)
            )
            rows = cursor.fetchall()
            if not rows:
                break
            yield rows  # ✅ yield a whole batch at once
            offset += batch_size
        cursor.close()
        connection.close()

def batch_processing(batch_size):
    """
    Processes users in batches and prints only those older than 25.
    """
    for batch in stream_users_in_batches(batch_size):   # loop 1
        for user in batch:                              # loop 2
            if user["age"] > 25:
                print(user)