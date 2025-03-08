# Zoho Mail Account ID Retriever

A simple Python script that helps you get your Zoho Mail account ID and OAuth token for API access.

## Features

- Guides you through OAuth2 authorization flow
- Gets access token and refresh token from Zoho
- Retrieves your Zoho Mail account ID
- Tests email access to verify credentials work

## Prerequisites

- Python 3.8+
- A Zoho Mail account
- Zoho API credentials (Client ID and Client Secret) [Zoho API Console](https://api-console.zoho.com/)

## Installation

1. Clone this repository:
```
git clone https://github.com/siscanu/Zoho-Mail-Account-ID-Retriever.git
cd Zoho-Mail-Account-ID-Retriever
```

2. Install required packages:
```
pip install requests
```

## Setup

1. Create a Zoho API client:
   - Go to [Zoho API Console](https://api-console.zoho.com/)
   - Sign in with your Zoho account
   - Click "Add Client" and select "Server-based Applications"
   - Fill in required details and add `http://localhost:8000/` or your real redirect URL as the Redirect URL
   - After creation, note the Client ID and Client Secret

2. Edit the script to add your credentials:
   - Open `get_zoho_account_id.py`
   - Replace `YOUR_CLIENT_ID` with your actual Client ID
   - Replace `YOUR_CLIENT_SECRET` with your actual Client Secret
   - Set the `zoho_domain` variable to match your region (default is "zoho.eu")
   - Save the file

```python
# Change this to match your region
zoho_domain = "zoho.eu"  # For Europe
# zoho_domain = "zoho.com"  # For US/Global
# zoho_domain = "zoho.in"  # For India
# etc.
```

## Usage

1. Run the script:
```
python get_zoho_account_id.py
```

2. The script will:
   - Open your browser to the Zoho authorization page
   - Ask you to authorize the application
   - Redirect you to a URL containing the authorization code
   - Exchange the code for an access token
   - Retrieve your account ID
   - Test email access

3. Once complete, you'll see your:
   - Account ID
   - Access Token (masked for security)
   - API Domain for your region
   - Confirmation that email access works

4. Use these credentials in your applications that need to access Zoho Mail

## Example Output

```
Opening browser to get a new authorization code with correct permissions...
URL: https://accounts.zoho.eu/oauth/v2/auth?scope=ZohoMail.messages.ALL,ZohoMail.accounts.READ,ZohoMail.folders.READ&client_id=YOUR_CLIENT_ID&response_type=code&access_type=offline&redirect_uri=http://localhost:8000/

After authorization, you'll be redirected to a URL.
Copy the FULL URL from your browser address bar and paste it below.

Paste the full redirect URL here: http://localhost:8000/?code=1000.abcdef123456...&location=eu&accounts-server=https%3A%2F%2Faccounts.zoho.eu
Extracted authorization code: 1000.abcdef123456...

Exchanging code for token...
Using token endpoint: https://accounts.zoho.eu/oauth/v2/token
Token status: 200
Token obtained successfully!
Access token: 1000.abcde...12345

Getting account ID...
Using API endpoint: https://mail.zoho.eu/api/accounts
Status code: 200

Your Zoho Mail accounts:
Account ID: 7890123000000456789
Email: yourmail@yourdomain.com
----------------------------------------

To use these credentials in your email script, use:
ACCOUNT_ID = "7890123000000456789"
OAUTH_TOKEN = "your_access_token"  # Replace with the actual access token
API_DOMAIN = "mail.zoho.eu"  # For your region

Testing email access...
Using endpoint: https://mail.zoho.eu/api/accounts/7890123000000456789/messages/view
Email access status: 200
Email access successful! You can now use these credentials to fetch emails.
```

## Refreshing Tokens

Zoho access tokens expire after 1 hour. To keep your application working, you'll need to either:

1. Run this script again to get a new token when the old one expires
2. Use the refresh token to get a new access token (not implemented in this script)

## License

MIT License - See LICENSE file for details. 
