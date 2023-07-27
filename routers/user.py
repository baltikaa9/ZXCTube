from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db import get_session
import services
from schemas import GetListVideo

router = APIRouter()


@router.get('/{user_id}')
async def get_user_videos(
        user_id: int,
        session: AsyncSession = Depends(get_session)
) -> list[GetListVideo]:
    return await services.get_videos_by_user(user_id, session)
