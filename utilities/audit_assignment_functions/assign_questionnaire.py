import allure
import time
import os
import json
import random
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from utilities.other_utils_functions.highlight import highlight_element


class AssignExportData:

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

   