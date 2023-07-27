from fastapi import APIRouter, UploadFile, Form, File, Depends, HTTPException, BackgroundTasks, Request
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession

import services
from db import get_session
from schemas import GetVideo, Message

router = APIRouter()


@router.post('/')
async def create_video(
        background_tasks: BackgroundTasks,
        title: str = Form(),
        description: str = Form(),
        file: UploadFile = File(),
        session: AsyncSession = Depends(get_session),
) -> services.VideoInfo:
    user = await services.get_user(session, 1)
    if user is None:
        raise HTTPException(status_code=403, detail='User not found')

    return await services.save_video(user.id, file, title, description, background_tasks, session)


@router.get('/{video_id}', response_model=GetVideo, responses={404: {'model': Message}})
async def get_video(
        video_id: int,
        session: AsyncSession = Depends(get_session)
) -> StreamingResponse:
    video = await services.get_video(session, video_id)
    if not video:
        raise HTTPException(status_code=404, detail='Video not found')

    def iterable():
        with open(video.file, 'rb') as file_like:
            yield from file_like

    return StreamingResponse(iterable(), media_type='video/mp4')


@router.get('/test')
async def get_test(request: Request):
    return request.url
