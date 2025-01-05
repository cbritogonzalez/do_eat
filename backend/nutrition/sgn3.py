import time
import random
import string
import urllib.parse
import hmac
import hashlib
import base64
import requests

# Your credentials
consumer_key = '64fa0f127d5f4b6c8697abdd84ca1034'  # Your consumer key
consumer_secret = 'a487c98c1bf0429988419e0c4ee6ce52'  # Your consumer secret
oauth_token = 'e1c2fbb42e9148309f62ff15ee5eafa5'  # The authorized request token obtained in Step 2
oauth_token_secret = 'f885b820f68847f08bbc2cc0b933e1be'  # The request token secret obtained in Step 1
oauth_verifier = '7558515'  # The verifier code received after user authorization

# Access Token URL
access_token_url = 'https://authentication.fatsecret.com/oauth/access_token'

# OAuth 1.0a parameters
oauth_version = '1.0'
oauth_signature_method = 'HMAC-SHA1'

def generate_nonce():
    """Generate a random string as a nonce"""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=32))

def get_oauth_timestamp():
    """Get the current timestamp in seconds since Unix epoch"""
    return str(int(time.time()))

def generate_base_string(method, url, params):
    """Generate the signature base string"""
    # Sort parameters by key
    sorted_params = sorted(params.items())
    # Percent-encode the parameters
    encoded_params = urllib.parse.urlencode(sorted_params, quote_via=urllib.parse.quote)

    # Prepare the base string
    base_string = '&'.join([method.upper(), urllib.parse.quote(url, safe=''), urllib.parse.quote(encoded_params, safe='')])

    print("Base String for Signature:\n", base_string)  # Debug: print the base string
    return base_string

def generate_signature(base_string, consumer_secret, token_secret=''):
    """Generate the OAuth signature using HMAC-SHA1"""
    # Prepare the signing key
    signing_key = f"{urllib.parse.quote(consumer_secret)}&{urllib.parse.quote(token_secret)}"
    
    # Create the HMAC-SHA1 signature
    signature = hmac.new(signing_key.encode(), base_string.encode(), hashlib.sha1)
    return base64.b64encode(signature.digest()).decode()

def get_access_token(oauth_token, oauth_token_secret):
    """Get the Access Token from the FatSecret API"""
    # OAuth parameters
    oauth_params = {
        'oauth_consumer_key': consumer_key,
        'oauth_token': oauth_token,
        'oauth_signature_method': oauth_signature_method,
        'oauth_timestamp': get_oauth_timestamp(),
        'oauth_nonce': generate_nonce(),
        'oauth_version': oauth_version,
        'oauth_verifier': oauth_verifier,
    }

    print("OAuth Parameters:\n", oauth_params)  # Debug: print OAuth parameters

    # Generate the base string
    base_string = generate_base_string('GET', access_token_url, oauth_params)

    # Generate the OAuth signature
    oauth_signature = generate_signature(base_string, consumer_secret, oauth_token_secret)

    # Add the signature to the parameters
    oauth_params['oauth_signature'] = oauth_signature

    # Prepare the request headers
    headers = {
        'Authorization': 'OAuth ' + ', '.join([f'{key}="{value}"' for key, value in oauth_params.items()])
    }

    print("Authorization Header:\n", headers['Authorization'])  # Debug: print the Authorization header

    # Make the request to get the access token
    response = requests.get(access_token_url, headers=headers, params=oauth_params)

    # Check for a successful response
    if response.status_code == 200:
        # Parse the response body (assuming it's URL-encoded)
        response_data = urllib.parse.parse_qs(response.text)
        
        # Extract the required parameters from the response
        oauth_token = response_data.get('oauth_token', [None])[0]
        oauth_token_secret = response_data.get('oauth_token_secret', [None])[0]

        if oauth_token and oauth_token_secret:
            print(f"Access Token: {oauth_token}")
            print(f"Access Token Secret: {oauth_token_secret}")
            return oauth_token, oauth_token_secret
        else:
            print("Error: The access token could not be obtained.")
            print("Response Data:", response_data)  # Debug: print the response data
            return None, None
    else:
        print(f"Error: {response.status_code}")
        print("Response Content:", response.content)  # Debug: print the response content for more details
        return None, None

# Call the function to get the access token
get_access_token(oauth_token, oauth_token_secret)
