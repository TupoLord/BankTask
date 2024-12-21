from src.auth.schemas import UserRead, UserCreate


class Router(object):
    def __init__(self, auth_backend):
        self.auth_backend = auth_backend

    def get_routes(self, fastapi_users):
        return (
            fastapi_users.get_register_router(UserRead, UserCreate),
            "/auth/jwt",
            ["auth"],
        ), (
            fastapi_users.get_auth_router(self.auth_backend),
            "/auth",
            ["auth"],
        )
