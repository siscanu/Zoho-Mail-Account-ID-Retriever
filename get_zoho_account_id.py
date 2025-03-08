#!/usr/bin/env python3
import requests
import json
import webbrowser
import time

# Replace with your Zoho API credentials
client_id = "YOUR_CLIENT_ID"  # Replace with your Zoho client ID
client_secret = "YOUR_CLIENT_SECRET"  # Replace with your Zoho client secret
redirect_uri = "http://localhost:8000/"

# Choose your Zoho domain based on your account region
# Available options:
# - "zoho.com"      # US/Global
# - "zoho.eu"       # Europe
# - "zoho.in"       # India
# - "zoho.com.au"   # Australia
# - "zoho.jp"       # Japan
# - "zoho.com.cn"   # China
# - "zohocloud.ca"  # Canada
# - "zoho.sa"       # Saudi Arabia
# - "zoho.uk"       # United Kingdom

# Default to EU, change this to match your region
zoho_domain = "zoho.eu"

# Multi-DC Support (Multiple Data Centers)
# If you have enabled Multi-DC in Zoho Developer Console, you can use the same
# client credentials for accounts across different regions, and the script will
# automatically use the correct endpoints based on the redirect URL.

# Construct the authorization URL with the selected domain
auth_url = f"https://accounts.{zoho_domain}/oauth/v2/auth?scope=ZohoMail.messages.ALL,ZohoMail.accounts.READ,ZohoMail.folders.READ&client_id={client_id}&response_type=code&access_type=offline&redirect_uri={redirect_uri}"

print("Opening browser to get a new authorization code with correct permissions...")
print(f"URL: {auth_url}")
print("\nAfter authorization, you'll be redirected to a URL.")
print("Copy the FULL URL from your browser address bar and paste it below.")

# Try to open the browser automatically
try:
    webbrowser.open(auth_url)
except:
    print("Could not open browser automatically. Please copy and paste the URL above into your browser.")

# Get the redirect URL from the user
redirect_url = input("\nPaste the full redirect URL here: ")

# Extract the authorization code from the URL
try:
    import urllib.parse
    parsed_url = urllib.parse.urlparse(redirect_url)
    query_params = urllib.parse.parse_qs(parsed_url.query)
    auth_code = query_params.get('code', [''])[0]
    
    if not auth_code:
        print("Could not extract authorization code from URL. Make sure to paste the full URL.")
        exit(1)
        
    print(f"Extracted authorization code: {auth_code}")
except Exception as e:
    print(f"Error extracting code: {e}")
    print("Please enter the code manually.")
    auth_code = input("Enter the code parameter from the URL: ")

# Determine the correct token URL based on the location in the redirect URL
token_domain = zoho_domain  # Default to the chosen domain
if "location=" in redirect_url:
    # Extract location from redirect URL
    location_match = urllib.parse.parse_qs(parsed_url.query).get('location', [''])[0]
    if location_match:
        if location_match == "eu":
            token_domain = "zoho.eu"
        elif location_match == "in":
            token_domain = "zoho.in"
        elif location_match == "au":
            token_domain = "zoho.com.au"
        elif location_match == "jp":
            token_domain = "zoho.jp"
        elif location_match == "com.cn":
            token_domain = "zoho.com.cn"
        elif location_match == "ca":
            token_domain = "zohocloud.ca"
        elif location_match == "sa":
            token_domain = "zoho.sa"
        elif location_match == "uk":
            token_domain = "zoho.uk"
        else:
            token_domain = "zoho.com"  # Default to US/Global

# Exchange the authorization code for a token
token_url = f"https://accounts.{token_domain}/oauth/v2/token"
token_data = {
    "code": auth_code,
    "client_id": client_id,
    "client_secret": client_secret,
    "redirect_uri": redirect_uri,
    "grant_type": "authorization_code"
}

print("\nExchanging code for token...")
print(f"Using token endpoint: {token_url}")
token_response = requests.post(token_url, data=token_data)
print(f"Token status: {token_response.status_code}")

# We don't print the full token response to avoid exposing sensitive information
if token_response.status_code != 200:
    print(f"Failed to get token: {token_response.text}")
    exit(1)
else:
    print("Token obtained successfully!")

# Extract the access token
try:
    token_json = token_response.json()
    access_token = token_json.get("access_token")
    refresh_token = token_json.get("refresh_token")
    
    # Print a masked version of the token for security
    if access_token:
        masked_token = access_token[:10] + "..." + access_token[-5:]
        print(f"Access token: {masked_token}")
        
        if refresh_token:
            print("Refresh token obtained. Save this for refreshing your access token later.")
except:
    print("Could not parse token response.")
    exit(1)

# Determine API domain based on token domain
api_domain = f"mail.{token_domain}"

# Now get the account ID
def get_account_id(access_token, api_domain):
    # Endpoint to list accounts
    endpoint = f"https://{api_domain}/api/accounts"
    
    # Headers
    headers = {
        "Authorization": f"Zoho-oauthtoken {access_token}",
        "Accept": "application/json"
    }
    
    # Make the request
    print("\nGetting account ID...")
    print(f"Using API endpoint: {endpoint}")
    response = requests.get(endpoint, headers=headers)
    
    # Print the status code for debugging
    print(f"Status code: {response.status_code}")
    
    # Check if successful
    if response.status_code == 200:
        try:
            data = response.json()
            print("\nYour Zoho Mail accounts:")
            for account in data.get("data", []):
                account_id = account.get("accountId")
                email = account.get("primaryEmailAddress")
                print(f"Account ID: {account_id}")
                print(f"Email: {email}")
                print("-" * 40)
                
                print("\nTo use these credentials in your email script, use:")
                print(f'ACCOUNT_ID = "{account_id}"')
                print('OAUTH_TOKEN = "your_access_token"  # Replace with the actual access token')
                print(f'API_DOMAIN = "{api_domain}"  # For your region')
                
                # Try listing emails as a test
                test_email_access(access_token, account_id, api_domain)
        except Exception as e:
            print(f"Error parsing response: {e}")
    else:
        print(f"Failed to get account ID. Error: {response.text}")

def test_email_access(access_token, account_id, api_domain):
    """Test if we can access emails with the given token and account ID"""
    endpoint = f"https://{api_domain}/api/accounts/{account_id}/messages/view"
    
    headers = {
        "Authorization": f"Zoho-oauthtoken {access_token}",
        "Accept": "application/json"
    }
    
    params = {
        "limit": 1  # Just get one email to test
    }
    
    print("\nTesting email access...")
    print(f"Using endpoint: {endpoint}")
    response = requests.get(endpoint, headers=headers, params=params)
    print(f"Email access status: {response.status_code}")
    
    if response.status_code == 200:
        print("Email access successful! You can now use these credentials to fetch emails.")
    else:
        print(f"Email access failed: {response.text}")

# Call the function with the access token
if access_token:
    get_account_id(access_token, api_domain)
else:
    print("No access token obtained.") 
