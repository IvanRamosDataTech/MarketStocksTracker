
import pandas as pd
import portfolio_queries as sqlmanager
import os
from dotenv import load_dotenv
from pathlib import Path
from datetime import datetime
import argparse


## Script setup
pd.set_option('display.max_rows', 100)
pd.set_option('display.max_columns', 50)

config_path = Path('.env')
load_dotenv(dotenv_path=config_path)

# TODO encapsulate connection to database with a funcion
APP_ENVIRONMENT = os.getenv('APP_ENVIRONMENT')
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
args = parser.parse_args()
if 'All' in args.portfolios:
    print("Running All portfolio updates")
else:
    if 'PPR' in args.portfolios:
        print("updating PPR")
    if 'Indexed' in args.portfolios:
         print("updating Indexed")
    if 'Equity' in args.portfolios:
         print("updating Equity")


print(f"==== Updating Database from Excel portfolio sheet .... ===== ")
print(f"Running Updater ETL process Environment: {args.env} version: {APP_VERSION} \n")


## Connect to database
# connection = sqlmanager.connect_to_database(environment=APP_ENVIRONMENT)



## Extract data from Excel master file



# ppr_snapshot = pd.read_excel("Portafolio Indizado_Patrimonial.xlsx", sheet_name="Indizado PPR", header=4)
# ppr_allianz = pd.read_excel("Portafolio Indizado_Patrimonial.xlsx", sheet_name="Allianz", header=None)
# indexed_snapshot = pd.read_excel("Portafolio Indizado_Patrimonial.xlsx", sheet_name="Indizado FIRE", header=4)

# print(indexed_snapshot.head(20))

# last_ppr_update = ppr_allianz.iat[0, 1]
# print(f"Last Allianz report  {last_ppr_update} \n")



# ## Transform it
# next_ppr_snapshotID = sqlmanager.next_snapshot_ID(connection, "ppr")
# ppr_snapshot["Snapshot ID"] = next_ppr_snapshotID
# ppr_snapshot["Snapshot Timestamp"] = datetime.now()
# ppr_snapshot["Statement Date"] = last_ppr_update

# next_indexed_snapshotID = sqlmanager.next_snapshot_ID(connection, "indexed")
# indexed_snapshot["Snapshot ID"] = next_indexed_snapshotID
# indexed_snapshot["Snapshot Timestamp"] = datetime.now()

# ## Load data into Database

# ppr_inserted_rows = sqlmanager.insert_snapshot(connection, "ppr", ppr_snapshot)
# indexed_inserted_rows = sqlmanager.insert_snapshot(connection, "indexed", indexed_snapshot)

# print(f" PPR Snapshot captured. Rows affected: {ppr_inserted_rows}")
# print(f" Indexed Based Strategy Snapshot captured. Rows affected: {indexed_inserted_rows}")