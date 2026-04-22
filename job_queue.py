from collections import deque
import asyncio

queue = deque()
lock = asyncio.Lock()

async def add_job(job):
    async with lock:
        queue.append(job)

async def get_job():
    async with lock:
        if queue:
            return queue.popleft()
        return None