from dotenv import load_dotenv
import os

load_dotenv()

class Application_Config:

    def __init__(self):
        self.DB_HOST = os.environ.get("DB_HOST")
        self.DB_PORT = os.environ.get("DB_PORT", 5432)
        self.DB_NAME = os.environ.get("DB_NAME")
        self.DB_USER = os.environ.get("DB_USER")
        self.DB_PASS = os.environ.get("DB_PASS")
        self.DB_SECRET = os.environ.get("DB_SECRET")
        self.DB_URL = os.environ.get("DB_URL")


