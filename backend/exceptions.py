from fastapi import HTTPException


class VideoNotFoundException(HTTPException):
    def __init__(self):
        super().__init__(status_code=404, detail='Video not found')


class UserNotFoundException(HTTPException):
    def __init__(self):
        super().__init__(status_code=404, detail='User not found')
