from datetime import timedelta, datetime
from uuid import UUID

import jwt

from config import ACCESS_TOKEN_EXPIRE_MINUTES

ALGORITHM = 'HS256'
ACCESS_TOKEN_JWT_SUBJECT = 'access'
SECRET_KEY = 'dsawqhjriwqhrhqwr'


def create_token(user_id: str) -> dict:
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    return {
        'access_token': create_access_token(
            data={'user_id': user_id}, expires_delta=access_token_expires
        ),
        'token_type': 'Token',
    }


def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({'exp': expire, 'sub': ACCESS_TOKEN_JWT_SUBJECT})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)
    return encoded_jwt
