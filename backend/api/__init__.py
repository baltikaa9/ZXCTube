from fastapi import APIRouter

from .endpoints import video_router, user_router, subscribe_router, auth_router, image_router

api_router = APIRouter(prefix='/api')

api_router.include_router(video_router)
api_router.include_router(user_router)
api_router.include_router(subscribe_router)
api_router.include_router(auth_router)
api_router.include_router(image_router)
