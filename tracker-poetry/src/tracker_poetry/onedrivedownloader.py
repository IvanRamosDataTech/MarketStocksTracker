from pathlib import Path
from dotenv import load_dotenv
import msal
import requests
import pandas as pd
import os


TENANT_ID = "consumers"  # For personal Microsoft accounts
AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
SCOPES = ["Files.Read"]

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

def get_portfolio(portfolio_path):
    """
    Reads the portfolio from an Excel file stored at a personal 
    OneDrive account and returns it as a DataFrame.

    :param portfolio_path: OneDrive Path to the Excel file.
    :param portfolio_name: Name of the sheet to read.
    :return: BytesIO object containing the portfolio data.
    """
    config_path = Path('.env')
    load_dotenv(dotenv_path=config_path)  # Load environment variables from .env file
    try:
        token = get_token()
    except Exception as e:
        print(f"Error obtaining access token: {e}")
        return pd.DataFrame()

    try:
        file_bytes = download_file(token, portfolio_path)
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

def main():
    item_path = "/Portfolios/DEV Portafolio Indizado_Patrimonial.xlsx"  # Change to your file's path
    # Read Excel from OneDrive
    df = pd.read_excel(get_portfolio(item_path), sheet_name="Indizado PPR", header=4)
    print(df.head(20))

if __name__ == "__main__":
    print("Starting download...")
    main()
    print("Download completed.")