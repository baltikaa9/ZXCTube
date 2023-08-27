#!/bin/bash
sleep 10
alembic upgrade head
uvicorn main:app --proxy-headers --host 0.0.0.0 --port 8000 --forwarded-allow-ips='*'