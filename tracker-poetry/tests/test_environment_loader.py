import os
import pytest
from tracker_poetry.environment import EnvironmentLoader

@pytest.fixture
def env_vars(monkeypatch):
    monkeypatch.setenv("APP_VERSION", "1.0.4v")
    monkeypatch.setenv("APP_VERSION_DEV", "0.56.1beta")
    monkeypatch.setenv("DB_SERVER", "db.supabase.urgttyz889")
    monkeypatch.setenv("DB_PORT", "5432")
    monkeypatch.setenv("DB_NAME", "prod_db")
    monkeypatch.setenv("DB_USER", "prod_user")
    monkeypatch.setenv("DB_PASSWORD", "prod_password")
    monkeypatch.setenv("DB_SERVER_DEV", "localhost")
    monkeypatch.setenv("DB_PORT_DEV", "1123")
    monkeypatch.setenv("DB_NAME_DEV", "test_db")
    monkeypatch.setenv("DB_USER_DEV", "test_user")
    monkeypatch.setenv("DB_PASSWORD_DEV", "test_password")
    monkeypatch.setenv("AZURE_APP_ID", "80xb-1603-4bf229")
    monkeypatch.setenv("AZURE_APP_ID_DEV", "1111-2222-wweplt")
    monkeypatch.setenv("EXCEL_FILE", "/Portfolios/prod_excel_file.xlsx")
    monkeypatch.setenv("EXCEL_FILE_DEV", "/Portfolios/test_excel_file.xlsx")
    EnvironmentLoader._loaded = True  # Prevents loading .env

@pytest.fixture
def dev_loader():
    EnvironmentLoader.load("Development")
    return EnvironmentLoader
    
@pytest.fixture
def prod_loader():
    EnvironmentLoader.load("Production")
    return EnvironmentLoader

def test_get_environment(dev_loader):
    assert EnvironmentLoader.get_environment() == "Development"

def test_get_environment(prod_loader):
    assert EnvironmentLoader.get_environment() == "Production"

def test_invalid_environment(env_vars):
    with pytest.raises(ValueError) as excinfo:
        EnvironmentLoader.load("InvalidEnvironment")
    assert "Environment must be either 'Development' or 'Production'." in str(excinfo.value)

def test_get_dev_app_version(dev_loader, env_vars):
    assert EnvironmentLoader.get_app_version() == "0.56.1beta"
    
def test_get_app_version(prod_loader, env_vars):
    assert EnvironmentLoader.get_app_version() == "1.0.4v"

def test_get_dev_db_vars(dev_loader, env_vars):
    db_vars = EnvironmentLoader.get_db_vars()
    assert db_vars["host"] == "localhost"
    assert db_vars["port"] == "1123"
    assert db_vars["dbname"] == "test_db"
    assert db_vars["user"] == "test_user"
    assert db_vars["password"] == "test_password"

def test_get_prod_db_vars(prod_loader, env_vars):
    db_vars = EnvironmentLoader.get_db_vars()
    assert db_vars["host"] == "db.supabase.urgttyz889"
    assert db_vars["port"] == "5432"
    assert db_vars["dbname"] == "prod_db"
    assert db_vars["user"] == "prod_user"
    assert db_vars["password"] == "prod_password"


def test_get_azure_ap_id(prod_loader, env_vars):
    assert EnvironmentLoader.get_azure_app_id() == "80xb-1603-4bf229"

def test_get_azure_ap_id_dev(dev_loader, env_vars):
    assert EnvironmentLoader.get_azure_app_id() == "1111-2222-wweplt"

def test_resolve_excel_file_path(dev_loader, env_vars):
    assert EnvironmentLoader.resolve_excel_file() == "/Portfolios/test_excel_file.xlsx"

def test_resolve_excel_file_path(prod_loader, env_vars):
    assert EnvironmentLoader.resolve_excel_file() == "/Portfolios/prod_excel_file.xlsx"
