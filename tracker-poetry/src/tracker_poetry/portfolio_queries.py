"""
    This module defines pre configured queries for project
"""
import psycopg2
import tracker_poetry.constants as constants
from psycopg2 import sql
import pandas
import datetime


class SQLManager:

    def __init__(self, credentials=None):
        self.connection = None
        """
        Initializes the SQLManager with a connection to the specified environment.
        """
        if credentials:
            self.connection = self.connect_to_database(credentials)
        self.date_config = sql.SQL('SET datestyle = {date_style}; ').format(
            date_style = sql.Identifier(constants.DB_DATE_STYLE)
        )

    def connect_to_database(self, credentials) -> psycopg2.extensions.connection:
        '''
            Tries to connect to specific database according to selected environment
            
            Returns a live Postgresql connection
        '''
        self.close()  # Ensure any previous connection is closed
        try:
            connection = psycopg2.connect(
                host = credentials["host"],
                port = credentials["port"],
                user = credentials["user"],
                password = credentials["password"],
                database = credentials["dbname"]
            )
        except psycopg2.Error as e:
            print (f'Can not connect to the postgress database "{credentials["dbname"]}". Make sure database server is running')
            print (e)
        else:
            print (f'Connection to database "{credentials["dbname"]}" stablished. Listening at port {credentials["port"]}')
            self.connection = connection
            return connection

    def next_snapshot_ID(self, table: str) -> int:
        """
        Finds out last registered snapshot in Database.
        
        Returns last registered Snapshot ID plus one, or default if error.
        """
        try:
            cursor = self.connection.cursor()
            select = sql.SQL("SELECT MAX({snapshot}) FROM public." + table).format(
                snapshot = sql.Identifier("Snapshot ID")
            )
            select_statement = self.date_config + select
            cursor.execute(select_statement)
            next_snapshot_result = cursor.fetchone()
            if next_snapshot_result[0] is None:
                return constants.DEFAULT_SNAPSHOT_ID
            else:
                return next_snapshot_result[0] + 1
        except psycopg2.Error as e:
            print ("An error ocurred in database")
            print (e)
            return constants.DEFAULT_SNAPSHOT_ID
        finally:
            cursor.close()

    def last_update(self, table) -> datetime.datetime:
        """
        Finds out last registered snapshot date in database.
        
        Returns last registered date for a captured snapshot, or default if error.
        """
        try:
            cursor = self.connection.cursor()
            select = sql.SQL("SELECT MAX({snapshot}) FROM public." + table).format(
                snapshot = sql.Identifier("Snapshot Timestamp")
            )
            select_statement = self.date_config + select
            cursor.execute(select_statement)
            next_snapshot_date = cursor.fetchone()
            if next_snapshot_date[0] is None:
                return constants.DEFAULT_SNAPSHOT_DATE
            else:
                return next_snapshot_date[0]
        except psycopg2.Error as e:
            print ("An error ocurred in database")
            print (e)
            return constants.DEFAULT_SNAPSHOT_DATE
        finally:
            cursor.close()

    def insert_snapshot(self, to_table: str, entries: pandas.DataFrame, auto_commit=True) -> int:
        """
        Performs upserts into a postgresql table from dataframe as source.
        
        Returns affected rows after insertion.
        """
        insert_header = sql.SQL("INSERT INTO " + to_table + " ({fields})").format(
            fields = sql.SQL(',').join([sql.Identifier(column) for column in entries.columns])
        )
        values_array = []
        for row in entries.iterrows():
            values_array.append(sql.SQL(" ({values})").format(
                values = sql.SQL(',').join([sql.Literal(value) for value in row[1].values])
            ))
        insert_values = sql.SQL(' VALUES ') + sql.SQL(',').join(values_array)
        insert_statement = self.date_config + insert_header + insert_values

        try:
            cursor = self.connection.cursor()
            cursor.execute(insert_statement)
            if auto_commit:
                self.connection.commit()
            return cursor.rowcount
        except psycopg2.Error as e:
            print("An error ocurred in database")
            print (e)
            return 0
        finally:
            cursor.close()

    def close(self):
        """
        Closes the database connection.
        """
        if self.connection:
            self.connection.close()
            self.connection = None
            print("Database connection closed.")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()