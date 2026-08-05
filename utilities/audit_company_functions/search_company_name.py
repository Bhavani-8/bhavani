import allure
import time
import os
import json
import random
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from utilities.other_utils_functions.highlight import highlight_element


class SearchCompanyName:

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

    def fetch_company_name(self):
        with allure.step("Fetch the task name from the task list"):
            try:
                company_name_elem = self.wait.until(EC.visibility_of_element_located((By.XPATH,"//tbody/tr[1]/td[2]")))
                highlight_element(self.driver, company_name_elem)
                company_name = company_name_elem.text.strip()
                print(f"🔹 Company Name: {company_name}")
            except Exception as e:
                msg = f"Failed to Fetch company name: {str(e)}"
                allure.attach(msg, name = 'Fetch Company name Error', attachment_type = allure.attachment_type.TEXT)
                raise Exception(msg)
            
    def search_company_name(self, company_name): 
        with allure.step(f"Search using task name: {company_name}"):
            try:
                search_input = self.wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@placeholder='Search records...']")))
                highlight_element(self.driver, search_input)
                search_input.clear()
                search_input.send_keys(company_name)
                time.sleep(3)  # Extra wait to ensure results load
            except Exception as e:
                msg = f"Failed to Search company name: {str(e)}"
                allure.attach(msg, name = 'Search Company name Error', attachment_type = allure.attachment_type.TEXT)
                raise Exception(msg)

   
        
    def search_company_name(self):
        self.click_audit()
        self.click_company()
        self.fetch_company_name()
        self.search_company_name()
        

        return True

                
