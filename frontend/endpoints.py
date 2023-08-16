from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request
from starlette.responses import RedirectResponse, HTMLResponse
from starlette.templating import Jinja2Templates

from backend.api.dependencies import get_session
from backend.exceptions import UserNotFoundException
from backend.schemas import GetVideoForHTML
from backend.services import VideoService, UserService
from config import GOOGLE_CLIENT_ID

router = APIRouter(tags=['Frontend'])

templates = Jinja2Templates(directory='frontend/templates')


class Data:
    def __init__(self, **kwargs):
        [setattr(self, field, value) for field, value in kwargs.items()]


@router.get('/ping')
async def ping():
    return {'success': True}


@router.get('/watch', response_class=HTMLResponse)
async def watch_video(
        video_id: Annotated[int, Query(alias='v')],
        request: Request,
        session: AsyncSession = Depends(get_session),
        video_service: VideoService = Depends(),
        user_service: UserService = Depends(),
):
    video = await video_service.get_video(video_id, session)
    if not video:
        # return RedirectResponse('/video/not_found')
        return RedirectResponse('https://www.youtube.com/watch?v=dQw4w9WgXcQ&ab_channel=RickAstley')
    author = await user_service.get_user(video.user, session)
    data = Data(video=video, author=author, client_id=GOOGLE_CLIENT_ID, created_at=video.created_at.strftime('%d.%m.%Y'))
    return templates.TemplateResponse(
        'video.html',
        # {'request': request, 'video': video, 'author': author}
        {'request': request, 'data': data}
    )


@router.get('/not_found')
async def video_not_found(request: Request):
    return templates.TemplateResponse('404.html', {'request': request})


@router.get('/{user_id}', response_class=HTMLResponse)
async def get_user(
        user_id: UUID,
        request: Request,
        session: AsyncSession = Depends(get_session),
        video_service: VideoService = Depends(),
        user_service: UserService = Depends(),
):
    user = await user_service.get_user(user_id, session)
    if not user:
        raise UserNotFoundException()
    videos = await video_service.get_videos_by_user(user_id, session)
    data = Data(videos=videos, user=user, client_id=GOOGLE_CLIENT_ID)
    return templates.TemplateResponse(
        'user.html',
        # {'request': request, 'user': user, 'videos': videos}
        {'request': request, 'data': data}
    )


@router.get('/', response_class=HTMLResponse)
async def get_homepage(
        request: Request,
        session: AsyncSession = Depends(get_session),
        video_service: VideoService = Depends(),
        user_service: UserService = Depends(),
):
    videos = await video_service.get_all_videos(session)
    videos = [GetVideoForHTML(
        id=video.id,
        title=video.title,
        description=video.description,
        file=video.file,
        like_count=video.like_count,
        preview=video.preview,
        created_at=video.created_at,
        user=await user_service.get_user(video.user, session),
    ) for video in videos]
    data = Data(videos=videos, client_id=GOOGLE_CLIENT_ID)
    return templates.TemplateResponse(
        'homepage.html',
        # {'request': request, 'videos': videos}
        {'request': request, 'data': data}
    )
