import pytest
from tracker_poetry.portfolio_queries import SQLManager
from tracker_poetry.environment import EnvironmentLoader
import pandas as pd

## Integration Tests for SQLManager class

@pytest.fixture
def test_db_credentials():
    EnvironmentLoader.load(env="Testing", dotenv_path="src/tracker_poetry/.env")
    return EnvironmentLoader.get_db_vars()

@pytest.fixture
def sql_manager(test_db_credentials):
    manager = SQLManager(test_db_credentials)
    # Start a transaction
    conn = manager.connection
    conn.autocommit = False
    yield manager
    # Rollback any changes made during the test
    conn.rollback()
    manager.close()

@pytest.fixture
def sql_manager_no_credentials():
    manager = SQLManager()
    return manager

@pytest.fixture
def ppr_entry():
    return  pd.DataFrame([{
    "Number": "001",
    "Name": "Sample Fund",
    "Ticker": "SAMP",
    "Shares": 100.0,
    "Average Unit Cost": 10.5,
    "Current Unit Cost": 11.0,
    "Purchased Value": 1050.00,
    "Market Value": 1100.00,
    "Balance": 50.00,
    "Balance %": 0.0476,
    "Weight %": 0.1000,
    "Statement Date": "2024-01-01",
    "Snapshot ID": 1,
    "Snapshot Timestamp": "2024-01-01 12:00:00"
}])  

# def test_credentials(test_db_credentials):
#     assert test_db_credentials["host"] == "db.fejnwiroicrcemokdefd.supabase.co"
#     assert test_db_credentials["port"] == "5432"
#     assert test_db_credentials["dbname"] == "postgres"

def test_connection(sql_manager):
    assert sql_manager.connection is not None

def test_empty_sqlmanager(sql_manager_no_credentials):
    assert sql_manager_no_credentials.connection is None

def test_insert_ppr_snapshot(sql_manager, ppr_entry):
    affected_rows = sql_manager.insert_snapshot(to_table="ppr", entries=ppr_entry, auto_commit=False)
    assert affected_rows == 1

# def test_next_snapshot_id_empty_table(sql_manager):
#     # Setup: Ensure the table is empty
#     # ...setup code...
#     result = sql_manager.next_snapshot_ID('test_table')
#     assert result == 1  # or your DEFAULT_SNAPSHOT_ID

# def test_insert_snapshot(sql_manager):
#     # Setup: Create a DataFrame with test data
#     import pandas as pd
#     df = pd.DataFrame([{"Snapshot ID": 1, "Snapshot Timestamp": "2024-01-01"}])
#     count = sql_manager.insert_snapshot('test_table', df)
#     assert count == 1
