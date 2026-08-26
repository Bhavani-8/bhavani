import allure
import time
import random
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from utilities.other_utils_functions.highlight import highlight_element


class QuestionnaireDropDownField:

    def __init__(self, driver, wait):
        self.driver = driver
        self.wait = wait

    def add_drop_down(self):
        with allure.step("Drop Down Section Without Validation"):
            try:
                unique_drop_down = "Test Automation Drop down Without Validation"
                enter_drop_down_section = self.wait.until(EC.presence_of_element_located((By.XPATH, "//textarea[@placeholder='Enter your question here...']")))
                highlight_element(self.driver, enter_drop_down_section)
                enter_drop_down_section.click()
                enter_drop_down_section.send_keys(unique_drop_down)
            except Exception as e:
                msg = f"Failed to Enter Drop Down Without Validation: {str(e)}"
                allure.attach(msg,name="Drop Down without validation Error",attachment_type=allure.attachment_type.TEXT)
                raise Exception(msg)

    def dropdown_options(self):
        
        try:
            unique_dropdown = "Test Dropdown1"
            enter_dropdown = self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Enter dropdown option']")))
            highlight_element(self.driver, enter_dropdown)
            enter_dropdown.click()
            enter_dropdown.send_keys(unique_dropdown)
            time.sleep(1)

            click_add_more = self.wait.until(EC.presence_of_element_located((By.XPATH, "//button[normalize-space()='Add More']")))
            highlight_element(self.driver, click_add_more)
            click_add_more.click()

            unique_dropdown2 = "Test Dropdown2"
            enter_dropdown2 = self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Enter dropdown option']")))
            highlight_element(self.driver, enter_dropdown2)
            enter_dropdown2.click()
            enter_dropdown2.send_keys(unique_dropdown2)
            time.sleep(1)
                
        except Exception as e:
            msg = f"Failed to Enter Dropdown': {str(e)}"
            allure.attach(msg, name="Enter Dropdown Error", attachment_type=allure.attachment_type.TEXT)
            raise Exception(msg) 

    def validation_drop_down(self):
        with allure.step("Drop Down Section Validation"):
            try:
                drop_down = "Test Automation Drop Down Validation"
                val_drop_down = self.wait.until(EC.presence_of_element_located((By.XPATH, "//textarea[@placeholder='Enter your question here...']")))
                highlight_element(self.driver, val_drop_down)
                val_drop_down.click()
                val_drop_down.send_keys(drop_down)
            except Exception as e:
                msg = f"Failed to Enter Drop down Section Validation: {str(e)}"
                allure.attach(msg,name="Drop Down Section Validation Error",attachment_type=allure.attachment_type.TEXT)
                raise Exception(msg)


     
        
    def select_at_least(self, at_least="3"):
    
        with allure.step("Select Length"):
            try:
                at_least_dropdown = self.wait.until(EC.presence_of_element_located((By.XPATH, "//button[@id='validation_type']")))
                highlight_element(self.driver, at_least_dropdown)
                at_least_dropdown.click()
                time.sleep(1)

                at_least_btn = self.wait.until(EC.presence_of_element_located((By.XPATH, "//div[text()='Select at least']")))
                highlight_element(self.driver, at_least_btn)
                at_least_btn.click()

                enter_num = self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Enter number']")))
                highlight_element(self.driver, enter_num)
                enter_num.click()
                enter_num.send_keys(at_least)
        
            except Exception as e:
                msg = f"failed to Select at least: {str(e)}"
                allure.attach(msg, name = "At least Error", attachment_type=allure.attachment_type.TEXT)
                raise Exception(msg)

    def select_at_most(self, at_most="3"):
    
        with allure.step("Select Length"):
            try:
                at_most_dropdown = self.wait.until(EC.presence_of_element_located((By.XPATH, "//button[@id='validation_type']")))
                highlight_element(self.driver, at_most_dropdown)
                at_most_dropdown.click()
                time.sleep(1)

                at_most_btn = self.wait.until(EC.presence_of_element_located((By.XPATH, "//div[text()='Select at most']")))
                highlight_element(self.driver, at_most_btn)
                at_most_btn.click()

                enter_num = self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Enter number']")))
                highlight_element(self.driver, enter_num)
                enter_num.click()
                enter_num.send_keys(at_most)
        
            except Exception as e:
                msg = f"failed to Select at most: {str(e)}"
                allure.attach(msg, name = "At most Error", attachment_type=allure.attachment_type.TEXT)
                raise Exception(msg)
    

    def select_exactly(self, exactly="3"):
        
        with allure.step("Select Exactly"):
            try:
                exactly_dropdown = self.wait.until(EC.presence_of_element_located((By.XPATH, "//button[@id='validation_type']")))
                highlight_element(self.driver, exactly_dropdown)
                exactly_dropdown.click()
                time.sleep(1)

                exactly_btn = self.wait.until(EC.presence_of_element_located((By.XPATH, "//div[text()='Select exactly']")))
                highlight_element(self.driver, exactly_btn)
                exactly_btn.click()

                enter_num = self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Enter number']")))
                highlight_element(self.driver, enter_num)
                enter_num.click()
                enter_num.send_keys(exactly)
        
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
        