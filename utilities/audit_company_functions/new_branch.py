import allure
import time
import os
import json
import random
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from utilities.other_utils_functions.highlight import highlight_element


class AuditBranchTask:

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

    def new_branch(self):
        with allure.step("Click New Company"):
            try:
                new_branch_btn = self.wait.until(EC.presence_of_element_located((By.XPATH, "//button[normalize-space()='New Branch']")))
                highlight_element(self.driver, new_branch_btn)
                new_branch_btn.click()
            except Exception as e:
                msg = f"Failed to click New branch btn: {str(e)}"
                allure.attach(msg, name ="New branch button Error", attachment_type=allure.attachment_type.TEXT)
                raise Exception(msg)

    def enter_company_name(self):
        with allure.step("Enter company name"):
            try:
                company_droprdown = self.wait.until(EC.presence_of_element_located((By.XPATH, "(//button[@role='combobox'])[2]")))
                company_droprdown.click()
                time.sleep(2)
                company_file = os.path.join("latest_data", "audit_company.txt")
                with open(company_file, "r") as f:
                    created_company_name = f.read().strip()
                company_name = self.wait.until(EC.presence_of_element_located((By.XPATH, f"//div[contains(@class,'whitespace-normal') and translate(normalize-space(.), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz') = translate('{created_company_name}', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz')]")))
                highlight_element(self.driver, company_name)
                company_name.click()
                allure.attach(company_name.text, name='Company name', attachment_type=allure.attachment_type.TEXT)
                            
            except Exception as e:
                msg = f"failed to Enter company name: {str(e)}"
                allure.attach(msg, name = "Company name Error", attachment_type=allure.attachment_type.TEXT)
                raise Exception(msg)

    def location(self):
        with allure.step("Enter Location name"):
            try:
                unique_location_name = f"Test Location {random.randint(100, 999)}"
                location_name = self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@name='branch_location']")))
                highlight_element(self.driver, location_name)
                location_name.send_keys(unique_location_name)
                allure.attach(location_name.get_attribute("value"),name="Location name",attachment_type=allure.attachment_type.TEXT)
            except Exception as e:
                msg = f"failed to Enter Location name: {str(e)}"
                allure.attach(msg, name = "Location name Error", attachment_type=allure.attachment_type.TEXT)
                raise Exception(msg)

    def address_line1(self):
        with allure.step("Enter Location name"):
            try:
                unique_address_line1 = f"Test Address {random.randint(100, 999)}"
                address_line = self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@name='address_line1']")))
                highlight_element(self.driver, address_line)
                address_line.send_keys(unique_address_line1)
                allure.attach(address_line.get_attribute("value"),name="Address Line1",attachment_type=allure.attachment_type.TEXT)
            except Exception as e:
                msg = f"failed to Enter Address Line1: {str(e)}"
                allure.attach(msg, name = "Address Line1 Error", attachment_type=allure.attachment_type.TEXT)
                raise Exception(msg)

    def country_name(self):
        with allure.step("Select country name"):
            try:
                country_droprdown = self.wait.until(EC.presence_of_element_located((By.XPATH, "(//button[@role='combobox'])[3]")))
                country_droprdown.click()
                time.sleep(2)
                country_name = self.wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class,'whitespace-normal') and text()='India']")))
                highlight_element(self.driver, country_name)
                country_name.click()
                allure.attach(country_name.text, name='Country_name', attachment_type=allure.attachment_type.TEXT)
            except Exception as e:
                msg = f"failed to Select Country name: {str(e)}"
                allure.attach(msg, name = "Country name Error", attachment_type=allure.attachment_type.TEXT)
                raise Exception(msg)

    def pincode_number(self):
        with allure.step("Enter Pincode number"):
            try:
                pincode_number = self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Enter Pincode']")))
                highlight_element(self.driver, pincode_number)
                pincode_number.send_keys("400092")
                time.sleep(1)
                allure.attach(pincode_number.get_attribute("value"), name='Pincode number', attachment_type=allure.attachment_type.TEXT)
            except Exception as e:
                msg = f"failed to Enter Pincode number: {str(e)}"
                allure.attach(msg, name = "Pincode number Error", attachment_type=allure.attachment_type.TEXT)
                raise Exception(msg)

    def manager_email(self):
        with allure.step("Enter Email Id"):
            try:
                branch_manager_email = f"branchmanager{random.randint(100, 999)}@gmail.com"
                manager_email = self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Enter Email']")))
                highlight_element(self.driver, manager_email)
                manager_email.send_keys(branch_manager_email)
                allure.attach(manager_email.get_attribute("value"), name='Branch Manager Email', attachment_type=allure.attachment_type.TEXT)
            except Exception as e:
                msg = f"failed to Enter Branch Manager Email: {str(e)}"
                allure.attach(msg, name = "Branch Manager Email Error", attachment_type=allure.attachment_type.TEXT)
                raise Exception(msg)

    def manager_name(self):
        with allure.step("Enter Manager name"):
            try:
                branch_manager_name = f"Audit Manager {random.randint(100, 999)}"
                manager_name = self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@name='manager_name']")))
                highlight_element(self.driver, manager_name)
                manager_name.send_keys(branch_manager_name)
                allure.attach(manager_name.get_attribute("value"),name="Address Line1",attachment_type=allure.attachment_type.TEXT)
            except Exception as e:
                msg = f"failed to Enter Address Line1: {str(e)}"
                allure.attach(msg, name = "Address Line1 Error", attachment_type=allure.attachment_type.TEXT)
                raise Exception(msg)

    def contact_number(self):
        with allure.step("Enter Contact Number"):
            try:
                unique_contact_number = f"987{random.randint(1000000, 9999999)}"
                contact_number = self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Enter Mobile No']")))
                highlight_element(self.driver, contact_number)
                contact_number.send_keys(unique_contact_number)
                allure.attach(unique_contact_number,name="Contact Number",attachment_type=allure.attachment_type.TEXT)
            except Exception as e:
                msg = f"failed to Enter Mobile Number : {str(e)}"
                allure.attach(msg, name = "Moible number Error", attachment_type=allure.attachment_type.TEXT)
                raise Exception(msg)

    def submit_button(self):
        with allure.step("Click Submit Button"):
            try:
                submit_button = self.wait.until(EC.presence_of_element_located((By.XPATH, "//button[@type='submit']")))
                highlight_element(self.driver, submit_button)
                submit_button.click()
                time.sleep(2)
            except Exception as e:
                msg = f"failed to Select Company Category: {str(e)}"
                allure.attach(msg, name = "Company Category Error", attachment_type=allure.attachment_type.TEXT)
                raise Exception(msg)
    

   
    def audit_branch(self):
        self.click_audit()
        self.click_company()
        self.new_branch()
        self.enter_company_name()
        self.location()
        self.address_line1()
        self.country_name()
        self.pincode_number()
        self.manager_email()
        self.manager_name()
        self.contact_number()
        self.submit_button()

        return True

            
