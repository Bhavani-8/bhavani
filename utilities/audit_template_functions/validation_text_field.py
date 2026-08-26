import allure
import time
import random
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from utilities.other_utils_functions.highlight import highlight_element


class QuestionnaireTextField:

    def __init__(self, driver, wait):
        self.driver = driver
        self.wait = wait

    def add_text(self):
        with allure.step("Text Section Question Without Validation"):
            try:
                unique_text = "Test Automation TEXT Without Validation"
                enter_text = self.wait.until(EC.presence_of_element_located((By.XPATH, "//textarea[@placeholder='Enter your question here...']")))
                highlight_element(self.driver, enter_text)
                enter_text.click()
                enter_text.send_keys(unique_text)
            except Exception as e:
                msg = f"Failed to Enter Text Without Validation: {str(e)}"
                allure.attach(msg,name="Text without validation Error",attachment_type=allure.attachment_type.TEXT)
                raise Exception(msg)

    def validation_text(self):
        with allure.step("Text Section Validation"):
            try:
                text_question = "Test Automation TEXT Section Validation"
                val_text = self.wait.until(EC.presence_of_element_located((By.XPATH, "//textarea[@placeholder='Enter your question here...']")))
                highlight_element(self.driver, val_text)
                val_text.click()
                val_text.send_keys(text_question)
            except Exception as e:
                msg = f"Failed to Enter Text Section Validation: {str(e)}"
                allure.attach(msg,name="Text Section Validation Error",attachment_type=allure.attachment_type.TEXT)
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
    
                enter_to_num = self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Enter max size']")))
                highlight_element(self.driver, enter_to_num)
                enter_to_num.click()
                enter_to_num.send_keys(to_num)
                
            except Exception as e:
                msg = f"Failed to Enter Maximum number': {str(e)}"
                allure.attach(msg, name="Maximum Number Error", attachment_type=allure.attachment_type.TEXT)
                raise Exception(msg)

        
    def select_regular_text(self):
        with allure.step("Select Regular Text"):
            try:
                regular_dropdown = self.wait.until(EC.presence_of_element_located((By.XPATH, "//button[@id='validation_type']")))
                highlight_element(self.driver, regular_dropdown)
                regular_dropdown.click()
                time.sleep(1)

                regular_btn = self.wait.until(EC.presence_of_element_located((By.XPATH, "//div[text()='Regular text']")))
                highlight_element(self.driver, regular_btn)
                regular_btn.click()
        
            except Exception as e:
                msg = f"failed to Select Regular Text: {str(e)}"
                allure.attach(msg, name = "Select Regular Text Error", attachment_type=allure.attachment_type.TEXT)
                raise Exception(msg)

    

    def enter_value_count(self):
        try:
            enter_value = self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Enter value']")))
            highlight_element(self.driver, enter_value)
            enter_value.click()
            enter_value.send_keys(1)
            time.sleep(1)

        except Exception as e:
            msg = f"failed to Enter value: {str(e)}"
            allure.attach(msg, name = "Enter value Error", attachment_type=allure.attachment_type.TEXT)
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
        