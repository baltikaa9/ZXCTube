from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

import services
from auth.user_manager import fastapi_users, auth_backend
from db.session import get_session
from schemas import GetListVideo, UserRead, UserCreate, UserUpdate

router = APIRouter()


@router.get('/{user_id}')
async def get_user_videos(
        user_id: int,
        session: AsyncSession = Depends(get_session)
) -> list[GetListVideo]:
    return await services.get_videos_by_user(user_id, session)


router.include_router(
    fastapi_users.get_auth_router(auth_backend), prefix="/auth/jwt", tags=["auth"]
)

router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

# router.include_router(
#     fastapi_users.get_reset_password_router(),
#     prefix="/auth",
#     tags=["auth"],
# )
#
# router.include_router(
#     fastapi_users.get_verify_router(UserRead),
#     prefix="/auth",
#     tags=["auth"],
# )
#
# router.include_router(
#     fastapi_users.get_users_router(UserRead, UserUpdate),
#     prefix="/users",
#     tags=["users"],
# )

