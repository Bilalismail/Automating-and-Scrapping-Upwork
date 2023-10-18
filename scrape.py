import time
from selenium.webdriver.common.by import By
import PyPDF2
import re


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
        # Define the path to your PDF file
        pdf_path = "./downloads/certificate-of-earnings.pdf/certificate-of-earnings.pdf"

        # Open the PDF file
        with open(pdf_path, "rb") as file:
            # Create a PDF reader object
            pdf_reader = PyPDF2.PdfReader(file)

            # Ensure the PDF has pages
            if len(pdf_reader.pages) == 0:
                print("The PDF file has no pages.")
                return

            # Extract text from each page
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                page_text = page.extract_text()

                # Regular expressions to capture the desired data
                name_pattern = r"Name (.*?)\n"
                title_pattern = r"Title (.*?)\n"
                profile_url_pattern = r"Upwork Profile URL (.*?)\n"
                active_since_pattern = r"Active on Upwork Since (.*?)\n"
                address_pattern = r"Address (.*?), (.*?), (.*?), (.*?)\n"

                # Extract the data using the patterns
                name_match = re.search(name_pattern, page_text)
                title_match = re.search(title_pattern, page_text)
                profile_url_match = re.search(profile_url_pattern, page_text)
                active_since_match = re.search(active_since_pattern, page_text)
                address_match = re.search(address_pattern, page_text)

                # Assign the extracted data to the dictionary
                if address_match:
                    address_line1 = address_match.group(1)
                    city = address_match.group(2)
                    state = address_match.group(3)
                    postal_code_country = address_match.group(4)
                    postal_code_country_split = postal_code_country.split(", ")

                    if len(postal_code_country_split) == 2:
                        postal_code, country = postal_code_country_split
                    else:
                        postal_code = postal_code_country_split[0]
                        country = ""  # or assign None or any default value

                # Create a dictionary to store the extracted data
                extracted_data = {
                    "Name": name_match.group(1) if name_match else "",
                    "Title": title_match.group(1) if title_match else "",
                    "Upwork Profile URL": profile_url_match.group(1) if profile_url_match else "",
                    "Active on Upwork Since": active_since_match.group(1) if active_since_match else "",
                    "Address": {
                        "Line1": address_line1,
                        "City": city,
                        "State": state,
                        "Postal Code": postal_code,
                        "Country": country
                    }
                }

        self.pdfToData(extracted_data)
    def pdfToData(self, data):
        # Check the relevant fields and update them if they are None
        if not self.userData["full_name"] and "Name" in data:
            self.userData["full_name"] = data["Name"]
            names = data["Name"].split()
            self.userData["first_name"] = names[0] if len(names) > 0 else ""
            self.userData["last_name"] = names[1] if len(names) > 1 else ""
        
        if not self.userData["job_title"] and "Title" in data:
            self.userData["job_title"] = data["Title"]
        
        # Assuming the "Upwork Profile URL" should map to "picture_url"
        if not self.userData["picture_url"] and "Upwork Profile URL" in data:
            self.userData["picture_url"] = data["Upwork Profile URL"]

        # Assuming the "Active on Upwork Since" should map to "hire_date"
        if not self.userData["hire_date"] and "Active on Upwork Since" in data:
            self.userData["hire_date"] = data["Active on Upwork Since"]

        # Update address details if they are None
        if "Address" in data:
            for key in ["city", "line1", "state", "country", "postal_code"]:
                if key.capitalize() in data["Address"] and not self.userData["address"][key]:
                    self.userData["address"][key] = data["Address"][key.capitalize()]

        # At this point, you can print or return the updated userData
        # print(self.userData)

    def dataFromURL(self):
        self.driver.get(
            "https://www.upwork.com/en-gb/freelancers/settings/contactInfo")
        time.sleep(5)

        self.contactSecret()
        self.contactPassword()
        self.contactInfo()

    def contactInfo(self):
        time.sleep(4)

        self.getName()
        self.getAddress()
        self.getPhoneNumber()

    def getPhoneNumber(self):
        try:
            phoneNumber = self.driver.find_element(
                By.CSS_SELECTOR, '[data-test="phone"]')
            phoneNumber = phoneNumber.text
            self.userData["phone_number"] = phoneNumber
        except:
            print("Error at getPhoneNumber")

    def getAddress(self):
        try:
            addressCity = self.driver.find_element(
                By.CSS_SELECTOR, '[data-test="addressCity"]')
            addressCity = addressCity.text
            self.userData["address"]["city"] = addressCity

            addressStreet = self.driver.find_element(
                By.CSS_SELECTOR, '[data-test="addressStreet"]')
            addressStreet = addressStreet.text
            self.userData["address"]["line1"] = addressStreet

            addressZip = self.driver.find_element(
                By.CSS_SELECTOR, '[data-test="addressZip"]')
            addressZip = addressZip.text
            self.userData["address"]["postal_code"] = addressZip

            addressState = self.driver.find_element(
                By.CSS_SELECTOR, '[data-test="addressState"]')
            addressState = addressState.text
            self.userData["address"]["state"] = addressState

            addressCountry = self.driver.find_element(
                By.CSS_SELECTOR, '[data-test="addressCountry"]')
            addressCountry = addressCountry.text
            self.userData["address"]["country"] = addressCountry

        except:
            print("getAddress failure")

    def getName(self):
        try:
            name = self.driver.find_element(
                By.CSS_SELECTOR, '[data-test="userName"]')
            name = name.text
            self.userData["full_name"] = name
            name = name.split()
            self.userData["first_name"] = name[0]
            self.userData["last_name"] = name[1]

        except:
            print("first name in data", self.userData["first_name"])

    def contactSecret(self):
        try:
            self.driver.find_element(
                By.ID, "deviceAuth_answer").send_keys(self.secret)
            login_button = self.driver.find_element(By.ID, "control_save")
            login_button.click()
        except:
            print("Not needed, page at:", self.driver.current_url)

    def contactPassword(self):
        try:
            self.driver.find_element(
                By.ID, "sensitiveZone_password").send_keys(self.password)
            login_button = self.driver.find_element(By.ID, "control_continue")
            login_button.click()
            print("hello cp")
        except:
            print("cp Not needed, page at:", self.driver.current_url)

    def enterPage(self):
        pass

    def scrapeInfo(self):
        self.dataFromURL()
        # self.dataFromPDF()
        return self.userData
