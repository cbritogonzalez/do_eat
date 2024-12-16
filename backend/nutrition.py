import requests

def get_food_details(food_id, access_token):
    url = "https://platform.fatsecret.com/rest/food/v4"

    # Query parameters
    params = {
        "food_id": food_id,
        "format": "json"
    }

    # Headers
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    try:
        # Make the GET request
        response = requests.get(url, headers=headers, params=params)
        
        # Check for a successful response
        if response.status_code == 200:
            return response.json()  # Return the JSON response
        else:
            return {
                "error": f"Request failed with status code {response.status_code}",
                "details": response.text
            }

    except requests.exceptions.RequestException as e:
        return {"error": "An exception occurred", "details": str(e)}

# Replace with your actual access token
ACCESS_TOKEN = 'e1c2fbb42e9148309f62ff15ee5eafa5'
FOOD_ID = 33691

if __name__ == "__main__":
    food_details = get_food_details(FOOD_ID, ACCESS_TOKEN)
    print(food_details)