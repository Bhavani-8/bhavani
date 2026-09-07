import allure
import time
import os
import json
import random
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from utilities.other_utils_functions.highlight import highlight_element


class AssignQuestionnaireForm:

    def __init__(self, driver, wait,email_id):
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
            except Exception as e:
                msg = f"Failed to click Assignment button: {str(e)}"
                allure.attach(msg, name = 'Audit Assignment Error', attachment_type = allure.attachment_type.TEXT)
                raise Exception(msg)

    def click_questionnaire_btn(self):
        with allure.step("Click Questionnaire Button"):
            try:
                latest_questionnaire = os.path.join("latest_data", "audit_company.txt")
                with open(latest_questionnaire, "r") as f:
                    created_latest_questionnaire = f.read().strip()
                questionnaire_btn = self.wait.until(EC.presence_of_element_located((By.XPATH, f"//tr[.//td[normalize-space()='{created_latest_questionnaire})']]//td[6]")))
                highlight_element(self.driver, questionnaire_btn)
                questionnaire_btn.click()
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

            except Exception as e:
                msg = f"Failed to Enter Email: {str(e)}"
                allure.attach(msg, name = 'Email Error', attachment_type = allure.attachment_type.TEXT)
                raise Exception(msg)

            try:
                fetch_name = self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@name='subordinates.0.name']")))
                highlight_element(self.driver, fetch_name)
                self.assign_fetched_name =  fetch_name.get_attribute("value").strip
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
            except Exception as e:
                msg = f"Failed to select Questionnaire Form: {str(e)}"
                allure.attach(msg, name = 'Questionnaire Form Selection Error', attachment_type = allure.attachment_type.TEXT)
                raise Exception(msg)

            try:
                select_option = self.wait.until(EC.presence_of_element_located((By.XPATH, f"//div[@role='option'][normalize-space()='{self.assign_fetched_name}']")))
                highlight_element(self.driver, select_option)
                select_option.click()
            except Exception as e:
                msg = f"Failed to select option '{self.fetched_name}' from Questionnaire Form: {str(e)}"
                allure.attach(msg, name='Option Selection Error', attachment_type=allure.attachment_type.TEXT)
                raise Exception(msg)

            try:
                save_btn = self.wait.until(EC.presence_of_element_located((By.XPATH, "//button[text()='Save']")))
                highlight_element(self.driver, save_btn)
                save_btn.click()
            except Exception as e:
                msg = f"Failed to Click Save Button: {str(e)}"
                allure.attach(msg, name = 'Save Button Error', attachment_type = allure.attachment_type.TEXT)
                raise Exception(msg)


    def assign_question_form(self):
        self.click_audit()
        self.click_assignment()
        self.click_questionnaire_btn()
        self.click_assign_questionnaire()
        self.new_member()
        self.select_questionnaire_form()

        return True

   