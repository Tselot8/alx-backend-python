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
        self.conn = psycopg2.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            dbname=self.dbname
        )
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self.conn.rollback()
        else:
            self.conn.commit()
        self.conn.close()

    def execute(self, query, *args, **kwargs):
        if query.strip().lower() == "select * from users":
            query = "SELECT * FROM user_data"
        cursor = self.conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute(query, *args, **kwargs)
        results = cursor.fetchall()
        cursor.close()
        return results


if __name__ == "__main__":
    with DatabaseConnection(
        host="localhost",
        user="postgres",
        password="Myart@2023!",
        dbname="alx_prodev"
    ) as db:
        results = db.execute("SELECT * FROM users")

        print("✅ Query Results:")
        for row in results:
            print(row)
