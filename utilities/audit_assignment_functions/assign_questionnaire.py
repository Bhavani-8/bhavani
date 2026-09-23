import allure
import time
import os
import json
import random
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from utilities.other_utils_functions.highlight import highlight_element
from utilities.login_utils import login_check


class AssignQuestionnaireForm:

    def __init__(self, driver, wait,  email_id):
        self.driver = driver
        self.wait = wait
        self.email_id = email_id
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

    def click_questionnaire_btn(self):
        with allure.step("Click Questionnaire Button"):
            try:
                latest_questionnaire = os.path.join("latest_data", "audit_file.txt")
                with open(latest_questionnaire, "r") as f:
                    created_latest_questionnaire = f.read().strip()
                questionnaire_btn = self.wait.until(EC.presence_of_element_located((By.XPATH, f"//tr[.//td[normalize-space()='{created_latest_questionnaire}']]//td[6]")))
                highlight_element(self.driver, questionnaire_btn)
                questionnaire_btn.click()
                time.sleep(3)
            except Exception as e:
                msg = f"Failed to click Questionnaire button: {str(e)}"
                allure.attach(msg, name = 'Questionnaire Error', attachment_type = allure.attachment_type.TEXT)
                raise Exception(msg)

    def click_assign_questionnaire(self):
        with allure.step("Click Assign Questionnaire"):
            try:
                assign_questionnaire_btn = self.wait.until(EC.presence_of_element_located((By.XPATH, "//button[text()='Assign Questionnaire']")))
                highlight_element(self.driver, assign_questionnaire_btn)
                assign_questionnaire_btn.click()
                time.sleep(1)
            except Exception as e:
                msg = f"Failed to click Assign Questionnaire button: {str(e)}"
                allure.attach(msg, name = 'Assign Questionnaire Error', attachment_type = allure.attachment_type.TEXT)
                raise Exception(msg)

    def new_member(self):
        with allure.step("Click Add New Member Button"):
            try:
                add_new_member_btn = self.wait.until(EC.presence_of_element_located((By.XPATH, "//button[text()='Add New Member']")))
                highlight_element(self.driver, add_new_member_btn)
                add_new_member_btn.click()
            except Exception as e:
                msg = f"Failed to click Add New Member button: {str(e)}"
                allure.attach(msg, name = 'Add New Member Error', attachment_type = allure.attachment_type.TEXT)
                raise Exception(msg)
        with allure.step("Enter Team Member"):
            try:
                enter_email = self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@id='subordinates.1.email']")))
                highlight_element(self.driver, enter_email)
                enter_email.click()
                enter_email.send_keys(self.email_id)
                allure.attach(f"Entered Team Member Email: {self.email_id}",name='Enter Team Member',attachment_type=allure.attachment_type.TEXT)
                time.sleep(1)
            except Exception as e:
                msg = f"Failed to Enter Email: {str(e)}"
                allure.attach(msg, name = 'Email Error', attachment_type = allure.attachment_type.TEXT)
                raise Exception(msg)

            try:
                time.sleep(0.5)
                fetch_name = self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@name='subordinates.0.name']")))
                highlight_element(self.driver, fetch_name)
                self.assign_fetched_name = fetch_name.get_attribute("value").strip()
                print(f"Fetched name: {self.assign_fetched_name}")

            except Exception as e:
                msg = f"Failed to fetch subordinate name: {str(e)}"
                allure.attach(msg, name='Fetch Subordinate Name Error', attachment_type=allure.attachment_type.TEXT)
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
        
    def select_questionnaire_form(self):
        with allure.step("Select Questionnaire Form"):
            try:
                select_form = self.wait.until(EC.presence_of_element_located((By.XPATH, "//button[@role='combobox']//span[normalize-space()='Select']")))
                highlight_element(self.driver, select_form)
                select_form.click()
                time.sleep(0.5)
            except Exception as e:
                msg = f"Failed to select Questionnaire Form: {str(e)}"
                allure.attach(msg, name = 'Questionnaire Form Selection Error', attachment_type = allure.attachment_type.TEXT)
                raise Exception(msg)

            try:
                select_option = self.wait.until(EC.presence_of_element_located((By.XPATH, f"//*[@role='option']//*[normalize-space(text())='{self.assign_fetched_name}']")))
                highlight_element(self.driver, select_option)
                select_option.click()
            except Exception as e:
                msg = f"Failed to select option '{self.assign_fetched_name}' from Questionnaire Form: {str(e)}"
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
                drop_down_btn = self.wait.until(EC.presence_of_element_located((By.XPATH, "//button[@data-slot='accordion-trigger']")))
                drop_down_btn.click()
                time.sleep(0.5)
                assign_to = self.wait.until(EC.presence_of_element_located((By.XPATH, f"//tr[.//td[normalize-space()='{self.assign_fetched_name}']]//td[5]")))
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

    def click_logout(self, tm_user, tm_pwd,):
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
                login_check(self.driver, waittime=30, trial=1, username=tm_user, password=tm_pwd) 
                time.sleep(1.5)
            except Exception as e:
                print(f"❌ Logout failed: {e}")
                return False

    def click_audit(self):
        with allure.step("Click Audit Tab"):
            try:
                audit_btn = self.wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class, '_tab_') and text()='Audit']")))
                highlight_element(self.driver, audit_btn)
                audit_btn.click()
            except Exception as e:
                msg = f"Failed to click Audit Tab: {str(e)}"
                allure.attach(msg, name = "Audit Tab Error", attachment_type = allure.attachment_type.TEXT)
                raise Exception(msg)
    
    

    def assign_question_form(self):
        self.click_audit()
        self.click_assignment()
        self.click_questionnaire_btn()
        self.click_assign_questionnaire()
        self.new_member()
        self.select_questionnaire_form()
        self.verify_assign_to()
        self.click_audit()

        return True

   