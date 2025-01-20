from typing import List, Union
from fastapi import FastAPI, HTTPException
from albert_heijn.ah import AHConnector
import httpx

app = FastAPI()

WEATHER_API = 'http://api.weatherapi.com/v1/current.json'
API_KEY = 'key_for_weather_api'
connector = AHConnector()

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


# AH bonus items API
@app.get("/ah/bonus", response_model=List[dict])
async def get_ah_bonus_items():
    try:
        # Retrieve bonus items using the AHConnector instance
        bonus_items = connector.get_bonus_items(10)
        return bonus_items
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching bonus items: {str(e)}")

# Example API call
@app.get("/weather")
async def get_weather():
    #define params
    params = {
        "q": 'Groningen',
        "key": API_KEY
    }

    try:
        #call async function
        async with httpx.AsyncClient() as client:
            # retrieve the info in response
            response = await client.get(WEATHER_API,params = params)
            # check response for errors
            response.raise_for_status() #Http error 400 or 500
            # retrieve data in a readable (json) format
            data = response.json()
            # data is structured based on API documenation
            return {
                "city": data['location']['name'],
                "country": data['location']['country'],
                "localtime": data['location']['localtime'],
                "temperature": data['current']['temp_c'],
                "feels_like": data['current']['feelslike_c']
            }
    # Add error exceptions for 4xx, 5xx, etc calls
    except httpx.HTTPStatusError as exception:
        raise HTTPException(
            status_code = exception.response.status_code,
            detail=f"Error retrieving weather data: {exception.response.text}"
        )
    except Exception as exception:
        raise HTTPException(
            status_code=500,
            detail=f"Unexpected error occured: {str(exception)}"
        )