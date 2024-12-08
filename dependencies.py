from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase

from auth.manager import UserManager
from models.model import User
from database.db import BankManager  # Adjust the import as necessary

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with BankManager.get_async_session() as session:
        yield session

async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)

async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)