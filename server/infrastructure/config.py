import os
from dotenv import load_dotenv
load_dotenv()
class Config:
    FLASK_ENV = os.getenv("FLASK_ENV", "production")
    FLASK_DEBUG = int(os.getenv("FLASK_DEBUG", 0))
    FLASK_PORT = int(os.getenv("FLASK_PORT", 5000))
    POSTGRES_USER = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_DB = os.getenv("POSTGRES_DB")
    POSTGRES_HOST = os.getenv("POSTGRES_HOST")
    POSTGRES_PORT = int(os.getenv("POSTGRES_PORT", 5432))
    DATABASE_URL = os.getenv("DATABASE_URL")