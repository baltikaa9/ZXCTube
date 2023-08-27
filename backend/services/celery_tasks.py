import os

from celery import Celery

from config import REDIS_URL

celery_app = Celery('tasks', broker=REDIS_URL)


@celery_app.task
def _delete_video_file(file_name: str) -> None:
    os.remove(file_name)
