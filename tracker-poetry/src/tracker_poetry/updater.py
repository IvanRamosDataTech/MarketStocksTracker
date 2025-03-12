
import pandas as pd
import numpy as np
import psycopg2
import portfolio_queries as sqlmanager
import os
from dotenv import load_dotenv
from pathlib import Path

## Script setup
pd.set_option('display.max_rows', 100)
pd.set_option('display.max_columns', 50)

config_path = Path('.env')
load_dotenv(dotenv_path=config_path)

# Stablish a connection to Database data source and fetch last game so we can know current matchweek
# TODO encapsulate connection to database with a funcion
APP_ENVIRONMENT = os.getenv('APP_ENVIRONMENT')
APP_VERSION = os.getenv('APP_VERSION')


DB_SERVER = os.getenv('DB_SERVER')
DB_PORT = os.getenv('DB_PORT')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME = os.getenv('DB_NAME')


try:
    connection = psycopg2.connect(
        host = DB_SERVER,
        port = DB_PORT,
        user = DB_USER,
        password = DB_PASSWORD,
        database = DB_NAME
    )
except psycopg2.Error as e:
    print (f'Can not connect to the postgress database "{DB_NAME}". Make sure database server is running')
    print (e)
else:
    print (f'Connection to database "{DB_NAME}" stablished. Listening at port {DB_PORT}')



## Insightful output data whenever the script runs
print(f"==== Updating Database from Excel portfolio sheet .... ===== ")
print(f"Running Updater ETL process Environment: {APP_ENVIRONMENT} version: {APP_VERSION} \n")



## Extract data from Excel master file

ppr_snapshot = pd.read_excel("Portafolio Indizado_Patrimonial.xlsx", sheet_name="Indizado PPR", header=4)
ppr_allianz = pd.read_excel("Portafolio Indizado_Patrimonial.xlsx", sheet_name="Allianz", header=None)

last_ppr_update = ppr_allianz.iat[0, 1]
print(f"Last Allianz report  {last_ppr_update} \n")



## Transform it
next_snapshot_ID = sqlmanager.next_snapshot_ID(connection, "ppr")
ppr_snapshot["Snapshot ID"] = next_snapshot_ID
ppr_snapshot["Upload Date"] = last_ppr_update

## Load data into Database

inserted_rows = sqlmanager.insert_snapshot(connection, "ppr", ppr_snapshot)

print(f" PPR Snapshot captured. Rows affected: {inserted_rows}")
