import os

from celery import Celery

from config import REDIS_URL

celery = Celery('tasks', broker=REDIS_URL)


@celery.task
def _delete_video_file(file_name: str) -> None:
    os.remove(file_name)
