from typing import AsyncGenerator
from fastapi import Depends
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from models.model import User
from utils.logger import app_logger

DATABASE_URL = f"postgresql+asyncpg://{app.conf.DB_USER}:{app.conf.DB_PASS}@{app.conf.DB_HOST}:{app.conf.DB_PORT}/{app.conf.DB_NAME}"


engine = create_async_engine(DATABASE_URL)
async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        app_logger.info("Создание асинхронной сессии к базе данных")
        yield session
        app_logger.info("Закрытие асинхронной сессии к базе данных")

async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    app_logger.info("Получение объекта SQLAlchemyUserDatabase")
    yield SQLAlchemyUserDatabase(session, User)
