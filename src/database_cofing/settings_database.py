from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from ..models.base_settings_models import BaseModel
from ..models.user_model import User
#from src.core import DEBUG
DEBUG = True

if DEBUG:
    SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///./database.db"
else:
    SQLALCHEMY_DATABASE_URL = "sqlite+sqlite:///./database.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
async_session_maker = sessionmaker(autocommit=False, autoflush=False, bind=engine)


async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.create_all)


async def get_async_session():
    async with async_session_maker() as session:
        yield session

