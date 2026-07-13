import allure
import pandas as pd
import os
import pytest
import json
import time
import glob
from utilities.add_task_functions.add_task_common import task_value_store
from utilities.add_task_functions.add_task_common import task_value_get
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from utilities.add_task_functions.show_toast import show_toast
from utilities.other_utils_functions.highlight import highlight_element
from utilities.add_task_utils import wait_for_loader_to_disappear
from utilities.add_task_functions.format_time_if_valid import format_time_if_valid
from utilities.add_task_functions.format_date_if_valid import format_date_if_valid
from utilities.special_add_task_utils import special_task_check
from utilities.add_task_functions.special_task_validation import special_task_validation
from utilities.login_utils import login_check

def step_fail(driver, step_name, error):
    allure.attach(str(error), name=f"{step_name} Error", attachment_type=allure.attachment_type.TEXT)
    allure.attach(driver.get_screenshot_as_png(), name=f"{step_name} Screenshot", attachment_type=allure.attachment_type.PNG)
    pytest.fail(f"❌ {step_name} failed")

def special_task_valid_details(driver, wait, special_task):
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
            task_close_btn = elements_details['task_close_btn']
            special_task_icon = elements_details['special_task_icon']
            print("✅ locators.json loaded")
        except Exception as e:
            step_fail(driver, "Load locators.json", e)
    
    # with allure.step("Open Dashboard"):
    #     try:
    #         time.sleep(2)
    #         special_task_icon_elem = wait.until(EC.element_to_be_clickable((By.XPATH, special_task_icon)))
    #         highlight_element(driver, special_task_icon_elem)
    #         special_task_icon_elem.click()
    #     except Exception as e:
    #         allure.attach(str(e), name="Dashboard Open Error", attachment_type=allure.attachment_type.TEXT)
    #         return False
        
    # 🧩 Load first test case data
    
    test_case_details = pd.read_excel(os.path.join("data", "test_case_selector.xlsx"), sheet_name=f"special_add_task_test_cases").fillna("")
    # test_case_details = pd.read_excel(os.path.join("data", "test_case_selector.xlsx")).fillna("")
    first_row = test_case_details.iloc[0]
    # task_name = first_row.get('task_name')
    current_task_name = special_task.strip() if special_task else "task_name"
    task_name = current_task_name
    task_value_store("task_name", task_name)
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
    task_category = first_row.get('task_category')
    description = first_row.get('description')
    attach_file_name= first_row.get('attach_file_name')
    impact_details = first_row.get('impact_details')
    impact_file_name = first_row.get('impact_file_name')
    circular_search = first_row.get('circular_search')
    test_type = first_row.get('test_type')
    with allure.step("Create Task"):
        try:
            if special_task_check(driver, task_name, start_date, due_date, frequency, repeat_if_holiday, end_freq_date,
                repeat_weekday, repeat_day_month, end_time, internal_deadline, assign_to, approver, cc,
                risk_rating, license_name, task_category, description, attach_file_name, impact_details, impact_file_name,
                circular_search, test_type, login_required=False):
                print("✅ Task creation successful")
                created_task = task_value_get("task_name")
                print(f"Created Taask{created_task}")
            else:
                allure.attach("Test case failed for Task Creation", name="Task Creation Validation Failed", attachment_type=allure.attachment_type.TEXT)
                return False
        except Exception as e:
            allure.attach(str(e), name="Add Task Error", attachment_type=allure.attachment_type.TEXT)
    
    
    try:
        search_close_btn = wait.until(EC.presence_of_element_located((By.XPATH,  task_search_close_btn)))
        highlight_element(driver, search_close_btn)
        search_close_btn.click()
        wait_for_loader_to_disappear(driver, wait)
        time.sleep(3)
        print("✅ Project Submit clicked")
    except Exception as e:
        step_fail(driver, "Click close button on task details panel", e)  
    
    
    time.sleep(2)
    special_team_perf_elem = wait.until(EC.element_to_be_clickable((By.XPATH, team_performance_btn)))
    highlight_element(driver, special_team_perf_elem)
    special_team_perf_elem.click()
    print("✅ Special Team Performance clicked")
    wait_for_loader_to_disappear(driver, wait)
    time.sleep(10)

    team_perf_today_btn= wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@class,'summary-item-key-today') and contains(@class,'cursor-pointer')]")))
    highlight_element(driver, team_perf_today_btn)
    time.sleep(1)
    team_perf_today_btn.click()
    print("✅ Team Performance clicked")
    wait_for_loader_to_disappear(driver, wait)
    time.sleep(3)
    with allure.step("Verify created task in Team Performance Search Button"):
        try:

            search_icon_btn = wait.until(EC.presence_of_element_located((By.XPATH, task_search_btn)))
            highlight_element(driver, search_icon_btn)
            search_icon_btn.click()

            search_input = wait.until(EC.visibility_of_element_located((By.XPATH, task_search_input)))
            highlight_element(driver, search_input)
            search_input.clear()
            search_input.send_keys(created_task)
            

            wait_for_loader_to_disappear(driver, wait)
            time.sleep(4)  

            print(f"🔍 Searching for task: {created_task}")
            

            no_task_elements = driver.find_elements(By.XPATH, "//*[contains(text(),'No Task Found')]")

            if no_task_elements and no_task_elements[0].is_displayed():
                msg = f"❌ Task NOT found: {created_task}"

                print(msg)

                allure.attach(msg,name="No Task Found Validation",attachment_type=allure.attachment_type.TEXT)

                allure.attach(driver.get_screenshot_as_png(),name="No Task Found Screenshot",attachment_type=allure.attachment_type.PNG)

                pytest.fail(msg)  
            task_elements = driver.find_elements(By.XPATH, f"//p[@title='{created_task}']")
            if not task_elements:
                msg = f"❌ Task element not found after search: {created_task}"

                print(msg)

                allure.attach(msg,name="Task Element Validation",attachment_type=allure.attachment_type.TEXT)

                allure.attach(driver.get_screenshot_as_png(),name="Task Element Missing",attachment_type=allure.attachment_type.PNG)
                pytest.fail(msg)
                

            # ✅ Validate task name
            actual_task_name = task_elements[0].text.strip() or \
                            task_elements[0].get_attribute("title")
            
            validation_msg = f"task_name: actual='{actual_task_name}', expected='{created_task}'"
            allure.attach(
            validation_msg,
            name="Task Name Validation",
            attachment_type=allure.attachment_type.TEXT
        )

            if actual_task_name != created_task:
                msg = f"❌ Task name mismatch"

                print(f"{msg}: expected='{created_task}', actual='{actual_task_name}'")

    
                allure.attach(driver.get_screenshot_as_png(),
                            name="Task Name Mismatch",
                            attachment_type=allure.attachment_type.PNG)

                pytest.fail(validation_msg)

            else:
                print(f"✅ Task name validated: {actual_task_name}")

        except Exception as e:
            step_fail(driver, "Step 5: Verify created task by searching", e)

        
        with allure.step("Verify created task in Team Performance"):
            try:
                task_open_btn_elem = wait.until(
                    EC.element_to_be_clickable((By.XPATH, task_open_btn))
                )

                highlight_element(driver, task_open_btn_elem)
                task_open_btn_elem.click()

                wait_for_loader_to_disappear(driver, wait)
                time.sleep(2)

                print("✅ Task found and opened")

            except Exception as e:
                step_fail(driver, "Task open failed", e)


    # -----------------------------
    # ✅ Validate task
    # -----------------------------
    validation_success = special_task_validation(driver, wait)

    if not validation_success:
        pytest.fail("❌ Task validation failed after search")

    print("✅ Task verified successfully")       
    with allure.step("Open Special Task Dashboard"):
        try:
            special_task_icon_elem = wait.until(EC.presence_of_element_located((By.XPATH, special_task_icon)))
            highlight_element(driver, special_task_icon_elem)
            special_task_icon_elem.click()
            wait_for_loader_to_disappear(driver, wait)
            time.sleep(3)
            print("✅ Special Task Dashboard icon clicked")
        except Exception as e:
            step_fail(driver, "Click close button on task details panel", e)
    with allure.step("Click close button on task details panel"):
        try:
            search_close_btn = wait.until(EC.presence_of_element_located((By.XPATH,  task_search_close_btn)))
            highlight_element(driver, search_close_btn)
            search_close_btn.click()
            wait_for_loader_to_disappear(driver, wait)
            time.sleep(3)
            print("✅Search Close Button clicked")
        except Exception as e:
            step_fail(driver, "Click close button on task details panel", e)
    
    return True 







    