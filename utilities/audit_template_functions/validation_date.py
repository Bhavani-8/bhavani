import allure
import time
import random
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from utilities.other_utils_functions.highlight import highlight_element


class QuestionnaireDateField:

    def __init__(self, driver, wait):
        self.driver = driver
        self.wait = wait

    def add_date(self):
        with allure.step("Date Without Validation"):
            try:
                unique_date = "Test Automation Date Without Validation"
                enter_date = self.wait.until(EC.presence_of_element_located((By.XPATH, "//textarea[@placeholder='Enter your question here...']")))
                highlight_element(self.driver, enter_date)
                enter_date.click()
                enter_date.send_keys(unique_date)
            except Exception as e:
                msg = f"Failed to Enter Date Without Validation: {str(e)}"
                allure.attach(msg,name="Date without validation Error",attachment_type=allure.attachment_type.TEXT)
                raise Exception(msg)

    def validation_date(self):
        with allure.step("Date Section Validation"):
            try:
                unique_val_date = "Test Automation Date Validation"
                val_date = self.wait.until(EC.presence_of_element_located((By.XPATH, "//textarea[@placeholder='Enter your question here...']")))
                highlight_element(self.driver, val_date)
                val_date.click()
                val_date.send_keys(unique_val_date)
            except Exception as e:
                msg = f"Failed to Enter Date Section Validation: {str(e)}"
                allure.attach(msg,name="Date Section Validation Error",attachment_type=allure.attachment_type.TEXT)
                raise Exception(msg)

    def date_sections(self, scenario=None):
        with allure.step("Date Section Question Validation"):
            try:
                if scenario == "past date":
                    unique_text = "Test Automation Date Past date Validation"
                elif scenario == "current date":
                    unique_text = "Test Automation Date current date Validation"
                elif scenario == "future date":
                    unique_text = "Test Automation Date Future Date Validation"
                else:
                    unique_text = "Test Automation TEXT Validation"
    
                enter_text = self.wait.until(EC.presence_of_element_located((By.XPATH, "//textarea[@placeholder='Enter your question here...']")))
                highlight_element(self.driver, enter_text)
                enter_text.click()
                enter_text.send_keys(unique_text)

            except Exception as e:
                msg = f"Failed to Enter Date Validation: {str(e)}"
                allure.attach(msg, name="Date validation Error", attachment_type=allure.attachment_type.TEXT)
                raise Exception(msg)
     
    def select_past_date(self):

         with allure.step("Select Past Date"):
            try:
                past_date_dropdown = self.wait.until(EC.presence_of_element_located((By.XPATH, "//button[@id='validation_type']")))
                highlight_element(self.driver, past_date_dropdown)
                past_date_dropdown.click()
                time.sleep(1)

                past_date_btn = self.wait.until(EC.presence_of_element_located((By.XPATH, "//div[text()='Past Date']")))
                highlight_element(self.driver, past_date_btn)
                past_date_btn.click()
        
            except Exception as e:
                msg = f"failed to Select Past Date: {str(e)}"
                allure.attach(msg, name = "Past Date Error", attachment_type=allure.attachment_type.TEXT)
                raise Exception(msg)

    def select_current_date(self):
    
        with allure.step("Select Current Date"):
            try:
                current_date_dropdown = self.wait.until(EC.presence_of_element_located((By.XPATH, "//button[@id='validation_type']")))
                highlight_element(self.driver, current_date_dropdown)
                current_date_dropdown.click()
                time.sleep(1)

                current_date_btn = self.wait.until(EC.presence_of_element_located((By.XPATH, "//div[text()='Current Date']")))
                highlight_element(self.driver, current_date_btn)
                current_date_btn.click()
        
            except Exception as e:
                msg = f"failed to Select Current Date: {str(e)}"
                allure.attach(msg, name = "Current Date Error", attachment_type=allure.attachment_type.TEXT)
                raise Exception(msg)
    

    def select_future_date(self):
        
        with allure.step("Select Future Date"):
            try:
                future_date_dropdown = self.wait.until(EC.presence_of_element_located((By.XPATH, "//button[@id='validation_type']")))
                highlight_element(self.driver, future_date_dropdown)
                future_date_dropdown.click()
                time.sleep(1)

                future_date_btn = self.wait.until(EC.presence_of_element_located((By.XPATH, "//div[text()='Future Date']")))
                highlight_element(self.driver, future_date_btn)
                future_date_btn.click()
        
            except Exception as e:
                msg = f"failed to Select exactly: {str(e)}"
                allure.attach(msg, name = "exactly Error", attachment_type=allure.attachment_type.TEXT)
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
        