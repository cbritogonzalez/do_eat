import time
import random
import string
import urllib.parse
import hmac
import hashlib
import base64
import requests

# Your credentials
consumer_key = 'consumer_key'
consumer_secret = 'consumer_secret'
callback_url = 'oob'

# OAuth 1.0a parameters
request_token_url = 'https://authentication.fatsecret.com/oauth/request_token'
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

def get_request_token():
    """Get the unauthorized request token from the FatSecret API"""
    # OAuth parameters
    oauth_params = {
        'oauth_consumer_key': consumer_key,
        'oauth_signature_method': oauth_signature_method,
        'oauth_timestamp': get_oauth_timestamp(),
        'oauth_nonce': generate_nonce(),
        'oauth_version': oauth_version,
        'oauth_callback': callback_url,
    }

    print("OAuth Parameters:\n", oauth_params)  # Debug: print OAuth parameters

    # Generate the base string
    base_string = generate_base_string('POST', request_token_url, oauth_params)

    # Generate the OAuth signature
    oauth_signature = generate_signature(base_string, consumer_secret)

    # Add the signature to the parameters
    oauth_params['oauth_signature'] = oauth_signature

    # Prepare the request headers
    headers = {
        'Authorization': 'OAuth ' + ', '.join([f'{key}="{value}"' for key, value in oauth_params.items()])
    }

    print("Authorization Header:\n", headers['Authorization'])  # Debug: print the Authorization header

    # Make the request to get the request token
    response = requests.post(request_token_url, headers=headers, data=oauth_params)

    # Check for a successful response
    if response.status_code == 200:
        # Parse the response body (assuming it's URL-encoded)
        response_data = urllib.parse.parse_qs(response.text)
        
        # Extract the required parameters from the response
        oauth_token = response_data.get('oauth_token', [None])[0]
        oauth_token_secret = response_data.get('oauth_token_secret', [None])[0]
        oauth_callback_confirmed = response_data.get('oauth_callback_confirmed', [None])[0]

        if oauth_token and oauth_token_secret and oauth_callback_confirmed == 'true':
            print(f"Request Token: {oauth_token}")
            print(f"Request Token Secret: {oauth_token_secret}")
            return oauth_token, oauth_token_secret
        else:
            print("Error: The request token could not be obtained.")
            print("Response Data:", response_data)  # Debug: print the response data
            return None, None
    else:
        print(f"Error: {response.status_code}")
        print("Response Content:", response.content)  # Debug: print the response content for more details
        return None, None

# Call the function to get the request token
get_request_token()
