from fastapi import APIRouter, UploadFile, Form, File, Depends, HTTPException, BackgroundTasks, Request
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates

import services
from db import get_session
from schemas import Message

router = APIRouter()


templates = Jinja2Templates(directory='templates')


@router.post('/')
async def create_video(
        background_tasks: BackgroundTasks,
        title: str = Form(),
        description: str = Form(),
        file: UploadFile = File(),
        session: AsyncSession = Depends(get_session),
) -> services.VideoInfo:
    user = await services.get_user(1, session)
    if user is None:
        raise HTTPException(status_code=403, detail='User not found')

    return await services.save_video(user.id, file, title, description, background_tasks, session)


@router.get('/{video_id}', responses={404: {'model': Message}})
async def get_video(
        video_id: int,
        request: Request,
        session: AsyncSession = Depends(get_session)
) -> StreamingResponse:
    file, status_code, content_length, headers = await services.open_file(video_id, request, session)

    response = StreamingResponse(
        file,
        media_type='video/mp4',
        status_code=status_code
    )

    response.headers.update({
        'Accept-Ranges': 'bytes',
        'Content-Length': str(content_length),
        **headers,
    })
    return response


@router.get('/index/{video_id}', response_class=HTMLResponse)
async def get_video(
        video_id: int,
        request: Request,
        session: AsyncSession = Depends(get_session)
):
    video = await services.get_video(video_id, session)
    return templates.TemplateResponse('index.html', {'request': request, 'path': video_id, 'video': video})


@router.get('/test')
async def get_test(request: Request):
    return request.url
