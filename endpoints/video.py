from typing import Annotated

from fastapi import APIRouter, UploadFile, Form, File, Depends, BackgroundTasks, Request
from fastapi.responses import StreamingResponse, RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates

import services
from dependencies import current_active_user
from dependencies import get_session
from models import UserDB
from schemas import GetVideo
from schemas import Message

router = APIRouter()


templates = Jinja2Templates(directory='templates')


@router.post('/')
async def create_video(
        background_tasks: BackgroundTasks,
        title: Annotated[str, Form()],
        file: Annotated[UploadFile, File()],
        description: Annotated[str | None, Form()] = None,
        session: AsyncSession = Depends(get_session),
        current_user: UserDB = Depends(current_active_user),
) -> GetVideo:
    video = await services.save_video(current_user, file, title, description, background_tasks, session)
    return video


@router.get('/not_found')
async def video_not_found(request: Request):
    return templates.TemplateResponse('404.html', {'request': request})


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
    if not video:
        # return RedirectResponse('http://localhost:8000/video/not_found')
        return RedirectResponse('https://www.youtube.com/watch?v=dQw4w9WgXcQ&ab_channel=RickAstley')
    return templates.TemplateResponse('index.html', {'request': request, 'path': video_id, 'video': video})


@router.delete('/{video_id}')
async def delete_video(
        video_id: int,
        session: AsyncSession = Depends(get_session),
        current_user: UserDB = Depends(current_active_user),
) -> GetVideo:
    video = await services.delete_video(video_id, current_user, session)
    return video


@router.get('/test')
async def get_test(request: Request):
    return request.url
