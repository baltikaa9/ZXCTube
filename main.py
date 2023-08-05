import uvicorn
from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

from api import api_router
from frontend import fr_router

app = FastAPI(title='ZXCTube')

app.include_router(api_router)
app.include_router(fr_router)

app.mount('/frontend/static', StaticFiles(directory='frontend/static'), name='static')


if __name__ == '__main__':
    uvicorn.run('main:app', reload=True, port=8000)
