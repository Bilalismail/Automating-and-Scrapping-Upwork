from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.chrome.service import Service
import time

import os

# Get the absolute path of the current script's directory
project_directory = os.path.dirname(os.path.abspath(__file__))

# Create a path to save the PDF (e.g., in a folder named 'downloads' within the project directory)
save_path = os.path.join(project_directory, 'downloads', 'certificate-of-earnings.pdf')
if not os.path.exists(os.path.join(project_directory, 'downloads')):
    os.makedirs(os.path.join(project_directory, 'downloads'))


class Login:
    def __init__(self, email, password, secretAnswer, entryPage):
        self.email = email
        self.password = password
        self.secretAnswer = secretAnswer
        self.entryPage = entryPage
        self.loggedIn = False
        self.driver = self.init_browser()

    def init_browser(self):
        """Initialize the Chrome browser with custom options."""
        chrome_options = webdriver.ChromeOptions()
        prefs = {
            "download.default_directory": save_path,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "plugins.always_open_pdf_externally": True,  # This should handle PDFs
            "pdfjs.disabled": True  # Disables the built-in PDF viewer
        }
        chrome_options.add_experimental_option('prefs', prefs)
        service = Service(executable_path='./chromedriver')
        return webdriver.Chrome(service=service, options=chrome_options)  # Notice the change here


    def wait_for_element(self, by, value, timeout=10):
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by, value))
            )
            return element
        except TimeoutException:
            print(f"Element with locator: ({by}, {value}) was not found in {timeout} seconds.")
            return None

    def userNameLogin(self):
        self.driver.get(self.entryPage)
        try:
            username_elem = self.wait_for_element(By.ID, "login_username")
            username_elem.send_keys(self.email)
            self.driver.find_element(By.ID, "login_password_continue").click()
            time.sleep(5)
        except NoSuchElementException:
            print(f"Failed to get expected page: {self.entryPage}")

    def passwordEntry(self):
        """Enter password and proceed."""
        password_elem = self.wait_for_element(By.ID, "login_password")
        password_elem.send_keys(self.password)
        self.driver.find_element(By.ID, "login_control_continue").click()
        print("login")
        time.sleep(5)

    def secretEntry(self):
        secret_elem = self.wait_for_element(By.ID, "login_answer")
        if secret_elem:
            secret_elem.send_keys(self.secretAnswer)
            self.driver.find_element(By.ID, "login_control_continue").click()
            time.sleep(7)
            if self.driver.current_url == "www.upwork.com/en-gb/nx/find-work/best-matches":
                self.loggedIn == True
        elif "www.upwork.com/en-gb/nx/find-work/best-matches" in self.driver.current_url:
            print("Logged in successfully without entering secret pass")
            self.loggedIn = True
        else:
            print("Failed to find the secret answer field. Check the page or handle this scenario.")

    def login(self):
        self.userNameLogin()

    def getDriver(self):
        return self.driver

    def downloadPDF(self):
        url = "https://www.upwork.com/en-gb/ab/payments/reports/certificate-of-earnings.pdf"
        self.driver.get(url)

        try:
            url = "https://www.upwork.com/en-gb/ab/payments/reports/certificate-of-earnings.pdf"
            self.driver.get(url)
        except NoSuchElementException:
            print("Failed at pdf page")
        time.sleep(10)  # Adjust this delay as needed. It's for ensuring the file gets downloaded.

    def close(self):
        """Close the browser."""
        self.driver.quit()
