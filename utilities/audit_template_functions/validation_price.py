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

    def price_section(self, scenario=None):
        with allure.step("Price Section Question Validation"):
            try:
                if scenario == "maximum value":
                    unique_text = "Test Automation Price Max Character Count Validation"
                elif scenario == "minimum value":
                    unique_text = "Test Automation Price Text Min Character Count Validation"
                elif scenario == "between":
                    unique_text = "Test Automation Price Text Between Count Validation"
                
                else:
                    unique_text = "Test Automation TEXT Validation"
    
                enter_text = self.wait.until(EC.presence_of_element_located((By.XPATH, "//textarea[@placeholder='Enter your question here...']")))
                highlight_element(self.driver, enter_text)
                enter_text.click()
                enter_text.send_keys(unique_text)

            except Exception as e:
                msg = f"Failed to Enter Price Validation: {str(e)}"
                allure.attach(msg, name="Price validation Error", attachment_type=allure.attachment_type.TEXT)
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

    def select_max_value(self):
        with allure.step("Select Maximum Value"):
            try:
                select_dropdown = self.wait.until(EC.presence_of_element_located((By.XPATH, "//button[@id='validation_option']")))
                highlight_element(self.driver, select_dropdown)
                select_dropdown.click()
                time.sleep(1)

                max_value = self.wait.until(EC.presence_of_element_located((By.XPATH, "//div[text()='Maximum value']")))
                highlight_element(self.driver, max_value)
                max_value.click()

                enter_max_value = self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Enter value']")))
                highlight_element(self.driver, enter_max_value)
                enter_max_value.send_keys(100)
                
        
            except Exception as e:
                msg = f"failed to Attach PDF Document File: {str(e)}"
                allure.attach(msg, name = "Attach PDF Document File Error", attachment_type=allure.attachment_type.TEXT)
                raise Exception(msg)
        
    def select_min_value(self):
        with allure.step("Select Minimum Value"):
            try:
                select_dropdown = self.wait.until(EC.presence_of_element_located((By.XPATH, "//button[@id='validation_option']")))
                highlight_element(self.driver, select_dropdown)
                select_dropdown.click()
                time.sleep(1)

                min_value = self.wait.until(EC.presence_of_element_located((By.XPATH, "//div[text()='Minimum value']")))
                highlight_element(self.driver, min_value)
                min_value.click()

                enter_min_value = self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Enter value']")))
                highlight_element(self.driver, enter_min_value)
                enter_min_value.send_keys(50)
        
            except Exception as e:
                msg = f"failed to Attach PDF Document File: {str(e)}"
                allure.attach(msg, name = "Attach PDF Document File Error", attachment_type=allure.attachment_type.TEXT)
                raise Exception(msg)
        
    def select_between(self):
        with allure.step("Select Between Length"):
            try:
                select_dropdown = self.wait.until(EC.presence_of_element_located((By.XPATH, "//button[@id='validation_option']")))
                highlight_element(self.driver, select_dropdown)
                select_dropdown.click()
                time.sleep(1)

                between = self.wait.until(EC.presence_of_element_located((By.XPATH, "//div[text()='Between']")))
                highlight_element(self.driver, between)
                between.click()
        
            except Exception as e:
                msg = f"failed to Attach PDF Document File: {str(e)}"
                allure.attach(msg, name = "Attach PDF Document File Error", attachment_type=allure.attachment_type.TEXT)
                raise Exception(msg)
        
        
    def enter_from_to(self, from_num="50", to_num="100"):
        with allure.step("Enter From and To"):
            try:
                enter_from_num = self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='From']")))
                highlight_element(self.driver, enter_from_num)
                enter_from_num.click()
                enter_from_num.send_keys(from_num)
                time.sleep(1)
    
                enter_to_num = self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='To']")))
                highlight_element(self.driver, enter_to_num)
                enter_to_num.click()
                enter_to_num.send_keys(to_num)
                
            except Exception as e:
                msg = f"Failed to Enter Maximum number': {str(e)}"
                allure.attach(msg, name="Maximum Number Error", attachment_type=allure.attachment_type.TEXT)
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
        