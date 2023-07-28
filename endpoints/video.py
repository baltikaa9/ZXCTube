from fastapi import APIRouter, UploadFile, Form, File, Depends, HTTPException, BackgroundTasks, Request
from fastapi.responses import StreamingResponse, RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates

import services
from db.session import get_session
from schemas.message import Message
from schemas.user import User
from schemas.video import GetVideo


router = APIRouter()


templates = Jinja2Templates(directory='templates')


@router.post('/')
async def create_video(
        background_tasks: BackgroundTasks,
        title: str = Form(),
        description: str | None = Form(default=None),
        file: UploadFile = File(),
        session: AsyncSession = Depends(get_session),
) -> GetVideo:
    user = await services.get_user(1, session)
    if user is None:
        raise HTTPException(status_code=403, detail='User not exists')

    video = await services.save_video(user.id, file, title, description, background_tasks, session)
    video.user = User.model_validate(user)
    return GetVideo.model_validate(video)


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
        return RedirectResponse('http://localhost:8000/404')
    return templates.TemplateResponse('index.html', {'request': request, 'path': video_id, 'video': video})


@router.delete('/{video_id}')
async def delete_video(
        video_id: int,
        session: AsyncSession = Depends(get_session)
) -> GetVideo:
    user = await services.get_user(1, session)
    video = await services.delete_video(video_id, session)
    video.user = User.model_validate(user)
    return GetVideo.model_validate(video)


@router.get('/test')
async def get_test(request: Request):
    return request.url
