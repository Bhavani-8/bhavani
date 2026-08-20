import allure
import time
import os
import json
import random
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from utilities.other_utils_functions.highlight import highlight_element


class EditTemplate:

    def __init__(self, driver, wait):
        self.driver = driver
        self.wait = wait
        self.load_locators()

    def load_locators(self):
        try:
            with open(os.path.join("data", "locators.json"), "r") as f:
                locators = json.load(f)
            self.audit_icon = locators["audit_icon"]
            self.toast_msg = locators["toast_msg"]
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

    def template_btn(self):
        with allure.step("Click Template Button"):
            try:
                click_template_btn = self.wait.until(EC.presence_of_element_located((By.XPATH, "//span[text() ='Templates']")))
                highlight_element(self.driver, click_template_btn)
                click_template_btn.click()
            except Exception as e:
                msg = f"Failed to click Template button: {str(e)}"
                allure.attach(msg, name = 'Template Error', attachment_type = allure.attachment_type.TEXT)
                raise Exception(msg)

    def edit_template_btn(self):
        with allure.step("Click Edit Template Button"):
            try:
                template_file = os.path.join("latest_data", "latest_template.txt")
                with open(template_file, "r") as f:
                    created_template_name = f.read().strip()
                edit_template_elem = self.wait.until(EC.presence_of_element_located((By.XPATH, f"//tr[.//*[contains(normalize-space(),'{created_template_name}')]]//button[.//*[contains(@class,'lucide-pencil')]]")))
                highlight_element(self.driver, edit_template_elem)
                edit_template_elem.click()
            except Exception as e:
                msg = f"Failed to click Edit Template button: {str(e)}"
                allure.attach(msg, name ="Edit Template button Error", attachment_type=allure.attachment_type.TEXT)
                raise Exception(msg)
       

    def edit_inside_template(self):
        with allure.step("Click Inside Edit Template"):
            try:
                edit_inside_template_btn = self.wait.until(EC.presence_of_element_located((By.XPATH, "//button[@data-slot='drawer-trigger']")))
                highlight_element(self.driver, edit_inside_template_btn)
                edit_inside_template_btn.click()
                time.sleep(0.5)
            except Exception as e:
                msg = f"Failed to click edit inside template button: {str(e)}"
                allure.attach(msg, name = "Edit button Error", attachment_type=allure.attachment_type.TEXT)
                raise Exception(msg)
            

    def enter_template_name(self):
        with allure.step("Enter Template Details"):
            try:
                template_name = self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Enter template name']")))
                highlight_element(self.driver, template_name)
                unique_template_name = f"Compliance Template {random.randint(1000, 9999)}"
                template_name.clear()
                template_name.send_keys(unique_template_name)
                template_file = os.path.join("latest_data", "latest_template.txt")
                with open(template_file, "w") as f:
                    f.write(unique_template_name)
                expected_template_name = template_name.get_attribute("value").strip()
                print(f"Expected Template: {expected_template_name}")
                allure.attach(expected_template_name,name="Template Name",attachment_type=allure.attachment_type.TEXT)
                return expected_template_name
            except Exception as e:
                msg = f"failed to Enter Template name: {str(e)}"
                allure.attach(msg, name = "Template name Error", attachment_type=allure.attachment_type.TEXT)
                raise Exception(msg) 

    def save_button(self):
        with allure.step("Click Save Button"):
            try:
                save_button = self.wait.until(EC.presence_of_element_located((By.XPATH, "//button[text()='Save']")))
                highlight_element(self.driver, save_button)
                save_button.click()
                time.sleep(1)
            except Exception as e:
                msg = f"failed to click save button: {str(e)}"
                allure.attach(msg, name = "Save button Error", attachment_type=allure.attachment_type.TEXT)
                raise Exception(msg)

            try:
                continue_btn = self.wait.until(EC.visibility_of_element_located((By.XPATH, "//button[text()='Continue']")))
                highlight_element(self.driver, continue_btn)
                continue_btn.click()
                time.sleep(2)
            except Exception as e:
                msg = f"Continue Button not found: {str(e)}"
                print(msg)
                allure.attach(str(e), name="Continue Button Error", attachment_type=allure.attachment_type.TEXT)
                raise Exception(msg)

            try:
                toast = self.wait.until(EC.visibility_of_element_located((By.XPATH, self.toast_msg)))
                highlight_element(self.driver, toast)
                toast_text = toast.text.strip()
                print(f"📢 Toast message: {toast.text.strip()}")
                allure.attach(toast_text, name = "Toast Message", attachment_type=allure.attachment_type.TEXT)
                time.sleep(7)
            except Exception as e:
                msg = f"Toast message not found: {str(e)}"
                print(msg)
                allure.attach(str(e), name="Toast message Error", attachment_type=allure.attachment_type.TEXT)
                raise Exception(msg)

    def fetch_template_name(self):
        with allure.step("Fetch Template name"):
            try:
                fetch_template = self.wait.until(EC.visibility_of_element_located((By.XPATH, "//h2[contains(@class,'text-lg') and contains(@class,'font-semibold')]")))
                highlight_element(self.driver, fetch_template)
                expected_fetch_template = fetch_template.text.strip()
                print(f"Fetched Template name : {expected_fetch_template}")
                allure.attach(expected_fetch_template, name = "Fetch Template Name", attachment_type=allure.attachment_type.TEXT)
                return expected_fetch_template
            except Exception as e:
                msg = f"Failed to Fetch Template name: {str(e)}"
                allure.attach(msg, name = 'Fetch Template Error', attachment_type = allure.attachment_type.TEXT)
                raise Exception(msg)


    def done_button(self):
        with allure.step("Click Done Button"):
            try:
                done_button = self.wait.until(EC.presence_of_element_located((By.XPATH, "//button[text()='Done']")))
                highlight_element(self.driver, done_button)
                done_button.click()
                time.sleep(2)
            except Exception as e:
                msg = f"failed to click save button: {str(e)}"
                allure.attach(msg, name = "Save button Error", attachment_type=allure.attachment_type.TEXT)
                raise Exception(msg)


    def validate_updated_template_name(self, expected_fetch_template):
        with allure.step("Validate Updated Template name"):
            try:
                actual_template = self.wait.until(EC.presence_of_element_located((By.XPATH, f"//td[contains(normalize-space(),'{expected_fetch_template}')]")))
                highlight_element(self.driver, actual_template)
                actual_template_name = actual_template.text.strip()
                print(f"Expected Template : {expected_fetch_template}")
                print(f"Actual Template   : {actual_template_name}")
                if expected_fetch_template == actual_template_name:
                    result = (
                        "TEMPLATE CREATED SUCCESSFULLY\n\n"
                        f"Expected : {expected_fetch_template}\n"
                        f"Actual   : {actual_template_name}\n\n"
                    )
                else:
                    result = (
                        "TEMPLATE VALIDATION FAILED\n\n"
                        f"Expected : {expected_fetch_template}\n"
                        f"Actual   : {actual_template_name}\n\n"
                    )

                allure.attach(result,name="Template Validation",attachment_type=allure.attachment_type.TEXT)

                assert expected_fetch_template == actual_template_name, result
            except Exception as e:
                msg = f"Validation Failed: {str(e)}"
                allure.attach(msg,name="Validation Error",attachment_type=allure.attachment_type.TEXT,)
                raise Exception(msg)
    
    
    def edit_inside_template_name(self):
        self.click_audit()
        self.template_btn()
        self.edit_template_btn()
        self.edit_inside_template()
        self.enter_template_name()
        self.save_button()
        expected_template_name = self.fetch_template_name()
        self.done_button()
        self.validate_updated_template_name(expected_template_name,)
        

        return True

                
