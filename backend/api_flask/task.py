import requests

url_ah = "http://localhost:5000/schedule/fetch_albert_heijn"
url_jumbo = "http://localhost:5000/schedule/fetch_jumbo"

try:
    response_ah = requests.post(url_ah)
    if response_ah.status_code == 200:
        print("Successfully scheduled Albert Heijn task.")
        print("Response:", response_ah.json())
    else:
        print(f"Failed to schedule Albert Heijn task. Status code: {response_ah.status_code}")
        print("Response:", response_ah.text)

    response_jumbo = requests.post(url_jumbo)
    
    if response_jumbo.status_code == 200:
        print("Successfully scheduled Jumbo task.")
        print("Response:", response_jumbo.json())
    else:
        print(f"Failed to schedule Jumbo task. Status code: {response_jumbo.status_code}")
        print("Response:", response_jumbo.text)

except requests.exceptions.RequestException as e:
    print(f"Error occurred while making the request: {e}")
