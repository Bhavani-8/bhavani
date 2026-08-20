import allure
import time
import os
import json
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from utilities.other_utils_functions.highlight import highlight_element

class SearchAssignmentTask:

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

    def fetch_assignment_name(self):
        with allure.step("Fetch the Assignment name from the task list"):
            try:
                assignment_name_elem = self.wait.until(EC.visibility_of_element_located((By.XPATH,"//tbody/tr[1]/td[2]")))
                assignment_name = assignment_name_elem.text.strip()
                print(f"Assignment Name: {assignment_name}")
                return assignment_name
            except Exception as e:
                msg = f"Failed to Fetch Assignment name: {str(e)}"
                allure.attach(msg, name = 'Fetch Assignment name Error', attachment_type = allure.attachment_type.TEXT)
                raise Exception(msg)
            
    def search_company_elem(self, assignment_name): 
        with allure.step(f"Search using Assignment name: {assignment_name}"):
            try:
                search_input = self.wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@placeholder='Search records...']")))
                highlight_element(self.driver, search_input)
                search_input.clear()
                search_input.send_keys(assignment_name)
                time.sleep(3) 
                allure.attach(assignment_name, name="Searched Assignment name", attachment_type=allure.attachment_type.TEXT) 
            except Exception as e:
                msg = f"Failed to Search Assignment name: {str(e)}"
                allure.attach(msg, name = 'Search Assignment name Error', attachment_type = allure.attachment_type.TEXT)
                raise Exception(msg)

    def search_assignment_name(self):
        self.click_audit()
        self.click_assignment()
        assignment_name = self.fetch_assignment_name()
        self.search_assignment_name(assignment_name)
        return True

                
