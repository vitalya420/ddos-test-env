from sanic import Sanic
from celery import Celery
from redis.asyncio import Redis


REDIS_URL = "redis://redis:6379/0"

app = Sanic(__name__)
celery = Celery(__name__, broker=REDIS_URL, backend=REDIS_URL)

from . import views  # noqa: E402, F401
from . import tasks  # noqa: E402, F401


@app.before_server_start
async def init_redis(app_):
    redis_ = Redis.from_url(REDIS_URL)
    await redis_.ping()
    app_.ctx.redis = redis_
