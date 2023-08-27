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

#RUN ["chmod", "+x", "./app.sh"]

#CMD ./app.sh

CMD ["uvicorn", "main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "8000", "--forwarded-allow-ips='*'"]
