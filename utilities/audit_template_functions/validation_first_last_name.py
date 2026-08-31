import allure
import time
import random
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from utilities.other_utils_functions.highlight import highlight_element


class QuestionnaireFirstLastName:

    def __init__(self, driver, wait):
        self.driver = driver
        self.wait = wait

    def add_name(self):
        with allure.step("First/Last Name Section Without Validation"):
            try:
                unique_name = "Test Automation First/Last Name Without Validation"
                enter_first_name = self.wait.until(EC.presence_of_element_located((By.XPATH, "//textarea[@placeholder='Enter your question here...']")))
                highlight_element(self.driver, enter_first_name)
                enter_first_name.click()
                enter_first_name.send_keys(unique_name)
            except Exception as e:
                msg = f"Failed to Enter First Last Name Without Validation: {str(e)}"
                allure.attach(msg,name="First/Last Name without validation Error",attachment_type=allure.attachment_type.TEXT)
                raise Exception(msg)

    def validation_name(self):
        with allure.step("First/Last Name Section Validation"):
            try:
                unique_val_name = "Test Automation First Last Name Section Validation"
                val_first_name = self.wait.until(EC.presence_of_element_located((By.XPATH, "//textarea[@placeholder='Enter your question here...']")))
                highlight_element(self.driver, val_first_name)
                val_first_name.click()
                val_first_name.send_keys(unique_val_name)
            except Exception as e:
                msg = f"Failed to Enter First Last Name Section Validation: {str(e)}"
                allure.attach(msg,name="First Last Name Section Validation Error",attachment_type=allure.attachment_type.TEXT)
                raise Exception(msg)

    def first_last_name(self, scenario=None):
        with allure.step("First/Last Name Section Question Validation"):
            try:
                if scenario == "max":
                    unique_text = "Test Automation Name Max Character Count Validation"
                elif scenario == "min":
                    unique_text = "Test Automation Name Text Min Character Count Validation"
                elif scenario == "between":
                    unique_text = "Test Automation Name Text Between Count Validation"
                
                else:
                    unique_text = "Test Automation TEXT Validation"
    
                enter_text = self.wait.until(EC.presence_of_element_located((By.XPATH, "//textarea[@placeholder='Enter your question here...']")))
                highlight_element(self.driver, enter_text)
                enter_text.click()
                enter_text.send_keys(unique_text)

            except Exception as e:
                msg = f"Failed to Enter Name Validation: {str(e)}"
                allure.attach(msg, name="Name validation Error", attachment_type=allure.attachment_type.TEXT)
                raise Exception(msg)
    def select_length(self):
    
        with allure.step("Select Length"):
            try:
                length_dropdown = self.wait.until(EC.presence_of_element_located((By.XPATH, "//button[@id='validation_type']")))
                highlight_element(self.driver, length_dropdown)
                length_dropdown.click()
                time.sleep(1)

                length_btn = self.wait.until(EC.presence_of_element_located((By.XPATH, "//div[text()='Length']")))
                highlight_element(self.driver, length_btn)
                length_btn.click()
        
            except Exception as e:
                msg = f"failed to Select Length: {str(e)}"
                allure.attach(msg, name = "Select Length Error", attachment_type=allure.attachment_type.TEXT)
                raise Exception(msg)

    def select_max_char_count(self):
        with allure.step("Select Maximum Character Count"):
            try:
                select_dropdown = self.wait.until(EC.presence_of_element_located((By.XPATH, "//button[@id='validation_option']")))
                highlight_element(self.driver, select_dropdown)
                select_dropdown.click()
                time.sleep(1)

                max_char_count = self.wait.until(EC.presence_of_element_located((By.XPATH, "//div[text()='Maximum Character Count']")))
                highlight_element(self.driver, max_char_count)
                max_char_count.click()

                enter_max_count = self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Enter value']")))
                highlight_element(self.driver, enter_max_count)
                enter_max_count.send_keys(100)
                
        
            except Exception as e:
                msg = f"failed to Attach PDF Document File: {str(e)}"
                allure.attach(msg, name = "Attach PDF Document File Error", attachment_type=allure.attachment_type.TEXT)
                raise Exception(msg)
    
    def select_min_char_count(self):
        with allure.step("Select Minimum Character Count"):
            try:
                select_dropdown = self.wait.until(EC.presence_of_element_located((By.XPATH, "//button[@id='validation_option']")))
                highlight_element(self.driver, select_dropdown)
                select_dropdown.click()
                time.sleep(1)

                min_char_count = self.wait.until(EC.presence_of_element_located((By.XPATH, "//div[text()='Minimum Character Count']")))
                highlight_element(self.driver, min_char_count)
                min_char_count.click()

                enter_min_count = self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Enter value']")))
                highlight_element(self.driver, enter_min_count)
                enter_min_count.send_keys(50)
        
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
        