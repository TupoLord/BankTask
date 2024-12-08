from fastapi import FastAPI, APIRouter
from fastapi_users import FastAPIUsers
from pydantic import BaseModel, Field
from auth.auth import cookie_transport, get_jwt_strategy
from models.model import user
from auth.manager import get_user_manager, UserManager
from database.db import Database
from router import Router
from utils.response import check_banks
from sdk import SDK
from config.config import Application_Config
from fastapi_users.authentication import AuthenticationBackend



# noinspection PyPropertyDefinition
class App(object):

    def __init__(self, fastapi_app: FastAPI):
        self.app = fastapi_app
        self.auth_backend = AuthenticationBackend(
            name="jwt",
            transport=cookie_transport,
            get_strategy=lambda: get_jwt_strategy(self.conf.DB_SECRET)
        )
        self.fastapi_users = FastAPIUsers[user, int](
            get_user_manager,
            [self.auth_backend],
        )
        self.router = Router(self.auth_backend)
        self.db = Database()
        self.server = SDK()
        self.conf = Application_Config()
        self.manager = UserManager(self.conf)

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