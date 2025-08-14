import os
import pytest
from tracker_poetry.environment import EnvironmentLoader

@pytest.fixture(autouse=True)
def set_env_vars(monkeypatch):
    monkeypatch.setenv(EnvironmentLoader.APP_VERSION, "1.0.4v")
    monkeypatch.setenv(EnvironmentLoader.DB_SERVER, "localhost")
    monkeypatch.setenv(EnvironmentLoader.AZURE_APP_ID, "80xb-1603-4bf229")
    EnvironmentLoader._loaded = True  # Prevents loading .env

def test_get_app_version():
    assert EnvironmentLoader.get(EnvironmentLoader.APP_VERSION) == "1.0.4v"

def test_get_db_server():
    assert EnvironmentLoader.get(EnvironmentLoader.DB_SERVER) == "localhost"

def test_get_azure_app_id():
    assert EnvironmentLoader.get(EnvironmentLoader.AZURE_APP_ID) == "80xb-1603-4bf229"
