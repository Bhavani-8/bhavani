import allure
import os
import json
import time
import pytest

from selenium.webdriver import ActionChains

import time
import allure
from selenium.common.exceptions import TimeoutException
from utilities.add_task_functions.wait_for_loader_to_disappear import wait_for_loader_to_disappear
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from utilities.other_utils_functions.highlight import highlight_element
from utilities.add_task_utils import wait_for_loader_to_disappear

def mark_circular_as_na(driver, wait, company_name, license_name):

    with allure.step("Load locators.json"):
        try:
            with open(os.path.join("data", "locators.json"), "r") as f:
                elements_details = json.load(f)
            dashboard_icon = elements_details["dashboard_icon"]
            settings_icon = elements_details["settings_icon"]
            toast_msg = elements_details["toast_msg"]
            column_chooser_btn = elements_details['column_chooser_btn']
            column_chooser_save_btn = elements_details['column_chooser_save_btn']
            task_open_btn = elements_details['task_open_btn']
            column_chooser_company_project = elements_details['column_chooser_company_project']
            column_chooser_license = elements_details['column_chooser_license']
            column_filter_company_project = elements_details['column_filter_company_project']
            column_filter_search_input = elements_details['column_filter_search_input']
            column_filter_ok_btn = elements_details['column_filter_ok_btn']
            column_filter_cancel_btn = elements_details['column_filter_cancel_btn']
            dash_total_btn = elements_details['dash_total_btn']
            task_search_btn = elements_details['task_search_btn']
            task_search_input = elements_details['task_search_input']
            task_license_label = elements_details['task_license_label']
            task_license_close_btn = elements_details['task_license_close_btn']
            task_search_close_btn = elements_details['task_search_close_btn'] 
            column_filter_license = elements_details['column_filter_license']
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
            print("✅ Dashboard icon clicked")
        except Exception as e:
            msg = f"Failed to Click Dashboard Icon: {str(e)}"
            print(msg)
            allure.attach(msg, name="Dashboard Icon Error", attachment_type=allure.attachment_type.TEXT)
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
    with allure.step("Select 'Company / Project' from Column Chooser"): 
        try:
            company_project_option_elm = wait.until(EC.presence_of_element_located((By.XPATH, column_chooser_company_project)))
            actions = ActionChains(driver)
            actions.move_to_element(company_project_option_elm).perform()
            time.sleep(0.5)
            company_project_option_elm.click()

            license_option = wait.until(EC.presence_of_element_located((By.XPATH, column_chooser_license)))
            actions = ActionChains(driver)
            actions.move_to_element(license_option).perform()
            time.sleep(0.5)
            # wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='dx-item-content dx-list-item-content' and normalize-space()='Assign To']")))
            license_option.click()

            save_btn = wait.until(EC.element_to_be_clickable((By.XPATH, column_chooser_save_btn)))
            highlight_element(driver, save_btn)
            save_btn.click()
            wait_for_loader_to_disappear(driver, wait)
            time.sleep(2)
            print("✅ Column Chooser saved")

        except Exception as e:
            msg = f"Failed to Clicking License option: {str(e)}"
            print(msg)
            allure.attach(msg, name="License Option Error", attachment_type=allure.attachment_type.TEXT)
            raise Exception(msg)
    with allure.step(f"Open Company/Project filter and search for company"):
        company_file = os.path.join("latest_data", "latest_company.txt")
        with open(company_file, "r") as f:
            created_company_name = f.read().strip()
        company_project_filter_btn = wait.until(EC.presence_of_element_located((By.XPATH, column_filter_company_project)))
        highlight_element(driver, company_project_filter_btn)
        company_project_filter_btn.click()
        time.sleep(3)

        search_input = wait.until(EC.presence_of_element_located((By.XPATH, column_filter_search_input)))
        search_input.clear()
        search_input.send_keys(created_company_name)
        time.sleep(6)

    try:
        search_task = wait.until(EC.presence_of_element_located((By.XPATH, f"//div[contains(@class,'dx-list-item-content') and normalize-space()='{created_company_name}']")))
        search_task.click()
        time.sleep(4)
        print("✅ Clicked 'Company'")
    
    except Exception as e:
        msg = f"Failed to Search Task: {str(e)}"
        print(msg)
        allure.attach(msg, name="Search Task Error", attachment_type=allure.attachment_type.TEXT)
        raise Exception(msg)
    try:
    
        column_filter_ok = wait.until(EC.presence_of_element_located((By.XPATH, column_filter_ok_btn)))
        column_filter_ok.click()
        time.sleep(4)
    except Exception as e:
        msg = f"Failed to Click Column Filter OK Button: {str(e)}"
        print(msg)
        allure.attach(msg, name="Column Filter OK Button Error", attachment_type=allure.attachment_type.TEXT)
        raise Exception(msg)
    

    with allure.step(f"Open License filter"):
        license_filter_btn = wait.until(EC.presence_of_element_located((By.XPATH, column_filter_license)))
        license_filter_btn.click()
        wait_for_loader_to_disappear(driver, wait)
        highlight_element(driver, license_filter_btn)
        time.sleep(4)

        search_input = wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@aria-label='Search' and contains(@class,'dx-texteditor-input')]")))
        search_input.clear()
        search_input.send_keys(license_name)
        wait_for_loader_to_disappear(driver, wait)
        time.sleep(3)

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
    except Exception as e:
        msg = f"Failed to Click Column Filter OK Button: {str(e)}"
        print(msg)
        allure.attach(msg, name="Column Filter OK Button Error", attachment_type=allure.attachment_type.TEXT)
        raise Exception(msg)
    
    wait_for_loader_to_disappear(driver, wait)
    time.sleep(4)

    with allure.step("Opening task from table"):
        try:
            task_open_btn_elem = wait.until(EC.element_to_be_clickable((By.XPATH, task_open_btn)))
            highlight_element(driver, task_open_btn_elem)
            fetched_license_task = task_open_btn_elem.text.strip()
            print(f"Task to open: {fetched_license_task}")
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
    with allure.step("Fetch the License task name from the opened task details page"):
        try:
            time.sleep(4)
            license_task_name_btn = wait.until(EC.visibility_of_element_located((By.XPATH, "//p[contains(@class,'task-details-sub-title') and @title]")))
            highlight_element(driver, license_task_name_btn)
            license_task_name = license_task_name_btn.text.strip()
            time.sleep(0.5)
            print("✅ Project Submit clicked")
        except Exception as e:
            msg = f"Failed to Fetch the License task name: {str(e)}"
            print(msg)
            allure.attach(msg, name="Fetch the License task name Error", attachment_type=allure.attachment_type.TEXT)
            raise Exception(msg)
    with allure.step("Click Not Applicable"):
        try:
            not_applicable = wait.until(EC.presence_of_element_located((By.XPATH, "//button[@title='Not Applicable']")))
            highlight_element(driver, not_applicable)
            not_applicable.click()
            time.sleep(1)
        except Exception as e:
            msg = f"Failed to Click Not Applicable: {str(e)}"
            print(msg)
            allure.attach(msg, name="Not Applicable Error", attachment_type=allure.attachment_type.TEXT)
            raise Exception(msg)

    with allure.step("Click Are you sure you want to mark this task as 'Not Applicable'?"):
        try:
            confirm_btn = wait.until(EC.presence_of_element_located((By.XPATH, "//button//span[text()='Confirm']")))
            highlight_element(driver, confirm_btn)
            confirm_btn.click()
            time.sleep(1)
        except Exception as e:
            msg = f"Failed to click Confirm Button: {str(e)}"
            print(msg)
            allure.attach(str(e), name="Confirm Button Error", attachment_type=allure.attachment_type.TEXT)
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
    with allure.step("Verify Not Applicable Task"):
        try:
            dashboard_btn = wait.until(EC.visibility_of_element_located((By.XPATH,  "//h2[text()=\"We couldn't locate this task\"]")))
            highlight_element(driver, dashboard_btn)
            fetched_task_name = dashboard_btn.text.strip()
            print(f"Task Window: {fetched_task_name}")
            allure.attach(f"Task Window: {fetched_task_name}", name="Task Window", attachment_type=allure.attachment_type.TEXT)   
            # step_fail(driver, "Verify Not Applicable Task", f"Dashboard with title: {fetched_task_name}")
        except Exception as e:
            msg = f"Failed to Click Dashboard Icon: {str(e)}"
            print(msg)
            allure.attach(msg, name="Dashboard Icon Error", attachment_type=allure.attachment_type.TEXT)
            raise Exception(msg)
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
    with allure.step("Search for the newly created task"):
        try:
            search_icon_btn = wait.until(EC.presence_of_element_located((By.XPATH, task_search_btn)))
            highlight_element(driver, search_icon_btn)
            search_icon_btn.click()

            search_input = wait.until(EC.visibility_of_element_located((By.XPATH, task_search_input)))
            highlight_element(driver, search_input)
            search_input.clear()
            search_input.send_keys(license_task_name)

            wait_for_loader_to_disappear(driver, wait)
            time.sleep(4)  # Extra wait to ensure results load
        except Exception as e:
            msg = f"Failed to Click Search Icon: {str(e)}"
            print(msg)
            allure.attach(msg, name="Search Icon Error", attachment_type=allure.attachment_type.TEXT)
            raise Exception(msg)
    with allure.step("Click close button on task details panel"):
        try:
            search_close_btn = wait.until(EC.presence_of_element_located((By.XPATH, task_search_close_btn)))
            highlight_element(driver, search_close_btn)
            search_close_btn.click()
            wait_for_loader_to_disappear(driver, wait)
            time.sleep(3)
            print("✅ Project Submit clicked")
        except Exception as e:
            msg = f"Failed to Click Search close button: {str(e)}"
            print(msg)
            allure.attach(msg, name="Search close button Error", attachment_type=allure.attachment_type.TEXT)
            raise Exception(msg)
    with allure.step("Click Settings"):
        try:
            settings_btn = wait.until(EC.presence_of_element_located((By.XPATH, settings_icon)))
            highlight_element(driver, settings_btn)
            settings_btn.click()
        except Exception as e:
            msg = f"Failed to Click Settings Icon: {str(e)}"
            print(msg)
            allure.attach(msg, name="Settings Icon Error", attachment_type=allure.attachment_type.TEXT)
            raise Exception(msg)
    
    with allure.step("Click Not Applicable"):
        try:
            not_applicable_tasks_btn = wait.until(EC.presence_of_element_located((By.XPATH, "//span[text()='Not Applicable tasks']")))
            highlight_element(driver,  not_applicable_tasks_btn)
            not_applicable_tasks_btn.click()
        except Exception as e:
            msg = f"Failed to Click Not Applicable: {str(e)}"
            print(msg)
            allure.attach(msg, name="Not Applicable Error", attachment_type=allure.attachment_type.TEXT)
            raise Exception(msg)
    wait_for_loader_to_disappear(driver, wait)
    time.sleep(3)
    
    with allure.step("Click Mark Applicable"):
        try:
            task_name_elem = wait.until(
            EC.presence_of_element_located((By.XPATH, f"//td[normalize-space()='{company_name}']/ancestor::tr//div[contains(@class,'wrap-break-word')]")))
            task_name = task_name_elem.text.strip()

            print(f"🔹 Task Name: {task_name}")

            allure.attach(task_name,name="Task Name Before Mark Applicable",attachment_type=allure.attachment_type.TEXT)
            applicable_tasks_btn = wait.until(EC.presence_of_element_located((By.XPATH, f"//td[normalize-space()='{company_name}']/ancestor::tr//button[normalize-space()='Mark Applicable']")))
            highlight_element(driver,  applicable_tasks_btn)
            driver.execute_script("arguments[0].scrollIntoView(true);", applicable_tasks_btn)
            applicable_tasks_btn.click()
        except Exception as e:
            msg = f"Failed to Click  Mark Applicable: {str(e)}"
            print(msg)
            allure.attach(msg, name=" Mark Applicable Error", attachment_type=allure.attachment_type.TEXT)
            raise Exception(msg)
    with allure.step("Click Are you sure you want to mark this task as 'Mark Applicable'?"):
        try:
            yes_btn = wait.until(EC.presence_of_element_located((By.XPATH, "//button[text()='Yes']")))
            highlight_element(driver, yes_btn)
            yes_btn.click()
            time.sleep(1)
        except Exception as e:
            msg = f"Failed to Click Yes Button: {str(e)}"
            print(msg)
            allure.attach(msg, name="Yes button Error", attachment_type=allure.attachment_type.TEXT)
            raise Exception(msg)
    wait_for_loader_to_disappear(driver, wait)
    time.sleep(3)

    with allure.step("Click Dashboard Icon"):
        try:
            time.sleep(3)
            dashboard_icon_elem = wait.until(EC.presence_of_element_located((By.XPATH, dashboard_icon)))
            highlight_element(driver, dashboard_icon_elem)
            dashboard_icon_elem.click()
            print("✅ Dashboard icon clicked")
        except Exception as e:
            msg = f"Failed to Click Dashboard Icon: {str(e)}"
            print(msg)
            allure.attach(msg, name="Dashboard Icon Error", attachment_type=allure.attachment_type.TEXT)
            raise Exception(msg)
    with allure.step("Click Dashboard Total button"):
        try:
            wait_for_loader_to_disappear(driver, wait)
            total_tab = wait.until(EC.element_to_be_clickable((By.XPATH, dash_total_btn)))
            highlight_element(driver, total_tab)
            total_tab.click()
            wait_for_loader_to_disappear(driver, wait)
        except Exception as e:
            msg = f"Failed to Click Total tab: {str(e)}"
            print(msg)
            allure.attach(msg, name="Total tab Error", attachment_type=allure.attachment_type.TEXT)
            raise Exception(msg)
    with allure.step("Search for the newly created task by name"):
        try:
            search_icon_btn = wait.until(EC.element_to_be_clickable((By.XPATH, task_search_btn)))
            highlight_element(driver, search_icon_btn)
            search_icon_btn.click()

            search_input = wait.until(EC.visibility_of_element_located((By.XPATH, task_search_input)))
            highlight_element(driver, search_input)
            search_input.clear()
            search_input.send_keys(license_task_name)

            wait_for_loader_to_disappear(driver, wait)
            time.sleep(4)  
        except Exception as e:
            msg = f"failed to Search for the newly created task by name: {str(e)}"
            print(msg)
            allure.attach(str(e), name="Search for the newly created task by name Error", attachment_type=allure.attachment_type.TEXT)
            raise Exception(msg)
    with allure.step(f"Open Company/Project filter and search for company"):
        try:
            company_file = os.path.join("latest_data", "latest_company.txt")
            with open(company_file, "r") as f:
                created_company_name = f.read().strip()
            company_project_filter_btn = wait.until(EC.presence_of_element_located((By.XPATH, column_filter_company_project)))
            highlight_element(driver, company_project_filter_btn)
            company_project_filter_btn.click()
            time.sleep(3)

            search_input = wait.until(EC.presence_of_element_located((By.XPATH, column_filter_search_input)))
            search_input.clear()
            search_input.send_keys(created_company_name)
            time.sleep(6)
        except Exception as e:
            msg = f"Failed to Open Company Project filter: {str(e)}"
            print(msg)
            allure.attach(msg, name="Company Project filter Error", attachment_type=allure.attachment_type.TEXT)
            raise Exception(msg)


    try:
        search_task = wait.until(EC.presence_of_element_located((By.XPATH, f"//div[contains(@class,'dx-list-item-content') and normalize-space()='{created_company_name}']")))
        search_task.click()
        time.sleep(4)
        print("✅ Clicked 'Company'")
    except Exception as e:
        msg = f"Failed to Search Task: {str(e)}"
        print(msg)
        allure.attach(msg, name="Search Task Error", attachment_type=allure.attachment_type.TEXT)
        raise Exception(msg)
    try:
        column_filter_ok = wait.until(EC.presence_of_element_located((By.XPATH, column_filter_ok_btn)))
        column_filter_ok.click()
        time.sleep(4)
    except Exception as e:
        msg = f"Failed to Click Column Filter OK Button: {str(e)}"
        print(msg)
        allure.attach(msg, name="Column Filter OK Button Error", attachment_type=allure.attachment_type.TEXT)
        raise Exception(msg)
    with allure.step("Opening task from table"):
        try:
            task_open_btn_elem = wait.until(EC.element_to_be_clickable((By.XPATH, task_open_btn)))
            highlight_element(driver, task_open_btn_elem)
            try:
                task_open_btn_elem.click()
            except Exception:
                driver.execute_script("arguments[0].scrollIntoView(true);", task_open_btn_elem)
                driver.execute_script("arguments[0].click();", task_open_btn_elem)
            time.sleep(3)
        except Exception as e:
            msg = f"Failed to Click Task button: {str(e)}"
            print(msg)
            allure.attach(msg, name="Click Task button Error", attachment_type=allure.attachment_type.TEXT)
            raise Exception(msg)
    with allure.step("Verify Not Applicable Task"):
        try:
            not_applicable_task_elem = wait.until(EC.visibility_of_element_located((By.XPATH, "//button[@title='Not Applicable']")))
            highlight_element(driver, not_applicable_task_elem)
            fetched_task_name = not_applicable_task_elem.text.strip()
            print(f"Not Applicable: {fetched_task_name}")
            allure.attach(f"Not Applicable: {fetched_task_name}", name="Not Applicable", attachment_type=allure.attachment_type.TEXT)   

            task_license_label_elem = wait.until(EC.visibility_of_element_located((By.XPATH, task_license_label)))
            highlight_element(driver, task_license_label_elem, 0.2)
            fetched_license = task_license_label_elem.text.strip()
            print(f"License: {fetched_license}")
            allure.attach(f"License Name: {fetched_license}", name="License Name", attachment_type=allure.attachment_type.TEXT)   

        except Exception as e:
            msg = f"Failed to Verify Not Applicable Task: {str(e)}"
            print(msg)
            allure.attach(msg, name="Verify Not Applicable Task Error", attachment_type=allure.attachment_type.TEXT)
            raise Exception(msg)
    with allure.step("Verify license name "):
        if fetched_license_task == license_task_name:
            print(f"✅ License Match: {fetched_license_task}: {license_task_name}")
            allure.attach(f"Actual : {fetched_license_task}, Expected : {license_task_name}",name="License Match",attachment_type=allure.attachment_type.TEXT)
        else:
            print(f"❌ License Mismatch!: {fetched_license_task}: {license_task_name}")
            allure.attach(f"Actual : {fetched_license_task}, Expected : {license_task_name}",name="License Mismatch",attachment_type=allure.attachment_type.TEXT)
    

    return True







