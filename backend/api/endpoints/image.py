import os

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

from config import PREVIEW_STORAGE_PATH

router = APIRouter(prefix='/image', tags=['Image'])


@router.get('/preview/{file_name}')
async def get_preview(file_name: str) -> FileResponse:
    path = f'{PREVIEW_STORAGE_PATH}/{file_name}'
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail='File not found')
    return FileResponse(path)
