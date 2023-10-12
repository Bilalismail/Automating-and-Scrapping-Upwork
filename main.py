import requests
from bs4 import BeautifulSoup

BASE_URL = "https://www.upwork.com"
LOGIN_URL = BASE_URL + "/ab/account-security/login"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.3"
}

def login(session, email, password):
    # Step 1: Submit email
    email_data = {
        "email": email
    }
    response = session.post(LOGIN_URL, data=email_data, headers=HEADERS)
    
    # Check if there's a redirect to a password page
    if response.status_code == 302:  # Or another condition that indicates a redirect
        password_url = BASE_URL + response.headers.get("Location")  # Extracting the redirect URL
        
        # Step 2: Submit password on the redirected page
        password_data = {
            "password": password
        }
        response = session.post(password_url, data=password_data, headers=HEADERS)
    
    return response

# Using the function
with requests.Session() as session:
    response = login(session, "Dave Worker - recruitment+scanners+task@argyle.com", "ArgyleAwesome!@")
    # TODO: Check if login was successful and proceed with scraping


# Using the function
with requests.Session() as session:
    response = login(session, "recruitment+scanners+data@argyle.com", "ArgyleAwesome!@")
    print(response.text)
    # TODO: Check if login was successful and proceed with scraping

