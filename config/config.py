from dotenv import load_dotenv
import os

load_dotenv()

# class Application_Config:

DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")
DB_SECRET = os.environ.get("DB_SECRET")
DB_URL = os.environ.get("DB_URL")
