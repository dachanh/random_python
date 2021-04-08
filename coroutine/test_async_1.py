import asyncio
import time


async def count():
     print("One")
     await asyncio.sleep(1)
     print("Two")

"""
async def main():
    await asyncio.gather(count(),count(),count())
"""

async def main():
    await count()
    await count()
    await count()

if __name__== "__main__":
   start = time.perf_counter()
   event_loop = asyncio.get_event_loop()
   event_loop.run_until_complete(main())
   print(time.perf_counter()-start)
