import os

from dotenv import load_dotenv

load_dotenv()

VIDEO_STORAGE_PATH = 'data/media'
PREVIEW_STORAGE_PATH = 'data/preview'

DB_URL = os.getenv('DB_URL')
SENTRY_URL = os.getenv('SENTRY_URL')
REDIS_URL = os.getenv('REDIS_URL')
GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')

ACCESS_TOKEN_EXPIRE_MINUTES = 30

SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')
ACCESS_TOKEN_JWT_SUBJECT = os.getenv('ACCESS_TOKEN_JWT_SUBJECT')

HOST = os.getenv('HOST', default='127.0.0.1')
