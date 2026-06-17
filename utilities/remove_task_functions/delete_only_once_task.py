
import allure
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from utilities.other_utils_functions.highlight import highlight_element   
import time
import json
import pytest
import os
import pandas as pd
from utilities.add_task_functions.wait_for_loader_to_disappear import wait_for_loader_to_disappear
from selenium.common.exceptions import TimeoutException
from utilities.login_utils import login_check
from load_test_config_excel_data import load_test_config_excel_data
from utilities.add_task_functions.format_time_if_valid import format_time_if_valid
from utilities.add_task_functions.format_date_if_valid import format_date_if_valid
from utilities.add_task_utils import add_task_check

    
def delete_only_once_task(driver, wait):
    
    with open(os.path.join("data", 'locators.json'), 'r') as f:
        elements_details = json.load(f)
        dash_total_btn = elements_details['dash_total_btn']
        dashboard_icon = elements_details['dashboard_icon']
        trash_icon = elements_details['trash_icon']
        task_search_btn = elements_details['task_search_btn']
        task_search_input = elements_details['task_search_input']
        task_open_btn = elements_details['task_open_btn']
        task_close_btn = elements_details['task_close_btn']
        task_search_close_btn = elements_details['task_search_close_btn']
        task_delete_btn = elements_details['task_delete_btn']
        delete_yes_btn = elements_details['delete_yes_btn']
        toast_msg = elements_details['toast_msg']

    with allure.step("Validating Dashboard Widgets - Clicking Dashboard Icon"):
        dashboard_icon_elem = wait.until(EC.presence_of_element_located((By.XPATH, dashboard_icon)))
        highlight_element(driver, dashboard_icon_elem)
        dashboard_icon_elem.click()
        print("📊 Dashboard icon clicked.")
        allure.attach("Dashboard icon clicked",name="Dashboard Icon Clicked",attachment_type=allure.attachment_type.TEXT)

    test_case_details = pd.read_excel(os.path.join("data", "test_case_selector.xlsx"), sheet_name=f"add_task_test_cases").fillna("")
    # test_case_details = pd.read_excel(os.path.join("data", "test_case_selector.xlsx")).fillna("")
    first_row = test_case_details.iloc[0]
    task_name = first_row.get('task_name')
    # task_name = delete_task_name if delete_task_name else "task_name"
    # task_name = project_task_name or first_row.get('task_name')
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
        task_name = f"{task_name}_only_once_check"
        try:
            if add_task_check(driver, task_name, start_date, due_date, frequency, repeat_if_holiday, end_freq_date,
                repeat_weekday, repeat_day_month, end_time, internal_deadline, assign_to, approver, cc,
                risk_rating, license_name, description, attach_file_name, impact_details, impact_file_name,
                circular_search, test_type, task_type='mandatory', direct_task_creation=False):
                print("✅ Task creation successful")
                time.sleep(6)
            else:
                allure.attach("Test case failed for Task Creation", name="Task Creation Validation Failed", attachment_type=allure.attachment_type.TEXT)
                return False
        except Exception as e:
            allure.attach(str(e), name="Add Task Error", attachment_type=allure.attachment_type.TEXT)
    
    with allure.step("Validating Dashboard - Click Search Icon and enter"):
        total_tab = wait.until(EC.presence_of_element_located((By.XPATH, dash_total_btn)))
        highlight_element(driver, total_tab)
        total_tab.click()
        wait_for_loader_to_disappear(driver, wait)
        # click search icon
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
        time.sleep(2)
        wait_for_loader_to_disappear(driver, wait)
    with allure.step("Validating Dashboard - Checking Delete Button"):
        delete = wait.until(EC.presence_of_element_located((By.XPATH, task_delete_btn)))
        highlight_element(driver, delete)
        delete.click()
        print("🗑️ Delete button clicked.")
        
    with allure.step("Validating Dashboard - Confirming Task Deactivation"):
    
        # Wait for the Deactivate Confirmation Modal
        confirm_deactivate = wait.until(EC.presence_of_element_located((By.XPATH, "//p[text()='Are you sure you want to De-activate this Task?']")))
        print(f"💬 Modal message displayed: {confirm_deactivate.text}")
       

        # ---- YES Button Flow ----
        yes_btn = wait.until(EC.element_to_be_clickable((By.XPATH, delete_yes_btn)))
        highlight_element(driver, yes_btn)
        yes_btn.click()
        print("✅ YES button clicked (Task Deactivated)")
        

    with allure.step("Validate toast message after saving"):
        toast_msg_elem = wait.until(EC.presence_of_element_located((By.XPATH, toast_msg)))
        msg = toast_msg_elem.text.strip()
        time.sleep(6)
        print(f"📢 Toast message after saving: {msg}")
        
    #  Validating Dashboard Widgets - Clicking Trash Icon
    with allure.step("Validating Dashboard - Clicking Trash Icon"):
       trash_icon_elem = wait.until(EC.presence_of_element_located((By.XPATH, trash_icon)))
       highlight_element(driver, trash_icon_elem)
       trash_icon_elem.click()
       print("🗑️ Trash icon clicked.")
   
        
    with allure.step("Click Tasks Tab"):
        try:
            time.sleep(3)
            tasks_tab = wait.until(EC.presence_of_element_located((By.XPATH, "//button[text()='Tasks']")))
            highlight_element(driver, tasks_tab)
            tasks_tab.click()
            print("📌 Tasks tab clicked")

        except Exception as e:
            allure.attach(str(e), name="Tasks Tab Error", attachment_type=allure.attachment_type.TEXT)
           
    with allure.step("Validating Dashboard - Clicking Restore Button"):
        try:
            task_name_elem = wait.until(EC.visibility_of_element_located((By.XPATH, f"//span[@title='{task_name}']")))
            highlight_element(driver, task_name_elem)
            fetch_task_name_elem = task_name_elem.text.strip()
            print(f"✅ Task '{fetch_task_name_elem}' found in Trash")
        except Exception as e:
            allure.attach(str(e), name="Task name Error", attachment_type=allure.attachment_type.TEXT)
    
    with allure.step("Click Restore Task"):
        try:
            time.sleep(3)
            restore_elem = wait.until(EC.presence_of_element_located((By.XPATH, f"//tr[@data-slot='table-row'][.//span[@title='{task_name}']]//button[@title='Restore Task']")))
            highlight_element(driver, restore_elem)
            restore_elem.click()
            time.sleep(3)
            print("📌 Restore Task button clicked")

        except Exception as e:
            allure.attach(str(e), name="Restore Error", attachment_type=allure.attachment_type.TEXT)
    # ---- Wait for Toast Message ----
    with allure.step("Validate toast message after saving"):
        toast_msg_elem = wait.until(EC.presence_of_element_located((By.XPATH, toast_msg)))
        msg = toast_msg_elem.text.strip()
        time.sleep(6)
        print(f"📢 Toast message after saving: {msg}")
    
    with allure.step("Verify created task by searching and validating data"):
        try:
            dashboard_icon_elem = wait.until(EC.presence_of_element_located((By.XPATH, dashboard_icon)))
            highlight_element(driver, dashboard_icon_elem)
            dashboard_icon_elem.click()
            print("✅ Dashboard icon clicked")
            wait_for_loader_to_disappear(driver, wait)
            
            total_tab = wait.until(EC.presence_of_element_located((By.XPATH, dash_total_btn)))
            highlight_element(driver, total_tab)
            total_tab.click()
            wait_for_loader_to_disappear(driver, wait)
            # click search icon
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
            time.sleep(2)
            wait_for_loader_to_disappear(driver, wait)
        except Exception as e:
            allure.attach(str(e), name="Restore Error", attachment_type=allure.attachment_type.TEXT)
    
    with allure.step("Validating Dashboard  - Checking Delete Button"):
        delete = wait.until(EC.presence_of_element_located((By.XPATH, task_delete_btn)))
        highlight_element(driver, delete)
        delete.click()
        print("🗑️ Delete button clicked.")
   
    with allure.step("Validating Dashboard  - Confirming Task Deactivation"):
        yes_btn = wait.until(EC.element_to_be_clickable((By.XPATH, delete_yes_btn)))
        highlight_element(driver, yes_btn)
        yes_btn.click()
        print("✅ YES button clicked (Task Deactivated)")


    return True

