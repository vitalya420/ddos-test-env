FROM python:3.11

RUN apt-get update && apt-get install -y 

WORKDIR /app

COPY . .

RUN pip install sqlalchemy sanic alembic matplotlib asyncpg psycopg2-binary "redis[hiredis]" celery

