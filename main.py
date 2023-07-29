import uvicorn
from fastapi import FastAPI
from starlette.requests import Request

from endpoints import user_router, video_router, subscribe_router
from endpoints.video import templates

app = FastAPI()

app.include_router(video_router, prefix='/video', tags=['Video'])
app.include_router(user_router, prefix='/user', tags=['User'])
app.include_router(subscribe_router, prefix='/subscribe', tags=['Subscribe'])


@app.get('/404')
async def not_found(request: Request):
    return templates.TemplateResponse('404.html', {'request': request})


if __name__ == '__main__':
    uvicorn.run('main:app', reload=True, port=8000)
