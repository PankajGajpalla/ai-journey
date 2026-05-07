# import asyncio

# async def say_hello():
#     print("Hello before wait")
#     await asyncio.sleep(1)
#     print("Hello after wait")

# asyncio.run(say_hello())


# import asyncio

# async def task_one():
#     print("Task 1 starting")
#     await asyncio.sleep(2)
#     print("Task 1 done")
#     return "Result from task 1"

# async def task_two():
#     print("Task 2 starting")
#     await asyncio.sleep(2)
#     print("Task 2 done")
#     return "Result from task 2"

# async def main():
#     results = await asyncio.gather(task_one(), task_two())
#     print(results)

# asyncio.run(main())

# import aiohttp
# import asyncio

# async def fetch_joke(session, category):
#     url = f"https://official-joke-api.appspot.com/jokes/{category}/random"
    
#     async with session.get(url) as response:
#         data = await response.json()
#         return data[0] if isinstance(data, list) else data

# async def main():
#     async with aiohttp.ClientSession() as session:
#         joke = await fetch_joke(session, "programming")
#         print(joke["setup"])
#         print(joke["punchline"])

# asyncio.run(main())


# import aiohttp
# import asyncio

# async def fetch_joke(session, category):
#     url = f"https://official-joke-api.appspot.com/jokes/{category}/random"
#     try:
#         async with session.get(url) as response:
#             data = await response.json()
#             return data[0] if isinstance(data, list) else data
#     except aiohttp.ConnectionError:
#         print("No Internet")
#         return None
#     except aiohttp.ClientResponseError as e:
#         print(f"HTTP Error {e}")
#         return None
#     except Exception as e:
#         print(f"Unexpected error {e}")
#         return None

# async def fetch_all_jokes(categories):
#     async with aiohttp.ClientSession() as session:
#         jokes = await asyncio.gather(
#             fetch_joke(session, categories[0]),
#             fetch_joke(session, categories[1]),
#             fetch_joke(session, categories[2])
#         )
#         return jokes

# def summarize(jokes):
#     for e,joke in enumerate(jokes):
#         print(e+1)
#         print(f"\n[{joke['type']}]")
#         print(f"Q: {joke['setup']}")
#         print(f"A: {joke['punchline']}")
#         print()

# async def main():
#     categories = ["programming", "general", "knock-knock"]
    
#     jokes = await fetch_all_jokes(categories)

#     summarize(jokes)
     
    


# asyncio.run(main())


# import aiohttp
# import asyncio


# async def fetch_joke(session, category):
#     url = f"https://official-joke-api.appspot.com/jokes/{category}/random"
#     try:
#         async with session.get(url, timeout=aiohttp.ClientTimeout(total=5)) as response:
#             response.raise_for_status()
#             data = await response.json()
#             return data[0] if isinstance(data, list) else data
#     except aiohttp.ClientConnectionError:
#         print("No internet")
#         return None
#     except aiohttp.ClientResponseError as e:
#         print(f"HTTP Error: {e}")
#         return None
#     except Exception as e:
#         print(f"Unexpected error: {e}")
#         return None


# async def fetch_all_jokes(categories):
#     async with aiohttp.ClientSession() as session:
#         jokes = await asyncio.gather(*[
#             fetch_joke(session, cat) for cat in categories
#         ])
#         return jokes


# def summarize(jokes):
#     valid = [j for j in jokes if j is not None]
#     print(f"Fetched {len(valid)} jokes:\n")
#     for i, joke in enumerate(valid):
#         print(f"{i+1}. [{joke['type']}] {joke['setup']} — {joke['punchline']}")


# async def main():
#     categories = ["programming", "general", "knock-knock"]
#     jokes = await fetch_all_jokes(categories)
#     summarize(jokes)


# asyncio.run(main())