import aiohttp
import asyncio


async def fetch_joke(session, category):
    url = f"https://official-joke-api.appspot.com/jokes/{category}/random"
    try:
        async with session.get(url, timeout=aiohttp.ClientTimeout(total=5)) as response:
            response.raise_for_status()
            data = await response.json()
            return data[0] if isinstance(data, list) else data
    except aiohttp.ClientConnectionError:
        print("No internet")
        return None
    except aiohttp.ClientResponseError as e:
        print(f"HTTP Error: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None


async def fetch_all_jokes(categories):
    async with aiohttp.ClientSession() as session:
        jokes = await asyncio.gather(*[
            fetch_joke(session, cat) for cat in categories
        ])
        return jokes


def summarize(jokes):
    valid = [j for j in jokes if j is not None]
    print(f"Fetched {len(valid)} jokes:\n")
    for i, joke in enumerate(valid):
        print(f"{i+1}. [{joke['type']}] {joke['setup']} — {joke['punchline']}")


async def main():
    categories = ["programming", "general", "knock-knock"]
    jokes = await fetch_all_jokes(categories)
    summarize(jokes)


asyncio.run(main())