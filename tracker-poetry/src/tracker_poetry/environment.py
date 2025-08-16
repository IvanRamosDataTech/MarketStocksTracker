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
    def get_environment() -> str:
        if EnvironmentLoader._env is None:
            raise ValueError("Environment not loaded. Call load() first.")
        return EnvironmentLoader._env

    @staticmethod
    def get_app_version() -> str:
        return EnvironmentLoader._get("APP_VERSION", "1.0.0")
    
    @staticmethod
    def get_db_vars() -> dict:
        return {
            "host": EnvironmentLoader._get("DB_SERVER"),
            "dbname": EnvironmentLoader._get("DB_NAME"),
            "user": EnvironmentLoader._get("DB_USER"),
            "password": EnvironmentLoader._get("DB_PASSWORD"),
            "port": EnvironmentLoader._get("DB_PORT")
        }
    
    @staticmethod
    def get_azure_app_id():
        return EnvironmentLoader._get("AZURE_APP_ID")

    @staticmethod
    def resolve_excel_file() -> str:
        return EnvironmentLoader._get("EXCEL_FILE")