from fastapi import FastAPI, APIRouter
from fastapi_users import FastAPIUsers
from auth.auth import cookie_transport, get_jwt_strategy
from basic_app import BasicApp
from models.model import User
from auth.manager import UserManager
from router import Router
from sdk import SDK
from utils.response import check_banks
from fastapi_users.authentication import AuthenticationBackend
from dependencies import get_user_manager

class App(BasicApp):

	def __init__(self, fastapi_app: FastAPI):
		super().__init__()
		self.app = fastapi_app
		self.auth_backend = AuthenticationBackend(
			name="jwt",
			transport=cookie_transport,
			get_strategy=lambda: get_jwt_strategy(self.conf.DB_SECRET)
		)
		self.user_manager = UserManager(self.conf)

		# Initialize FastAPIUsers with the standalone dependency function
		self.fastapi_users = FastAPIUsers[User, int](
			get_user_manager,  # Use the standalone function
			[self.auth_backend],
		)
		self.router = Router(self.auth_backend)
		self.server = SDK(
			logger=self.logger,
			db=self.db,
			current_user_callback=self.get_current_user
		)
		self._run_routines()

	def _run_routines(self):
		self.register_routers(self.router.get_routes(self.fastapi_users))
		check_banks(self.db.session)

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
