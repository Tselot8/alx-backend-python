import psycopg2
from psycopg2.extras import RealDictCursor
from decimal import Decimal

class ExecuteQuery:
    def __init__(self, query, params=None):
        self.query = query
        self.params = params or ()
        self.conn = None
        self.result = None

    def __enter__(self):
        # Open the database connection
        self.conn = psycopg2.connect(
            host='localhost',
            user='postgres',
            password='Myart@2023!',
            dbname='alx_prodev'
        )
        cursor = self.conn.cursor(cursor_factory=RealDictCursor)
        # Execute the query with parameters
        cursor.execute(self.query, self.params)
        self.result = cursor.fetchall()
        cursor.close()
        return self.result  # Return query results to the with-block

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Close the connection
        if self.conn:
            self.conn.close()
        # Do not suppress exceptions
        return False

# Using the context manager
query = "SELECT * FROM user_data WHERE age > %s"
params = (25,)

with ExecuteQuery(query, params) as results:
    print("✅ Query Results for age > 25:")
    for row in results:
        print(row)
