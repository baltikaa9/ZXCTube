import sentry_sdk
import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis

from backend import api_router
from config import HOST, SENTRY_URL
from frontend import fr_router

sentry_sdk.init(
    dsn=SENTRY_URL,
    traces_sample_rate=1.0,
)

app = FastAPI(title='ZXCTube')

app.include_router(api_router)
app.include_router(fr_router)

app.mount('/frontend/static', StaticFiles(directory='frontend/static'), name='static')


@app.on_event("startup")
async def startup():
    redis = aioredis.from_url("redis://localhost")
    FastAPICache.init(RedisBackend(redis), prefix="zxctube-cache")


if __name__ == '__main__':
    uvicorn.run('main:app', port=8000, host=HOST)
