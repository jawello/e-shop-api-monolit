FROM python:3.7-alpine
MAINTAINER jawello, jawello@gmail.com

RUN apk update \
  && apk add --virtual build-deps autoconf automake g++ make build-deps gcc python3-dev musl-dev \
  && apk add postgresql-dev \
  && pip install --no-cache-dir psycopg2-binary SQLAlchemy pytoml py-bcrypt aiohttp aiohttp-rest-api \
  aiohttp-security aiohttp-session aioredis\
  && apk del build-deps gcc

COPY . /app

VOLUME ["/config/config.toml"]

WORKDIR /app

ENTRYPOINT ["python", "main.py", "-c", "/config/config.toml"]
#ENTRYPOINT ["python", "generate_data.py", "-c", "/config/config.toml"]

