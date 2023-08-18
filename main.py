import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from loguru import logger

from config import HOST

app = FastAPI(title='ZXCTube')

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
