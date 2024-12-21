from fastapi import FastAPI

from src.server import App

fastapi_app = FastAPI()

app = App(fastapi_app)

