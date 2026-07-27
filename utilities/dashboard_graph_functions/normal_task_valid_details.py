import allure
import pandas as pd
import os
import pytest
import json
import time
import glob
import random
from datetime import datetime
from utilities.add_task_functions.add_task_common import task_value_store
from utilities.add_task_functions.add_task_common import task_value_get
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from utilities.other_utils_functions.highlight import highlight_element
from utilities.add_task_utils import wait_for_loader_to_disappear
from utilities.add_task_functions.format_time_if_valid import format_time_if_valid
from utilities.add_task_functions.format_date_if_valid import format_date_if_valid
from utilities.add_task_utils import add_task_check
from utilities.add_task_functions.task_validation import task_validation
from utilities.add_task_functions.show_toast import show_toast
from utilities.login_utils import login_check

def normal_task_valid_details(driver, wait, normal_task):
    with allure.step("Load locators.json"):
        try:
            with open(os.path.join("data", "locators.json"), "r") as f:
                elements_details = json.load(f)
            dashboard_icon = elements_details['dashboard_icon']
            task_search_btn = elements_details['task_search_btn']
            task_search_input = elements_details['task_search_input']
            task_search_close_btn = elements_details['task_search_close_btn']
            task_open_btn = elements_details['task_open_btn']
            dash_total_btn = elements_details['dash_total_btn']
            team_performance_btn = elements_details['team_performance_btn']
            dash_search_close_btn = elements_details['dash_search_close_btn']
            print("✅ locators.json loaded")
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
            allure.attach(str(e), name="Dashboard Open Error", attachment_type=allure.attachment_type.TEXT)
            return False
    # 🧩 Load first test case data
    
    test_case_details = pd.read_excel(os.path.join("data", "test_case_selector.xlsx"), sheet_name=f"add_task_test_cases").fillna("")
    # test_case_details = pd.read_excel(os.path.join("data", "test_case_selector.xlsx")).fillna("")
    first_row = test_case_details.iloc[0]
    # task_name = str(first_row.get('task_name', '')).strip()
    task_name =  (f"{normal_task.strip() if normal_task else 'task_name'}_{random.randint(100000, 999999)}")
    # task_value_store("task_name", task_name)
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
                circular_search, test_type, task_type='mandatory', direct_task_creation=False):
                print("✅ Task creation successful")
            
            else:
                allure.attach("Test case failed for Task Creation", name="Task Creation Validation Failed", attachment_type=allure.attachment_type.TEXT)
                return False
        except Exception as e:
            allure.attach(str(e), name="Add Task Error", attachment_type=allure.attachment_type.TEXT)

   
    try:
        time.sleep(6)
        search_close_btn = wait.until(EC.presence_of_element_located((By.XPATH, task_search_close_btn)))
        highlight_element(driver, search_close_btn)
        search_close_btn.click()
        wait_for_loader_to_disappear(driver, wait)
        time.sleep(3)
        print("✅ Search Close button clicked")
    except Exception as e:
        msg = f"Failed to Click Search Close Button: {str(e)}"
        print(msg)
        allure.attach(msg, name="Search Close Button Error", attachment_type=allure.attachment_type.TEXT)
        raise Exception(msg)
    try:
        time.sleep(2)
        team_perf_elem = wait.until(EC.presence_of_element_located((By.XPATH, team_performance_btn)))
        highlight_element(driver, team_perf_elem)
        team_perf_elem.click()
        wait_for_loader_to_disappear(driver, wait)
        time.sleep(10)
    except Exception as e:
        msg = f"Failed to Click Special Team Performance Button: {str(e)}"
        print(msg)
        allure.attach(msg, name="Special Team Performance Button Error", attachment_type=allure.attachment_type.TEXT)
        raise Exception(msg)
    try:
        team_perf_today_btn= wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@class,'summary-item-key-today') and contains(@class,'cursor-pointer')]")))
        highlight_element(driver, team_perf_today_btn)
        time.sleep(1)
        team_perf_today_btn.click()
        print("✅ Today Total Button clicked")
        wait_for_loader_to_disappear(driver, wait)
        time.sleep(3)
    except Exception as e:
        msg = f"Failed to Click Team Performance Today Button: {str(e)}"
        print(msg)
        allure.attach(msg, name="Special Team Performance Today Button Error", attachment_type=allure.attachment_type.TEXT)
        raise Exception(msg)
    with allure.step("Verify created task in Team Performance Search Button"):
        try:
        
            search_icon_btn = wait.until(EC.presence_of_element_located((By.XPATH, task_search_btn)))
            highlight_element(driver, search_icon_btn)
            search_icon_btn.click()

            search_input = wait.until(EC.visibility_of_element_located((By.XPATH, task_search_input)))
            highlight_element(driver, search_input)
            search_input.clear()
            search_input.send_keys(task_name)

            wait_for_loader_to_disappear(driver, wait)
            time.sleep(5)  

            print(f"🔍 Searching for task: {task_name}")

            no_task_elements = driver.find_elements(By.XPATH, "//*[contains(text(),'No Task Found')]")

            if no_task_elements and no_task_elements[0].is_displayed():
                msg = f"❌ Task NOT found: {task_name}"

                print(msg)

                allure.attach(msg,name="No Task Found Validation",attachment_type=allure.attachment_type.TEXT)

                raise Exception(msg)  
            task_elements = driver.find_elements(By.XPATH, f"//p[@title='{task_name}']")
            if not task_elements:
                msg = f"❌ Task element not found after search: {task_name}"

                print(msg)

                allure.attach(msg,name="Task Element Validation",attachment_type=allure.attachment_type.TEXT)

                raise Exception(msg)
                

            # ✅ Validate task name
            actual_task_name = task_elements[0].text.strip() or \
                            task_elements[0].get_attribute("title")
            
            validation_msg = f"task_name: actual='{actual_task_name}', expected='{task_name}'"
            allure.attach(
            validation_msg,
            name="Task Name Validation",
            attachment_type=allure.attachment_type.TEXT
        )
            if actual_task_name != task_name:
                msg = f"❌ Task name mismatch"

                print(f"{msg}: expected='{task_name}', actual='{actual_task_name}'")


                raise Exception(validation_msg)

            else:
                print(f"✅ Task name validated: {actual_task_name}")

        except Exception as e:
            msg = f"Failed to Click Search Button: {str(e)}"
            print(msg)
            allure.attach(msg, name="Search Button Error", attachment_type=allure.attachment_type.TEXT)
            raise Exception(msg)
    with allure.step("Verify created task in Team Performance"):  
        try:
            task_open_btn_elem = wait.until(EC.element_to_be_clickable((By.XPATH, task_open_btn)))

            highlight_element(driver, task_open_btn_elem)
            task_open_btn_elem.click()

            wait_for_loader_to_disappear(driver, wait)
            time.sleep(2)

            print("✅ Task found and opened")

        except Exception as e:
            msg = f"Failed to Click Task Open Button: {str(e)}"
            print(msg)
            allure.attach(msg, name="Task Open Button Error", attachment_type=allure.attachment_type.TEXT)
            raise Exception(msg)
    # with allure.step("Validate Task Details in Team Performance Task"):
    #     try:
    #         validation_success = task_validation(driver, wait)

    #         if not validation_success:
    #             pytest.fail("❌ Task validation failed after search")
    #     except Exception as e:
    #         allure.attach(str(e),name="Task Validation Error",attachment_type=allure.attachment_type.TEXT)
    #         raise
    with allure.step("Open Dashboard"):
        try:
            time.sleep(2)
            dashboard_icon_elem = wait.until(EC.presence_of_element_located((By.XPATH, dashboard_icon)))
            highlight_element(driver, dashboard_icon_elem)
            dashboard_icon_elem.click()
            print("✅ Dashboard icon clicked")
            time.sleep(3)
        except Exception as e:
            allure.attach(str(e), name="Dashboard Open Error", attachment_type=allure.attachment_type.TEXT)
            return False
    with allure.step("Click close button on task details panel"):
        try:
            search_close_btn = wait.until(EC.presence_of_element_located((By.XPATH, dash_search_close_btn)))
            highlight_element(driver, search_close_btn)
            search_close_btn.click()
            wait_for_loader_to_disappear(driver, wait)
            time.sleep(3)
            print("✅ Project Submit clicked")
        except Exception as e:
            msg = f"Failed to Click Search Close Button: {str(e)}"
            print(msg)
            allure.attach(msg, name="Search Close  Button Error", attachment_type=allure.attachment_type.TEXT)
            raise Exception(msg)
    return True 