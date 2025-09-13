import asyncio
import asyncpg
from decimal import Decimal

DB_CONFIG = {
    "user": "postgres",
    "password": "Myart@2023!",
    "database": "alx_prodev",
    "host": "localhost",
    "port": 5432,
}

# Async function to fetch all users
async def async_fetch_users(pool):
    async with pool.acquire() as conn:
        rows = await conn.fetch("SELECT * FROM user_data")
        return rows

# Async function to fetch users older than 40
async def async_fetch_older_users(pool):
    async with pool.acquire() as conn:
        rows = await conn.fetch("SELECT * FROM user_data WHERE age > $1", 40)
        return rows

# Function to fetch both queries concurrently
async def fetch_concurrently():
    # Create a connection pool
    pool = await asyncpg.create_pool(**DB_CONFIG)

    # Schedule both queries concurrently, each acquires its own connection
    all_users_task = async_fetch_users(pool)
    older_users_task = async_fetch_older_users(pool)

    all_users, older_users = await asyncio.gather(all_users_task, older_users_task)

    print("All users:")
    for user in all_users:
        print(dict(user))

    print("\nUsers older than 40:")
    for user in older_users:
        print(dict(user))

    await pool.close()

# Run the concurrent fetch
asyncio.run(fetch_concurrently())
