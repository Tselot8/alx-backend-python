#!/usr/bin/python3
import psycopg2
import psycopg2.extras

# ---------------- Generator to fetch users in batches ---------------- #
def stream_users_in_batches(batch_size):
    """
    Generator that fetches rows from user_data table in batches
    """
    connection = psycopg2.connect(
        host="localhost",
        user="postgres",         # replace with your DB user
        password="Myart@2023!",  # replace with your DB password
        database="ALX_prodev"
    )
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
        for row in rows:
            yield row  # yield each user individually
        offset += batch_size

    cursor.close()
    connection.close()


# ---------------- Process batches ---------------- #
def batch_processing(batch_size):
    """
    Processes each batch of users, filtering those over age 25
    """
    for user in stream_users_in_batches(batch_size):
        if user['age'] > 25:
            yield user  # yield filtered users individually
