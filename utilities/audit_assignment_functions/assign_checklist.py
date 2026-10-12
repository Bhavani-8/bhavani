import allure
import time
import os
import json
import random
import pandas as pd
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from utilities.other_utils_functions.highlight import highlight_element
from utilities.add_task_functions.wait_for_loader_to_disappear import wait_for_loader_to_disappear
from utilities.login_utils import login_check


class AssignChecklistForm:

    def __init__(self, driver, wait,  email_head, email_subauditee1, email_subauditee2, tm_user, tm_pswd):
        self.driver = driver
        self.wait = wait
        self.email_head = email_head
        self.email_subauditee1 = email_subauditee1
        self.email_subauditee2 = email_subauditee2
        self.tm_user = tm_user
        self.tm_pswd = tm_pswd
        self.load_locators()

    def load_locators(self):
        try:
            with open(os.path.join("data", "locators.json"), "r") as f:
                locators = json.load(f)
            self.audit_icon = locators["audit_icon"]
            self.logout_icon = locators["logout_icon"]
            self.settings_icon = locators["settings_icon"]

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

    def click_assignment(self):
        with allure.step("Click Assignment"):
            try:
                audit_assignment_btn = self.wait.until(EC.presence_of_element_located((By.XPATH, "//span[text() = 'Assignments']")))
                highlight_element(self.driver, audit_assignment_btn)
                audit_assignment_btn.click()
                time.sleep(2)
            except Exception as e:
                msg = f"Failed to click Assignment button: {str(e)}"
                allure.attach(msg, name = 'Audit Assignment Error', attachment_type = allure.attachment_type.TEXT)
                raise Exception(msg)

    def click_checklist_btn(self):
        with allure.step("Click Checklist Button"):
            try:
                latest_checklist = os.path.join("latest_data", "audit_file.txt")
                with open(latest_checklist, "r") as f:
                    created_latest_checklist = f.read().strip()
                checklist_btn = self.wait.until(EC.presence_of_element_located((By.XPATH, f"//tr[.//td[normalize-space()='{created_latest_checklist}']]//td[7]")))
                highlight_element(self.driver, checklist_btn)
                checklist_btn.click()
                time.sleep(3)
            except Exception as e:
                msg = f"Failed to click checklist button: {str(e)}"
                allure.attach(msg, name = 'Checklist Error', attachment_type = allure.attachment_type.TEXT)
                raise Exception(msg)

    def click_assign_checklist(self):
        with allure.step("Click Assign Checklist"):
            try:
                assign_checklist_btn = self.wait.until(EC.presence_of_element_located((By.XPATH, "//button[text()='Assign Checklist']")))
                highlight_element(self.driver, assign_checklist_btn)
                assign_checklist_btn.click()
                time.sleep(1)
            except Exception as e:
                msg = f"Failed to click Assign Checklist button: {str(e)}"
                allure.attach(msg, name = 'Assign Checklist Error', attachment_type = allure.attachment_type.TEXT)
                raise Exception(msg)

    def new_member(self):
            
        with allure.step("Enter Team Member"):
            try:
                enter_email = self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@id='manager_email']")))
                highlight_element(self.driver, enter_email)
                enter_email.click()
                enter_email.send_keys(self.email_head)
                allure.attach(f"Entered Manager Auditor Email: {self.email_head}",name='Enter Team Member',attachment_type=allure.attachment_type.TEXT)
            except Exception as e:
                msg = f"Failed to Enter Email: {str(e)}"
                allure.attach(msg, name = 'Email Error', attachment_type = allure.attachment_type.TEXT)
                raise Exception(msg)

            try:
                enter_email = self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@id='subordinates.0.email']")))
                highlight_element(self.driver, enter_email)
                enter_email.click()
                enter_email.send_keys(self.email_subauditee1)
                allure.attach(f"Entered Subordinate Auditor's Email ID 1: {self.email_subauditee1}",name='Enter Team Member',attachment_type=allure.attachment_type.TEXT)
                time.sleep(1)
            except Exception as e:
                msg = f"Failed to Enter Email: {str(e)}"
                allure.attach(msg, name = 'Email Error', attachment_type = allure.attachment_type.TEXT)
                raise Exception(msg)

            try:
                time.sleep(0.5)
                fetch_subauditee_name = self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@name='subordinates.0.name']")))
                highlight_element(self.driver, fetch_subauditee_name)
                self.assign_fetched_name = fetch_subauditee_name.get_attribute("value").strip()
                allure.attach(f"Fetched Sub-Auditee Name: {self.assign_fetched_name}",name="Fetched Subordinate Name",attachment_type=allure.attachment_type.TEXT)
                print(f"Fetched name: {self.assign_fetched_name}")
            except Exception as e:
                msg = f"Failed to fetch subordinate name: {str(e)}"
                allure.attach(msg, name='Fetch Subordinate Name Error', attachment_type=allure.attachment_type.TEXT)
                raise Exception(msg)

        with allure.step("Click Add New Member Button"):
            try:
                add_new_member_btn = self.wait.until(EC.presence_of_element_located((By.XPATH, "//button[text()='Add New Member']")))
                highlight_element(self.driver, add_new_member_btn)
                add_new_member_btn.click()
            except Exception as e:
                msg = f"Failed to click Add New Member button: {str(e)}"
                allure.attach(msg, name = 'Add New Member Error', attachment_type = allure.attachment_type.TEXT)
                raise Exception(msg)

            try:
                enter_email = self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@id='subordinates.1.email']")))
                highlight_element(self.driver, enter_email)
                enter_email.click()
                enter_email.send_keys(self.email_subauditee2)
                allure.attach(f"Entered Subordinate Auditor's Email ID 2: {self.email_subauditee2}",name='Enter Team Member',attachment_type=allure.attachment_type.TEXT)
            except Exception as e:
                msg = f"Failed to Enter Email: {str(e)}"
                allure.attach(msg, name = 'Email Error', attachment_type = allure.attachment_type.TEXT)
                raise Exception(msg)
            
        with allure.step("Click Save Button"):
            try:
                save_btn = self.wait.until(EC.presence_of_element_located((By.XPATH, "//button[text()='Save']")))
                highlight_element(self.driver, save_btn)
                save_btn.click()
            except Exception as e:
                msg = f"Failed to Click Save Button: {str(e)}"
                allure.attach(msg, name = 'Save Button Error', attachment_type = allure.attachment_type.TEXT)
                raise Exception(msg)
   
    def select_checklist_form(self):
        with allure.step("Select Checklist Form"):
            try:
                checklist_select_form = self.wait.until(EC.presence_of_element_located((By.XPATH, "//button[@role='combobox']//span[normalize-space()='Select']")))
                highlight_element(self.driver, checklist_select_form)
                checklist_select_form.click()
                time.sleep(0.5)
            except Exception as e:
                msg = f"Failed to select Checklist Form: {str(e)}"
                allure.attach(msg, name = 'Checklist Form Selection Error', attachment_type = allure.attachment_type.TEXT)
                raise Exception(msg)

            try:
                checklist_select_option = self.wait.until(EC.presence_of_element_located((By.XPATH, f"//*[@role='option']//*[normalize-space(text())='{self.assign_fetched_name}']")))
                highlight_element(self.driver, checklist_select_option)
                checklist_select_option.click()
            except Exception as e:
                msg = f"Failed to select option '{self.assign_fetched_name}' from Checklist Form: {str(e)}"
                allure.attach(msg, name='Option Selection Error', attachment_type=allure.attachment_type.TEXT)
                raise Exception(msg)

            try:
                save_btn = self.wait.until(EC.presence_of_element_located((By.XPATH, "//button[text()='Save']")))
                highlight_element(self.driver, save_btn)
                save_btn.click()
                time.sleep(2)
            except Exception as e:
                msg = f"Failed to Click Save Button: {str(e)}"
                allure.attach(msg, name = 'Save Button Error', attachment_type = allure.attachment_type.TEXT)
                raise Exception(msg)

    def verify_assign_to(self):
        try:
            with allure.step("Verify Assign To"):
                assign_to = self.wait.until(EC.presence_of_element_located((By.XPATH, f"//tr[.//td[normalize-space()='{self.assign_fetched_name}']]//td[4]")))
                highlight_element(self.driver, assign_to)
                actual_value = assign_to.text.strip() 
                # Expected vs Actual 
                expected_value = self.assign_fetched_name 
                print(f"Expected : {expected_value}") 
                print(f"Actual : {actual_value}") 
                if expected_value.strip().lower() == actual_value.strip().lower(): 
                    allure.attach( f"Expected : {expected_value}\n" f"Actual : {actual_value}", name="Assign To - PASS", attachment_type=allure.attachment_type.TEXT ) 
                    return True 
                else:
                    allure.attach( f"Expected : {expected_value}\n" f"Actual : {actual_value}", name="Assign To - FAIL", attachment_type=allure.attachment_type.TEXT ) 
                    raise AssertionError( f"Assign To mismatch: " f"Expected '{expected_value}', " f"Actual '{actual_value}'" )
        except Exception as e: 
            allure.attach( str(e), name="Verify Assign To Error", attachment_type=allure.attachment_type.TEXT ) 
            raise

    def click_settings(self):
        with allure.step("Verify User name"):
            try:
                settings_btn = self.wait.until(EC.presence_of_element_located((By.XPATH, self.settings_icon)))
                highlight_element(self.driver, settings_btn)
                settings_btn.click()
                fetch_user_name = self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@id='full_name']")))
                highlight_element(self.driver, fetch_user_name)
                self.fetch_user_name = fetch_user_name.get_attribute("value").strip()
            except Exception as e:
                msg = f"Failed to fetch user name: {str(e)}"
                allure.attach(msg, name='Fetch User Name Error', attachment_type=allure.attachment_type.TEXT)
                raise Exception(msg)

    def click_logout(self):
        with allure.step("Logout from application"):
            try:
                logout_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, self.logout_icon)))
                highlight_element(self.driver, logout_btn)
                logout_btn.click()
                yes_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[.//span[text()='Yes']]")))
                yes_btn.click()
                print("🚪 Logged out successfully")
            except Exception as e:
                print(f"❌ Logout failed: {e}")
                return False
    
        with allure.step("Login again with same credentials"):
            try:
                # driver.get("http://192.168.30.11:8081/login") 
                login_check(self.driver, waittime=30, trial=1, username=self.tm_user, password=self.tm_pswd) 
                time.sleep(1.5)
                self.driver.refresh()
                time.sleep(1)
            except Exception as e:
                print(f"❌ Logout failed: {e}")
                return False

    def click_audit_btn(self):
        with allure.step("Click Audit Tab"):
            try:
                audit_btn = self.wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class, '_tab_') and text()='Audit']")))
                highlight_element(self.driver, audit_btn)
                audit_btn.click()
            except Exception as e:
                msg = f"Failed to click Audit Tab: {str(e)}"
                allure.attach(msg, name = "Audit Tab Error", attachment_type = allure.attachment_type.TEXT)
                raise Exception(msg)
    
    def verify_dash_assign_name(self):
        with allure.step("Fetch Assign name in Dashboard"):
            try:
                latest_assign_name = os.path.join("latest_data", "audit_file.txt")
                with open(latest_assign_name, "r") as f:
                    created_latest_assign_name = f.read().strip()
                fetch_assign_name = self.wait.until(EC.presence_of_element_located((By.XPATH, f"//tr[.//td[normalize-space()='{created_latest_assign_name}']]//td[6]")))
                highlight_element(self.driver, fetch_assign_name)
                actual_assign_name = fetch_assign_name.text.strip()
                expected_assign_name = self.fetch_user_name
                if expected_assign_name.strip().lower() == actual_assign_name.strip().lower():
                    allure.attach(f"Expected : {expected_assign_name}\n" f"Actual : {actual_assign_name}", name="Assign Name - PASS", attachment_type=allure.attachment_type.TEXT)
                    return True 
                else:
                    allure.attach(f"Expected : {expected_assign_name}\n" f"Actual : {actual_assign_name}", name="Assign To - FAIL", attachment_type=allure.attachment_type.TEXT) 
                    raise AssertionError(f"Assign To mismatch: " f"Expected '{expected_assign_name}', " f"Actual '{actual_assign_name}'")
            except Exception as e: 
                allure.attach(str(e), name="Verify Assign To Error", attachment_type=allure.attachment_type.TEXT ) 
                raise

    def assign_checklist_form(self):
        self.click_audit()
        self.click_assignment()
        self.click_checklist_btn()
        self.click_assign_checklist()
        self.new_member()
        self.select_checklist_form()
        self.verify_assign_to()
        self.click_settings()
        self.click_logout()
        self.click_audit_btn()
        self.verify_dash_assign_name()

        return True

   