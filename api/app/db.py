from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base


# Sync for celery
# Async for this web app

DATABASE_URL = "postgresql://postgres:postgres@postgres:5432/postgres"

sync_engine = create_engine(DATABASE_URL)
async_engine = create_async_engine(
    "postgresql+asyncpg://postgres:postgres@postgres:5432/postgres"
)


sync_sessin_factory = sessionmaker(sync_engine, expire_on_commit=False)
async_session_factory = async_sessionmaker(async_engine, expire_on_commit=False)


Base = declarative_base()
