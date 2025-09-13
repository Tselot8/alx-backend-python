import psycopg2
import functools
from psycopg2.extras import RealDictCursor

# --- Global query cache ---
query_cache = {}

# --- DB connection decorator ---
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

# --- Cache decorator ---
def cache_query(func):
    @functools.wraps(func)
    def wrapper(conn, query, *args, **kwargs):
        if query in query_cache:
            print("✅ Returning cached result for query:", query)
            return query_cache[query]

        print("⚡ Executing and caching query:", query)
        result = func(conn, query, *args, **kwargs)
        query_cache[query] = result
        return result
    return wrapper

# --- Example function using both decorators ---
@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute(query)
    rows = cursor.fetchall()
    cursor.close()
    return rows

# --- Usage ---
if __name__ == "__main__":
    # First call will hit DB
    users = fetch_users_with_cache(query="SELECT * FROM user_data LIMIT 5")
    print("Users (first call):", users)

    # Second call will use cache
    users_again = fetch_users_with_cache(query="SELECT * FROM user_data LIMIT 5")
    print("Users (cached call):", users_again)
