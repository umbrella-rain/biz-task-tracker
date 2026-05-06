from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase

SQLALCHEMY_DATABASE_URL = "postgresql+asyncpg://postgres:Password@127.0.0.1:5432/postgres"
engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True)
SessionLocal = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)



class Base(DeclarativeBase):
    pass

async def get_db():
    async with SessionLocal() as db:
        try:
            yield db
        finally:
            await db.close()
