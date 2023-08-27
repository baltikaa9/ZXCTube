FROM python:3.11.1-slim-buster

COPY ./backend/services/celery_tasks.py ./backend/services/celery_tasks.py
COPY ./config.py .
COPY ./data ./data
#COPY ./run_celery.sh .
WORKDIR .

RUN python3 -m pip install celery flower redis python-dotenv

#RUN ["chmod", "+x", "./run_celery.sh"]

CMD celery -A backend.services.celery_tasks:celery_app worker --loglevel=INFO -B