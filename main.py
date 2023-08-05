import uvicorn
from fastapi import FastAPI

from api import api_router

app = FastAPI(title='ZXCTube')

app.include_router(api_router)


if __name__ == '__main__':
    uvicorn.run('main:app', reload=True, port=8000)
