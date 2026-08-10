import allure
import time
import os
import json
import random
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from utilities.other_utils_functions.highlight import highlight_element


class CreateTemplate:

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

    def update_template_btn(self):
        with allure.step("Click Update Template Button"):
            try:
                template_file = os.path.join("latest_data", "latest_template.txt")
                with open(template_file, "r") as f:
                    created_template_name = f.read().strip()
                update_template_elem = self.wait.until(EC.presence_of_element_located((By.XPATH, f"//tr[.//*[contains(normalize-space(),'{created_template_name}')]]//button[.//*[contains(@class,'lucide-pencil')]]")))
                highlight_element(self.driver, update_template_elem)
                update_template_elem.click()
            except Exception as e:
                msg = f"Failed to click Update Template button: {str(e)}"
                allure.attach(msg, name ="Update Template button Error", attachment_type=allure.attachment_type.TEXT)
                raise Exception(msg)
       
    def enter_template_name(self):
        with allure.step("Click Add Section"):
            try:
                question_section = self.wait.until(EC.presence_of_element_located((By.XPATH, "//button[normalize-space()='Section']")))
                highlight_element(self.driver, question_section)
                question_section.click()
                time.sleep(1)
            except Exception as e:
                msg = f"failed to Enter Template name: {str(e)}"
                allure.attach(msg, name = "Template name Error", attachment_type=allure.attachment_type.TEXT)
                raise Exception(msg) 

    def enter_template_name(self):
        with allure.step("Enter Template Details"):
            try:
                unique_questionnaire_name = f"Test Automation Question {random.randint(1000, 9999)}"
                question_section = self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@id='checklist_section']")))
                highlight_element(self.driver, question_section)
                question_section.send_keys(unique_questionnaire_name)
                template_file = os.path.join("latest_data", "latest_template.txt")
                with open(template_file, "w") as f:
                    f.write(unique_questionnaire_name)
            except Exception as e:
                msg = f"failed to Enter Template name: {str(e)}"
                allure.attach(msg, name = "Template name Error", attachment_type=allure.attachment_type.TEXT)
                raise Exception(msg) 
            
    def enter_duration(self):
        with allure.step("Enter Duration"):
            try:
                enter_duration_num = self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@id='duration_of_completion']")))
                highlight_element(self.driver, enter_duration_num)
                enter_duration_num.send_keys("4")
                allure.attach(enter_duration_num.get_attribute("value"),name="Enter Duration",attachment_type=allure.attachment_type.TEXT)
            except Exception as e:
                msg = f"failed to Enter Duration name: {str(e)}"
                allure.attach(msg, name = "Duration name Error", attachment_type=allure.attachment_type.TEXT)
                raise Exception(msg) 

    def enter_buffer(self):
        with allure.step("Enter Buffer Duration"):
            try:
                enter_buffer_num = self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@name='buffer_period']")))
                highlight_element(self.driver, enter_buffer_num)
                enter_buffer_num.send_keys("1")
                allure.attach(enter_buffer_num.get_attribute("value"),name="Enter Buffer",attachment_type=allure.attachment_type.TEXT)
            except Exception as e:
                msg = f"failed to Enter Buffer name: {str(e)}"
                allure.attach(msg, name = "Enter Buffer name Error", attachment_type=allure.attachment_type.TEXT)
                raise Exception(msg) 

    def document_file(self):
        with allure.step("Attach PDF Document File"):
            try:
                drag_document_file = self.wait.until(EC.presence_of_element_located((By.XPATH, "//p[text()='Guidelines Documents from Regulators']/preceding-sibling::input[@type='file']")))
                highlight_element(self.driver, drag_document_file)
                # drag_document_file.click()
                first_file_path = os.path.abspath(os.path.join("data", "dummy_use_file.pdf"))
                drag_document_file.send_keys(first_file_path)
                time.sleep(3)
                print(f"📤 First file selected: {first_file_path}")
            except Exception as e:
                msg = f"failed to Attach PDF Document File: {str(e)}"
                allure.attach(msg, name = "Attach PDF Document File Error", attachment_type=allure.attachment_type.TEXT)
                raise Exception(msg)

    def add_attachment_file(self):
        with allure.step("Attach Word Documant File"):
            try:
                drag_attachment_file = self.wait.until(EC.presence_of_element_located((By.XPATH, "//p[text()='Add Attachments']/preceding-sibling::input[@type='file']")))
                highlight_element(self.driver, drag_attachment_file)
                # drag_attachment_file.click()
                second_file_path = os.path.abspath(os.path.join("data", "impact_file.docx"))
                drag_attachment_file.send_keys(second_file_path)
                time.sleep(3)
                print(f"📤 First file selected: {second_file_path}")
            except Exception as e:
                msg = f"failed to Attach Word Document File: {str(e)}"
                allure.attach(msg, name = "Attach Word Document File Error", attachment_type=allure.attachment_type.TEXT)
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
                toast = self.wait.until(EC.visibility_of_element_located((By.XPATH, self.toast_msg)))
                highlight_element(self.driver, toast)
                toast_text = toast.text.strip()
                print(f"📢 Toast message: {toast.text.strip()}")
                allure.attach(toast_text, name = "Toast Message Error", attachment_type=allure.attachment_type.TEXT)
                time.sleep(7)
            except Exception as e:
                msg = f"Toast message not found: {str(e)}"
                print(msg)
                allure.attach(str(e), name="Toast message Error", attachment_type=allure.attachment_type.TEXT)
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

    def validate_all_details(self,expected_template_name):
        with allure.step("Validate Created Template"):
            try:
                actual_template = self.wait.until(EC.presence_of_element_located((By.XPATH, f"//td[normalize-space()='{expected_template_name}']")))
                highlight_element(self.driver, actual_template)
                actual_template_name = actual_template.text.strip()
                print(f"Expected Template : {expected_template_name}")
                print(f"Actual Template   : {actual_template_name}")
                if expected_template_name == actual_template_name:
                    result = (
                        "TEMPLATE CREATED SUCCESSFULLY\n\n"
                        f"Expected : {expected_template_name}\n"
                        f"Actual   : {actual_template_name}\n\n"
                    )
                else:
                    result = (
                        "TEMPLATE VALIDATION FAILED\n\n"
                        f"Expected : {expected_template_name}\n"
                        f"Actual   : {actual_template_name}\n\n"
                    )

                allure.attach(result,name="Template Validation",attachment_type=allure.attachment_type.TEXT)

                assert expected_template_name == actual_template_name, result
            except Exception as e:
                msg = f"Validation Failed: {str(e)}"
                allure.attach(msg,name="Validation Error",attachment_type=allure.attachment_type.TEXT,)
                raise Exception(msg)
    

    def create_template(self):
        self.click_audit()
        self.template_btn()

        # Create template and store its name
        self.update_template_btn()
        self.enter_template_name()
        self.enter_buffer()
        self.document_file()
        self.add_attachment_file()
        self.save_button()
        self.done_button()

       
        
        

        return True

                
