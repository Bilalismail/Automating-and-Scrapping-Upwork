from selenium import webdriver
from selenium.webdriver.common.by import By
import time, json
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from login import Login
from data import Data
from scrape import Scrape
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import json

# driver.get("https://www.upwork.com/en-gb/freelancers/settings/contactInfo")

# time.sleep(5)


USERNAME = "recruitment+scanners+data@argyle.com"
PASSWORD = "ArgyleAwesome!@"
SECRET = "The Dude1"
LINK = "https://www.upwork.com/ab/account-security/login"

def main():
    login_instance = Login(USERNAME, PASSWORD, SECRET, LINK)
    # login_instance.login()
    login_instance.userNameLogin()
    login_instance.passwordEntry()
    login_instance.secretEntry()
    scrape_instance = Scrape(login_instance.getDriver(), SECRET, PASSWORD)
    scrape_instance.scrapeInfo()
    data = Data(**scrape_instance.scrapeInfo()).dict()
    print("serilizesd data", data)
    time.sleep(5)
    with open('data.json', 'w') as json_file:
        json.dump(data, json_file, indent=4)



if __name__ == "__main__":
    main()

# def save_name_as_json(name_text: str) 
#     """
#     Takes a name string, splits it into first name and surname, 
#     and saves it as a JSON file.
    
#     Args:
#     - name_text: A string containing the full name (e.g., "Rachel Worker").
    
#     Returns:
#     - A dictionary containing the split name.
#     """
#     name_parts = name_text.split()
#     first_name = name_parts[0]
#     last_name = " ".join(name_parts[1:])
    
#     # Store the data in a dictionary
#     data = {
#         "name": first_name,
#         "surname": last_name
#     }

#     # Save the data to a JSON file
#     with open("name_data.json", "w") as file:
#         json.dump(data, file)

#     print("Data saved to name_data.json")
#     return data

