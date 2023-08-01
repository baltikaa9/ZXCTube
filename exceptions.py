from fastapi import HTTPException


class VideoNotFoundException(Exception):
    def __init__(self):
        raise HTTPException(status_code=404, detail='Video not found')


class UserNotFoundException(Exception):
    def __init__(self):
        raise HTTPException(status_code=404, detail='User not found')
