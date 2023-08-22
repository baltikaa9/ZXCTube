import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from loguru import logger
import sentry_sdk

from config import HOST

sentry_sdk.init(
    dsn="https://2963fb855b14dd7256ad02bdf6f2c959@o4505749463105536.ingest.sentry.io/4505749492924416",

    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production,
    traces_sample_rate=1.0,
)

app = FastAPI(title='ZXCTube')


@app.get("/sentry-debug")
async def trigger_error():
    division_by_zero = 1 / 0


try:
    from backend import api_router

    app.include_router(api_router)
except Exception as e:
    logger.exception(e)
try:
    from frontend import fr_router

    app.include_router(fr_router)
except Exception as e:
    logger.exception(e)

app.mount('/frontend/static', StaticFiles(directory='frontend/static'), name='static')

if __name__ == '__main__':
    logger.add('logs.log', enqueue=True, serialize=True)
    uvicorn.run('main:app', port=8000, host=HOST)
