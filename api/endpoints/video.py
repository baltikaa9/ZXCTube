from typing import Annotated

from fastapi import APIRouter, UploadFile, Form, File, Depends, BackgroundTasks, Request
from fastapi.responses import StreamingResponse, RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates


from api.dependencies import get_current_user
from api.dependencies import get_session
from models import UserDB
from schemas import GetVideo
from schemas import Message
from services import VideoService, UserService

router = APIRouter(prefix='/video', tags=['Video'])


templates = Jinja2Templates(directory='templates')


@router.post('/')
async def create_video(
        background_tasks: BackgroundTasks,
        title: Annotated[str, Form()],
        file: Annotated[UploadFile, File()],
        description: Annotated[str | None, Form()] = None,
        session: AsyncSession = Depends(get_session),
        current_user: UserDB = Depends(get_current_user),
        service: VideoService = Depends()
) -> GetVideo:
    video = await service.save_video(current_user, file, title, description, background_tasks, session)
    return video


@router.get('/not_found')
async def video_not_found(request: Request):
    return templates.TemplateResponse('404.html', {'request': request})


@router.get('/{video_id}', responses={404: {'model': Message}})
async def get_video(
        video_id: int,
        request: Request,
        session: AsyncSession = Depends(get_session),
        service: VideoService = Depends(),
) -> StreamingResponse:
    file, status_code, content_length, headers = await service.open_file(video_id, request, session)

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


# @router.get('/index/{video_id}', response_class=HTMLResponse)
# async def get_video(
#         video_id: int,
#         request: Request,
#         session: AsyncSession = Depends(get_session),
#         video_service: VideoService = Depends(),
#         user_service: UserService = Depends(),
# ):
#     video = await video_service.get_video(video_id, session)
#     if not video:
#         # return RedirectResponse('http://localhost:8000/video/not_found')
#         return RedirectResponse('https://www.youtube.com/watch?v=dQw4w9WgXcQ&ab_channel=RickAstley')
#     user = await user_service.get_user(video.user, session)
#     return templates.TemplateResponse(
#         'video.html',
#         {'request': request, 'path': video_id, 'video': video, 'user': user}
#     )


@router.delete('/{video_id}')
async def delete_video(
        video_id: int,
        session: AsyncSession = Depends(get_session),
        service: VideoService = Depends()
) -> GetVideo:
    video = await service.delete_video(video_id, session)
    return video


@router.post('/{video_id}/like')
async def like_video(
        video_id: int,
        session: AsyncSession = Depends(get_session),
        current_user: UserDB = Depends(get_current_user),
        service: VideoService = Depends()
):
    video = await service.add_or_delete_like(video_id, session, current_user)
    return video
