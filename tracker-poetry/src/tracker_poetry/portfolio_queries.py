"""
    This module defines pre configured queries for project
"""
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
        Returns:
            Last registerered matchweek plus one. If there's any problem 
            with databse or season has not even started, then returns default matchweek "1"
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