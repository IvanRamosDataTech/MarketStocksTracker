"""
    This module defines pre configured queries for project
"""
#TODO Convert this script into a class
import psycopg2
import constants
from psycopg2 import sql

date_config = sql.SQL('SET datestyle = {date_style}; ').format(
    date_style = sql.Identifier(constants.DB_DATE_STYLE)
)

def next_snapshot_ID(connection, table):
    """
        Finds out last registered matchweek for current season in Database. 
        
        Input:
            connection - An active connection to postgresql database
            table - table name to extract snapshot ID from
        Returns:
            Last registerered Snapshop ID plus one. If there's any problem 
            with databse, then returns default snapshot ID "1"
    """
    try:
        cursor = connection.cursor()
        
        select = sql.SQL("SELECT MAX({snapshot}) FROM public." + table).format(
            snapshot = sql.Identifier("Snapshot ID")
        )
        
        select_statement = date_config + select

        cursor.execute(select_statement)
        next_snapshot_result = cursor.fetchone()
        if next_snapshot_result[0] is None:
            return constants.DEFAULT_SNAPSHOT_ID
        else:
            # Next Snapshot ID
            return next_snapshot_result[0] + 1
    except psycopg2.Error as e:
        print ("An error ocurred in database")
        print (e)
        return constants.DEFAULT_SNAPSHOT_ID
    finally:
        cursor.close()

# TODO Adapt it to portfolio 
def insert_snapshot(connection, to_table, dataframe):
    """
        Generates a Composed SQL object that contains all necessary SQL code to 
        perform upserts into a postgresql table from dataframe as source.
        
        Input:
            connection - active Postgresql connection to database
            to_table - target table name in format 'schema.table_name' to generate inserts 
            dataframe - pandas dataframe containing all rows to be inserted
        Returns:
            Affected rows after insertion
    """
    insert_header = sql.SQL("INSERT INTO " + to_table + " ({fields})").format(
        fields = sql.SQL(',').join([sql.Identifier(column) for column in dataframe.columns])
    )
    
    values_array = []
    for row in dataframe.iterrows():
        values_array.append(sql.SQL(" ({values})").format(
            values = sql.SQL(',').join([sql.Literal(value) for value in row[1].values])
        ))
    
    insert_values = sql.SQL(' VALUES ') + sql.SQL(',').join(values_array)
    insert_statement = date_config + insert_header + insert_values

    try:
        cursor = connection.cursor()
        cursor.execute(insert_statement)
        connection.commit()
        return cursor.rowcount
    except psycopg2.Error as e:
        print("An error ocurred in database")
        print (e)
        return 0
    finally:
        cursor.close()
