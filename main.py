import time, json
from login import Login
from data import Data
from scrape import Scrape
import concurrent.futures

USERS = [
    {
        "username": "recruitment+scanners+data@argyle.com",
        "password": "ArgyleAwesome!@",
        "secret": "The Dude1",
        "link": "https://www.upwork.com/ab/account-security/login"
     },
    {
        "username": "recruitment+scanners+task@argyle.com",
        "password": "ArgyleAwesome!@",
        "secret": "TheDude1",
        "link": "https://www.upwork.com/ab/account-security/login"
    },
    {
        "username": "recruitment+tasks@argyle.com",
        "password": "ArgyleAwesome!@",
        "secret": "TheDude12",
        "link": "https://www.upwork.com/ab/account-security/login"
    }
]



# USERNAME = "recruitment+scanners+data@argyle.com"
# PASSWORD = "ArgyleAwesome!@"
# SECRET = "The Dude1"
# LINK = "https://www.upwork.com/ab/account-security/login"

def main(username, password, secret, link):
    login_instance = Login(username, password, secret, link)

    login_instance.userNameLogin()
    login_instance.passwordEntry()
    login_instance.secretEntry()
    login_instance.downloadPDF()
    scrape_instance = Scrape(login_instance.getDriver(), secret, password)
    data = Data(**scrape_instance.scrapeInfo()).dict()
    with open('data.json', 'w') as json_file:
        json.dump(data, json_file, indent=4)

if __name__ == "__main__":
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(main, user["username"], user["password"], user["secret"], user["link"]) for user in USERS]
        for future in concurrent.futures.as_completed(futures):
            future.result()
