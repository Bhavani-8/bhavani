import allure
import time
import random
import os
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

    def max_min_counts(self, scenario=None):
        with allure.step("Text Section Question Validation"):
            try:
                if scenario == "max":
                    unique_text = "Test Automation Text Max Character Count Validation"
                elif scenario == "min":
                    unique_text = "Test Automation Text Min Character Count Validation"
                elif scenario == "between":
                    unique_text = "Test Automation Text Between Count Validation"
                elif scenario == "contains":
                    unique_text = "Test Automation Text Contains Validation"
                elif scenario == "doesn't contains":
                    unique_text = "Test Automation Text Doesn't Contains  Validation"
                elif scenario == "matche's":
                    unique_text = "Test Automation Text matche's Validation" 
                elif scenario == "doesn't match":
                    unique_text = "Test Automation Text doesn't match  Validation" 
                else:
                    unique_text = "Test Automation TEXT Validation"

                enter_text = self.wait.until(EC.presence_of_element_located((By.XPATH, "//textarea[@placeholder='Enter your question here...']")))
                highlight_element(self.driver, enter_text)
                enter_text.click()
                enter_text.send_keys(unique_text)

            except Exception as e:
                msg = f"Failed to Enter Text Validation: {str(e)}"
                allure.attach(msg, name="Text validation Error", attachment_type=allure.attachment_type.TEXT)
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

    def select_max_char_count(self, max_num="100"):
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
                enter_max_count.send_keys(max_num)
                
        
            except Exception as e:
                msg = f"failed to Attach PDF Document File: {str(e)}"
                allure.attach(msg, name = "Attach PDF Document File Error", attachment_type=allure.attachment_type.TEXT)
                raise Exception(msg)

    def select_min_char_count(self, min_num="50"):
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
                enter_min_count.send_keys(min_num)
        
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

                entered_values = (f"From Number: {from_num}\n"f"To Number: {to_num}")

                allure.attach(entered_values,name="From To Values Entered",attachment_type=allure.attachment_type.TEXT)
                
            except Exception as e:
                msg = f"Failed to Enter From To number': {str(e)}"
                allure.attach(msg, name="From To Number Error", attachment_type=allure.attachment_type.TEXT)
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

    
    def select_contains(self):
        with allure.step("Select Contains"):
            try:
                contains_dropdown = self.wait.until(EC.presence_of_element_located((By.XPATH, "//button[@id='validation_option']")))
                highlight_element(self.driver, contains_dropdown)
                contains_dropdown.click()
                time.sleep(1)

                contain_btn = self.wait.until(EC.presence_of_element_located((By.XPATH, "//div[text()='Contains']")))
                highlight_element(self.driver, contain_btn)
                contain_btn.click()

                enter_value = self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Enter value']")))
                highlight_element(self.driver, enter_value)
                enter_value.click()
                enter_value.send_keys(1)
                time.sleep(1)
        
            except Exception as e:
                msg = f"failed to Select Contains: {str(e)}"
                allure.attach(msg, name = "Select Contains Error", attachment_type=allure.attachment_type.TEXT)
                raise Exception(msg)
    
    def select_doesnt_contain(self):
        with allure.step("Select Doesn't Contains"):
            try:
                doesnt_contain_dropdown = self.wait.until(EC.presence_of_element_located((By.XPATH, "//button[@id='validation_option']")))
                highlight_element(self.driver, doesnt_contain_dropdown)
                doesnt_contain_dropdown.click()
                time.sleep(1)

                doesnt_contain_btn = self.wait.until(EC.presence_of_element_located((By.XPATH, '//div[text()="Doesn\'t contain"]')))
                highlight_element(self.driver, doesnt_contain_btn)
                doesnt_contain_btn.click()

                enter_value = self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Enter value']")))
                highlight_element(self.driver, enter_value)
                enter_value.click()
                enter_value.send_keys(2)
                time.sleep(1)
        
            except Exception as e:
                msg = f"failed to Select Doesn't Contains: {str(e)}"
                allure.attach(msg, name = "Select Doesn't Contains Error", attachment_type=allure.attachment_type.TEXT)
                raise Exception(msg)
    
    def select_matches(self):
        with allure.step("Select Matches"):
            try:
                matches_dropdown = self.wait.until(EC.presence_of_element_located((By.XPATH, "//button[@id='validation_option']")))
                highlight_element(self.driver, matches_dropdown)
                matches_dropdown.click()
                time.sleep(1)

                matches_btn = self.wait.until(EC.presence_of_element_located((By.XPATH, "//div[text()='Matches']")))
                highlight_element(self.driver, matches_btn)
                matches_btn.click()

                enter_value = self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Enter value']")))
                highlight_element(self.driver, enter_value)
                enter_value.click()
                enter_value.send_keys(1)
                time.sleep(1)
        
            except Exception as e:
                msg = f"failed to Select Matches: {str(e)}"
                allure.attach(msg, name = "Select Matches Error", attachment_type=allure.attachment_type.TEXT)
                raise Exception(msg)
    
    def select_doesnt_match(self):
        with allure.step("Select Doesn't Match"):
            try:
                doesnt_match_dropdown = self.wait.until(EC.presence_of_element_located((By.XPATH, "//button[@id='validation_option']")))
                highlight_element(self.driver, doesnt_match_dropdown)
                doesnt_match_dropdown.click()
                time.sleep(1)

                doesnt_match_btn = self.wait.until(EC.presence_of_element_located((By.XPATH, '//div[text()="Doesn\'t match"]')))
                highlight_element(self.driver, doesnt_match_btn)
                doesnt_match_btn.click()

                enter_value = self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Enter value']")))
                highlight_element(self.driver, enter_value)
                enter_value.click()
                enter_value.send_keys(1)
                time.sleep(1)
        
            except Exception as e:
                msg = f"failed to Select Doesnt match: {str(e)}"
                allure.attach(msg, name = "Select Doesnt Match Error", attachment_type=allure.attachment_type.TEXT)
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
        