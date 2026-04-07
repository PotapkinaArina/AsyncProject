import time
import asyncio
import aiosqlite
from aiohttp import ClientSession

async def create_db():
    async with aiosqlite.connect("cache_db.sqlite3") as db:
        await db.execute("""CREATE TABLE IF NOT EXISTS urls (
        url TEXT PRIMARY KEY,
        data TEXT NOT NULL,
        start_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        end_time TIMESTAMP NOT NULL
        )""")
        await db.execute("""CREATE INDEX IF NOT EXISTS idx_end_time ON urls (end_time)""")
        await db.commit()


async def get_data(url, session):
    async with aiosqlite.connect("cache_db.sqlite3") as db:
        async with db.execute('SELECT data FROM urls WHERE url = ? AND end_time > datetime("now")', (url,)
        ) as cursor:
            data = await cursor.fetchone()
            if data:
                return data[0]
        data = await conn(url, session)
        if data:
            end_time = 60
            await db.execute("""INSERT OR REPLACE INTO urls (url, data, end_time) VALUES (?, ?, datetime("now", "+" || ? || " seconds")
            )""", (url, data, end_time))
            await db.commit()
            return data
        else :
            return None

async def open_file():
    s = []
    try:
        with open("urls.txt") as f:
            s = [line.strip() for line in f if line.strip() and line.startswith("http")]
    except FileNotFoundError:
        print("File not found")
        exit(1)
    except Exception as e:
        print(f"Error: {e}")
        exit(1)
    else:
        return s

async def conn(url,session):
    try:
        async with session.get(url, timeout=10) as response:
            return await response.text()
    except Exception as e:
        print(f"Error: {e}")
        return None

async def main():
    await create_db()

    s = await open_file()
    async with ClientSession() as session:
        tasks = []
        for url in s:
            tasks.append(asyncio.create_task(get_data(url, session)))
        results = await asyncio.gather(*tasks)
    success = sum(1 for r in results if r is not None)
    print(success)

print(time.strftime('%X'))
asyncio.run(main())
print(time.strftime('%X'))
