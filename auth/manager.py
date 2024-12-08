from typing import Optional
from fastapi import Request
from fastapi_users import BaseUserManager, IntegerIDMixin, models, exceptions, schemas
from fastapi_users.db import BaseUserDatabase

from config.config import Application_Config
from models.model import User
from utils.logger import AppLogger


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):

    def __init__(self, config: Application_Config):
        super().__init__(BaseUserDatabase[models.UP, models.ID])
        self.logger = AppLogger('bank_task_user_manager').get_logger()
        self.reset_password_token_secret = config.DB_SECRET
        self.verification_token_secret = config.DB_SECRET

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        self.logger.info(f"User {user.id} has registered.")

    async def create(
            self,
            user_create: schemas.UC,
            safe: bool = False,
            request: Optional[Request] = None,
    ) -> models.UP:
        await self.validate_password(user_create.password, user_create)
        existing_user = await self.user_db.get_by_email(user_create.email)

        if existing_user is not None:
            self.logger.warning(
                f"User with email {user_create.email} already exists.")
            raise exceptions.UserAlreadyExists()

        user_dict = (
            user_create.create_update_dict()
            if safe
            else user_create.create_update_dict_superuser()
        )

        password = user_dict.pop("password")
        user_dict["hashed_password"] = self.password_helper.hash(password)
        user_dict["role_id"] = 1

        created_user = await self.user_db.create(user_dict)
        self.logger.info(f"User {created_user.id} has been created.")
        await self.on_after_register(created_user, request)
        return created_user

