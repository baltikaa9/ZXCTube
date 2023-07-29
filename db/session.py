from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

DB_URL = 'sqlite+aiosqlite:///zxctube.db'

engine = create_async_engine(DB_URL)
async_session = async_sessionmaker(engine, expire_on_commit=False)
