#!/usr/bin/python3
seed = __import__('seed')

# ---------------- Helper: fetch a page of users ---------------- #
def paginate_users(page_size, offset):
    """Fetch a single page of users from the database."""
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(f"SELECT * FROM user_data LIMIT {page_size} OFFSET {offset}")
    rows = cursor.fetchall()
    cursor.close()
    connection.close()
    return rows

# ---------------- Generator: lazy pagination ---------------- #
def lazy_pagination(page_size):
    """Generator that lazily fetches pages of users."""
    offset = 0
    while True:  # ✅ Only one loop
        page = paginate_users(page_size, offset)
        if not page:
            break
        yield page
        offset += page_size
