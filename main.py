import uvicorn
from fastapi import FastAPI
from starlette.requests import Request

from endpoints import user, video
from endpoints.video import templates

app = FastAPI()

app.include_router(video.router, prefix='/video', tags=['Video'])
app.include_router(user.router, prefix='/user', tags=['User'])


@app.get('/404')
async def not_found(request: Request):
    return templates.TemplateResponse('404.html', {'request': request})


if __name__ == '__main__':
    uvicorn.run('main:app', reload=True, port=8000)
