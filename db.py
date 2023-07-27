from typing import Generator

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

# metadata = sqlalchemy.MetaData()
# db = databases.Database('sqlite://zxctube.db')

engine = create_async_engine('sqlite+aiosqlite:///zxctube.db')
async_session = async_sessionmaker(engine, expire_on_commit=False)


async def get_session() -> Generator:
    async with async_session() as session:
        yield session
