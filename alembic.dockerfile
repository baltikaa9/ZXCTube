FROM python:3.11.1-slim-buster

COPY ./migrations ./migrations
COPY ./backend/db ./backend/db
COPY ./backend/models ./backend/models
COPY ./alembic.ini .
COPY ./config.py .
COPY ./alembic_upgrade.sh .
WORKDIR .

RUN python3 -m pip install alembic psycopg2-binary asyncpg python-dotenv

#RUN sleep 10
#
#CMD ["alembic", "upgrade", "head"]
