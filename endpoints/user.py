from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

import services
from db.session import get_session
from schemas import GetListVideo

router = APIRouter()


@router.get('/{user_id}')
async def get_user_videos(
        user_id: int,
        session: AsyncSession = Depends(get_session)
) -> list[GetListVideo]:
    return await services.get_videos_by_user(user_id, session)
