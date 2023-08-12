from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request
from starlette.responses import RedirectResponse, HTMLResponse
from starlette.templating import Jinja2Templates

from api.dependencies import get_session
from exceptions import UserNotFoundException
from schemas import GetVideoForHTML
from services import VideoService, UserService

router = APIRouter(tags=['Frontend'])

templates = Jinja2Templates(directory='frontend/templates')


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
        # return RedirectResponse('http://localhost:8000/video/not_found')
        return RedirectResponse('https://www.youtube.com/watch?v=dQw4w9WgXcQ&ab_channel=RickAstley')
    author = await user_service.get_user(video.user, session)
    return templates.TemplateResponse(
        'video.html',
        {'request': request, 'video': video, 'author': author}
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
    return templates.TemplateResponse(
        'user.html',
        {'request': request, 'user': user, 'videos': videos}
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
        user=await user_service.get_user(video.user, session),
    ) for video in videos]
    return templates.TemplateResponse(
        'homepage.html',
        {'request': request, 'videos': videos}
    )
