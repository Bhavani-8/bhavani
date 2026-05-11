from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import allure 
import pandas as pd
import pyautogui as pg
import os
import json
import pytest
import time


from utilities.other_utils_functions.highlight import highlight_element
from selenium.common.exceptions import TimeoutException
from utilities.add_task_utils import wait_for_loader_to_disappear
from utilities.add_task_utils import add_task_check
from utilities.add_task_functions.format_time_if_valid import format_time_if_valid
from utilities.add_task_functions.format_date_if_valid import format_date_if_valid

def step_fail(driver, step_name, error):
    allure.attach(str(error), name=f"{step_name} Error", attachment_type=allure.attachment_type.TEXT)
    allure.attach(driver.get_screenshot_as_png(), name=f"{step_name} Screenshot", attachment_type=allure.attachment_type.PNG)
    pytest.fail(f"❌ {step_name} failed")

def updates_add_task(driver, wait, updates_task_name):
    wait_less = WebDriverWait(driver, 5)

    with allure.step("Load locators.json"):
        try:
            with open(os.path.join("data", 'locators.json'), 'r') as f:
                elements_details = json.load(f)
                task_update_tab = elements_details['task_update_tab']
                updates_icon = elements_details['updates_icon']
                dash_total_btn = elements_details['dash_total_btn']
                task_open_btn = elements_details['task_open_btn']
                task_search_btn = elements_details['task_search_btn']
                task_search_input = elements_details['task_search_input']
                task_search_close_btn = elements_details['task_search_close_btn']
                task_close_btn = elements_details['task_close_btn']
                update_circ_checkbox_label = elements_details['update_circ_checkbox_label']
                select_circular = elements_details['select_circular']
                create_own_task = elements_details['create_own_task']
                task_update_circ = elements_details['task_update_circ']
                task_fetch_circ = elements_details['task_fetch_circ']
                task_circ_close_btn = elements_details['task_circ_close_btn']

            print("✅ locators.json loaded successfully")
        except Exception as e:
            step_fail(driver, "Load locators.json", e)
    with allure.step("Open Updates Section"):
        try:
            time.sleep(2)
            updates_btn = wait.until(EC.element_to_be_clickable((By.XPATH, updates_icon)))
            highlight_element(driver, updates_btn)
            updates_btn.click()
            wait_for_loader_to_disappear(driver, wait)
            time.sleep(1)
            print("✅ Updates icon clicked")
        except Exception as e:
            allure.attach(str(e), name="Updates Section Error", attachment_type=allure.attachment_type.TEXT)
            return False

    with allure.step("Select Update Checkbox"):
        try:
            circular_label = wait.until(EC.visibility_of_element_located((By.XPATH, update_circ_checkbox_label)))
            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", circular_label)
            time.sleep(0.3)
            highlight_element(driver, circular_label, 0.2)  # Assuming your highlight function exists
            fetched_circular = circular_label.text.strip()
            print(f"Circular: {fetched_circular}")

            select_elem = wait.until(EC.presence_of_element_located((By.XPATH, select_circular)))
            highlight_element(driver, select_elem)
            select_elem.click()
            print("🟦 First checkbox clicked")
            time.sleep(2)
        except Exception as e:
            step_fail(driver, "Load locators.json", e)

    with allure.step("Click Create Your Own Task"):
        try:
            create_task_btn = wait.until(EC.element_to_be_clickable((By.XPATH, create_own_task)))
            highlight_element(driver, create_task_btn)
            create_task_btn.click()
            print("✅ 'Create your own task' clicked")
        except Exception as e:
            step_fail(driver, "Load locators.json", e)

    test_case_details = pd.read_excel(os.path.join("data", "test_case_selector.xlsx"), sheet_name=f"add_task_test_cases").fillna("")
    # test_case_details = pd.read_excel(os.path.join("data", "test_case_selector.xlsx")).fillna("")
    first_row = test_case_details.iloc[0]
    # task_name = updates_task_name if updates_task_name else "task_name"
    task_name = updates_task_name.strip() if updates_task_name else "task_name"

    # task_name = first_row.get('updates_task')
    start_date = format_date_if_valid(first_row.get('start_date'))
    due_date = format_date_if_valid(first_row.get('due_date'))
    frequency = first_row.get('frequency')
    repeat_if_holiday = first_row.get('repeat_if_holiday')
    end_freq_date = first_row.get('end_freq_date')
    repeat_weekday = first_row.get('repeat_weekday')
    repeat_day_month = first_row.get('repeat_day_month')
    # end_time = first_row.get('end_time')
    end_time = format_time_if_valid(first_row.get('end_time')) if pd.notna(first_row.get('end_time')) else None
    internal_deadline = first_row.get('internal_deadline')
    assign_to = first_row.get('assign_to')
    approver = first_row.get('approver')
    cc = first_row.get('cc')
    risk_rating = first_row.get('risk_rating')
    license_name = first_row.get('license_name')
    description = first_row.get('description')
    attach_file_name= first_row.get('attach_file_name')
    impact_details = first_row.get('impact_details')
    impact_file_name = first_row.get('impact_file_name')
    circular_search = first_row.get('circular_search')
    test_type = first_row.get('test_type')

    with allure.step("Create Task"):
        try:
            if add_task_check(driver, task_name, start_date, due_date, frequency, repeat_if_holiday, end_freq_date,
                repeat_weekday, repeat_day_month, end_time, internal_deadline, assign_to, approver, cc,
                risk_rating, license_name, description, attach_file_name, impact_details, impact_file_name,
                circular_search, test_type, task_type='mandatory', direct_task_creation=True):
                print("✅ Task creation successful")
                # return True
            else:
                allure.attach("Test case failed for Task Creation", name="Task Creation Validation Failed", attachment_type=allure.attachment_type.TEXT)
                return False
        except Exception as e:
            step_fail(driver, "Load locators.json", e)

    with allure.step("Validate Update Task in Dashboard"):
        try:
            wait_for_loader_to_disappear(driver, wait)
            total_tab = wait.until(EC.element_to_be_clickable((By.XPATH, dash_total_btn)))
            highlight_element(driver, total_tab)
            total_tab.click()
            wait_for_loader_to_disappear(driver, wait)
            time.sleep(3)

            search_icon_btn = wait.until(EC.presence_of_element_located((By.XPATH, task_search_btn)))
            highlight_element(driver, search_icon_btn)
            search_icon_btn.click()

            search_input = wait.until(EC.visibility_of_element_located((By.XPATH, task_search_input)))
            highlight_element(driver, search_input)
            search_input.clear()
            search_input.send_keys(task_name)

            wait_for_loader_to_disappear(driver, wait)
            time.sleep(4)  # Extra wait to ensure results load
    
            task_open_btn_elem = wait.until(EC.presence_of_element_located((By.XPATH, task_open_btn)))
            highlight_element(driver, task_open_btn_elem)
            task_open_btn_elem.click()
            time.sleep(4)
            wait_for_loader_to_disappear(driver, wait)
           
        except Exception as err:
            allure.attach(str(err), "Total tab error", allure.attachment_type.TEXT)
            pytest.fail("Failed to click Total tab")

    with allure.step("Click on Update Tab"):
        try:
            print()
            update_tab_elem = wait.until(EC.presence_of_element_located((By.XPATH, task_update_tab)))
            highlight_element(driver, update_tab_elem)
            update_tab_elem.click()
            time.sleep(2)
            print("✅ Update tab clicked successfully.")
        except Exception as e:
            step_fail(driver, "Load locators.json", e)

    with allure.step("Validate Update Circular"):
        try:
            update_circ = wait.until(EC.visibility_of_element_located((By.XPATH, task_update_circ)))
            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", update_circ)
            time.sleep(1)
            highlight_element(driver, update_circ, 0.2)  # Assuming your highlight function exists
            fetched_update_circ = update_circ.text.strip()
            print(f"Update Circular: {fetched_update_circ}")

            update_circular_checkbox = wait.until(EC.presence_of_element_located((By.XPATH, task_fetch_circ)))
            highlight_element(driver, update_circular_checkbox)
            update_circular_checkbox.click()
            time.sleep(2)
            print("Update Circular Opened successfully.")
        except Exception as e:
            step_fail(driver, "Validate Update Circular Failed", e)   
    with allure.step("Verify Circular"):
        if fetched_circular == fetched_update_circ:
            print("✅ Circular Verified successfully!")
            allure.attach(f"Circular: {fetched_circular}",name="Circular Check",attachment_type=allure.attachment_type.TEXT)
            time.sleep(2)
        else:
            print(f"❌ Circular Mismatch: {fetched_circular}: {fetched_update_circ}")
            allure.attach(f"Circular: {fetched_circular}, Update Circular: {fetched_update_circ}",name="Circular Mismatch",attachment_type=allure.attachment_type.TEXT)
            return False

    with allure.step("Close Circular and Task"):
        try:
            time.sleep(2)
            close_circular = wait.until(EC.presence_of_element_located((By.XPATH, task_circ_close_btn)))
            highlight_element(driver, close_circular)
            close_circular.click()
            print("✅ Circular closed successfully.")
            time.sleep(3)

            close_task_btn = wait.until(EC.presence_of_element_located((By.XPATH, task_close_btn)))
            highlight_element(driver, close_task_btn)
            close_task_btn.click()
            print("✅ Task closed successfully.")
            wait_for_loader_to_disappear(driver, wait)
            time.sleep(3)
        
            search_close_btn = wait.until(EC.presence_of_element_located((By.XPATH,  task_search_close_btn)))
            highlight_element(driver, search_close_btn)
            search_close_btn.click()
            print("✅ Search closed successfully.")
            wait_for_loader_to_disappear(driver, wait)
            time.sleep(3)
        
        except Exception as e:
            step_fail(driver, "Close button Failed", e)  


   
    return True

