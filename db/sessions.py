from sqlalchemy import URL

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker

from models import Base

url_object = URL.create(
    "postgresql+asyncpg",
    username="postgres",
    password="pg123",
    host="localhost",
    database="postgres",
)

async_engine = create_async_engine(
    url_object,
    #future=True,
    echo=True,
    execution_options={"isolation_level": "AUTOCOMMIT"},
)

async_session_factory = async_sessionmaker(async_engine, expire_on_commit=False, class_=AsyncSession)
