FROM python:3.11.1-slim-buster

COPY ./migrations ./migrations
COPY ./backend/db ./backend/db
COPY ./backend/models ./backend/models
COPY ./alembic.ini .
COPY ./config.py .
COPY ./alembic_migrations.sh .
WORKDIR .

RUN python3 -m pip install alembic psycopg2-binary asyncpg python-dotenv

RUN ["chmod", "+x", "./alembic_migrations.sh"]

CMD ./alembic_migrations.sh