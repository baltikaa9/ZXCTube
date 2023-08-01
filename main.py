import uvicorn
from fastapi import FastAPI

from endpoints import user_router, video_router, subscribe_router, auth_router

app = FastAPI()

app.include_router(video_router, prefix='/video', tags=['Video'])
app.include_router(user_router, prefix='/user', tags=['User'])
app.include_router(subscribe_router, prefix='/subscribe', tags=['Subscribe'])
app.include_router(auth_router, tags=['Auth'])


if __name__ == '__main__':
    uvicorn.run('main:app', reload=True, port=8000)
