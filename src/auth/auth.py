from fastapi_users.authentication import CookieTransport
from fastapi_users.authentication import JWTStrategy

cookie_transport = CookieTransport(cookie_max_age=3600)


def get_jwt_strategy(DB_SECRET: str) -> JWTStrategy:
    return JWTStrategy(secret=DB_SECRET, lifetime_seconds=3600)



