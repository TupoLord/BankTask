from auth.auth import auth_backend
from auth.schemas import UserRead, UserCreate
from server import app

class Router(object):
    routes = (
            app.fastapi_users.get_register_router(UserRead, UserCreate),
            "/auth/jwt",
            ["auth"],
        ), (
            app.fastapi_users.get_auth_router(auth_backend),
            "/auth",
            ["auth"],
        )
