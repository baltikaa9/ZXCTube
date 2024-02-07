# ZXCTube [pet project]

## About
A small video hosting.

## Features
- Registration and authorization of users using [Google OAuth 2.0](https://developers.google.com/identity/protocols/oauth2?hl=ru)
- Upload and delete videos
- Viewing videos
- Subscriptions to other users
- Likes to videos 
- [API documentation](https://zxctube.ru/docs)

## Built With
![](https://img.shields.io/badge/python-3.11-blue)
![](https://img.shields.io/badge/fastapi-0.100.0-blue)
![](https://img.shields.io/badge/SQL_Alchemy-2.0.19-blue)
![](https://img.shields.io/badge/alembic-1.11.1-blue)
![](https://img.shields.io/badge/asyncpg-0.28.0-blue)
![](https://img.shields.io/badge/pydantic-2.1.1-blue)
![](https://img.shields.io/badge/google_auth-2.22.0-blue)
![](https://img.shields.io/badge/sentry-1.29.2-blue)
![](https://img.shields.io/badge/bootstrap-5-blue)


## Getting Started
### Setup
1. Clone the repo.
    ```sh
    git clone https://github.com/baltikaa9/ZXCTube.git
    ```
2. Define environment variables
    ```sh
   cd ZXCTube
   nano .env
    ```
   
   ```env
   DB_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/zxctube
   GOOGLE_CLIENT_ID=<your_google_client_id>
   SECRET_KEY=<your_secret_key_to_create_access_token>
   ALGORITHM=HS256
   ACCESS_TOKEN_JWT_SUBJECT=access
   SENTRY_URL=<your_sentry_url>
   REDIS_URL=redis://localhost:6379
   LOCAL=True
    ```

### Run docker compose
- For windows
  - Up container: `docker-compose -f docker-compose.yml up --build`
  - Up container in detach mode: `docker-compose -f docker-compose.yml up --build -d`
  - Down container: `docker-compose -f docker-compose.yml down && docker network prune --force`

- For linux
  - Up container: `make up`
  - Up container in detach mode: `make up-d`
  - Down container: `make down`

> WARNING! <br>
> If database connection fails, try again in a few seconds. It could be because postgres server is not running yet.
 
### Run as python script
1. Activate virtual environment.
   ```bat
   python -m venv venv
   venv\Sripts\activate

2. Install requirements.
    ```bat
   pip install -r requirements.txt
   ```

3. Migrate database.
    ```bat
   alembic upgrade head
   ```
4. Run
    ```bat
   uvicorn main:app --reload
   ```
