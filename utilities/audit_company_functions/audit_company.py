import allure
import time
import os
import json
import random
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from utilities.other_utils_functions.highlight import highlight_element


class AuditCompanyTask:

    def __init__(self, driver, wait, email_id):
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

    def click_new_company(self):
        with allure.step("Click New Company"):
            try:
                new_company_btn = self.wait.until(EC.presence_of_element_located((By.XPATH, "//button[normalize-space()='New Company']")))
                highlight_element(self.driver, new_company_btn)
                new_company_btn.click()
            except Exception as e:
                msg = f"Failed to click New company btn: {str(e)}"
                allure.attach(msg, name ="New company button Error", attachment_type=allure.attachment_type.TEXT)
                raise Exception(msg)

    def enter_company_name(self):
        with allure.step("Enter company name"):
            try:
                audit_company_name = f"Test {random.randint(1000, 99999)}"
                enter_company_name = self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Enter company name']")))
                highlight_element(self.driver, enter_company_name)
                enter_company_name.send_keys(audit_company_name)
                expected_company_name = enter_company_name.get_attribute("value").strip()
                print(f"Expected Company Name: {expected_company_name}")
                allure.attach(expected_company_name,name="Company Name",attachment_type=allure.attachment_type.TEXT)
                return expected_company_name
            except Exception as e:
                msg = f"failed to Enter company name: {str(e)}"
                allure.attach(msg, name = "Company name Error", attachment_type=allure.attachment_type.TEXT)
                raise Exception(msg)

    def register_id(self):
        with allure.step("Enter Register ID"):
            try:
                unique_register_id = str(random.randint(100000, 999999))
                register_id = self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Enter ID']")))
                highlight_element(self.driver, register_id)
                register_id.send_keys(unique_register_id)
                expected_register_id = register_id.get_attribute("value").strip() 
                print(f"Audit company name :{expected_register_id}")
                allure.attach(expected_register_id,name="Register ID",attachment_type=allure.attachment_type.TEXT)
                return expected_register_id
            except Exception as e:
                msg = f"failed to Enter Register ID: {str(e)}"
                allure.attach(msg, name = "Register ID Error", attachment_type=allure.attachment_type.TEXT)
                raise Exception(msg)

    def country_name(self):
        with allure.step("Select country name"):
            try:
                country_droprdown = self.wait.until(EC.presence_of_element_located((By.XPATH, "(//button[@role='combobox'])[2]")))
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

    def company_category(self):
        with allure.step("Select Company Category"):
            try:
                category_droprdown = self.wait.until(EC.presence_of_element_located((By.XPATH, "(//button[@role='combobox'])[3]")))
                category_droprdown.click()
                time.sleep(2)
                company_category = self.wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class,'whitespace-normal') and text()='Limited']")))
                highlight_element(self.driver, company_category)
                company_category.click()
                expected_company_category = company_category.text.strip()
                print(f"Company Category: {expected_company_category}")
                allure.attach(expected_company_category, name='Company category', attachment_type=allure.attachment_type.TEXT)
                return expected_company_category
            except Exception as e:
                msg = f"failed to Select Company Category: {str(e)}"
                allure.attach(msg, name = "Company Category Error", attachment_type=allure.attachment_type.TEXT)
                raise Exception(msg)

    def enter_email_id(self):
        with allure.step("Enter Email Id"):
            try:
                enter_email_id = self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Enter Email']")))
                highlight_element(self.driver, enter_email_id)
                enter_email_id.send_keys(self.email_id)
                expected_enter_email_id = enter_email_id.get_attribute("value").strip()
                print(f"Company Category: {expected_enter_email_id}")
                allure.attach(expected_enter_email_id, name='Email Id', attachment_type=allure.attachment_type.TEXT)
                return expected_enter_email_id
            except Exception as e:
                msg = f"failed to Enter Email Id: {str(e)}"
                allure.attach(msg, name = "Enter Email Id Error", attachment_type=allure.attachment_type.TEXT)
                raise Exception(msg)
    
    def contact_number(self):
        with allure.step("Enter Contact Number"):
            try:
                unique_contact_number = f"987{random.randint(1000000, 9999999)}"
                contact_number = self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Enter Mobile No']")))
                highlight_element(self.driver, contact_number)
                contact_number.send_keys(unique_contact_number)
                expected_contact_number = contact_number.get_attribute("value").strip() 
                print(f"Audit company name :{expected_contact_number}")
                allure.attach(expected_contact_number,name="Contact Number",attachment_type=allure.attachment_type.TEXT)
                return expected_contact_number
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

    def validate_all_details(self,expected_company_name,expected_register_id,expected_company_category,expected_enter_email_id,expected_contact_number,):
        with allure.step("Validate all details"):
            try:
                actual_company_name = self.wait.until(EC.presence_of_element_located((By.XPATH, f"//td[contains(normalize-space(),'{expected_company_name}')]")))
                highlight_element(self.driver, actual_company_name)
                actual_company_name_text = actual_company_name.text.strip()
                # self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", actual_company_name)
                actual_register_id = self.wait.until(EC.presence_of_element_located((By.XPATH, f"//td[normalize-space()='{expected_register_id}']")))
                highlight_element(self.driver, actual_register_id)
                actual_register_id_text = actual_register_id.text.strip()

                actual_company_category = self.wait.until(EC.presence_of_element_located((By.XPATH, f"//tr[.//td[normalize-space()='{expected_company_name}']]//td[normalize-space()='{expected_company_category}']")))
                highlight_element(self.driver, actual_company_category)
                actual_company_category_text = actual_company_category.text.strip()

                actual_enter_email_id = self.wait.until(EC.presence_of_element_located((By.XPATH, f"//td[normalize-space()='{expected_enter_email_id}']")))
                highlight_element(self.driver, actual_enter_email_id)
                actual_enter_email_id_text = actual_enter_email_id.text.strip()

                actual_contact_number = self.wait.until(EC.presence_of_element_located((By.XPATH, f"//td[normalize-space()='{expected_contact_number}']")))
                highlight_element(self.driver, actual_contact_number)
                actual_contact_number_text = actual_contact_number.text.strip()

                assert expected_company_name == actual_company_name_text, \
                    f"Company Name Mismatch! Expected: {expected_company_name}, Actual: {actual_company_name_text}"
                assert expected_register_id == actual_register_id_text, \
                    f"Register ID Mismatch! Expected: {expected_register_id}, Actual: {actual_register_id_text}"

                assert expected_company_category == actual_company_category_text, \
                    f"Company Category Mismatch! Expected: {expected_company_category}, Actual: {actual_company_category_text}"

                assert expected_enter_email_id == actual_enter_email_id_text, \
                    f"Email ID Mismatch! Expected: {expected_enter_email_id}, Actual: {actual_enter_email_id_text}"

                assert expected_contact_number == actual_contact_number_text, \
                    f"Contact Number Mismatch! Expected: {expected_contact_number}, Actual: {actual_contact_number_text}"

                allure.attach(f"""
                Company Name      : {expected_company_name} == {actual_company_name_text}
                Register ID       : {expected_register_id} == {actual_register_id_text}
                Company Category  : {expected_company_category} == {actual_company_category_text}
                Email ID          : {expected_enter_email_id} == {actual_enter_email_id_text}
                Contact Number    : {expected_contact_number} == {actual_contact_number_text}""",
                name="Audit Company Validation",attachment_type=allure.attachment_type.TEXT,)

            except Exception as e:
                msg = f"Validation Failed: {str(e)}"
                allure.attach(msg,name="Validation Error",attachment_type=allure.attachment_type.TEXT,)
                raise Exception(msg)
        
    def audit_company(self):
        self.click_audit()
        self.click_company()
        self.click_new_company()
        expected_company_name = self.enter_company_name()
        expected_register_id = self.register_id()
        self.country_name()
        self.pincode_number()
        expected_company_category = self.company_category()
        expected_enter_email_id = self.enter_email_id()
        expected_contact_number = self.contact_number()
        self.submit_button() 
        self.validate_all_details(expected_company_name,expected_register_id,expected_company_category,expected_enter_email_id,expected_contact_number)


        return True

            
