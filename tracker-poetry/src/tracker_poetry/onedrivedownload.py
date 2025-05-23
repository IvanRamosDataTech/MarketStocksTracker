import msal
import requests
import pandas as pd

CLIENT_ID = "03ad1e3e-524d-4408-aa98-41274583fec8"
TENANT_ID = "consumers"  # For personal Microsoft accounts
AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
SCOPES = ["Files.Read"]

def get_token():
    app = msal.PublicClientApplication(CLIENT_ID, authority=AUTHORITY)
    flow = app.initiate_device_flow(scopes=SCOPES)
    #print(flow["message"])  # Follow the printed instructions to authenticate
    result = app.acquire_token_by_device_flow(flow)
    return result["access_token"]

def download_file(access_token, item_path):
    # Example: item_path = '/Documents/yourfile.xlsx'
    endpoint = f"https://graph.microsoft.com/v1.0/me/drive/root:{item_path}:/content"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(endpoint, headers=headers)
    response.raise_for_status()
    return response.content

def main():
    token = get_token()
    item_path = "/Portfolios/DEV Portafolio Indizado_Patrimonial.xlsx"  # Change to your file's path
    file_bytes = download_file(token, item_path)
    # Read Excel from bytes
    df = pd.read_excel(pd.io.common.BytesIO(file_bytes), sheet_name="Allianz", header=None)
    print(df.head())

if __name__ == "__main__":
    print("Starting download...")
    main()