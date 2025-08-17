import pytest
from tracker_poetry.portfolio_queries import SQLManager
from tracker_poetry.environment import EnvironmentLoader
import pandas as pd
import datetime
import tracker_poetry.constants as constants

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

@pytest.fixture
def indexed_entries():
    return pd.DataFrame([
        {
            "Number": "IDX001",
            "Name": "Index Fund A",
            "Ticker": "IDXA",
            "Shares": 50.0,
            "To Buy": 10.0,
            "Average Unit Cost": 20.0,
            "Potential Average Unit Cost": 19.5,
            "Current Unit Cost": 21.0,
            "Unit Cost Diff %": 0.0500,
            "Purchased Value": 1000.00,
            "Market Value": 1050.00,
            "Potential Purchased Value": 1100.00,
            "Balance": 50.00,
            "Balance %": 0.0476,
            "Current Weight %": 0.2000,
            "Potential Weight %": 0.2200,
            "Target Weight %": 0.2500,
            "Snapshot ID": 1,
            "Snapshot Timestamp": "2024-01-01 12:00:00",
            "Current Unit Cost (Original)": 20.5
        },
        {
            "Number": "IDX002",
            "Name": "Index Fund B",
            "Ticker": "IDXB",
            "Shares": 75.0,
            "To Buy": 5.0,
            "Average Unit Cost": 30.0,
            "Potential Average Unit Cost": 29.0,
            "Current Unit Cost": 31.0,
            "Unit Cost Diff %": 0.0667,
            "Purchased Value": 2250.00,
            "Market Value": 2325.00,
            "Potential Purchased Value": 2350.00,
            "Balance": 75.00,
            "Balance %": 0.0323,
            "Current Weight %": 0.3000,
            "Potential Weight %": 0.3200,
            "Target Weight %": 0.3500,
            "Snapshot ID": 1,
            "Snapshot Timestamp": "2024-01-01 12:00:00",
            "Current Unit Cost (Original)": 30.5
        },
        {
            "Number": "GKXX515",
            "Name": "Debt Fund",
            "Ticker": "GUBX",
            "Shares": 42.8,
            "To Buy": 0,
            "Average Unit Cost": 17.50,
            "Potential Average Unit Cost": 17.50,
            "Current Unit Cost": 15.82,
            "Unit Cost Diff %": -0.0667,
            "Purchased Value": 4520.00,
            "Market Value": 4427.816,
            "Potential Purchased Value": 16.30,
            "Balance": 75.00,
            "Balance %": 0.0323,
            "Current Weight %": 0.3000,
            "Potential Weight %": 0.3200,
            "Target Weight %": 0.3500,
            "Snapshot ID": 2,
            "Snapshot Timestamp": "2024-12-24 18:19:32",
            "Current Unit Cost (Original)": 30.5
        },
        {
            "Number": "23BB08",
            "Name": "Bovespra Ltd",
            "Ticker": "BVP",
            "Shares": 42.8,
            "To Buy": 0,
            "Average Unit Cost": 17.50,
            "Potential Average Unit Cost": 17.50,
            "Current Unit Cost": 15.82,
            "Unit Cost Diff %": -0.0667,
            "Purchased Value": 4520.00,
            "Market Value": 4427.816,
            "Potential Purchased Value": 16.30,
            "Balance": 75.00,
            "Balance %": 0.0323,
            "Current Weight %": 0.3000,
            "Potential Weight %": 0.3200,
            "Target Weight %": 0.3500,
            "Snapshot ID": 2,
            "Snapshot Timestamp": "2024-12-24 18:19:32",
            "Current Unit Cost (Original)": 30.5
        }
    ])

def test_initialized_manager_with_credentials(sql_manager):
    assert sql_manager.connection is not None

def test_empty_sqlmanager(sql_manager_no_credentials):
    assert sql_manager_no_credentials.connection is None

def test_connection(sql_manager_no_credentials, test_db_credentials):
    sql_manager_no_credentials.connect_to_database(test_db_credentials)
    assert sql_manager_no_credentials.connection is not None

def test_close_connection(test_db_credentials):
    manager = SQLManager()
    manager.connect_to_database(test_db_credentials)
    assert manager.connection is not None
    manager.close()
    assert manager.connection is None

def test_insert_ppr_snapshot(sql_manager, ppr_entry):
    affected_rows = sql_manager.insert_snapshot(to_table="ppr", entries=ppr_entry, auto_commit=False)
    assert affected_rows == 1

def test_insert_indexed_snapshot(sql_manager, indexed_entries):
    affected_rows = sql_manager.insert_snapshot(to_table="indexed", entries=indexed_entries, auto_commit=False)
    assert affected_rows == 4

def test_next_snapshot_id(sql_manager, indexed_entries):
    #Arrange: Insert some entries first 
    sql_manager.insert_snapshot(to_table="indexed", entries=indexed_entries, auto_commit=False)
    # Act, get the next snapshot ID
    next_id = sql_manager.next_snapshot_ID(table="indexed")
    # Assert expected snapshot ID
    assert next_id == 3  # Assuming the last snapshot was 2 after inserting indexed entries

def test_next_snapshot_id_empty_table(sql_manager):
    # with empty table
    next_id = sql_manager.next_snapshot_ID(table="indexed")
    assert next_id == 1  # or your DEFAULT_SNAPSHOT_ID

def test_last_update(sql_manager, indexed_entries):
    # Arrange: Insert some entries first
    sql_manager.insert_snapshot(to_table="indexed", entries=indexed_entries, auto_commit=False)
    # Act: Get the last update timestamp
    last_update = sql_manager.last_update(table="indexed")
    # Assert expected last update timestamp
    assert last_update == datetime.datetime(2024, 12, 24, 18, 19, 32)  # last update timestamp in dummy data

def test_last_update_empty_table(sql_manager):
    last_update = sql_manager.last_update(table="indexed")
    assert last_update == constants.DEFAULT_SNAPSHOT_DATE

