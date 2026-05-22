# import asyncio

# async def say_hi():
#     print("Hi!")

# asyncio.run(say_hi())

# async def say_hi() — this defines a special function called a coroutine. It's like a regular function, but it can pause and resume.
# asyncio.run(...) — this starts Python's "event loop" — the thing that runs async functions.
# That's it. That's the minimum async program. Just 2 keywords.


# import asyncio

# async def say_hi():
#     print("Hi!")

# say_hi()    # notice: no asyncio.run, just calling it normally



# async def           → creates a COROUTINE
#                       (a pausable function, NOT executed yet)

# await something     → PAUSE here, wait for result, then continue
#                       (only allowed inside async def)

# asyncio.run(...)    → starts the EVENT LOOP
#                       (the thing that actually runs coroutines)

# asyncio.gather(...) → run MANY coroutines at once, wait for all




