from fastapi import FastAPI, APIRouter
from fastapi_users import FastAPIUsers
from pydantic import BaseModel, Field
from auth.auth import auth_backend
from auth.database import User
from auth.manager import get_user_manager
from database.db import Database
from utils.response import check_banks


class App(object):
    def __init__(self):
        self.app = FastAPI()
        self.fastapi_users = FastAPIUsers[User, int](
            get_user_manager,
            [auth_backend],
        )
        self._run_routines()
        self.db = Database()

    @staticmethod
    def _run_routines():
        check_banks()

    def _include_router(self, entity: APIRouter, prefix: str, tags: list):
        self.app.include_router(entity, prefix=prefix, tags=tags)

    def register_routers(self, routers: tuple[tuple[APIRouter, str, list[str]], ...]):
        for entity, prefix, tags in routers:
            self._include_router(entity, prefix=prefix, tags=tags)

    def get_current_user(self):
        return self.fastapi_users.current_user()

    @property
    def middlewares(self):
        return self.app


class BankNameRequest(BaseModel): # Вынести
    bank_name: str = Field(default="")


class CustomNameRequest(BaseModel):
    bank_name_rus: str = Field(default="")
    custom_name_eng: str = Field(default="")