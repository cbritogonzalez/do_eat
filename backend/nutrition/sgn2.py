import urllib.parse

# Your credentials and previously obtained oauth_token
oauth_token = 'e1c2fbb42e9148309f62ff15ee5eafa5'  # The Request Token you obtained in Step 1

# User Authorization URL
authorization_url = 'https://authentication.fatsecret.com/oauth/authorize'

# Construct the URL to redirect the user for authorization
auth_url = f"{authorization_url}?oauth_token={urllib.parse.quote(oauth_token)}"

# Output the URL to the user
print("Please visit the following URL to authorize the request token:")
print(auth_url)
