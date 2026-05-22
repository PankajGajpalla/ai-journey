import asyncio
import aiohttp
import time

async def fetch_joke(session, category):
    if category.startswith("http"):
        url = category   # use directly for testing
    else:
        url = f"https://official-joke-api.appspot.com/jokes/{category}/random"
    try:
        async with session.get(url, timeout=aiohttp.ClientTimeout(total=5)) as response:
            response.raise_for_status()
            data = await response.json()
            return data[0]
    except aiohttp.ClientConnectionError:
        print(f"❌ No connection for {category}")
        return None
    except aiohttp.ClientResponseError as e:
        print(f"❌ HTTP error for {category}: {e.status}")
        return None
    except Exception as e:
        print(f"❌ Error for {category}: {e}")
        return None

async def main():
    categories = ["programming", "general", "knock-knock", "https://thisurldoesnotexist123.com/fail"]
    
    async with aiohttp.ClientSession() as session:
        jokes = await asyncio.gather(*[
            fetch_joke(session, c) for c in categories
        ])
    
    valid_jokes = [j for j in jokes if j is not None]
    
    print(f"\nFetched {len(valid_jokes)} jokes successfully:\n")
    for i, joke in enumerate(valid_jokes, 1):
        print(f"{i}. [{joke['type']}] {joke['setup']} — {joke['punchline']}")

asyncio.run(main())