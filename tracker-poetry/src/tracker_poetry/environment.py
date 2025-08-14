from dotenv import load_dotenv
from pathlib import Path
import os

class EnvironmentLoader:
    """
    Loads environment variables from a .env file for the application.
    Ensures variables are available for all scripts.
    """
    _loaded = False
    
    APP_VERSION = "APP_VERSION"
    DB_SERVER = "DB_SERVER"
    DB_PORT = "DB_PORT"
    DB_USER = "DB_USER"
    

    AZURE_APP_ID = "AZURE_APP_ID"

    @classmethod
    def load(cls, dotenv_path=".env"):
        if not cls._loaded:
            load_dotenv(dotenv_path=Path(dotenv_path))
            cls._loaded = True

    @staticmethod
    def get(var_name, default=None):
        return os.getenv(var_name, default)
    
    @staticmethod
    def get_db_vars() -> dict:
        return {
            "DB_SERVER": EnvironmentLoader.get(EnvironmentLoader.DB_SERVER),
            "DB_NAME": EnvironmentLoader.get(EnvironmentLoader.DB_NAME),
            "DB_USER": EnvironmentLoader.get(EnvironmentLoader.DB_USER),
            "DB_PASSWORD": EnvironmentLoader.get(EnvironmentLoader.DB_PASSWORD),
        }

    