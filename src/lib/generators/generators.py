from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from src.auth.manager import UserManager
from src.config.config import Application_Config
from src.database.db import Database
from src.models.model import User


def get_config() -> Application_Config:
    return Application_Config()


def get_db() -> Database:
    return Database(Application_Config())

async def get_session(db: Database = Depends(get_db)) -> AsyncSession:
    async with db.async_session() as session:
        yield session


async def get_user_db(
    session: AsyncSession = Depends(get_session),
) -> SQLAlchemyUserDatabase:
    return SQLAlchemyUserDatabase(session, User)


async def get_user_manager(
    user_db: SQLAlchemyUserDatabase = Depends(get_user_db),
    config: Application_Config = Depends(get_config),
) -> UserManager:
    return UserManager(config, user_db)
