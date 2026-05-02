from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from app.core.configuration import settings


db_url = f"mysql+aiomysql://{settings.db_username}:{settings.db_password}@{settings.db_host}:{settings.db_port}/{settings.db_name}"
engine = create_async_engine(db_url)
async_session_local = async_sessionmaker(bind=engine, expire_on_commit=False)


async def get_session():
    async with async_session_local() as session:
        yield session