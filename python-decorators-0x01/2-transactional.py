import psycopg2
import functools

# Decorator to handle database connection
def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = psycopg2.connect(
            host='localhost',
            user='postgres',
            password='Myart@2023!',  # replace with your actual password
            dbname='alx_prodev'      # replace with your database name
        )
        try:
            result = func(conn, *args, **kwargs)
        finally:
            conn.close()
        return result
    return wrapper


# Decorator to handle transactions (commit or rollback)
def transactional(func):
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        try:
            result = func(conn, *args, **kwargs)
            conn.commit()
            return result
        except Exception as e:
            conn.rollback()
            raise e
    return wrapper


@with_db_connection
@transactional
def update_user_email(conn, old_email, new_email):
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE user_data SET email = %s WHERE email = %s",
        (new_email, old_email)
    )
    cursor.close()


# ✅ Example: update by existing email
update_user_email(
    old_email="Ross.Reynolds21@hotmail.com",
    new_email="Crawford_Cartwright@hotmail.com"
)

print("✅ Email updated successfully (or rolled back on error).")
