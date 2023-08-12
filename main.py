import uvicorn
from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

from backend import api_router
from config import HOST
from frontend import fr_router

app = FastAPI(title='ZXCTube')

app.include_router(api_router)
app.include_router(fr_router)

app.mount('/frontend/static', StaticFiles(directory='frontend/static'), name='static')


if __name__ == '__main__':
    uvicorn.run('main:app', port=8000, host=HOST)
