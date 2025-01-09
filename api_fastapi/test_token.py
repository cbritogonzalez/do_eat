import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv
import os

load_dotenv()
# Replace these with your FatSecret client ID and client secret
CLIENT_ID = os.getenv('FATSECRET_CLIENT_ID')
CLIENT_SECRET = os.getenv('FATSECRET_CLIENT_SECRET')

# OAuth token endpoint
url = "https://oauth.fatsecret.com/connect/token"

# POST data
data = {
    "grant_type": "client_credentials",
    "scope": "basic",
}

# Make the POST request with Basic Auth
response = requests.post(url, data=data, auth=HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET))

# Check the response
if response.status_code == 200:
    # Successful response
    token_info = response.json()
    print("Access Token:", token_info["access_token"])
    print("Token Type:", token_info["token_type"])
    print("Expires In:", token_info["expires_in"])
else:
    # Handle errors
    print("Error:", response.status_code)
    print(response.text)
