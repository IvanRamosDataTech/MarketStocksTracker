from multiprocessing import connection
from environment import EnvironmentLoader
import argparse
import subprocess

def backup_database(environment="Development") -> str:
    """
    Backup the PostgreSQL database using pg_dump.
    This function generates a logical backup file with schema and
    data using INSERT statements.

    Returns name of backup file
    """
    from datetime import datetime   
    EnvironmentLoader.load(environment)

    conn_vars = EnvironmentLoader.get_db_vars()
    connection_string_arg = f"--dbname=postgresql://{conn_vars['user']}:{conn_vars['password']}@{conn_vars['host']}:{conn_vars['port']}/{conn_vars['dbname']}"

    output_filename = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.sql"
    if environment == 'Development':
        output_filename = f"dev_{output_filename}"

    # Define the command to run pg_dump
    command = [
        "pg_dump",
        connection_string_arg,
        f"--file={output_filename}",  # Temporary file to hold the raw dump
        "--inserts",    # generates INSERT statements
        "--schema=public",  # specify the schema to dump
         "--clean",  # clean the database before restoring
        "--if-exists",  # to avoid errors if the table already exists,
        "--no-acl", # Prevents dumping access privileges (ACLs)
        "-F", "p",  # format as plain text (It could also be t for tar or c for custom)
    ]

    # Run the command
    try:
        subprocess.run(command, check=True)
        print("Database backup completed successfully.\n Backup file:", output_filename)
        return output_filename
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while backing up the database: {e}")

def restore_database(environment="Development", backup_file=None):
    """
    Restore the PostgreSQL database from a backup file.
    This function uses psql to restore the database from a given backup file.
    """
    if not backup_file:
        raise ValueError("Backup file must be specified for restoration.")
    EnvironmentLoader.load(environment)
    conn_vars = EnvironmentLoader.get_db_vars()
    connection_string_arg = f"--dbname=postgresql://{conn_vars['user']}:{conn_vars['password']}@{conn_vars['host']}:{conn_vars['port']}/{conn_vars['dbname']}"

    command = [
        "psql",
        connection_string_arg,
        "-f", backup_file
    ]

    try:
        subprocess.run(command, check=True)
        print("Database restoration completed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while restoring the database: {e}")
    
if __name__ == "__main__":
   
    parser = argparse.ArgumentParser(description="PostgreSQL database tools for MarketStocksTracker project.")
    parser.add_argument("env", 
                        help="Database environment to backup. Accepted values: Production | Development",
                        type=str,
                        choices=['Production', 'Development'])
    parser.add_argument("mode",
                        help="Mode: 'backup' to create a backup, 'restore' to restore from a backup file.",
                        type=str,
                        choices=['backup', 'restore'])
    parser.add_argument("-f", "--backup-file",
                        help="Path to the backup file to restore from. Required if mode is 'restore'.",
                        type=str,
                        required=False)    
    args = parser.parse_args()

    EnvironmentLoader.load(args.env)

    if args.mode == 'restore' and not args.backup_file:
        parser.error("The --backup-file argument is required when mode is 'restore'.")

    if args.mode == 'backup':
        print(f"==== Backing up {args.env} database .... ===== ")
        backup_database(args.env)
    elif args.mode == 'restore':
        print(f"==== Restoring {args.env} database .... ===== ")
        restore_database(args.env, args.backup_file)