
import pandas as pd
import portfolio_queries as sqlmanager
import os
from dotenv import load_dotenv
from pathlib import Path
from datetime import datetime
import argparse
import onedrive_tool as onedrive

## Definitions

def etl_ppr(connection, filepath):
    
    # Verbose
    ppr_allianz = pd.read_excel(filepath, sheet_name="Allianz", header=None)  
    last_ppr_update = ppr_allianz.iat[0, 1]
    print(f"Last Allianz report  {last_ppr_update}")
    # Extract data from excel
    ppr_snapshot = pd.read_excel(filepath, sheet_name="Indizado PPR", header=4)   
    # Transform it
    next_ppr_snapshotID = sqlmanager.next_snapshot_ID(connection, "ppr")
    ppr_snapshot["Snapshot ID"] = next_ppr_snapshotID
    ppr_snapshot["Snapshot Timestamp"] = datetime.now()
    ppr_snapshot["Statement Date"] = last_ppr_update
    # Load data into Database
    ppr_inserted_rows = sqlmanager.insert_snapshot(connection, "ppr", ppr_snapshot)
    #Verbose
    print(f"PPR Snapshot captured. Rows affected: {ppr_inserted_rows}\n\n")
    print(ppr_snapshot[["Name", "Purchased Value", "Market Value", "Balance", "Snapshot ID", "Snapshot Timestamp"]])

    return ppr_inserted_rows
   

def etl_indexed(connection, filepath):
    #Verbose
    last_date = sqlmanager.last_update(connection, "indexed")
    print(f"Last Indexed Strategy investment {last_date}")
    # Extract data from excel
    indexed_snapshot = pd.read_excel(filepath, sheet_name="Indizado FIRE", header=4)
    # Transform
    indexed_snapshot.drop(columns=["Ticker Full Name"], inplace=True)
    next_indexed_snapshotID = sqlmanager.next_snapshot_ID(connection, "indexed")
    indexed_snapshot["Snapshot ID"] = next_indexed_snapshotID
    indexed_snapshot["Snapshot Timestamp"] = datetime.now()
    # Load into database
    indexed_inserted_rows = sqlmanager.insert_snapshot(connection, "indexed", indexed_snapshot)
    # Verbose
    print(f"Indexed Based Strategy Snapshot captured. Rows affected: {indexed_inserted_rows} \n\n")
    print(indexed_snapshot[["Ticker", "Shares", "To Buy", "Snapshot ID", "Snapshot Timestamp"]])
    
    return indexed_inserted_rows


def etl_equity(connection, filepath):
    # TODO Perform equity snapshots
    print(f"TODO: Perform Equity Startegy snapshots \n")
    
    return

# Function to determine the data source based on the environment and data source depending on argument --data-source
def get_data_source(environment, data_source):
    """
    Determines the Excel file path based on environment and data source.
    - environment: 'Development' or 'Production'
    - data_source: 'Local' or 'Cloud'
    Returns the appropriate file path or identifier.
    """
    if data_source == 'Local':
        if environment == 'Development':
            return os.getenv('EXCEL_FILE_DEV')
        elif environment == 'Production':
            return os.getenv('EXCEL_FILE')
        else:
            raise ValueError(f"Unknown environment {environment}")
    elif data_source == 'Cloud':
        if environment == 'Development':
            return f"/Portfolios/{os.getenv('EXCEL_FILE_DEV')}"
        elif environment == 'Production':
            return f"/Portfolios/{os.getenv('EXCEL_FILE')}"
        else:
            raise ValueError(f"Unknown environment {environment}")
    else:
        raise ValueError(f"Unknown data source {data_source}")


### Script setup
pd.set_option('display.max_rows', 100)
pd.set_option('display.max_columns', 50)

config_path = Path('.env')
load_dotenv(dotenv_path=config_path)

# TODO encapsulate connection to database with a funcion
APP_VERSION = os.getenv('APP_VERSION')


## Insightful output data whenever the script runs, setup of arguments 
parser = argparse.ArgumentParser(prog="Market Stocks Tracker",
                                 description="Stores portafolio updates from excel to database.",
                                 epilog=f"Running version {APP_VERSION}")
parser.add_argument("env", 
                    help="Database environment system will interact with. Accepted values:  Production | Development",
                    type=str,
                    choices=['Production', 'Development'])
parser.add_argument("-p", "--portfolios",
                    help= "Selectts portfolio(s) to be updated. Accepted values: All, PPR, Indexed, Equity",
                    nargs="+",
                    required=True,
                    type=str,
                    choices=["All", "PPR", "Indexed", "Equity"])
parser.add_argument("-d", "--data-source",
                    help="Specifies the data source for the portfolio. Accepted values: Local, Cloud",
                    type=str,
                    choices=["Local", "Cloud"],
                    default="Cloud") 

args = parser.parse_args()


print(f"==== Updating Database from Excel portfolio sheet .... ===== ")
print(f"Running Updater ETL process Environment: {args.env} version: {APP_VERSION}")
print(f"Extracting data from: {args.data_source}")

## Connect to database
connection = sqlmanager.connect_to_database(environment=args.env)

if args.data_source == 'Local':
    # Local file path
    porftolio_path = get_data_source(environment=args.env, data_source=args.data_source)
    #porftolio_path = Path(excel_local_file)
elif args.data_source == 'Cloud':
    # Cloud file path
    porftolio_path = onedrive.get_portfolio(f"/Portfolios/{os.getenv('EXCEL_FILE_DEV') if args.env == 'Development' else os.getenv('EXCEL_FILE')}")
else:
    raise ValueError(f"Unknown data source {args.data_source}")


if 'All' in args.portfolios:
    print(f"Running All portfolio updates ...\n\n")
    etl_ppr(connection, filepath=porftolio_path)
    etl_indexed(connection, filepath=porftolio_path)
    etl_equity(connection, filepath=porftolio_path)
else:
    if 'PPR' in args.portfolios:
        etl_ppr(connection, filepath=porftolio_path)
    if 'Indexed' in args.portfolios:
        etl_indexed(connection, filepath=porftolio_path)
    if 'Equity' in args.portfolios:
        etl_equity(connection, filepath=porftolio_path)
        
# close connection
connection.close()
