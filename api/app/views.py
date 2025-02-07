import pickle
from http import HTTPStatus
from datetime import datetime, timedelta
from io import BytesIO

from sanic.request import Request
from sanic.response import HTTPResponse

from sqlalchemy import func, select
import matplotlib.pyplot as plt

from . import app
from app.db import async_session_factory
from app.models import Hit


@app.route("/hits")
async def hits(request: Request):
    N = 1
    now = datetime.utcnow()
    five_minutes_ago = now - timedelta(minutes=2)

    stmt = (
        select(
            (func.floor(func.extract("epoch", Hit.ts) / N) * N).label("interval_start"),
            func.count(Hit.id).label("requests_per_interval"),
        )
        .where(Hit.ts >= five_minutes_ago)
        .group_by("interval_start")
        .order_by("interval_start")
    )

    async with async_session_factory() as session:
        async with session.begin():
            results = (await session.execute(stmt)).all()

    intervals = [
        datetime.fromtimestamp(float(interval_start)) for interval_start, _ in results
    ]
    rps_values = [rps for _, rps in results]

    plt.figure(figsize=(10, 5))
    plt.plot(intervals, rps_values, marker="o", linestyle="-")
    plt.xlabel("Time Interval")
    plt.ylabel(f"Requests per {N} seconds")
    plt.title("Requests Per Interval")
    plt.grid(True)
    plt.xticks(rotation=45)

    buf = BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    plt.close()

    return HTTPResponse(body=buf.read(), headers={"Content-Type": "image/png"})


@app.route("/hit1")
async def hit1(request: Request):
    """
    Write hit in redis. Celery worker will write in db.
    """
    hit = Hit(ts=datetime.utcnow())
    serialized_hit = pickle.dumps(hit)

    await request.app.ctx.redis.rpush("hits", serialized_hit)
    return HTTPResponse(status=HTTPStatus.ACCEPTED, body="Accepted")


@app.route("/hit2")
async def hit2(request: Request):
    """
    Write hit directly to database.
    """
    hit = Hit()
    async with async_session_factory() as session:
        async with session.begin():
            session.add(hit)
    return HTTPResponse(status=HTTPStatus.ACCEPTED, body="Accepted")
