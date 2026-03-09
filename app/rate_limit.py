import time
from fastapi import Request, HTTPException


REQUEST_LIMIT = 5
WINDOW_SECONDS = 60

requests = {}


async def rate_limiter(request: Request):
    """Limita as requisicoes a 5 por minuto."""
    ip = request.client.host
    now = time.time()

    timestamps = requests.get(ip, [])
    timestamps = [t for t in timestamps if now - t < WINDOW_SECONDS]

    if len(timestamps) >= REQUEST_LIMIT:
        raise HTTPException(status_code=429, detail='Too many requests')

    timestamps.append(now)
    requests[ip] = timestamps