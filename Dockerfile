FROM python:3.11.1-slim-buster

COPY requirements.txt .

RUN apt-get -y update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    openssl libssl-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# pip & poetry
RUN python3 -m pip install --user --upgrade pip && \
    python3 -m pip install -r requirements.txt

COPY . .
WORKDIR .

CMD ["python", "main.py"]