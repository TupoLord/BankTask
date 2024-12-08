from fastapi import FastAPI

from m import App

fastapi_app = FastAPI()

app = App(fastapi_app)

