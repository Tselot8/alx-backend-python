#!/usr/bin/python3
import psycopg2
import csv
import uuid
from psycopg2.extras import RealDictCursor

# ---------------- Database setup functions ---------------- #

def connect_db():
    """Connect to the PostgreSQL server (no DB selected yet)."""
    try:
        connection = psycopg2.connect(
            host="localhost",
            user="postgres",       # replace with your PostgreSQL user
            password="Myart@2023!"    # replace with your PostgreSQL password
        )
        connection.autocommit = True  # needed to create DB
        return connection
    except psycopg2.Error as e:
        print(f"Error connecting to PostgreSQL: {e}")
        return None

def create_database(connection):
    """Create ALX_prodev database if it does not exist."""
    cursor = connection.cursor()
    cursor.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = 'ALX_prodev';")
    exists = cursor.fetchone()
    if not exists:
        cursor.execute("CREATE DATABASE ALX_prodev;")
        print("Database ALX_prodev created")
    else:
        print("Database ALX_prodev already exists")
    cursor.close()

def connect_to_prodev():
    """Connect to ALX_prodev database."""
    try:
        connection = psycopg2.connect(
            host="localhost",
            user="postgres",
            password="admin123",
            dbname="ALX_prodev"
        )
        return connection
    except psycopg2.Error as e:
        print(f"Error connecting to ALX_prodev: {e}")
        return None

def create_table(connection):
    """Create user_data table if it does not exist."""
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_data (
            user_id UUID PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL UNIQUE,
            age DECIMAL NOT NULL
        );
    """)
    connection.commit()
    cursor.close()
    print("Table user_data created successfully")

def insert_data(connection, csv_file):
    """Insert rows from CSV file if they don’t already exist."""
    cursor = connection.cursor()
    with open(csv_file, newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            user_id = str(uuid.uuid4())  # generate UUID
            name = row["name"]
            email = row["email"]
            age = row["age"]

            cursor.execute("""
                INSERT INTO user_data (user_id, name, email, age)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (email) DO NOTHING
            """, (user_id, name, email, age))
    connection.commit()
    cursor.close()
    print(f"Data inserted from {csv_file}")

# ---------------- Generator function ---------------- #

def stream_users():
    """Generator that streams rows from user_data table one by one."""
    connection = connect_to_prodev()
    if connection:
        cursor = connection.cursor(cursor_factory=RealDictCursor)
        cursor.execute("SELECT * FROM user_data;")
        for row in cursor:
            yield row
        cursor.close()
        connection.close()
