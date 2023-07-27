import uvicorn
from fastapi import FastAPI

from routers import user, video

app = FastAPI()


app.include_router(video.router, prefix='/video', tags=['Video'])
app.include_router(user.router, prefix='/user', tags=['User'])


if __name__ == '__main__':
    uvicorn.run('main:app', reload=True, port=8000)
