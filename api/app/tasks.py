import pickle

from redis import Redis

from . import celery
from .db import sync_sessin_factory

redis_client = Redis.from_url("redis://redis:6379/0")


celery.conf.beat_schedule = {
    "save_hits_to_db": {
        "task": "app.tasks.save_hits_to_db",
        "schedule": 10.0,
    }
}

celery.conf.timezone = "UTC"


@celery.task
def save_hits_to_db():
    hits_data = redis_client.lrange("hits", 0, -1)
    hits = [pickle.loads(hit) for hit in hits_data]

    with sync_sessin_factory() as session:
        with session.begin():
            session.add_all(hits)
    redis_client.ltrim("hits", 1, 0)
