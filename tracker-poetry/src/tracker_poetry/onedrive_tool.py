import msal
import requests
import pandas as pd
import argparse
from environment import EnvironmentLoader
import os


TENANT_ID = "consumers"  # For personal Microsoft accounts
AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
SCOPES = ["Files.ReadWrite.All"]

def get_token():
    app = msal.PublicClientApplication(os.getenv("AZURE_APP_ID"), authority=AUTHORITY)
    flow = app.initiate_device_flow(scopes=SCOPES)
    print(flow["message"])  # Follow the printed instructions to authenticate
    result = app.acquire_token_by_device_flow(flow)
    return result["access_token"]

def download_file(access_token, item_path):
    # Example: item_path = '/Documents/yourfile.xlsx'
    endpoint = f"https://graph.microsoft.com/v1.0/me/drive/root:{item_path}:/content"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(endpoint, headers=headers)
    response.raise_for_status()
    return response.content

# A function that uploads a file to my ONeDrive personal account
def upload_file(access_token, file_path: str, item_path: str):
    """
    Uploads a file to OneDrive.
    
    :param access_token: Access token for Microsoft Graph API.
    :param file_path: Local path to the file to upload.
    :param item_path: Path in OneDrive where the file will be uploaded.
    """
    endpoint = f"https://graph.microsoft.com/v1.0/me/drive/root:/{item_path}:/content"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/octet-stream"
    }
    
    with open(file_path, 'rb') as file:
        file_content = file.read()

    response = requests.put(endpoint, headers=headers, data=file_content)
    response.raise_for_status()
    return response.json() 

def get_portfolio(excel_file):
    """
    Reads the portfolio from an Excel file stored at a personal 
    OneDrive account and returns it as a DataFrame.

    :param portfolio_path: OneDrive Path to the Excel file.
    :param portfolio_name: Name of the sheet to read.
    :return: BytesIO object containing the portfolio data.
    """
    full_path = f"/Portfolios/{excel_file}"
    try:
        token = get_token()
    except Exception as e:
        print(f"Error obtaining access token: {e}")
        return pd.DataFrame()

    try:
        file_bytes = download_file(token, full_path)
    except requests.HTTPError as e:
        print(f"HTTP error downloading file: {e}")
        return pd.DataFrame()
    except Exception as e:
        print(f"Unexpected error downloading file: {e}")
        return pd.DataFrame()

    try:
        return pd.io.common.BytesIO(file_bytes) # Return the BytesIO object for further processing  
    except Exception as e:
        print(f"Error creating BytesIO object: {e}")
        return pd.io.common.BytesIO()
    
def upload_backup_portfolio(backup_file):
    """
    Takes a dump file from local storage and uploads it to OneDrive.

    :param backup_file: Local filename of the backup file to upload.
    """
    onedrive_path = f"/Portfolios/MarketStocksTracker_backups/{os.path.basename(backup_file)}"
    try:
        token = get_token()
    except Exception as e:
        print(f"Error obtaining access token: {e}")
        return

    try:
        response = upload_file(token, backup_file, onedrive_path)
        print(f"Backup file {backup_file} uploaded successfully to {onedrive_path}.")
    except requests.HTTPError as e: 
        print(f"HTTP error uploading file: {e}")
    except Exception as e:
        print(f"Error saving portfolio: {e}")
    except Exception as e:
        print(f"Error downloading portfolio: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="OneDrive Tool for Market Stocks Tracker")
    parser.add_argument("env", 
                        help="Database environment to backup. Accepted values: Production | Development",
                        type=str,
                        choices=['Production', 'Development'])
    parser.add_argument("action", 
                        help="Action to perform: upload or download",
                        type=str,
                        choices=['upload', 'download'])
    parser.add_argument("-f", "--file",
                       help="Local file to upload (required for upload action).",
                       type=str,
                       required=False)
    args = parser.parse_args()

    EnvironmentLoader.load(env=args.env)

    if args.action == "upload" and not args.file:
        parser.error("The --file argument is required when action is 'upload'.")

    if args.action == "upload":
        upload_backup_portfolio(args.file)
    elif args.action == "download":
        print("Starting download...")
        porfolio_file = EnvironmentLoader.resolve_excel_file()
        df = pd.read_excel(get_portfolio(porfolio_file), sheet_name="Indizado PPR", header=4)
        print(df.head(20))
        print("Download completed.")
        