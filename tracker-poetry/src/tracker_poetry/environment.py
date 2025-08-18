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
        if env not in ["Development", "Production", "Testing"]:
            raise ValueError("Environment must be either 'Development', 'Production' or 'Testing'.")
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
        _processed_var_name = None
        if EnvironmentLoader._env == "Testing": 
            _processed_var_name = f"{var_name}_TEST"
        elif EnvironmentLoader._env == "Development":
            _processed_var_name = f"{var_name}_DEV"
        else:
            _processed_var_name = var_name

        return os.getenv(_processed_var_name, default)

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