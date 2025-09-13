import psycopg2
from psycopg2 import extras
import functools

#### decorator to log SQL queries
def log_queries(func):
    def wrapper(*args, **kwargs):
        query = kwargs.get('query') if 'query' in kwargs else args[0]
        print(f"[LOG] Executing query: {query}")  # <-- this should print
        result = func(*args, **kwargs)
        print(f"[LOG] Query returned {len(result)} rows")  # <-- optional
        return result
    return wrapper

@log_queries
def fetch_all_users(query):
    conn = psycopg2.connect(
        host="localhost",
        user="postgres",
        password="Myart@2023!",
        dbname="alx_prodev"  # replace with your actual database name
    )
    cursor = conn.cursor(cursor_factory=extras.RealDictCursor)
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return results

#### fetch users while logging the query
users = fetch_all_users(query="SELECT * FROM user_data")
for user in users:
    print(user)
