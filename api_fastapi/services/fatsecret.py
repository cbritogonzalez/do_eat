import requests
from requests.auth import HTTPBasicAuth
from fastapi import HTTPException
from core.config import FATSECRET_CLIENT_ID, FATSECRET_CLIENT_SECRET


fat_secret_token = {}


def get_fatsecret_service():
    if 'token' not in fat_secret_token:
        url = "https://oauth.fatsecret.com/connect/token"
        data = {
            "grant_type": "client_credentials",
            "scope": "basic",
        }
        response = requests.post(url, data=data, auth=HTTPBasicAuth(FATSECRET_CLIENT_ID, FATSECRET_CLIENT_SECRET))
        if response.status_code == 200:
            fat_secret_token['token'] = response.json()["access_token"]
            return fat_secret_token['token']
        else:
            raise HTTPException(status_code=401, detail='FatSecret authentication failed')
    return fat_secret_token['token']

