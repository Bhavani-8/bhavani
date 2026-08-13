import allure
import time
import os
import json
import random
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from utilities.other_utils_functions.highlight import highlight_element
from selenium.webdriver.common.keys import Keys


class EditCompanyTask:

    def __init__(self, driver, wait):
        self.driver = driver
        self.wait = wait
        self.load_locators()

    def load_locators(self):
        try:
            with open(os.path.join("data", "locators.json"), "r") as f:
                locators = json.load(f)
            self.audit_icon = locators["audit_icon"]

        except FileNotFoundError as e:
            allure.attach(str(e),name="Locators File Missing",attachment_type=allure.attachment_type.TEXT)
            raise
        
        except json.JSONDecodeError as e:
            allure.attach(str(e),name="Invalid JSON",attachment_type=allure.attachment_type.TEXT)
            raise


    def click_audit(self):
        with allure.step("Click Audit"):
            try:
                audit_btn = self.wait.until(EC.presence_of_element_located((By.XPATH, self.audit_icon)))
                highlight_element(self.driver, audit_btn)
                audit_btn.click()
            except Exception as e:
                msg = f"Failed to click Audit Icon: {str(e)}"
                allure.attach(msg, name = "Audit Icon Error", attachment_type = allure.attachment_type.TEXT)
                raise Exception(msg)

    def click_company(self):
        with allure.step("Click Company"):
            try:
                audit_company_btn = self.wait.until(EC.presence_of_element_located((By.XPATH, "//span[text() = 'Company']")))
                highlight_element(self.driver, audit_company_btn)
                audit_company_btn.click()
            except Exception as e:
                msg = f"Failed to click Company button: {str(e)}"
                allure.attach(msg, name = 'Audit Company Error', attachment_type = allure.attachment_type.TEXT)
                raise Exception(msg)

    def click_edit_btn(self):
        with allure.step("Click Edit Button"):
            try:
                company_file = os.path.join("latest_data", "audit_company.txt")
                with open(company_file, "r") as f:
                    created_company_name = f.read().strip()
                company_edit_btn = self.wait.until(EC.presence_of_element_located((By.XPATH, f"(//tr[.//td[translate(normalize-space(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz') =translate('{created_company_name}', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz')]]//button[1])[1]")))
                highlight_element(self.driver, company_edit_btn)
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", company_edit_btn)
                company_edit_btn.click()

            except Exception as e:
                msg = f"Failed to click Assign button: {str(e)}"
                allure.attach(msg, name = 'Assign Button Error', attachment_type = allure.attachment_type.TEXT)
                raise Exception(msg)

    def edit_company_name(self):
        with allure.step("Edit Company name"):
            try:
                company_name = self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@name='company_name']")))
                highlight_element(self.driver, company_name)
                old_company_name = company_name.get_attribute("value").strip()
                company_name.click()
                company_name.send_keys(Keys.CONTROL, "a")
                company_name.send_keys(Keys.BACKSPACE)
                new_company_name = f"Test Audit {random.randint(1000, 9999)}"
                company_name.send_keys(new_company_name)
                expected_company_name = company_name.get_attribute("value").strip()

                allure.attach(
                    f"Old Company Name : {old_company_name}\n"
                    f"New Company Name : {expected_company_name}",
                    name="Company Name Edited",attachment_type=allure.attachment_type.TEXT)

                return expected_company_name
            except Exception as e:
                msg = f"Failed to Edit Company name: {str(e)}"
                allure.attach(msg, name = 'Edit Company Error', attachment_type = allure.attachment_type.TEXT)
                raise Exception(msg)

    def submit_button(self):
        with allure.step("Click Submit Button"):
            try:
                submit_button = self.wait.until(EC.presence_of_element_located((By.XPATH, "//button[@type='submit']")))
                highlight_element(self.driver, submit_button)
                submit_button.click()
                time.sleep(2)
            except Exception as e:
                msg = f"failed to click submit button: {str(e)}"
                allure.attach(msg, name = "Submit button Error", attachment_type=allure.attachment_type.TEXT)
                raise Exception(msg)

    def validate_new_company(self, expected_company_name):
        with allure.step("Validate Company name"):
            try:
                actual_company = self.wait.until(EC.presence_of_element_located((By.XPATH, f"//tr[.//td[normalize-space()='{expected_company_name}']]//td[2]")))
                self.driver.execute_script("arguments[0].scrollIntoView({inline: 'start'});",actual_company)
                highlight_element(self.driver, actual_company)
                actual_company_name = actual_company.text.strip()
                if expected_company_name == actual_company_name:
                    allure.attach(
                        f"Expected : {expected_company_name}\n"
                        f"Actual   : {actual_company_name}\n",
                        name="Company Name - PASS",attachment_type=allure.attachment_type.TEXT)
                    return True

                else:
                    allure.attach(
                        f"Expected : {expected_company_name}\n"
                        f"Actual   : {actual_company_name}\n",
                        name="Company Name - FAIL",attachment_type=allure.attachment_type.TEXT)
                    return False

            except Exception as e:
                allure.attach(
                    f"Expected : {expected_company_name}\n"
                    f"Actual   : Not Found\n",name="Company Name - FAIL",attachment_type=allure.attachment_type.TEXT)

                return False


    def edit_company(self):

        self.click_audit()
        self.click_company()
        self.click_edit_btn()

        expected_company_name = self.edit_company_name()

        self.submit_button()

        validation_result = self.validate_new_company(expected_company_name)

        assert validation_result, "Company name validation failed"
        return True