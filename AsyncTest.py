import time
import asyncio
from aiohttp import ClientSession

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
    s = await open_file()
    async with ClientSession() as session:
        tasks = []
        for url in s:
            tasks.append(asyncio.create_task(conn(url, session)))
        results = await asyncio.gather(*tasks)
    count = 0
    for result in results:
        if result is not None:
            try:
                with open(f"file_{count}.html", "w", encoding="utf-8") as f:
                    f.write(result)
            except Exception as e:
                print(f"Error: {e}")
            finally: count += 1
        else:
            continue

print(time.strftime('%X'))
asyncio.run(main())
print(time.strftime('%X'))

