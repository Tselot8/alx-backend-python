import psycopg2
from psycopg2.extras import RealDictCursor


class DatabaseConnection:
    def __init__(self, host, user, password, dbname):
        self.host = host
        self.user = user
        self.password = password
        self.dbname = dbname
        self.conn = None

    def __enter__(self):
        # Open connection when entering the context
        self.conn = psycopg2.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            dbname=self.dbname
        )
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Rollback on error, else commit
        if exc_type is not None:
            self.conn.rollback()
        else:
            self.conn.commit()
        # Always close connection
        self.conn.close()


if __name__ == "__main__":
    # Use the custom context manager
    with DatabaseConnection(
        host="localhost",
        user="postgres",
        password="Myart@2023!",
        dbname="alx_prodev"
    ) as conn:
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute("SELECT * FROM user_data LIMIT 5;")
        results = cursor.fetchall()
        cursor.close()

        print("✅ Query Results:")
        for row in results:
            print(row)
