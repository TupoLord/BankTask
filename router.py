from auth.schemas import UserRead, UserCreate
from server import app



class Router(object):

    def __init__(self, auth_backend):
        self.auth_backend = auth_backend

    routes = (
            app.fastapi_users.get_register_router(UserRead, UserCreate),
            "/auth/jwt",
            ["auth"],
        ), (
            app.fastapi_users.get_auth_router(auth_backend),
            "/auth",
            ["auth"],
        )
