from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request
from starlette.responses import RedirectResponse, HTMLResponse
from starlette.templating import Jinja2Templates

from api.dependencies import get_session
from services import VideoService, UserService

router = APIRouter(tags=['Frontend'])

templates = Jinja2Templates(directory='frontend/templates')


@router.get('/watch', response_class=HTMLResponse)
async def watch_video(
        v: int,
        request: Request,
        session: AsyncSession = Depends(get_session),
        video_service: VideoService = Depends(),
        user_service: UserService = Depends(),
):
    v = await video_service.get_video(v, session)
    # print(v.model_dump())
    if not v:
        # return RedirectResponse('http://localhost:8000/video/not_found')
        return RedirectResponse('https://www.youtube.com/watch?v=dQw4w9WgXcQ&ab_channel=RickAstley')
    user = await user_service.get_user(v.user, session)
    return templates.TemplateResponse(
        'video.html',
        {'request': request, 'video_id': v.id, 'video': v, 'user': user}
    )


@router.get('/{user_id}', response_class=HTMLResponse)
async def get_user(
        user_id: UUID,
        request: Request,
        session: AsyncSession = Depends(get_session),
        video_service: VideoService = Depends(),
        user_service: UserService = Depends(),
):
    user = await user_service.get_user(user_id, session)
    videos = await video_service.get_videos_by_user(user_id, session)
    return templates.TemplateResponse(
        'user.html',
        {'request': request, 'user': user, 'videos': videos}
    )
