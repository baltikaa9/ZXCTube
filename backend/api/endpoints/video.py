from typing import Annotated

from fastapi import APIRouter, UploadFile, Form, File, Depends, Request
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession

from backend.api.dependencies import get_current_user
from backend.api.dependencies import get_session
from backend.exceptions import VideoNotFoundException
from backend.models import UserDB
from backend.schemas import GetVideo
from backend.schemas import Message
from backend.services import VideoService

router = APIRouter(prefix='/video', tags=['Video'])


@router.post('/')
async def create_video(
        title: Annotated[str, Form()],
        file: Annotated[UploadFile, File()],
        description: Annotated[str | None, Form()] = None,
        preview: Annotated[UploadFile | None, File()] = None,
        session: AsyncSession = Depends(get_session),
        current_user: UserDB = Depends(get_current_user),
        service: VideoService = Depends()
) -> GetVideo:
    video = await service.save_video(current_user, file, title, description, preview, session)
    return video


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


@router.delete('/{video_id}')
async def delete_video(
        video_id: int,
        session: AsyncSession = Depends(get_session),
        service: VideoService = Depends()
) -> GetVideo:
    video = await service.delete_video(video_id, session)
    if not video:
        raise VideoNotFoundException()
    return video


@router.get('/{video_id}/like')
async def like_video(
        video_id: int,
        session: AsyncSession = Depends(get_session),
        current_user: UserDB = Depends(get_current_user),
        service: VideoService = Depends()
) -> GetVideo:
    video = await service.add_or_delete_like(video_id, session, current_user)
    return video
