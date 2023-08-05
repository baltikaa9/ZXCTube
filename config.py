import os

from dotenv import load_dotenv

load_dotenv()

DB_URL = os.getenv('DB_URL')
GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')

ACCESS_TOKEN_EXPIRE_MINUTES = 30

SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')
ACCESS_TOKEN_JWT_SUBJECT = os.getenv('ACCESS_TOKEN_JWT_SUBJECT')
