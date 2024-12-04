from fastapi import FastAPI, APIRouter
from fastapi_users import FastAPIUsers
from pydantic import BaseModel, Field
from auth.auth import auth_backend
from auth.database import User
from auth.manager import get_user_manager
from database.db import Database
from router import Router
from utils.response import check_banks


# noinspection PyPropertyDefinition
class App(object):
    router = property(
        fset=lambda self, value: self.register_routers(value.routes),
    )
    def __init__(self):
        self.app = FastAPI()
        self.fastapi_users = FastAPIUsers[User, int](
            get_user_manager,
            [auth_backend],
        )
        self.router = Router()
        self.db = Database()

    def set_router(self):

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

    def start(self):
        self._run_routines()

    @property
    def middlewares(self):
        return self.app


class BankNameRequest(BaseModel): # Вынести
    bank_name: str = Field(default="")


class CustomNameRequest(BaseModel):
    bank_name_rus: str = Field(default="")
    custom_name_eng: str = Field(default="")