import psycopg2
import time
import functools
from psycopg2.extras import RealDictCursor


# --- Decorator for DB connection ---
def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = psycopg2.connect(
            host="localhost",
            user="postgres",
            password="Myart@2023!",
            dbname="alx_prodev"
        )
        try:
            result = func(conn, *args, **kwargs)
        finally:
            conn.close()
        return result
    return wrapper


# --- Retry decorator ---
def retry_on_failure(retries=3, delay=2):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempts += 1
                    print(f"⚠️ Attempt {attempts} failed: {e}")
                    if attempts >= retries:
                        print("❌ All retry attempts failed.")
                        raise
                    print(f"⏳ Retrying in {delay} seconds...")
                    time.sleep(delay)
        return wrapper
    return decorator


# --- Example function using both decorators ---
@with_db_connection
@retry_on_failure(retries=3, delay=1)
def fetch_users_with_retry(conn):
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute("SELECT * FROM user_data")  # your actual table is user_data
    result = cursor.fetchall()
    cursor.close()
    return result


# --- Run with retry ---
users = fetch_users_with_retry()
print("✅ Users fetched:", users)
