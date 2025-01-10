from fastapi import APIRouter, Query, HTTPException
from models.event import Event
from services.fatsecret import get_fatsecret_service
import requests


router = APIRouter()


@router.get("/recipe/")
async def get_recipes(search_expression: str = Query(...)):
    auth_token = get_fatsecret_service()
    params = {
        "search_expression": search_expression,  # Replace with your search term
        "format": "json",
    }
    headers = {
        "Authorization": f"Bearer {auth_token}",
        "Content-Type": "application/json",
    }
    response = requests.get("https://platform.fatsecret.com/rest/recipes/search/v3", headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=response.status_code, detail=response.text)



