import time
import os
import uuid
from fastapi import Request, HTTPException
from redis.asyncio import Redis
from dotenv import load_dotenv

load_dotenv()


REQUEST_LIMIT = 5
WINDOW_SECONDS = 60

requests = {}


"""async def rate_limiter(request: Request):
    ip = request.client.host
    now = time.time()

    timestamps = requests.get(ip, [])
    timestamps = [t for t in timestamps if now - t < WINDOW_SECONDS]

    if len(timestamps) >= REQUEST_LIMIT:
        raise HTTPException(status_code=429, detail='Too many requests')

    timestamps.append(now)
    requests[ip] = timestamps"""


REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))
REDIS_DB = int(os.getenv('REDIS_DB', 0))

redis_client = Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, decode_responses=True)

async def rate_limiter(request: Request):
    ip = request.client.host
    key = f'rate_limit:{ip}'
    now = int(time.time())
    member = f'{now}-{uuid.uuid4().hex}'

    pipeline = redis_client.pipeline()
    pipeline.zremrangebyscore(key, 0, now - WINDOW_SECONDS)
    pipeline.zadd(key, {member: now})
    pipeline.zcard(key)
    pipeline.expire(key, WINDOW_SECONDS + 1)
    _, _, count, _ = await pipeline.execute()

    if count > REQUEST_LIMIT:
        raise HTTPException(status_code=429, detail='Too many requests')