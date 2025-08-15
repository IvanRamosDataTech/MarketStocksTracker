from dotenv import load_dotenv
from pathlib import Path
import os

class EnvironmentLoader:
    """
    Loads environment variables from a .env file for the application.
    Ensures variables are available for all scripts.
    """
    _loaded = False
    _env = None

    @classmethod
    def load(cls, env, dotenv_path=".env"):
        if env not in ["Development", "Production"]:
            raise ValueError("Environment must be either 'Development' or 'Production'.")
        cls._env = env
        if not cls._loaded:
            load_dotenv(dotenv_path=Path(dotenv_path))
            cls._loaded = True

    @classmethod
    def clear(cls):
        cls._loaded = False
        cls._env = None

    @staticmethod
    def _get(var_name, default=None):
        return os.getenv(f"{var_name}_DEV" if EnvironmentLoader._env == "Development" else var_name, default)

    @staticmethod
    def get_app_version() -> str:
        return EnvironmentLoader._get("APP_VERSION", "1.0.0")
    
    @staticmethod
    def get_db_vars() -> dict:
        return {
            "DB_SERVER": EnvironmentLoader._get("DB_SERVER"),
            "DB_NAME": EnvironmentLoader._get("DB_NAME"),
            "DB_USER": EnvironmentLoader._get("DB_USER"),
            "DB_PASSWORD": EnvironmentLoader._get("DB_PASSWORD"),
            "PORT": EnvironmentLoader._get("DB_PORT")
        }
    
    @staticmethod
    def get_azure_app_id():
        return EnvironmentLoader._get("AZURE_APP_ID")

    