from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import time
import json
from pydantic import BaseModel
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json




driver = webdriver.Chrome()

driver.get("https://www.upwork.com/ab/account-security/login")

time.sleep(5)


USERNAME = "recruitment+scanners+data@argyle.com"
PASSWORD = "ArgyleAwesome!@"
SECRET = "The Dude1"

def save_name_as_json(name_text: str) -> dict:
    """
    Takes a name string, splits it into first name and surname, 
    and saves it as a JSON file.
    
    Args:
    - name_text: A string containing the full name (e.g., "Rachel Worker").
    
    Returns:
    - A dictionary containing the split name.
    """
    name_parts = name_text.split()
    first_name = name_parts[0]
    last_name = " ".join(name_parts[1:])
    
    # Store the data in a dictionary
    data = {
        "name": first_name,
        "surname": last_name
    }

    # Save the data to a JSON file
    with open("name_data.json", "w") as file:
        json.dump(data, file)

    print("Data saved to name_data.json")
    return data

username_field = driver.find_element(By.ID, "login_username")
username_field.send_keys(USERNAME)
login_button = driver.find_element(By.ID, "login_password_continue")
login_button.click()
time.sleep(3)
password_field = driver.find_element(By.ID, "login_password")
password_field.send_keys(PASSWORD)
login_button = driver.find_element(By.ID, "login_control_continue")
login_button.click()
time.sleep(5)
try:
    secret_field = driver.find_element(By.ID, "login_answer")
    secret_field.send_keys(SECRET)
    login_button = driver.find_element(By.ID, "login_control_continue")
    login_button.click()
    time.sleep(7)
except NoSuchElementException:
    # If the secret answer field is not present, check if you're on the expected dashboard page
    if "www.upwork.com/en-gb/nx/find-work/best-matches" in driver.current_url:
        print("Logged in successfully and on the dashboard page!")
    else:
        print("Unexpected page. Take appropriate action.")
time.sleep(7)

# After the login process
driver.get("https://www.upwork.com/en-gb/freelancers/settings/contactInfo")
try:
    # Wait for the div with the data-test attribute "userName" to be present
    element_present = EC.presence_of_element_located((By.CSS_SELECTOR, 'div[data-test="userName"]'))
    WebDriverWait(driver, 10).until(element_present)
    
    # Once the element is present, extract its text
    user_name_div = driver.find_element(By.CSS_SELECTOR, 'div[data-test="userName"]')
    name_text = user_name_div.text
    print(name_text)
    
except TimeoutException:
    try:
        # Check for the presence of the element with id="deviceAuth_answer"
        device_auth_field = driver.find_element(By.ID, "deviceAuth_answer")
        
        # If found, assume secret answer is required and fill it out
        device_auth_field.send_keys(SECRET)
        # You may also need to submit the form or click a button after entering the secret.
        login_button = driver.find_element(By.ID, "control_save")
        login_button.click()
        print("contact page")

        element_present = EC.presence_of_element_located((By.CSS_SELECTOR, 'div[data-test="userName"]'))
        WebDriverWait(driver, 10).until(element_present)
    
        # Once the element is present, extract its text
        user_name_div = driver.find_element(By.CSS_SELECTOR, 'div[data-test="userName"]')
        name_text = user_name_div.text
        save_name_as_json(name_text)
    
    except NoSuchElementException:
        print("Neither 'userName' div nor 'deviceAuth_answer' field were found. Check the page or handle this scenario.")
time.sleep(7)


