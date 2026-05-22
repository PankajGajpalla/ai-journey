# import asyncio
# import aiohttp

# async def fetch_one(session, url):
#     async with session.get(url) as response:
#         data = await response.json()
#         return data

# async def main():
#     url = "https://official-joke-api.appspot.com/random_joke"
    
#     async with aiohttp.ClientSession() as session:
#         joke = await fetch_one(session, url)
    
#     print(joke)

# asyncio.run(main())



import asyncio
import aiohttp
import time

async def fetch_joke(session, category):
    url = f"https://official-joke-api.appspot.com/jokes/{category}/random"
    async with session.get(url) as response:
        data = await response.json()
        return data[0]    # API returns a list, take first item

async def main():
    categories = ["programming", "general", "knock-knock"]
    
    start = time.time()
    
    async with aiohttp.ClientSession() as session:
        jokes = await asyncio.gather(
            fetch_joke(session, categories[0]),
            fetch_joke(session, categories[1]),
            fetch_joke(session, categories[2])
        )
    
    end = time.time()
    
    for joke in jokes:
        print(f"[{joke['type']}] {joke['setup']} — {joke['punchline']}")
    
    print(f"\nTotal time: {end - start:.2f}s")

asyncio.run(main())