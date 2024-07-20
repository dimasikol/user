import asyncio

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import create_engine, URL, text
from config_education_sqlalchemy import settings

sync_engine = create_engine(
    url=settings.DATABASE_URL_psycopg,
    echo=True,
    pool_size=5,
)

async_engine = create_async_engine(
    url=settings.DATABASE_URL_asyncpg,
    echo=False,
)

async def get_db(engine):
    async with engine.begin() as connection:
        res = await connection.execute(text("SELECT VERSION()"))
        print(res.all())

if settings.DB_TYPE_CONNECTION == 'async':
    asyncio.run(get_db(async_engine))

elif settings.type_connection == 'sync':
    with sync_engine.connect() as connection: # connect without save, begin with save
        connection.execute(text("SELECT VERSION()"))