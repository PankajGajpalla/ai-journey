import asyncio
import time

async def slow_task(name, seconds):
    print(f"{name} starting...")
    await asyncio.sleep(seconds)
    print(f"{name} done!")
    return name

async def main():
    start = time.time()
    
    # Both tasks run AT THE SAME TIME with gather
    results = await asyncio.gather(
        slow_task("Task A", 2),
        slow_task("Task B", 2)
    )
    
    print(f"Got: {results}")
    
    end = time.time()
    print(f"Time taken: {end - start:.1f}s")

asyncio.run(main())