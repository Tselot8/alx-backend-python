import psycopg2
import functools
from psycopg2.extras import RealDictCursor

def with_db_connection(func):
    def wrapper(*args, **kwargs):
        conn = psycopg2.connect(
            host='localhost',
            user='postgres',
            password='Myart@2023!',
            dbname='alx_prodev'
        )
        try:
            result=func(conn, *args, **kwargs)
        finally:
            conn.close()
        return result
    return wrapper

@with_db_connection
def get_user_by_id(conn, user_id):
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute("SELECT * FROM user_data WHERE id = %s", (user_id,))
    result = cursor.fetchone()
    cursor.close()
    return result

#### Fetch user by ID with automatic connection handling
user = get_user_by_id(user_id=1)
print(user)
