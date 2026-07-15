from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import allure 
import os
import json
import pytest
import time

from selenium.common.exceptions import TimeoutException
from utilities.other_utils_functions.highlight import highlight_element
from selenium.webdriver import ActionChains
from utilities.other_utils_functions.license_utils import validate_license_subscription
from utilities.add_task_utils import wait_for_loader_to_disappear
from selenium.common.exceptions import StaleElementReferenceException

def license_task(driver, wait, company_name, license_name):
    wait_less = WebDriverWait(driver, 5)
    # ------------------------------------------
    # STEP 1: LOAD LOCATORS
    # ------------------------------------------
    with allure.step("Load locators.json"):
        try:
            with open(os.path.join("data", 'locators.json'), 'r') as f:
                elements_details = json.load(f)
                dash_total_btn = elements_details['dash_total_btn']
                column_chooser_btn = elements_details['column_chooser_btn']
                column_chooser_company_project = elements_details['column_chooser_company_project']
                column_chooser_save_btn = elements_details['column_chooser_save_btn']
                column_filter_company_project= elements_details['column_filter_company_project']
                column_filter_ok_btn = elements_details['column_filter_ok_btn']
                column_filter_cancel_btn = elements_details['column_filter_cancel_btn']
                task_open_btn = elements_details['task_open_btn']
                dash_not_assigned_tab = elements_details['dash_not_assigned_tab']
                dashboard_icon = elements_details['dashboard_icon']
                task_license_close_btn = elements_details['task_license_close_btn']
                task_company_label = elements_details['task_company_label']
                task_license_label = elements_details['task_license_label']
                column_chooser_license = elements_details['column_chooser_license']
                column_filter_license = elements_details['column_filter_license']
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

    with allure.step("Open Dashboard"):
        try:
            time.sleep(2)
            dashboard_icon_elem = wait.until(EC.presence_of_element_located((By.XPATH, dashboard_icon)))
            highlight_element(driver, dashboard_icon_elem)
            dashboard_icon_elem.click()
            time.sleep(1)
            wait_for_loader_to_disappear(driver, wait)
            print("✅ Dashboard icon clicked")
        except Exception as e:
            msg = f"Failed to Click Dashboard Icon: {str(e)}"
            print(msg)
            allure.attach(msg, name="Dashboard Icon Error", attachment_type=allure.attachment_type.TEXT)
            raise Exception(msg)

    # with allure.step("Validate License Subscription after login"):
    #     try:
    #         validate_license_subscription(driver)
    #         print("✅ License subscription validated successfully")
    #     except Exception as e:
    #         allure.attach(str(e), name="License Validation Error", attachment_type=allure.attachment_type.TEXT)
    #         return False
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
    with allure.step("Clicking Not Assigned Tab"):
        try:
            not_assigned_tab = wait.until(EC.element_to_be_clickable((By.XPATH, dash_not_assigned_tab)))
            not_assigned_tab.click()
            time.sleep(1)
            wait_for_loader_to_disappear(driver, wait)
        except Exception as e:
            msg = f"Failed to Click Not Assigned Tab: {str(e)}"
            print(msg)
            allure.attach(msg, name="Not Assigned Tab Error", attachment_type=allure.attachment_type.TEXT)
            raise Exception(msg)
         
    with allure.step("Open Column Chooser from task list"):
        column_chooser_btn_elem = wait.until(EC.presence_of_element_located((By.XPATH, column_chooser_btn)))
        highlight_element(driver, column_chooser_btn_elem)
        driver.execute_script("arguments[0].click();", column_chooser_btn_elem)
        print("Clicked Column Chooser button")
        wait_for_loader_to_disappear(driver, wait)
    
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
    with allure.step("Select 'Company / Project, License' from Column Chooser"): 
        try:
            company_project_option_elm = wait.until(EC.presence_of_element_located((By.XPATH, column_chooser_company_project)))
            actions = ActionChains(driver)
            actions.move_to_element(company_project_option_elm).perform()
            time.sleep(0.5)
            company_project_option_elm.click()
        except Exception as e:
            msg = f"Failed to Select Company project: {str(e)}"
            print(msg)
            allure.attach(msg, name="Selecting all Error", attachment_type=allure.attachment_type.TEXT)
            raise Exception(msg)
        try:
            license_option = wait.until(EC.presence_of_element_located((By.XPATH, column_chooser_license)))
            actions = ActionChains(driver)
            actions.move_to_element(license_option).perform()
            time.sleep(0.5)
            license_option.click()
        except Exception as e:
            msg = f"Failed to Select License Option {str(e)}"
            print(msg)
            allure.attach(msg, name="Selecting all Error", attachment_type=allure.attachment_type.TEXT)
            raise Exception(msg)
        try:
            save_btn = wait.until(EC.element_to_be_clickable((By.XPATH, column_chooser_save_btn)))
            highlight_element(driver, save_btn)
            save_btn.click()
            time.sleep(2)
            print("✅ Column Chooser saved")

        except Exception as e:
            msg = f"Failed to Save Button: {str(e)}"
            print(msg)
            allure.attach(msg, name="Save Button Error", attachment_type=allure.attachment_type.TEXT)
            raise Exception(msg)
    with allure.step(f"Open Company/Project filter"):
        company_file = os.path.join("latest_data", "latest_company.txt")
        with open(company_file, "r") as f:
            created_company_name = f.read().strip()
        company_project_filter_btn = wait.until(EC.presence_of_element_located((By.XPATH, column_filter_company_project)))
        highlight_element(driver, company_project_filter_btn)
        company_project_filter_btn.click()
        wait_for_loader_to_disappear(driver, wait)
        time.sleep(3)

        search_input = wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@aria-label='Search' and contains(@class,'dx-texteditor-input')]")))
        search_input.clear()
        search_input.send_keys(created_company_name)
        wait_for_loader_to_disappear(driver, wait)
        time.sleep(3)

    try:
        company_option = wait.until(EC.element_to_be_clickable((By.XPATH, f"//div[contains(@class,'dx-list-item-content') and normalize-space()='{created_company_name}']")))
        highlight_element(driver, company_option)
        company_option.click()

    except Exception as e:
        msg = f"Failed to License Option: {str(e)}"
        print(msg)
        allure.attach(msg, name="License Option Error", attachment_type=allure.attachment_type.TEXT)
        raise Exception(msg)

    try:
        column_filter_ok = wait.until(EC.presence_of_element_located((By.XPATH, column_filter_ok_btn)))
        column_filter_ok.click()
    except Exception as e:
        msg = f"Failed to Click Column Filter OK Button: {str(e)}"
        print(msg)
        allure.attach(msg, name="Column Filter OK Button Error", attachment_type=allure.attachment_type.TEXT)
        raise Exception(msg)
    
    wait_for_loader_to_disappear(driver, wait)
    time.sleep(4)

    with allure.step("Open License filter"):
        try:
            license_filter_btn = wait_less.until(EC.presence_of_element_located((By.XPATH, column_filter_license)))
            highlight_element(driver, license_filter_btn)
            license_filter_btn.click()
            wait_for_loader_to_disappear(driver, wait)
            time.sleep(4)

            search_input = wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@aria-label='Search' and contains(@class,'dx-texteditor-input')]")))
            search_input.clear()
            search_input.send_keys(license_name)
            wait_for_loader_to_disappear(driver, wait)
            time.sleep(4)
        except Exception as e:
            msg = f"Failed to Open License filter: {str(e)}"
            print(msg)
            allure.attach(msg, name="License filter Error", attachment_type=allure.attachment_type.TEXT)
            raise Exception(msg)

    try:
        license_option = wait.until(EC.element_to_be_clickable((By.XPATH, f"//div[contains(@class,'dx-list-item-content') and normalize-space()='{license_name}']")))
        highlight_element(driver, license_option)
        license_option.click()  
        time.sleep(3)
    except Exception as e:
        msg = f"Failed to License Option: {str(e)}"
        print(msg)
        allure.attach(msg, name="License Option Error", attachment_type=allure.attachment_type.TEXT)
        raise Exception(msg)

    try:
        column_filter_ok = wait.until(EC.presence_of_element_located((By.XPATH, column_filter_ok_btn)))
        column_filter_ok.click()
        time.sleep(3)
    except Exception as e:
        msg = f"Failed to Click Column Filter OK Button: {str(e)}"
        print(msg)
        allure.attach(msg, name="Column Filter OK Button Error", attachment_type=allure.attachment_type.TEXT)
        raise Exception(msg)
    
    wait_for_loader_to_disappear(driver, wait)
    time.sleep(6)

    with allure.step("Click on task from table to open details"):
        try:
            task_open_btn_elem = wait.until(EC.element_to_be_clickable((By.XPATH, task_open_btn)))
            highlight_element(driver, task_open_btn_elem)
            try:
                task_open_btn_elem.click()
            except Exception:
                driver.execute_script("arguments[0].scrollIntoView(true);", task_open_btn_elem)
                driver.execute_script("arguments[0].click();", task_open_btn_elem)
            print("✅ Task opened from table")
            time.sleep(1)
            wait_for_loader_to_disappear(driver, wait)
        except Exception as e:
            msg = f"Failed to Click Task Open button: {str(e)}"
            print(msg)
            allure.attach(msg, name="Task Open Button Error", attachment_type=allure.attachment_type.TEXT)
            raise Exception(msg)
    with allure.step("Validate Company name and License in Task Details"):
        try:
            task_company_license_label_elem = wait.until(EC.visibility_of_element_located((By.XPATH, task_company_label)))
            highlight_element(driver, task_company_license_label_elem, 0.2)
            fetched_company = task_company_license_label_elem.text.strip()
            print(f"Company: {fetched_company}")

            task_license_label_elem = wait.until(EC.visibility_of_element_located((By.XPATH, task_license_label)))
            highlight_element(driver, task_license_label_elem, 0.2)
            fetched_license = task_license_label_elem.text.strip()
            print(f"License: {fetched_license}")
        
    
        except Exception as e:
            msg = f"Failed to Validate Comapny name and License: {str(e)}"
            print(msg)
            allure.attach(msg, name="Validate Company name and License Error", attachment_type=allure.attachment_type.TEXT)
            raise Exception(msg)
    with allure.step("Click Task window close button"):
        try:
            
            close_btn = wait.until(EC.presence_of_element_located((By.XPATH, task_license_close_btn)))
            highlight_element(driver, close_btn)
            close_btn.click()
            time.sleep(2)
            print("✅ Task WindowClose Button clicked")
        except Exception as e:
            msg = f"Failed to Click Task window close button: {str(e)}"
            print(msg)
            allure.attach(msg, name="Click Task window close button Error", attachment_type=allure.attachment_type.TEXT)
            raise Exception(msg)
    with allure.step("Click reset button on task details"):
        try: 
            reset_btn = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@title='Reset Filters']")))
            highlight_element(driver, reset_btn)
            reset_btn.click()
            time.sleep(2)
            print("✅ Reset Button Clicked")
        except Exception as e:
            msg = f"Failed to Click Reset button: {str(e)}"
            print(msg)
            allure.attach(msg, name="Click Reset button Error", attachment_type=allure.attachment_type.TEXT)
            raise Exception(msg)
    return True
    