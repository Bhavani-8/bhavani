
import allure
import os
import json
import time
import pytest
import random

from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from utilities.other_utils_functions.highlight import highlight_element
from utilities.other_utils_functions.license_utils import validate_license_subscription
from utilities.add_task_utils import wait_for_loader_to_disappear


def company_details(driver, wait, company_name):

    with allure.step("Load locators.json"):
        try:
            with open(os.path.join("data", "locators.json"), "r") as f:
                elements_details = json.load(f)
            settings_icon = elements_details["settings_icon"]
            toast_msg = elements_details["toast_msg"]
            dashboard_icon = elements_details['dashboard_icon']
            dash_total_btn = elements_details['dash_total_btn']
            column_chooser_btn = elements_details['column_chooser_btn']
            column_chooser_company_project = elements_details['column_chooser_company_project']
            column_chooser_save_btn = elements_details['column_chooser_save_btn']
            column_filter_company_project = elements_details['column_filter_company_project']
            column_filter_ok_btn = elements_details['column_filter_ok_btn']
            select_company_btn = elements_details['select_company_btn']
            add_another_btn = elements_details['add_another_btn']
            company_name_input = elements_details['company_name_input']
            company_type_dropdown_btn = elements_details['company_type_dropdown_btn']
            select_first_option = elements_details['select_first_option']
            select_country_dropdown = elements_details['select_country_dropdown']
            select_country_option = elements_details['select_country_option']
            country_pincode_input = elements_details['country_pincode_input']
            assign_co_officer_btn = elements_details['assign_co_officer_btn']
            co_officer_label = elements_details['co_officer_label']
            select_license_btn = elements_details['select_license_btn']
            license_checkbox_btn = elements_details['license_checkbox_btn']
            select_license = elements_details['select_license']
            inside_add_licenses = elements_details['inside_add_licenses']
            inside_add_company = elements_details['inside_add_company']
            add_license = elements_details['add_license']
            search_input = elements_details['search_input']

           
            print("✅ locators.json loaded successfully")
        except FileNotFoundError as e:
            msg = f"locators.json file not found: {str(e)}"
            print(msg)
            allure.attach(msg, name="Locators File Missing", attachment_type=allure.attachment_type.TEXT)
            return False
        except json.JSONDecodeError as e:
            msg = f"Invalid JSON in locators.json: {str(e)}"
            print(msg)
            allure.attach(msg, name="Locators JSON Error", attachment_type=allure.attachment_type.TEXT)
            return False
    
    with allure.step("👤 Reading User Title from Dashboard"):
        try:
            user_title_elem = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='user-title']")))
            highlight_element(driver, user_title_elem)
            username = user_title_elem.text.strip()
            username = (username.replace('Hi', '').replace('Hello', '').replace(',', '').replace(';', '').strip())
            username = " ".join(username.split())
            print(f"✅ Username detected: {username}")
            allure.attach(username, "Logged-in Username", allure.attachment_type.TEXT)

        except Exception as e:
            msg = f"Failed to Reading user title: {str(e)}"
            print(msg)
            allure.attach(msg, name="Reading user title Error", attachment_type=allure.attachment_type.TEXT)
            raise Exception(msg)
    with allure.step("Create Company"):
        try:
            settings_btn = wait.until(EC.presence_of_element_located((By.XPATH, settings_icon)))
            highlight_element(driver, settings_btn)
            settings_btn.click()
            print("✅ Settings Icon Clicked")
            time.sleep(2)
        except Exception as e:
            msg = f"Failed to Click Settings Icon: {str(e)}"
            print(msg)
            allure.attach(msg, name="Settings Icon Error", attachment_type=allure.attachment_type.TEXT)
            raise Exception(msg)
            
        try: 
            company_btn = wait.until(EC.presence_of_element_located((By.XPATH, select_company_btn)))
            highlight_element(driver, company_btn)
            company_btn.click()
            print("✅ Company Button Clicked")
            time.sleep(2)
        except Exception as e:
            msg = f"Failed to Click Company button: {str(e)}"
            print(msg)
            allure.attach(msg, name="company button Error", attachment_type=allure.attachment_type.TEXT)
            raise Exception(msg)
            
        try:
       
            add_btn = wait.until(EC.presence_of_element_located((By.XPATH, add_another_btn)))
            highlight_element(driver, add_btn)
            add_btn.click()
            print("✅ Add Another Company Button Clicked")
            time.sleep(1)
        except Exception as e:
            msg = f"Failed to Click Add button: {str(e)}"
            print(msg)
            allure.attach(msg, name="Add button Error", attachment_type=allure.attachment_type.TEXT)
            raise Exception(msg)
            
        
    with allure.step("Enter Company Name"):
        try:
            company_input = wait.until(EC.presence_of_element_located((By.XPATH, company_name_input)))
            highlight_element(driver, company_input)
            company_input.click()
            unique_company_name = f"{company_name}_{random.randint(1000, 9999)}"
            company_input.send_keys(unique_company_name)
            # Save latest company name
            company_file = os.path.join("latest_data", "latest_company.txt")
            with open(company_file, "w") as f:
                f.write(unique_company_name)

            print(f"✅ Company Name Created: {unique_company_name}")

            time.sleep(1)

        except Exception as e:
            msg = f"Failed to Enter Company Name: {str(e)}"
            print(msg)
            allure.attach(msg, name="Company name Error", attachment_type=allure.attachment_type.TEXT)
            raise Exception(msg)
            

    with allure.step("Select Company Type"):
        try:
            company_type_dropdown = wait.until(EC.element_to_be_clickable((By.XPATH, company_type_dropdown_btn)))
            highlight_element(driver, company_type_dropdown)
            company_type_dropdown.click()
            time.sleep(0.5)
            first_option = wait.until(EC.element_to_be_clickable((By.XPATH, select_first_option)))
            highlight_element(driver, first_option)
            first_option.click()
            print("✅ Selected first option from Company Type dropdown")
        except Exception as e:
            msg = f"Failed to Click Company Dropdown: {str(e)}"
            print(msg)
            allure.attach(msg, name="Company Dropdown Error", attachment_type=allure.attachment_type.TEXT)
            raise Exception(msg)
            
    with allure.step("Select Country Name"):
        try:
            select_country = wait.until(EC.presence_of_element_located((By.XPATH, select_country_dropdown)))
            highlight_element(driver, select_country)
            select_country.click()
            time.sleep(0.5)
            
            country_option = wait.until(EC.presence_of_element_located((By.XPATH, select_country_option)))
            highlight_element(driver, country_option)
            country_option.click()
        except Exception as e:
            msg = f"Failed to Select Country name: {str(e)}"
            print(msg)
            allure.attach(msg, name="Country name Error", attachment_type=allure.attachment_type.TEXT)
            raise Exception(msg)
            
    with allure.step("Enter Pincode Number"):
        try:
            pincode_input = wait.until(EC.presence_of_element_located((By.XPATH, country_pincode_input)))
            highlight_element(driver, pincode_input)
            pincode_input.send_keys("400092")
            wait_for_loader_to_disappear(driver, wait)
            time.sleep(3)
        except Exception as e:
            msg = f"Failed to Enter Pincode number: {str(e)}"
            print(msg)
            allure.attach(msg, name="Pincode number Error", attachment_type=allure.attachment_type.TEXT)
            raise Exception(msg)
              

    with allure.step("Assign Compliance Officer"):
        try:
            assign_btn = wait.until(EC.presence_of_element_located((By.XPATH, assign_co_officer_btn)))
            highlight_element(driver, assign_btn)
            assign_btn.click()
            time.sleep(0.5)

            assign_to_me_elem = wait.until(EC.presence_of_element_located((By.XPATH, f"//div[text()='{username}']")))
            highlight_element(driver, assign_to_me_elem)
            assign_to_me_elem.click()

            compliance_officer_label = wait.until(EC.presence_of_element_located((By.XPATH, co_officer_label)))
            compliance_officer_label.click()
        except Exception as e:
            msg = f"Failed to select assign name: {str(e)}"
            print(msg)
            allure.attach(msg, name="Assign name Error", attachment_type=allure.attachment_type.TEXT)
            raise Exception(msg)
            
    
    with allure.step("Add License"):
        try:
            license_btn = wait.until(EC.presence_of_element_located((By.XPATH, add_license)))
            highlight_element(driver, license_btn)
            license_btn.click()

            choose_license_btn = wait.until(EC.presence_of_element_located((By.XPATH, select_license_btn)))
            highlight_element(driver, choose_license_btn)
            choose_license_btn.click()

            license_checkbox = wait.until(EC.presence_of_element_located((By.XPATH, license_checkbox_btn)))
            highlight_element(driver, license_checkbox)
            license_checkbox.click()

            choose_licenses = wait.until(EC.presence_of_element_located((By.XPATH, select_license)))
            choose_licenses.click()
            time.sleep(1)

            add_license_btn = wait.until(EC.presence_of_element_located((By.XPATH, inside_add_licenses)))
            highlight_element(driver, add_license_btn)
            add_license_btn.click()
            print("✅ License Added")

        except Exception as e:
            msg = f"Failed to Click License button: {str(e)}"
            print(msg)
            allure.attach(msg, name="License button Error", attachment_type=allure.attachment_type.TEXT)
            raise Exception(msg)
            
    with allure.step("Add Company"):
        try:
            add_company_btn = wait.until(EC.element_to_be_clickable((By.XPATH, inside_add_company)))
            highlight_element(driver, add_company_btn)

            driver.execute_script("arguments[0].scrollIntoView(true);", add_company_btn)
            time.sleep(0.5)
            driver.execute_script("arguments[0].click();", add_company_btn)
            time.sleep(3)

            print("🟦 Add Company clicked")

        except Exception as e:
            msg = f"Failed to click add company button: {str(e)}"
            print(msg)
            allure.attach(msg, name="Company button Error", attachment_type=allure.attachment_type.TEXT)
            raise Exception(msg)
            

    with allure.step("Toast Msg"):
        try:
            toast = wait.until(EC.presence_of_element_located((By.XPATH, toast_msg)))
            highlight_element(driver, toast)
            print(f"📢 Toast message: {toast.text.strip()}")
            time.sleep(7)
        except Exception as e:
            msg = f"Toast message not found: {str(e)}"
            print(msg)
            allure.attach(str(e), name="Toast message Error", attachment_type=allure.attachment_type.TEXT)
            raise Exception(msg)
            
    with allure.step("Fetch Company Name from Company Details"):
        try:
            company_name_elem = wait.until(EC.visibility_of_element_located((By.XPATH, f"//td[contains(text(),'{company_name}')]")))
            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", company_name_elem)
            highlight_element(driver, company_name_elem, 0.2)
            fetched_company = company_name_elem.text.strip()
            print(f"Company Name from Settings: {fetched_company}")
            allure.attach(fetched_company,name="Settings Company Name",attachment_type=allure.attachment_type.TEXT)
            
            time.sleep(2)
        # personal_btn = wait.until(EC.presence_of_element_located((By.XPATH, "//span[text()='Personal']")))
        # driver.execute_script("arguments[0].scrollIntoView({block:'center'});", personal_btn)
        # highlight_element(driver, personal_btn)
        # personal_btn.click()
        # print("✅ Personal Details tab clicked")
        
        # time.sleep(1)
        # license_option = wait.until(EC.presence_of_element_located((By.XPATH, "//button[.//span[text()='BSE']]")))
        # highlight_element(driver, license_option)
        # license_option.click()

        # save_btn = wait.until(EC.presence_of_element_located((By.XPATH, "(//button[text()='Save Changes'])[2]")))
        # driver.execute_script("""arguments[0].scrollIntoView({block:'center', behavior:'instant'});""", save_btn)
        # highlight_element(driver, save_btn)
        # save_btn.click()
        # time.sleep(2)
    
        except Exception as e:
            msg = f"Failed to Fetch company name: {str(e)}"
            print(msg)
            allure.attach(msg, name="Fetch company name Error", attachment_type=allure.attachment_type.TEXT)
            raise Exception(msg)
    with allure.step("Open Dashboard"):
        try:
            
            dashboard_icon_elem = wait.until(EC.presence_of_element_located((By.XPATH, dashboard_icon)))
            highlight_element(driver, dashboard_icon_elem)
            dashboard_icon_elem.click()
            time.sleep(2)
            wait_for_loader_to_disappear(driver, wait)
            print("✅ Dashboard icon clicked")
        except Exception as e:
            msg = f"Failed to click Dashboard Icon: {str(e)}"
            allure.attach(str(e), name="Dashboard Open Error", attachment_type=allure.attachment_type.TEXT)
            raise Exception(msg)
    with allure.step("Validate License Subscription after login"):
        try:
            if validate_license_subscription(driver):
                print("✅ License present")
            else:
                print("ℹ️ License not present — continue")

        except Exception as e:
            print(f"⚠️ Error occurred — continue: {e}")
    with allure.step("Clicking Dashboard Total button"):
        try:
            wait_for_loader_to_disappear(driver, wait)
            total_tab = wait.until(EC.element_to_be_clickable((By.XPATH, dash_total_btn)))
            highlight_element(driver, total_tab)
            total_tab.click()
            wait_for_loader_to_disappear(driver, wait)
            time.sleep(2)
        except Exception as e:
            msg = f"Failed to Click Total tab: {str(e)}"
            print(msg)
            allure.attach(msg, name="Total tab Error", attachment_type=allure.attachment_type.TEXT)
            raise Exception(msg)
    with allure.step("Open Column Chooser from task list"):
        try:
            column_chooser_btn_elem = wait.until(EC.presence_of_element_located((By.XPATH, column_chooser_btn)))
            highlight_element(driver, column_chooser_btn_elem)
            driver.execute_script("arguments[0].click();", column_chooser_btn_elem)
            print("Clicked Column Chooser button")
            wait_for_loader_to_disappear(driver, wait)
        except Exception as e:
            msg = f"Failed to Click Column chooser button: {str(e)}"
            print(msg)
            allure.attach(msg, name="Column chooser Error", attachment_type=allure.attachment_type.TEXT)
            raise Exception(msg)
    
        def get_state(elem):
            """
            Returns: 'selected', 'deselected', 'mixed'
            """
            aria = elem.get_attribute("aria-checked")
            if aria == "true":
                return "selected"
            elif aria == "false":
                return "deselected"
            else:
                return "mixed"   

        try:
            select_all_checkbox = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".dx-list-select-all-checkbox")))
            driver.execute_script("arguments[0].scrollIntoView(true);", select_all_checkbox)
            time.sleep(0.2)

            state = get_state(select_all_checkbox)
            print(f"➤ Initial 'Select All' state: {state}")
            if state == "deselected":
                print("✅ Already deselected, no action needed")
            elif state == "selected":
                print("🔁 Deselecting 'Select All'")
                driver.execute_script("arguments[0].click();", select_all_checkbox)
                wait_for_loader_to_disappear(driver, wait)
                time.sleep(0.3)
            elif state == "mixed":
                print("🔁 Mixed state detected → select all → deselect")
                driver.execute_script("arguments[0].click();", select_all_checkbox)
                wait_for_loader_to_disappear(driver, wait)
                time.sleep(0.3)
                select_all_checkbox = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".dx-list-select-all-checkbox")))
                driver.execute_script("arguments[0].click();", select_all_checkbox)
                wait_for_loader_to_disappear(driver, wait)
                time.sleep(0.3)

            select_all_checkbox = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".dx-list-select-all-checkbox")))
            final_state = get_state(select_all_checkbox)
            print(f"➤ Final 'Select All' state: {final_state}")

            if final_state != "deselected":
                pytest.fail(f"❌ Select All normalization failed, state: {final_state}")

            print("✅ 'Select All' normalized successfully")

        except Exception as e:
            msg = f"Failed to Selecting all: {str(e)}"
            print(msg)
            allure.attach(msg, name="Selecting all Error", attachment_type=allure.attachment_type.TEXT)
            raise Exception(msg)
    with allure.step("Select 'Company / Project from Column Chooser"): 
        try:
            company_project_option_elm = wait.until(EC.presence_of_element_located((By.XPATH, column_chooser_company_project)))
            actions = ActionChains(driver)
            actions.move_to_element(company_project_option_elm).perform()
            time.sleep(0.5)
            company_project_option_elm.click()

            save_btn = wait.until(EC.element_to_be_clickable((By.XPATH, column_chooser_save_btn)))
            highlight_element(driver, save_btn)
            save_btn.click()
            time.sleep(2)
            print("✅ Column Chooser saved")
            wait_for_loader_to_disappear(driver, wait)

        except Exception as e:
            msg = f"Failed to Clicking Company/project option: {str(e)}"
            print(msg)
            allure.attach(msg, name="Approver Option Error", attachment_type=allure.attachment_type.TEXT)
            raise Exception(msg)
    with allure.step(f"Click Company/Project and License filter option"): 
        try:
            company_project_filter_btn = wait.until(EC.presence_of_element_located((By.XPATH, column_filter_company_project)))
            time.sleep(2)
            highlight_element(driver, company_project_filter_btn)
            company_project_filter_btn.click()
            wait_for_loader_to_disappear(driver, wait)
            
            search_input = wait.until(EC.visibility_of_element_located((By.XPATH, search_input)))
            search_input.clear()
            search_input.send_keys(unique_company_name)
            wait_for_loader_to_disappear(driver, wait)
            time.sleep(5)

            company_option = wait.until(EC.element_to_be_clickable((By.XPATH, f"//div[contains(@class,'dx-list-item-content') and normalize-space()='{unique_company_name}']")))
            highlight_element(driver, company_option)
            company_option.click()
        
            column_filter_ok = wait.until(EC.presence_of_element_located((By.XPATH, column_filter_ok_btn)))
            column_filter_ok.click()
            wait_for_loader_to_disappear(driver, wait)
            time.sleep(5)
        except Exception as e:
            msg = f"Failed to Open Company Project filter: {str(e)}"
            print(msg)
            allure.attach(msg, name="Company Project filter Error", attachment_type=allure.attachment_type.TEXT)
            raise Exception(msg)

    with allure.step("Fetch Company Name from Dashboard"):
        try:
            company_project_elem = wait.until(EC.visibility_of_element_located((By.XPATH, f"//td//p[contains(normalize-space(),'{unique_company_name}')]")))
            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", company_project_elem)
            highlight_element(driver, company_project_elem, 0.2)
            fetched_dashboard_company = company_project_elem.text.strip()
            print(f"Company Name from Dashboard: {fetched_dashboard_company}")
            allure.attach(fetched_dashboard_company,name="Dashboard Company Name",attachment_type=allure.attachment_type.TEXT)
        except Exception as e:
            msg = f"Failed to Fetch Company name: {str(e)}"
            print(msg)
            allure.attach(msg, name="Fetch Company name Error", attachment_type=allure.attachment_type.TEXT)
            raise Exception(msg)
    with allure.step("Verify Company Name in Dashboard"):
        try:
            # If dashboard text contains extra values like company/license
            if unique_company_name in fetched_dashboard_company:
                print("✅ Company Name Verified successfully!")

                allure.attach(f"Expected Company: {unique_company_name}\n"f"Dashboard Company: {fetched_dashboard_company}",name="Company Name Check",attachment_type=allure.attachment_type.TEXT)
                time.sleep(2)
                return True

            else:
                error_msg = (f"❌ Company Name Mismatch!\n"f"Expected: {unique_company_name}\n"f"Settings Company: {fetched_company}\n"f"Dashboard Company: {fetched_dashboard_company}")
                print(error_msg)
                allure.attach(error_msg, name="Company name Error", attachment_type=allure.attachment_type.TEXT)
               

        except Exception as e:
            msg = f"Failed to Validate company name: {str(e)}"
            print(msg)
            allure.attach(msg, name="Company name Error", attachment_type=allure.attachment_type.TEXT)
            raise Exception(msg)
    return True