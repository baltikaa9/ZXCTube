import os

from dotenv import load_dotenv

load_dotenv()

DB_URL = os.getenv('DB_URL')
GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')

ACCESS_TOKEN_EXPIRE_MINUTES = 30
