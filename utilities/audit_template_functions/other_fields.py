import allure
import time
import random
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from utilities.other_utils_functions.highlight import highlight_element


class QuestionnaireOtherFields:


    def __init__(self, driver, wait):
        self.driver = driver
        self.wait = wait

    def add_date_range(self):
        with allure.step("Date Range Section without Validation"):
            try:
                unique_date_range = "Test Automation Date Range without Validation"
                enter_date_range = self.wait.until(EC.presence_of_element_located((By.XPATH, "//textarea[@placeholder='Enter your question here...']")))
                highlight_element(self.driver, enter_date_range)
                enter_date_range.click()
                enter_date_range.send_keys(unique_date_range)
            except Exception as e:
                msg = f"Failed to enter Date Range Section without validation: {str(e)}"
                allure.attach(msg,name="Date Range Section without validation Error",attachment_type=allure.attachment_type.TEXT)
                raise Exception(msg)

    def add_phone_number(self):
        with allure.step("Phone Number Section without Validation"):
            try:
                unique_phone_number = "Test Automation Phone Number without Validation"
                enter_phone_number = self.wait.until(EC.presence_of_element_located((By.XPATH, "//textarea[@placeholder='Enter your question here...']")))
                highlight_element(self.driver, enter_phone_number)
                enter_phone_number.click()
                enter_phone_number.send_keys(unique_phone_number)
            except Exception as e:
                msg = f"Failed to enter Phone Number Section without validation: {str(e)}"
                allure.attach(msg,name="Phone Number Section without validation Error",attachment_type=allure.attachment_type.TEXT)
                raise Exception(msg)

    def add_address(self):
        with allure.step("Address Section without Validation"):
            try:
                unique_address = "Test Automation Address without Validation"
                enter_address = self.wait.until(EC.presence_of_element_located((By.XPATH, "//textarea[@placeholder='Enter your question here...']")))
                highlight_element(self.driver, enter_address)
                enter_address.click()
                enter_address.send_keys(unique_address)
            except Exception as e:
                msg = f"Failed to enter Address Section without validation: {str(e)}"
                allure.attach(msg,name="Address Section without validation Error",attachment_type=allure.attachment_type.TEXT)
                raise Exception(msg)

    def add_url(self):
        with allure.step("URL Section without Validation"):
            try:
                unique_url = "Test Automation URL without Validation"
                enter_url = self.wait.until(EC.presence_of_element_located((By.XPATH, "//textarea[@placeholder='Enter your question here...']")))
                highlight_element(self.driver, enter_url)
                enter_url.click()
                enter_url.send_keys(unique_url)
            except Exception as e:
                msg = f"Failed to enter URL Section without validation: {str(e)}"
                allure.attach(msg,name="URL Section without validation Error",attachment_type=allure.attachment_type.TEXT)
                raise Exception(msg)

    def add_pan(self):
        with allure.step("PAN Section without Validation"):
            try:
                unique_pan = "Test Automation PAN without Validation"
                enter_pan = self.wait.until(EC.presence_of_element_located((By.XPATH, "//textarea[@placeholder='Enter your question here...']")))
                highlight_element(self.driver, enter_pan)
                enter_pan.click()
                enter_pan.send_keys(unique_pan)
            except Exception as e:
                msg = f"Failed to enter PAN Section without validation: {str(e)}"
                allure.attach(msg,name="PAN Section without validation Error",attachment_type=allure.attachment_type.TEXT)
                raise Exception(msg)

    def add_email(self):
        with allure.step("Email Section without Validation"):
            try:
                unique_email = "Test Automation Email without Validation"
                enter_email = self.wait.until(EC.presence_of_element_located((By.XPATH, "//textarea[@placeholder='Enter your question here...']")))
                highlight_element(self.driver, enter_email)
                enter_email.click()
                enter_email.send_keys(unique_email)
            except Exception as e:
                msg = f"Failed to enter Email Section without validation: {str(e)}"
                allure.attach(msg,name="Email Section without validation Error",attachment_type=allure.attachment_type.TEXT)
                raise Exception(msg)

    def add_attachment(self):
        with allure.step("Attachment Section without Validation"):
            try:
                unique_attachment = "Test Automation Attachment without Validation"
                enter_attachment = self.wait.until(EC.presence_of_element_located((By.XPATH, "//textarea[@placeholder='Enter your question here...']")))
                highlight_element(self.driver, enter_attachment)
                enter_attachment.click()
                enter_attachment.send_keys(unique_attachment)
            except Exception as e:
                msg = f"Failed to enter Email Section without validation: {str(e)}"
                allure.attach(msg,name="Email Section without validation Error",attachment_type=allure.attachment_type.TEXT)
                raise Exception(msg)

    def add_radio(self):
        with allure.step("Radio Section without Validation"):
            try:
                unique_radio = "Test Automation Radio without Validation"
                enter_radio = self.wait.until(EC.presence_of_element_located((By.XPATH, "//textarea[@placeholder='Enter your question here...']")))
                highlight_element(self.driver, enter_radio)
                enter_radio.click()
                enter_radio.send_keys(unique_radio)
            except Exception as e:
                msg = f"Failed to enter Radio Section without validation: {str(e)}"
                allure.attach(msg,name="Radio Section without validation Error",attachment_type=allure.attachment_type.TEXT)
                raise Exception(msg)