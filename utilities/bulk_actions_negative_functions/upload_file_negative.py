import pytest
import os
import json
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from utilities.other_utils_functions.highlight import highlight_element
from selenium.webdriver import ActionChains
import pyautogui as pg
import time
import allure
from selenium.common.exceptions import TimeoutException
from utilities.add_task_functions.wait_for_loader_to_disappear import wait_for_loader_to_disappear
from selenium.common.exceptions import StaleElementReferenceException

def step_fail(driver, step_name, error):
    allure.attach(str(error), name=f"{step_name} Error", attachment_type=allure.attachment_type.TEXT)
    allure.attach(driver.get_screenshot_as_png(), name=f"{step_name} Screenshot", attachment_type=allure.attachment_type.PNG)
    pytest.fail(f"❌ {step_name} failed")

try:
    with open(os.path.join("data", 'locators.json'), 'r') as f:
        elements_details = json.load(f)
        dash_col_all_selection_btn = elements_details['dash_col_all_selection_btn']
        dash_bulk_task_dropdown_btn = elements_details['dash_bulk_task_dropdown_btn']
        dash_total_btn = elements_details['dash_total_btn']
        dash_col_selected_label = elements_details['dash_col_selected_label']
        dash_bulk_task_dropdown_form_label = elements_details['dash_bulk_task_dropdown_form_label']
        dash_bulk_task_dropdown_form_input = elements_details['dash_bulk_task_dropdown_form_input']
        dash_bulk_task_dropdown_form_member_confirmation = elements_details['dash_bulk_task_dropdown_form_member_confirmation']
        dash_not_assigned_tab = elements_details['dash_not_assigned_tab']
        column_chooser_btn = elements_details['column_chooser_btn']
        column_chooser_save_btn = elements_details['column_chooser_save_btn']
        file_input = elements_details['file_input']
        scroller = elements_details['scroller']
        toast_msg = elements_details['toast_msg']
        error_toast_msg = elements_details['error_toast_msg']
        dash_bulk_options_upload_file = elements_details['dash_bulk_options_upload_file']
        column_chooser_company_project = elements_details['column_chooser_company_project']
        column_filter_company_project = elements_details['column_filter_company_project']

except FileNotFoundError:
    pytest.fail("❌ locators.json file not found")
except json.JSONDecodeError:
    pytest.fail("❌ Invalid JSON in locators.json")


def upload_file_negative(driver, wait, dropdown_selection_val_data, dropdown_selection_val=None, task_name='Internal Task', text_case_id=None):
    wait_less = WebDriverWait(driver, 5)
    with allure.step("Clicking Dashboard Total button"):
        try:
            total_tab = wait.until(EC.element_to_be_clickable((By.XPATH, dash_total_btn)))
            highlight_element(driver, total_tab)
            total_tab.click()
            wait_for_loader_to_disappear(driver, wait)
            print("✅ Clicked Total tab")
        except Exception as e:
            step_fail(driver, "Clicking Total tab failed", e)
    with allure.step("Open Column Chooser from task list"):
        column_chooser_btn_elem = wait.until(EC.presence_of_element_located((By.XPATH, column_chooser_btn)))
        highlight_element(driver, column_chooser_btn_elem)
        driver.execute_script("arguments[0].click();", column_chooser_btn_elem)
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
            step_fail(driver, "Column normalization failed", e)
    with allure.step("Select 'Company / Project' from Column Chooser"):   
        try:
            company_project_option_elm = wait.until(EC.presence_of_element_located((By.XPATH, column_chooser_company_project)))
            actions = ActionChains(driver)
            actions.move_to_element(company_project_option_elm).perform()
            time.sleep(0.5)
            wait.until(EC.element_to_be_clickable((By.XPATH, column_chooser_company_project)))
            company_project_option_elm.click()

            save_btn = wait.until(EC.element_to_be_clickable((By.XPATH, column_chooser_save_btn)))
            highlight_element(driver, save_btn)
            save_btn.click()
        except Exception as e:
            step_fail(driver, "Column chooser save failed", e)
    
        try:
            toast = wait.until(EC.presence_of_element_located((By.XPATH,f"{toast_msg} | {error_toast_msg}")))
            highlight_element(driver, toast)
            toast_class = toast.get_attribute("class")

            if "Toastify__toast--success" in toast_class:
                print(f"📢 Success Toast: {toast.text.strip()}")
            elif "Toastify__toast--error" in toast_class:
                print(f"❌ Error Toast: {toast.text.strip()}")
        except Exception as e:
            step_fail(driver, "Toast validation failed", e)
        wait_for_loader_to_disappear(driver, wait)

    with allure.step(f"Open Company/Project filter and search for '{task_name}'"):
        company_filter = wait.until(EC.element_to_be_clickable((By.XPATH, column_filter_company_project)))
        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", company_filter)
        time.sleep(0.5)
        driver.execute_script("arguments[0].click();", company_filter)
        time.sleep(2)
        
        search_input = wait.until(EC.presence_of_element_located((By.XPATH,"//input[contains(@class,'dx-texteditor-input') and @role='textbox']")))
        search_input.clear()
        search_input.send_keys(task_name)
        time.sleep(2)

        try:
            search_task = wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class,'dx-list-item-content') and normalize-space()='Internal Task']")))
            search_task.click()
            time.sleep(4)
            print("✅ Clicked 'Internal Task'")

            ok_btn = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@aria-label='OK']")))
            highlight_element(driver, ok_btn)
            ok_btn.click()
            time.sleep(3)
            wait_for_loader_to_disappear(driver, wait)
           
        except Exception as e:
            step_fail(driver, "Failed to click Internal Task", e)

    with allure.step("Select first task from task list"):
        try:
            first_checkbox = wait.until(EC.presence_of_element_located((By.XPATH, "(//td[@aria-colindex='1']//span[contains(@class,'dx-checkbox-icon')])[2]")))
            first_checkbox.click()
            time.sleep(2)
        except Exception as e:
            step_fail(driver, "Failed to select first task", e)

    with allure.step("Open Bulk Action and select 'Upload File'"): 
        try:
            bulk_dd = wait.until(EC.element_to_be_clickable((By.XPATH, dash_bulk_task_dropdown_btn)))
            highlight_element(driver, bulk_dd)
            bulk_dd.click()

            uppload_btn = wait.until(EC.element_to_be_clickable((By.XPATH, dash_bulk_options_upload_file)))
            highlight_element(driver, uppload_btn)
            uppload_btn.click()
        except Exception as e:
            step_fail(driver, "Upload File failed", e)

        try:
            file_input_elem = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='file']")))
            driver.execute_script("""
                arguments[0].style.display='block';
                arguments[0].style.visibility='visible';
                arguments[0].style.opacity=1;
            """, file_input_elem)
            large_file_path = os.path.abspath(os.path.join("data", "large_size_dummy_file.pdf"))
            if not os.path.exists(large_file_path):
                pytest.fail(f"❌ File not found: {large_file_path}")
            file_input_elem.send_keys(large_file_path)
            print(f"📤 File selected: {large_file_path}")
        except Exception as e:
            step_fail(driver, "File selection failed", e)

        try:
            toast = wait.until(EC.presence_of_element_located((By.XPATH, toast_msg)))
            highlight_element(driver, toast)
            print(f"📢 Toast message: {toast.text.strip()}")
        except Exception as e:
           print("⚠️ No toast message appeared after file upload attempt")
    
