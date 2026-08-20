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
                enter_company_name_btn = self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Enter company name']")))
                highlight_element(self.driver, enter_company_name_btn)
                audit_company_name = f"Test Audit {random.randint(100, 9999)}"
                enter_company_name_btn.send_keys(audit_company_name)
                company_file = os.path.join("latest_data", "audit_company.txt")
                with open(company_file, "w") as f:
                    f.write(audit_company_name)
                expected_company_name = enter_company_name_btn.get_attribute("value").strip()
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
                register_id_elem = self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Enter ID']")))
                highlight_element(self.driver, register_id_elem)
                register_id_elem.send_keys(unique_register_id)
                expected_register_id = register_id_elem.get_attribute("value").strip() 
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

    def click_company_category(self):
        with allure.step("Select Company Category"):
            try:
                category_droprdown = self.wait.until(EC.presence_of_element_located((By.XPATH, "(//button[@role='combobox'])[3]")))
                category_droprdown.click()
                time.sleep(2)
                company_category = self.wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class,'whitespace-normal') and text()='Limited']")))
                highlight_element(self.driver, company_category)
                company_category.click()
                expected_company_category = company_category.text.strip()
                print(f"Expected Company Category: {expected_company_category}")
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
                print(f"Expected Email ID: {expected_enter_email_id}")
                allure.attach(expected_enter_email_id, name='Email Id', attachment_type=allure.attachment_type.TEXT)
                return expected_enter_email_id
            except Exception as e:
                msg = f"failed to Enter Email Id: {str(e)}"
                allure.attach(msg, name = "Enter Email Id Error", attachment_type=allure.attachment_type.TEXT)
                raise Exception(msg)
    
    def click_contact_number(self):
        with allure.step("Enter Contact Number"):
            try:
                unique_contact_number = f"987{random.randint(1000000, 9999999)}"
                contact_number = self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Enter Mobile No']")))
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

    def submit_button(self):
        with allure.step("Click Submit Button"):
            try:
                submit_button = self.wait.until(EC.presence_of_element_located((By.XPATH, "//button[@type='submit']")))
                highlight_element(self.driver, submit_button)
                submit_button.click()
                time.sleep(2)
            except Exception as e:
                msg = f"failed to click submit button: {str(e)}"
                allure.attach(msg, name = "Submit button Error", attachment_type=allure.attachment_type.TEXT)
                raise Exception(msg)

    def validate_company_details(self,expected_company_name,expected_register_id,expected_company_category,expected_contact_number,expected_enter_email_id):
        all_matched = True
        with allure.step("Validate company name"):
            try:
               
                actual_company = self.wait.until(EC.presence_of_element_located((By.XPATH, f"//tr[.//td[normalize-space()='{expected_register_id}']]//td[2]")))
                highlight_element(self.driver, actual_company)
                actual_company_name = actual_company.text.strip()
                print(f"Expected Company Name     : {expected_company_name}")
                print(f"Actual Company Name       : {actual_company_name}")

                if expected_company_name == actual_company_name:
                    allure.attach(
                        f"Expected : {expected_company_name}\n"
                        f"Actual   : {actual_company_name}\n",
                        name="Template Name - PASS",attachment_type=allure.attachment_type.TEXT)
                else:
                    all_matched = False

                    allure.attach(
                        f"Expected : {expected_company_name}\n"
                        f"Actual   : {actual_company_name}\n",
                        name="Template Name - FAIL",attachment_type=allure.attachment_type.TEXT)

            except Exception as e:
                all_matched = False
                allure.attach(
                    f"Expected : {expected_company_name}\n"
                    f"Actual   : Not Found\n",
                    name="Template Name - FAIL",attachment_type=allure.attachment_type.TEXT)
        with allure.step("Validate Register ID"):
            try:
                actual_register_id = self.wait.until(EC.presence_of_element_located((By.XPATH, f"//td[normalize-space()='{expected_register_id}']")))
                highlight_element(self.driver, actual_register_id)
                actual_register_id_text = actual_register_id.text.strip()
                print(f"Expected Register ID      : {expected_register_id}")
                print(f"Actual Register ID        : {actual_register_id_text}")

                if expected_register_id == actual_register_id_text:
                    allure.attach(
                        f"Expected : {expected_register_id}\n"
                        f"Actual   : {actual_register_id_text}\n",
                        name="Audit Name - PASS",attachment_type=allure.attachment_type.TEXT)
                else:
                    all_matched = False

                    allure.attach(
                        f"Expected : {expected_register_id}\n"
                        f"Actual   : {actual_register_id_text}\n",
                        name="Audit Name - FAIL",attachment_type=allure.attachment_type.TEXT)

            except Exception as e:
                all_matched = False

                error_msg = str(e).split("Stacktrace:")[0].strip()

                allure.attach(
                    f"Expected : {expected_register_id}\n"
                    f"Actual   : Not Found\n",
                    name="Audit Name - FAIL",attachment_type=allure.attachment_type.TEXT)

        with allure.step("Validate Company Category"):
            try:
                actual_company_category = self.wait.until(EC.presence_of_element_located((By.XPATH, f"//tr[.//td[normalize-space()='{expected_register_id}']]//td[4]")))
                highlight_element(self.driver, actual_company_category)
                actual_company_category_text = actual_company_category.text.strip()
                print(f"Expected Company Category : {expected_company_category}")
                print(f"Actual Company Category   : {actual_company_category_text}")

                if expected_company_category == actual_company_category_text:
                    allure.attach(
                        f"Expected : {expected_company_category}\n"
                        f"Actual   : {actual_company_category_text}\n",
                        name="Audit Name - PASS",attachment_type=allure.attachment_type.TEXT)
                else:
                    all_matched = False

                    allure.attach(
                        f"Expected : {expected_company_category}\n"
                        f"Actual   : {actual_company_category_text}\n",
                        name="Audit Name - FAIL",attachment_type=allure.attachment_type.TEXT)

            except Exception as e:
                all_matched = False

                error_msg = str(e).split("Stacktrace:")[0].strip()

                allure.attach(
                    f"Expected : {expected_company_category}\n"
                    f"Actual   : Not Found\n",
                                    name="Audit Name - FAIL",attachment_type=allure.attachment_type.TEXT)

        with allure.step("Validate Contact number"):
            try:
                actual_contact_number = self.wait.until(EC.presence_of_element_located((By.XPATH, f"//tr[.//td[normalize-space()='{expected_register_id}']]//td[5]")))
                highlight_element(self.driver, actual_contact_number)
                actual_contact_number_text = actual_contact_number.text.strip()
                print(f"Expected Contact Number   : {expected_contact_number}")
                print(f"Actual Contact Number     : {actual_contact_number_text}")   

                
                if expected_contact_number == actual_contact_number_text:
                    allure.attach(
                        f"Expected : {expected_contact_number}\n"
                        f"Actual   : {actual_contact_number_text}\n",
                        name="Audit Name - PASS",attachment_type=allure.attachment_type.TEXT)
                else:
                    all_matched = False

                    allure.attach(
                        f"Expected : {expected_contact_number}\n"
                        f"Actual   : {actual_contact_number_text}\n",
                        name="Audit Name - FAIL",attachment_type=allure.attachment_type.TEXT)

            except Exception as e:
                all_matched = False

                error_msg = str(e).split("Stacktrace:")[0].strip()

                allure.attach(
                    f"Expected : {expected_contact_number}\n"
                    f"Actual   : Not Found\n",
                    name="Audit Name - FAIL",attachment_type=allure.attachment_type.TEXT)
        with allure.step("Validate Email ID"):
            try:
                actual_enter_email_id = self.wait.until(EC.presence_of_element_located((By.XPATH, f"//tr[.//td[normalize-space()='{expected_register_id}']]//td[6]")))
                highlight_element(self.driver, actual_enter_email_id)
                actual_enter_email_id_text = actual_enter_email_id.text.strip()
                print(f"Expected Email ID         : {expected_enter_email_id}")
                print(f"Actual Email ID           : {actual_enter_email_id_text}")

                
                if expected_enter_email_id == actual_enter_email_id_text:
                    allure.attach(
                        f"Expected : {expected_enter_email_id}\n"
                        f"Actual   : {actual_enter_email_id_text}\n",
                        name="Audit Name - PASS",attachment_type=allure.attachment_type.TEXT)
                else:
                    all_matched = False

                    allure.attach(
                        f"Expected : {expected_enter_email_id}\n"
                        f"Actual   : {actual_enter_email_id_text}\n",
                        name="Audit Name - FAIL",attachment_type=allure.attachment_type.TEXT)

            except Exception as e:
                all_matched = False

                error_msg = str(e).split("Stacktrace:")[0].strip()

                allure.attach(
                    f"Expected : {expected_enter_email_id}\n"
                    f"Actual   : Not Found\n",
                    name="Audit Name - FAIL",attachment_type=allure.attachment_type.TEXT)
        with allure.step("Final Assignment Validation"):
        
            if all_matched:
                allure.attach(
                    "All Assignment Details Matched Successfully",
                    name="FINAL RESULT - PASS",
                    attachment_type=allure.attachment_type.TEXT
                )
            else:
                allure.attach(
                    "Failed",
                    name="FINAL RESULT - FAIL",
                    attachment_type=allure.attachment_type.TEXT
                )

        assert all_matched, "Assignment validation failed"

    
        
    def audit_company(self):

        self.click_audit()
        self.click_company()
        self.click_new_company()

        expected_company_name = self.enter_company_name()

        expected_register_id = self.register_id()

        self.country_name()
        self.pincode_number()

        expected_company_category = self.click_company_category()

        expected_enter_email_id = self.enter_email_id()

        expected_contact_number = self.click_contact_number()

        self.submit_button()

        self.validate_company_details(
            expected_company_name,
            expected_register_id,
            expected_company_category,
            expected_contact_number,
            expected_enter_email_id
        )

        return True
            
# //div[contains(@class,'overflow-auto') and contains(@class,'rounded-md') and contains(@class,'border')][.//table]