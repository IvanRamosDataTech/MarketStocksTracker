
import pandas as pd
import portfolio_queries as sqlmanager
from datetime import datetime
import argparse
import os
import database_tool as dbtool
import onedrive_tool as onedrive
from environment import EnvironmentLoader

## Definitions

def etl_ppr(connection, source):
    
    # Verbose
    ppr_allianz = pd.read_excel(source, sheet_name="Allianz", header=None)  
    last_ppr_update = ppr_allianz.iat[0, 1]
    print(f"Last Allianz report  {last_ppr_update}")
    # Extract data from excel
    ppr_snapshot = pd.read_excel(source, sheet_name="Indizado PPR", header=4)   
    # Transform it
    next_ppr_snapshotID = sqlmanager.next_snapshot_ID(connection, "ppr")
    ppr_snapshot["Snapshot ID"] = next_ppr_snapshotID
    ppr_snapshot["Snapshot Timestamp"] = datetime.now()
    ppr_snapshot["Statement Date"] = last_ppr_update
    # Load data into Database
    ppr_inserted_rows = sqlmanager.insert_snapshot(connection, "ppr", ppr_snapshot)
    #Verbose
    print(f"PPR Snapshot captured. Rows affected: {ppr_inserted_rows}")
    print(ppr_snapshot[["Name", "Purchased Value", "Market Value", "Balance", "Snapshot ID", "Snapshot Timestamp"]], "\n\n")

    return ppr_inserted_rows
   

def etl_indexed(connection, source):
    #Verbose
    last_date = sqlmanager.last_update(connection, "indexed")
    print(f"Last Indexed Strategy investment {last_date}")
    # Extract data from excel
    indexed_snapshot = pd.read_excel(source, sheet_name="Indizado FIRE", header=4)
    # Transform
    indexed_snapshot.drop(columns=["Ticker Full Name"], inplace=True)
    next_indexed_snapshotID = sqlmanager.next_snapshot_ID(connection, "indexed")
    indexed_snapshot["Snapshot ID"] = next_indexed_snapshotID
    indexed_snapshot["Snapshot Timestamp"] = datetime.now()
    # Load into database
    indexed_inserted_rows = sqlmanager.insert_snapshot(connection, "indexed", indexed_snapshot)
    # Verbose
    print(f"Indexed Based Strategy Snapshot captured. Rows affected: {indexed_inserted_rows}")
    print(indexed_snapshot[["Ticker", "Shares", "To Buy", "Snapshot ID", "Snapshot Timestamp"]], "\n\n")
    
    return indexed_inserted_rows


def etl_equity(connection, source):
    # TODO Perform equity snapshots
    print(f"TODO: Perform Equity Strategy snapshots \n")

    return

### Script setup
pd.set_option('display.max_rows', 100)
pd.set_option('display.max_columns', 50)

if __name__ == "__main__":
    ## Insightful output data whenever the script runs, setup of arguments 
    parser = argparse.ArgumentParser(prog="Market Stocks Tracker",
                                    description="Stores portafolio updates from excel to database.",
                                    epilog=f"Running version")
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
    parser.add_argument("-b", "--backup",
                        help="Uploads a backup copy of the portfolio file to OneDrive personal account",
                        required=False,
                        action="store_true")
    args = parser.parse_args()

    #Environment resolution
    EnvironmentLoader.load(env=args.env)

    print(f"==== Updating Database from Excel portfolio sheet .... ===== ")
    print(f"Running Updater ETL process Environment: {EnvironmentLoader.get_environment()} version: {EnvironmentLoader.get_app_version()}")

    ## Connect to database
    connection = sqlmanager.connect_to_database(environment=EnvironmentLoader.get_environment())

    portfolio_file = onedrive.get_portfolio(EnvironmentLoader.resolve_excel_file())

    if 'All' in args.portfolios:
        print(f"Running All portfolio updates ...\n\n")
        etl_ppr(connection, source=portfolio_file)
        etl_indexed(connection, source=portfolio_file)
        etl_equity(connection, source=portfolio_file)
    else:
        if 'PPR' in args.portfolios:
            etl_ppr(connection, source=portfolio_file)
        if 'Indexed' in args.portfolios:
            etl_indexed(connection, source=portfolio_file)
        if 'Equity' in args.portfolios:
            etl_equity(connection, source=portfolio_file)

    if args.backup:
        backup_file = dbtool.backup_database(EnvironmentLoader.get_environment())
        onedrive.upload_backup_portfolio(backup_file)
        os.remove(backup_file)

    # close connection
    connection.close()
