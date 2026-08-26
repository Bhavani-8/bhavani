import allure
import time
import random
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from utilities.other_utils_functions.highlight import highlight_element


class QuestionnaireShortAnswer:

    def __init__(self, driver, wait):
        self.driver = driver
        self.wait = wait


    def add_short_answer(self):
        with allure.step("Short Answer Without Validation"):
            try:
                unique_short = "Test Automation Short Answer Without Validation"
                enter_short_answer = self.wait.until(EC.presence_of_element_located((By.XPATH, "//textarea[@placeholder='Enter your question here...']")))
                highlight_element(self.driver, enter_short_answer)
                enter_short_answer.click()
                enter_short_answer.send_keys(unique_short)
            except Exception as e:
                msg = f"Failed to Enter Short Answer Without validation: {str(e)}"
                allure.attach(msg,name="Short Answer without validation Error",attachment_type=allure.attachment_type.TEXT)
                raise Exception(msg)

    def validation_short_answer(self):
        with allure.step("Short Answer Section Validation"):
            try:
                short_question = "Test Automation Short Answer Validation"
                val_short = self.wait.until(EC.presence_of_element_located((By.XPATH, "//textarea[@placeholder='Enter your question here...']")))
                highlight_element(self.driver, val_short)
                val_short.click()
                val_short.send_keys(short_question)
            except Exception as e:
                msg = f"Failed to Enter Short Answer Section validation: {str(e)}"
                allure.attach(msg,name="Short Answer Section validation Error",attachment_type=allure.attachment_type.TEXT)
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
                enter_max_count.click()
        
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
                enter_min_count.click()
        
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
        with allure.step("Select Contains"):
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
                enter_value.send_keys(1)
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

    def select_number(self):
        with allure.step("Select Number"):
            try:
                number_dropdown = self.wait.until(EC.presence_of_element_located((By.XPATH, "//button[@id='validation_type']")))
                highlight_element(self.driver, number_dropdown)
                number_dropdown.click()
                time.sleep(1)

                number_btn = self.wait.until(EC.presence_of_element_located((By.XPATH, "//div[text()='Number']")))
                highlight_element(self.driver, number_btn)
                number_btn.click()
        
            except Exception as e:
                msg = f"failed to Select Number: {str(e)}"
                allure.attach(msg, name = "Select Number Error", attachment_type=allure.attachment_type.TEXT)
                raise Exception(msg)

    def select_all_validation_types(self, validation_types=None):

        if validation_types is None:
            validation_types = [
                "Greater than", "Greater than or equal to", "Less than", "Less than or equal to",
                "Equal to", "Not equal to", "Is number", "Whole number", "Between"
            ]

        with allure.step(f"Select validation types: {validation_types}"):
            try:
                for validation_type in validation_types:

                    validation_dropdown = self.wait.until(EC.presence_of_element_located((By.XPATH, "//button[@id='validation_option']")))
                    highlight_element(self.driver, validation_dropdown)
                    validation_dropdown.click()
                    time.sleep(1)

                    validation_option = self.wait.until(EC.presence_of_element_located((By.XPATH, f"//div[text()='{validation_type}']")))
                    validation_option = self.scroll_to_option_with_arrow_keys(validation_option)
                    highlight_element(self.driver, validation_option)
                    validation_option.click()

                    if validation_type in ["Is number", "Whole number"]:
                        time.sleep(1)
                        continue

                    elif validation_type == "Between":
                        from_value = self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='From']")))
                        highlight_element(self.driver, from_value)
                        from_value.send_keys("50")

                        to_value = self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Enter max size']")))
                        highlight_element(self.driver, to_value)
                        to_value.send_keys("100")

                    else:
                        enter_value = self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Enter value']")))
                        highlight_element(self.driver, enter_value)
                        enter_value.click()
                        enter_value.send_keys("1")

                    time.sleep(1)

            except Exception as e:
                msg = f"Failed to select validation types: {str(e)}"
                allure.attach(msg,name="Validation Types Error",attachment_type=allure.attachment_type.TEXT)
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
        