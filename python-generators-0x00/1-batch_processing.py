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
        password="yourpassword", # replace with your DB password
        database="ALX_prodev"
    )
    cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cursor.execute("SELECT * FROM user_data;")

    while True:
        rows = cursor.fetchmany(batch_size)
        if not rows:
            break
        yield rows  # yields a batch of rows

    cursor.close()
    connection.close()


# ---------------- Process batches ---------------- #
def batch_processing(batch_size):
    """
    Processes each batch of users, filtering those over age 25
    """
    for batch in stream_users_in_batches(batch_size):  # loop 1
        for user in batch:                              # loop 2
            if user['age'] > 25:
                yield user                              # yield filtered users
