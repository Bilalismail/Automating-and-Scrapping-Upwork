import time, json
from login import Login
from data import Data
from scrape import Scrape




USERNAME = "recruitment+scanners+data@argyle.com"
PASSWORD = "ArgyleAwesome!@"
SECRET = "The Dude1"
LINK = "https://www.upwork.com/ab/account-security/login"

def main():
    login_instance = Login(USERNAME, PASSWORD, SECRET, LINK)

    login_instance.userNameLogin()
    login_instance.passwordEntry()
    login_instance.secretEntry()
    scrape_instance = Scrape(login_instance.getDriver(), SECRET, PASSWORD)
    data = Data(**scrape_instance.scrapeInfo()).dict()
    login_instance.downloadPDF()
    scrape_instance.dataFromPDF()
    time.sleep(5)
    with open('data.json', 'w') as json_file:
        json.dump(data, json_file, indent=4)

if __name__ == "__main__":
    main()