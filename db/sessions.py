from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from config import get_settings

settings = get_settings()

async_engine = create_async_engine(settings.DATABASE_URL, echo=True)
async_session_factory = sessionmaker(
    async_engine, class_=AsyncSession, expire_on_commit=False
)
