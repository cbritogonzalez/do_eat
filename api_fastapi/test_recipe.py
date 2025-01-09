import requests

# API endpoint
url = "https://platform.fatsecret.com/rest/recipes/search/v3"

# Your bearer token (replace with the actual token)
bearer_token = "eyJhbGciOiJSUzI1NiIsImtpZCI6IjEwOEFEREZGRjZBNDkxOUFBNDE4QkREQTYwMDcwQzE5NzNDRjMzMUUiLCJ0eXAiOiJhdCtqd3QiLCJ4NXQiOiJFSXJkX19ha2tacWtHTDNhWUFjTUdYUFBNeDQifQ.eyJuYmYiOjE3MzY0MzEzMzgsImV4cCI6MTczNjUxNzczOCwiaXNzIjoiaHR0cHM6Ly9vYXV0aC5mYXRzZWNyZXQuY29tIiwiYXVkIjoiYmFzaWMiLCJjbGllbnRfaWQiOiJjOWU3NGVjOWM4NjQ0YjE5OGNlYTUwNTgyMWRmMGNmNiIsInNjb3BlIjpbImJhc2ljIl19.JgL8lH8JlUfrX_qTxPq1Yf3ayJVsJG8JEaxDwJN41nJmYdKSPwwLzhQEPRDmCm0bX8bWq_az10pCQx_VBsBzyQJIgXywtCn1rKsAzSJPFweeEZTxnkgvSklOrkyIE1d4z9IIFByLaD_6XslHo83YvuSE6bim4oWctBeWX7Y5DmEg-b-MvuHgxu-i6yf7agkS8wjik-X_VDXRKSQLa12YnTV6FNLon8TQXZL5gN34IpzwgI3GEjlvM8-FSEowM2ihLDsTzC36ld096J8uhG9gzNeiEka34zRjqH2w4pKjjp1KhQvmGiiK9OWAi4KuqiJoq55sIBXAEBeScEp-RvP8pB6pdOBrr7RSAY_0tXYoea6otGUACIY6rry80AaVtsjXYkW7JryyYYPEXyT3mOzP76ZQ7lpefHOjEL29l9Bk04MzkUOtkfLcAfq1lbBYLeBOn7yh6wuYQv95M5aX2rbuK4C3gP-eRskscbsWpLd89Xbeq3DEocof_X_1n8w2fbchXouRlF44M9CtRZz8JOUQQ-20H2hxqXWjTwNcR98Bn3K60JmhjKW5MiwsFWXJ1G078rbVUeWJOM7wWnXIAczxws-v1B8bWjsRC-eW4e325BftciY1cvzYW9qYvuxvEQv9j_6OmMAValx1rKwh_n8RaMMegpDJtEqaZ3pTFRL4BSo"

# Query parameter
params = {
    "search_expression": "chicken",  # Replace with your search term
    "format": "json",
}

# Headers for the request
headers = {
    "Authorization": f"Bearer {bearer_token}",
    "Content-Type": "application/json",
}

# Make the GET request
response = requests.get(url, headers=headers, params=params)

# Check the response
if response.status_code == 200:
    # Successful response
    print(response.json())
else:
    # Handle errors
    print("Error:", response.status_code)
    print(response.text)
