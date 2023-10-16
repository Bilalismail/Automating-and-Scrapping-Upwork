from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import time

class Login:
    def __init__(self, email, password, secretAnswer, entryPage):
        self.email = email
        self.password = password
        self.secretAnswer = secretAnswer
        self.driver = self.init_browser()
        self.entryPage = entryPage
        self.loggedIn = False
    def init_browser(self):
        """Initialize the Chrome browser."""
        return webdriver.Chrome()

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
        if secret_elem:  # check if secret_elem is not None
            secret_elem.send_keys(self.secretAnswer)
            self.driver.find_element(By.ID, "login_control_continue").click()
            time.sleep(7)
            if self.driver.url == "www.upwork.com/en-gb/nx/find-work/best-matches":
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
    def close(self):
        """Close the browser."""
        self.driver.quit()