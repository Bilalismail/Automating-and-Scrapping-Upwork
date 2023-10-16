import time
from selenium.webdriver.common.by import By

class Scrape:
    def __init__(self, driver, secret, password):
        self.driver = driver
        self.secret = secret
        self.password = password
        self.userData = {
            "id": None,
            "account": None,
            "address": {
                "city": None,
                "line1": None,
                "line2": None,
                "state": None,
                "country": None,
                "postal_code": None
            },
            "first_name": None,
            "last_name": None,
            "full_name": None,
            "birth_date": None,
            "email": None,
            "phone_number": None,
            "picture_url": None,
            "employment_status": None,
            "employment_type": None,
            "job_title": None,
            "ssn": None,
            "marital_status": None,
            "gender": None,
            "hire_date": None,
            "termination_date": None,
            "termination_reason": None,
            "employer": None,
            "base_pay": {
                "amount": None,
                "period": None,
                "currency": None
            },
            "pay_cycle": None,
            "platform_ids": {
                "employee_id": None,
                "position_id": None,
                "platform_user_id": None
            },
            "created_at": None,
            "updated_at": None,
            "metadata": {}
        }

    def isLoggedIn(self):
        return self.driver.current_url == "https://www.upwork.com/en-gb/nx/find-work/best-matches"

    def dataFromPDF(self):
        self.downloadPDF(
            "https://www.upwork.com/en-gb/ab/payments/reports/certificate-of-earnings.pdf")
    # def downloadPDF(self, url):
    #     print(self.driver)
    #         # Set up Chrome download preferences
    #     chrome_options = self.driver.ChromeOptions()
    #     prefs = {
    #     "download.default_directory": '/',
    #     "download.prompt_for_download": False,
    #     "download.directory_upgrade": True,
    #     "plugins.always_open_pdf_externally": True  # It will not display PDF directly in chrome
    #      }
    #     chrome_options.add_experimental_option('prefs', prefs)
    #     driver = self.driver.Chrome(options=chrome_options)

    #     driver.get(url)

    # # wait for the download to complete (you might need to adjust the time)
    # # or implement a more sophisticated wait mechanism
    #     time.sleep(10)
    def dataFromURL(self):
        self.driver.get(
            "https://www.upwork.com/en-gb/freelancers/settings/contactInfo")
        time.sleep(5)
                    
        self.contactSecret()
        self.contactPassword()
        self.contactInfo()

    def contactInfo(self):
        time.sleep(4)
        try: 
            name = self.driver.find_element(By.CSS_SELECTOR, '[data-test="userName"]')
            self.getName(name.text)
            
        except:
            print("Not found")
    def getName(self, name):
        print("getName", name )
        self.userData["full_name"] = name
        name = name.split()
        self.userData["first_name"] = name[0]
        self.userData["last_name"] = name[1]

        print("first name in data",self.userData["first_name"])
    def contactSecret(self):
        try: 
            self.driver.find_element(By.ID, "deviceAuth_answer").send_keys(self.secret)
            login_button = self.driver.find_element(By.ID, "control_save")
            login_button.click()
        except:
            print("Not needed, page at:", self.driver.current_url)

    def contactPassword(self):
        try: 
            self.driver.find_element(By.ID, "sensitiveZone_password").send_keys(self.password)
            login_button = self.driver.find_element(By.ID, "control_continue")
            login_button.click()
            print("hello cp")
        except:
            print("cp Not needed, page at:", self.driver.current_url)
           
    def enterPage(self):
        pass

    def scrapeInfo(self):
        self.dataFromURL()
        return self.userData
        # self.dataFromPDF()
