# test_db.py
import asyncio
import asyncpg
import os

async def test_connection():
    try:
        # Replace with your actual connection string
        conn = await asyncpg.connect(
            "postgresql://postgres:slon_311.@212.111.87.142:5666/postgres"
        )
        print("✅ Database connection successful!")
        await conn.close()
    except Exception as e:
        print(f"❌ Connection failed: {e}")

if __name__ == "__main__":
    asyncio.run(test_connection())