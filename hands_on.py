import asyncio
import time


async def long_running_task(s_time) -> None:
    print(f'Async redy to sleep {s_time}')
    await asyncio.sleep(s_time)
    print(f'Well done to sleep {s_time}!')


async def main():
    task1 = asyncio.create_task(long_running_task(5))
    task2 = asyncio.create_task(long_running_task(3))
    task3 = asyncio.create_task(long_running_task(2))

    await asyncio.gather(task1, task2, task3)

s =time.perf_counter()
asyncio.run(main())
elapsed = time.perf_counter() - s
print(f'Exwcution time {elapsed: 0.2f} seconds.')