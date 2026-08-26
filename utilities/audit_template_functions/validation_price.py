import allure
import time
import random
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from utilities.other_utils_functions.highlight import highlight_element


class QuestionnairePrice:

    def __init__(self, driver, wait):
        self.driver = driver
        self.wait = wait

    def add_price(self):
        with allure.step("Price Section Without Validation"):
            try:
                unique_price = "Test Automation Price Without Validation"
                enter_price = self.wait.until(EC.presence_of_element_located((By.XPATH, "//textarea[@placeholder='Enter your question here...']")))
                highlight_element(self.driver, enter_price)
                enter_price.click()
                enter_price.send_keys(unique_price)
            except Exception as e:
                msg = f"Failed to Enter Price Without Validation: {str(e)}"
                allure.attach(msg,name="Price Without Validation Error",attachment_type=allure.attachment_type.TEXT)
                raise Exception(msg)

    def validation_price(self):
        with allure.step("Price Section Validation"):
            try:
                price_question = "Test Automation Price Section Validation"
                val_price = self.wait.until(EC.presence_of_element_located((By.XPATH, "//textarea[@placeholder='Enter your question here...']")))
                highlight_element(self.driver, val_price)
                val_price.click()
                val_price.send_keys(price_question)
            except Exception as e:
                msg = f"Failed to Enter Price Section Section Validation: {str(e)}"
                allure.attach(msg,name="Price Section Setion Validation Error",attachment_type=allure.attachment_type.TEXT)
                raise Exception(msg)

    def select_value(self):
    
        with allure.step("Select Value"):
            try:
                value_dropdown = self.wait.until(EC.presence_of_element_located((By.XPATH, "//button[@id='validation_type']")))
                highlight_element(self.driver, value_dropdown)
                value_dropdown.click()
                time.sleep(1)

                value_btn = self.wait.until(EC.presence_of_element_located((By.XPATH, "//div[text()='Value']")))
                highlight_element(self.driver, value_btn)
                value_btn.click()
        
            except Exception as e:
                msg = f"failed to Select Length: {str(e)}"
                allure.attach(msg, name = "Select Length Error", attachment_type=allure.attachment_type.TEXT)
                raise Exception(msg)

   
    def error_message(self):

        try:
            enter_error_message = self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@id='validation_custom_error']")))
            highlight_element(self.driver, enter_error_message)
            enter_error_message.click()
            enter_error_message.send_keys("Test Error Message")
            time.sleep(1)

        except Exception as e:
            msg = f"failed to Enter value: {str(e)}"
            allure.attach(msg, name = "Enter value Error", attachment_type=allure.attachment_type.TEXT)
            raise Exception(msg)
        