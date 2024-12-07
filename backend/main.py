from typing import Union
from fastapi import FastAPI, HTTPException
import httpx

app = FastAPI()

WEATHER_API = 'http://api.weatherapi.com/v1/current.json'
API_KEY = '00284f2cd52346b8aad124825242011'

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

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