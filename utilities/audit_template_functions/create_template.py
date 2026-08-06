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
                click_template_btn = self.wait.until(EC.presence_of_element_located((By.XPATH, "//span[text() = 'Templates']")))
                highlight_element(self.driver, click_template_btn)
                click_template_btn.click()
            except Exception as e:
                msg = f"Failed to click Template button: {str(e)}"
                allure.attach(msg, name = 'Template Error', attachment_type = allure.attachment_type.TEXT)
                raise Exception(msg)

    def click_create_template(self):
        with allure.step("Click Create Button"):
            try:
                create_template_btn = self.wait.until(EC.presence_of_element_located((By.XPATH, "//button[normalize-space()='New Company']")))
                highlight_element(self.driver, create_template_btn)
                create_template_btn.click()
            except Exception as e:
                msg = f"Failed to click Create Template button: {str(e)}"
                allure.attach(msg, name ="Create Template button Error", attachment_type=allure.attachment_type.TEXT)
                raise Exception(msg)
       
    def enter_template_name(self):
        with allure.step("Enter Template Details"):
            try:
                unique_template_name = f"Compliance Template {random.randint(1000, 9999)}"
                template_name = self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Enter template name']")))
                highlight_element(self.driver, template_name)
                template_name.send_keys(template_name)
                expected_template_name = unique_template_name.get_attribute("value").strip()
                print(f"Expected Company Name: {expected_template_name}")
                allure.attach(expected_template_name,name="Template Name",attachment_type=allure.attachment_type.TEXT)
                return expected_template_name
            except Exception as e:
                msg = f"failed to Enter Template name: {str(e)}"
                allure.attach(msg, name = "Template name Error", attachment_type=allure.attachment_type.TEXT)
                raise Exception(msg) 

    def audit_description(self):
        with allure.step("Enter Description name"):
            try:
                enter_description = self.wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='cursor-text min-h-24 bg-background']")))
                highlight_element(self.driver, enter_description)
                enter_description.send_keys("Test Description")
                allure.attach(enter_description,name="Company Name",attachment_type=allure.attachment_type.TEXT)
            except Exception as e:
                msg = f"failed to Enter Description name: {str(e)}"
                allure.attach(msg, name = "Description name Error", attachment_type=allure.attachment_type.TEXT)
                raise Exception(msg) 
            
    def enter_duration(self):
        with allure.step("Enter Duration"):
            try:
                enter_duration_num = self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@id='duration_of_completion']")))
                highlight_element(self.driver, enter_duration_num)
                enter_duration_num.send_keys("4")
                allure.attach(enter_duration_num,name="Enter Duration",attachment_type=allure.attachment_type.TEXT)
            except Exception as e:
                msg = f"failed to Enter Description name: {str(e)}"
                allure.attach(msg, name = "Description name Error", attachment_type=allure.attachment_type.TEXT)
                raise Exception(msg) 

    def enter_buffer(self):
        with allure.step("Enter Duration"):
            try:
                enter_buffer_num = self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@id='duration_of_completion']")))
                highlight_element(self.driver, enter_buffer_num)
                enter_buffer_num.send_keys("4")
                allure.attach(enter_buffer_num,name="Enter Buffer",attachment_type=allure.attachment_type.TEXT)
            except Exception as e:
                msg = f"failed to Enter Buffer name: {str(e)}"
                allure.attach(msg, name = "Enter Buffer name Error", attachment_type=allure.attachment_type.TEXT)
                raise Exception(msg) 

    def document_file(self):
        with allure.step("Add File"):
            try:
                drag_document_file = self.wait.until(EC.presence_of_element_located((By.XPATH, "//p[normalize-space()='Drag and drop your files here']")))
                highlight_element(self.driver, drag_document_file)
                drag_document_file.click()
                first_file_path = os.path.abspath(os.path.join("data", "dummy_use_file.pdf"))
                drag_document_file.send_keys(first_file_path)
                time.sleep(3)
                print(f"📤 First file selected: {first_file_path}")
            except Exception as e:
                msg = f"failed to Enter Buffer name: {str(e)}"
                allure.attach(msg, name = "Enter Buffer name Error", attachment_type=allure.attachment_type.TEXT)
                raise Exception(msg)


            
    def search_company_name(self):
        self.click_audit()
        self.click_company()
        company_name = self.fetch_company_name()
        self.search_company_name(company_name)
        

        return True

                
