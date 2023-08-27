#!/bin/bash
celery -A backend.services.celery_tasks:celery worker --loglevel=INFO -B
celery -A backend.services.celery_tasks:celery flower