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
    Generator that fetches rows from user_data in batches of batch_size.
    """
    connection = connect_to_prodev()
    if connection:  # only proceed if connection succeeded
        cursor = connection.cursor()
        offset = 0

        while True:
            cursor.execute(
                "SELECT user_id, name, email, age FROM user_data ORDER BY user_id LIMIT %s OFFSET %s;",
                (batch_size, offset)
            )
            rows = cursor.fetchall()
            if not rows:
                break
            for row in rows:
                yield {
                    "user_id": row[0],
                    "name": row[1],
                    "email": row[2],
                    "age": row[3]
                }
            offset += batch_size

        cursor.close()
        connection.close()


def batch_processing(batch_size):
    """
    Processes users in batches and prints only those older than 25.
    """
    batch = []
    for user in stream_users_in_batches(batch_size):
        if user["age"] > 25:
            batch.append(user)
        if len(batch) == batch_size:
            for u in batch:
                print(u)
            batch = []

    # Print remaining users if any
    for u in batch:
        print(u)
