import allure
import time
import os
import json
import random
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from utilities.other_utils_functions.highlight import highlight_element
from selenium.webdriver.common.keys import Keys


class CreateAssignment:

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

    def scroll_to_element(self, element):
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center', behavior:'smooth'});",element)
        time.sleep(0.3)
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

    def click_assignment_btn(self):
        with allure.step("Click Create Audit Assignment"):
            try:
                template_file = os.path.join("latest_data", "latest_template.txt")
                with open(template_file, "r") as f:
                    created_template_name = f.read().strip()
                audit_assign = self.wait.until(EC.presence_of_element_located((By.XPATH, f"//div[contains(@class,'overflow-hidden') and normalize-space()='{created_template_name}']/following::button[3]")))
                highlight_element(self.driver, audit_assign)
                audit_assign.click()

            except Exception as e:
                msg = f"Failed to click Assign button: {str(e)}"
                allure.attach(msg, name = 'Assign Button Error', attachment_type = allure.attachment_type.TEXT)
                raise Exception(msg)
    def fetch_audit_template(self):
        with allure.step("Fetch Audit Template name"):
            try:
                audit_template = self.wait.until(EC.visibility_of_element_located((By.XPATH, "(//span[@class='flex flex-1 text-left'])[1]")))
                highlight_element(self.driver, audit_template)
                expected_template_name = audit_template.text.strip()
                print(f"Fetched Template name : {expected_template_name}")
                allure.attach(expected_template_name, name = "Audit Template", attachment_type=allure.attachment_type.TEXT)
            except Exception as e:
                msg = f"Failed to Fetch Assign Template: {str(e)}"
                allure.attach(msg, name = 'Assign Template Error', attachment_type = allure.attachment_type.TEXT)
                raise Exception(msg)

    def enter_audit_name(self):
        with allure.step("Enter Template Details"):
            try:
                audit_name = self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Enter name']")))
                highlight_element(self.driver, audit_name)
                unique_audit_name = f"Audit Name {random.randint(1000, 9999)}"
                audit_name.send_keys(unique_audit_name)
                expected_audit_name = audit_name.get_attribute("value").strip()
                print(f"Expected Audit: {expected_audit_name}")
                allure.attach(expected_audit_name,name="Audit Name",attachment_type=allure.attachment_type.TEXT)
                return expected_audit_name
            except Exception as e:
                msg = f"failed to Enter Audit name: {str(e)}"
                allure.attach(msg, name = "Audit name Error", attachment_type=allure.attachment_type.TEXT)
                raise Exception(msg) 
        

    def enter_start_date(self):
        with allure.step("Enter Start Date"):
            try:
                start_date = self.wait.until(EC.presence_of_element_located((By.XPATH, "//button[@aria-label='Select date']")))
                highlight_element(self.driver, start_date)
                start_date.click()
                time.sleep(1)

                today_btn = self.wait.until(EC.presence_of_element_located((By.XPATH, "//button[text() = 'Today']")))
                highlight_element(self.driver, today_btn)
                today_btn.click()
                time.sleep(0.5)

                selected_date = self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@name='start_date']")))
                date_value = selected_date.text.strip()
                print(f"Selected Start Date: {date_value}")
                allure.attach(date_value,name="Selected Start Date",attachment_type=allure.attachment_type.TEXT)
            except Exception as e:
                msg = f"failed to click Today Button: {str(e)}"
                allure.attach(msg, name = "Today button Error", attachment_type=allure.attachment_type.TEXT)
                raise Exception(msg) 
    def click_company_name(self):
        with allure.step("Select Company name"):
            try:
                company_droprdown = self.wait.until(EC.presence_of_element_located((By.XPATH, "(//button[@role='combobox' and .//span[normalize-space()='--Select--']])[1]")))
                company_droprdown.click()
                time.sleep(2)
                company_file = os.path.join("latest_data", "audit_company.txt")
                with open(company_file, "r") as f:
                    created_company_name = f.read().strip()
                company_name = self.wait.until(EC.presence_of_element_located((By.XPATH, f"//div[contains(@class,'whitespace-normal') and text()='{created_company_name}']")))
                highlight_element(self.driver, company_name)
                company_name.click()
                expected_company_name = company_name.get_attribute("value").strip()
                print(f"Company Name: {expected_company_name}")
                time.sleep(1)
                allure.attach(company_name.text, name='Company Name', attachment_type=allure.attachment_type.TEXT)
                    
            except Exception as e:
                msg = f"failed to Select Company Name: {str(e)}"
                allure.attach(msg, name = "Company Name Error", attachment_type=allure.attachment_type.TEXT)
                raise Exception(msg)

    def click_branch_name(self):
        with allure.step("Select Branch name"):
            try:
                branch_droprdown = self.wait.until(EC.presence_of_element_located((By.XPATH, "(//button[@role='combobox' and .//span[normalize-space()='--Select--']])[1]")))
                branch_droprdown.click()
                time.sleep(2)
                
                branch_name = self.wait.until(EC.visibility_of_element_located((By.XPATH, f"//div[contains(@class,'whitespace-normal') and normalize-space()='Automation location - Test Audit 76']")))
                self.scroll_to_element(branch_name)
                highlight_element(self.driver, branch_name)
                self.driver.execute_script("arguments[0].click();",branch_name)
                expected_branch_name = branch_name.text.strip()
                print(f"Expected Branch name : {expected_branch_name}")
                time.sleep(2)
                allure.attach(branch_name.text.strip(), name='Branch Name', attachment_type=allure.attachment_type.TEXT)         
            except Exception as e:
                msg = f"failed to Select Branch Name: {str(e)}"
                allure.attach(msg, name = "Branch Name Error", attachment_type=allure.attachment_type.TEXT)
                raise Exception(msg) 

    def branch_manager_email(self):
        with allure.step("Fecth Branch manager email"):
            try:
                manager_email = self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@name='manager_email']")))
                self.scroll_to_element(manager_email)
                manager_email_value = manager_email.text.strip()
                print(f"Manager Email: {manager_email_value}")
                allure.attach(manager_email_value, name = 'Manager Email', attachment_type=allure.attachment_type.TEXT)
            except Exception as e:
                msg = f"failed to Fetch Manager email: {str(e)}"
                allure.attach(msg, name = "Manager email Error", attachment_type=allure.attachment_type.TEXT)
                raise Exception(msg) 
    def branch_manager_name(self):
        with allure.step("Fecth Branch manager email"):
            try:
                manager_name = self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@name='manager_name']")))
                self.scroll_to_element(manager_name)
                expected_manager_name = manager_name.text.strip()
                print(f"Manager Name: {expected_manager_name}")
                allure.attach(expected_manager_name, name = 'Manager Name', attachment_type=allure.attachment_type.TEXT)
            except Exception as e:
                msg = f"failed to Fetch Manager name: {str(e)}"
                allure.attach(msg, name = "Manager name Error", attachment_type=allure.attachment_type.TEXT)
                raise Exception(msg) 

    def head_of_auditor_email(self):
        with allure.step("Enter Email Id"):
            try:
                enter_email_id = self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@name='auditor_email_id']")))
                self.scroll_to_element(enter_email_id)
                highlight_element(self.driver, enter_email_id)
                unique_auditor_email = f"testhead{random.randint(100, 999)}@gmail.com" 
                enter_email_id.send_keys(unique_auditor_email)
                expected_enter_email_id = enter_email_id.get_attribute("value").strip()
                print(f"Expected Email ID: {expected_enter_email_id}")
                allure.attach(expected_enter_email_id, name='Email Id', attachment_type=allure.attachment_type.TEXT)
                return expected_enter_email_id
            except Exception as e:
                msg = f"failed to Enter Email Id: {str(e)}"
                allure.attach(msg, name = "Enter Email Id Error", attachment_type=allure.attachment_type.TEXT)
                raise Exception(msg)

    def head_of_auditor_name(self):
        with allure.step("Enter Head of Auditor name"):
            try:
                enter_name = self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@name='auditor_name']")))
                highlight_element(self.driver, enter_name)
                unique_auditor_name = f"Audit Name {random.randint(1000, 9999)}"
                enter_name.send_keys(unique_auditor_name)
                expected_enter_name = enter_name.get_attribute("value").strip()
                print(f"Expected Enter name: {expected_enter_name}")
                allure.attach(expected_enter_name, name='Auditor name', attachment_type=allure.attachment_type.TEXT)
                return expected_enter_name
            except Exception as e:
                msg = f"failed to Enter Auditor name: {str(e)}"
                allure.attach(msg, name = "Enter Auditor name Error", attachment_type=allure.attachment_type.TEXT)
                raise Exception(msg)

    def click_contact_number(self):
        with allure.step("Enter Contact Number"):
            try:
                unique_contact_number = f"987{random.randint(1000000, 9999999)}"
                contact_number = self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Enter mobile number']")))
                self.scroll_to_element(contact_number)
                highlight_element(self.driver, contact_number)
                contact_number.send_keys(unique_contact_number)
                expected_contact_number = contact_number.get_attribute("value").strip() 
                print(f"Expected Contact  :{expected_contact_number}")
                allure.attach(expected_contact_number,name="Contact Number",attachment_type=allure.attachment_type.TEXT)
                return expected_contact_number
            except Exception as e:
                msg = f"failed to Enter Mobile Number : {str(e)}"
                allure.attach(msg, name = "Moible number Error", attachment_type=allure.attachment_type.TEXT)
                raise Exception(msg)
    
    def click_save_button(self):
        with allure.step("Click save Button"):
            try:
                save_button = self.wait.until(EC.presence_of_element_located((By.XPATH, "//button[text()='Save']")))
                highlight_element(self.driver, save_button)
                save_button.click()
            
            except Exception as e:
                msg = f"failed to click save button : {str(e)}"
                allure.attach(msg, name = "Save Button Error", attachment_type=allure.attachment_type.TEXT)
                raise Exception(msg)

    def validate_assignment_details(self, expected_template_name, expected_audit_name, expected_manager_name, expected_company_name,
        expected_enter_name, expected_branch_name):
        with allure.step("Validate Created company details"):
            try:
                actual_template_name = self.wait.until(EC.presence_of_element_located((By.XPATH, f"//td[contains(normalize-space(),'{expected_company_name}')]")))
                time.sleep(0.5)
                highlight_element(self.driver, actual_template_name)
                actual_template = actual_template_name.text.strip()
                print(f"expected_template_name     : {expected_template_name}")
                print(f"Actual Template Name       : {actual_template}")
                # self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", actual_company_name)
                actual_audit_name = self.wait.until(EC.presence_of_element_located((By.XPATH, f"//td[normalize-space()='{expected_enter_name}']/ancestor::tr//td[normalize-space()='{expected_audit_name}']")))
                highlight_element(self.driver, actual_audit_name)
                actual_audit = actual_audit_name.text.strip()
                print(f"Expected Register ID      : {expected_audit_name}")
                print(f"Actual Register ID        : {actual_audit}")

                actual_manager_name = self.wait.until(EC.presence_of_element_located((By.XPATH, f"//tr[.//td[normalize-space()='{expected_company_name}']]//td[normalize-space()='{expected_manager_name}']")))
                highlight_element(self.driver, actual_manager_name)
                actual_manager = actual_manager_name.text.strip()
                print(f"Expected Company Category : {expected_manager_name}")
                print(f"Actual Company Category   : {actual_manager}")

                actual_head_auditor_name = self.wait.until(EC.presence_of_element_located((By.XPATH, f"//tr[.//td[normalize-space()='{expected_company_name}']]//td[normalize-space()='{expected_enter_name}']")))
                highlight_element(self.driver, actual_head_auditor_name)
                actual_head_auditor = actual_head_auditor_name.text.strip()
                print(f"Expected Email ID         : {expected_enter_name}")
                print(f"Actual Email ID           : {actual_head_auditor}")

                actual_company = self.wait.until(EC.presence_of_element_located((By.XPATH, f"//td[contains(normalize-space(),'{expected_company_name}')]")))
                time.sleep(0.5)
                highlight_element(self.driver, actual_company)
                actual_company_name = actual_company.text.strip()
                print(f"Expected Company Name     : {expected_company_name}")
                print(f"Actual Company Name       : {actual_company_name}")

                actual_location_name = self.wait.until(EC.presence_of_element_located((By.XPATH, f"//tr[.//td[normalize-space()='{expected_company_name}']]//td[normalize-space()='{expected_branch_name}']")))
                highlight_element(self.driver, actual_location_name)
                actual_location_name_text = actual_location_name.text.strip()
                print(f"Expected Contact Number   : {expected_branch_name}")
                print(f"Actual Contact Number     : {actual_location_name_text}")                

                # Validate all details
                all_matched = (
                    expected_company_name == actual_company_name
                    and expected_template_name == actual_template
                    and expected_audit_name == actual_audit
                    and expected_manager_name == actual_manager
                    and expected_enter_name == actual_head_auditor
                    and expected_branch_name == actual_location_name_text
                )
                if all_matched:
                    result = (
                        "AUDIT COMPANY CREATED SUCCESSFULLY\n\n"
                        f"Company Name     : {expected_company_name} == {actual_company_name}\n"
                        f"Register ID      : {expected_template_name} == {actual_template}\n"
                        f"Company Category : {expected_audit_name} == {actual_audit}\n"
                        f"Email ID         : {expected_manager_name} == {actual_manager}\n"
                        f"Contact Number   : {expected_enter_name} == {actual_head_auditor}\n"
                        f"Branch Name       : {expected_branch_name} == {actual_location_name_text}\n"
                    )
                else:
                    result = (
                        "AUDIT COMPANY VALIDATION FAILED\n\n"
                        f"Company Name     : {expected_company_name} == {actual_company_name}\n"
                        f"Register ID      : {expected_template_name} == {actual_template}\n"
                        f"Company Category : {expected_audit_name} == {actual_audit}\n"
                        f"Email ID         : {expected_manager_name} == {actual_manager}\n"
                        f"Contact Number   : {expected_enter_name} == {actual_head_auditor}\n"
                        f"Branch Name       : {expected_branch_name} == {actual_location_name_text}\n"
                    )
                allure.attach(result,name="Audit Company Validation",attachment_type=allure.attachment_type.TEXT)

                assert all_matched, result
            except Exception as e:
                msg = f"Validation Failed: {str(e)}"
                allure.attach(msg,name="Validation Error",attachment_type=allure.attachment_type.TEXT,)
                raise Exception(msg)
                        
    def create_audit_assignment(self):
        self.click_audit()
        self.template_btn()
        self.click_assignment_btn()
        self.fetch_audit_template()
        self.enter_audit_name()
        self.enter_start_date()
        self.click_company_name()
        self.click_branch_name()
        self.branch_manager_email()
        self.branch_manager_name()
        self.head_of_auditor_email()
        self.head_of_auditor_name()
        self.click_contact_number()
        self.click_save_button()
        

        return True

                
