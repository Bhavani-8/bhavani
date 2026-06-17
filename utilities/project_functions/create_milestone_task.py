
import allure
import json
import os
import time
import pytest
import pyautogui as pg
import pandas as pd
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from utilities.other_utils_functions.highlight import highlight_element
from utilities.add_task_utils import wait_for_loader_to_disappear
from utilities.add_task_functions.format_time_if_valid import format_time_if_valid
from utilities.add_task_functions.format_date_if_valid import format_date_if_valid
from utilities.add_task_utils import add_task_check


def step_fail(driver, step_name, error):
    allure.attach(str(error), name=f"{step_name} Error", attachment_type=allure.attachment_type.TEXT)
    allure.attach(driver.get_screenshot_as_png(), name=f"{step_name} Screenshot", attachment_type=allure.attachment_type.PNG)
    pytest.fail(f"❌ {step_name} failed")
   
def create_milestone_task(driver, wait, milestone_task_name=None):

    with allure.step("Load locators.json"):
        try:
            with open(os.path.join("data", "locators.json"), "r") as f:
                elements_details = json.load(f)

            project_icon = elements_details["project_icon"]
            task_project_close_btn = elements_details['task_project_close_btn']
            dashboard_icon = elements_details['dashboard_icon']
            dash_total_btn = elements_details['dash_total_btn']
            task_search_btn = elements_details['task_search_btn']
            task_search_input = elements_details['task_search_input']
            task_open_btn = elements_details['task_open_btn']
            task_close_btn = elements_details['task_close_btn']
            task_project_close_btn = elements_details['task_project_close_btn']
            task_search_close_btn = elements_details['task_search_close_btn']
            milestone_cancel_btn = elements_details['milestone_cancel_btn']
            print("✅ locators.json loaded")
        except Exception as e:
            step_fail(driver, "Load locators.json", e)
        
    with allure.step(" Click project icon"):
        try:
            project_btn = wait.until(EC.presence_of_element_located((By.XPATH, project_icon)))
            highlight_element(driver, project_btn)
            project_btn.click()
            time.sleep(2)
        except Exception as e:
            step_fail(driver, " Click project icon", e)
    with allure.step("Click project task in the list"):
        try:
            project_file = os.path.join("data", "latest_project.txt")
            with open(project_file, "r") as f:
                created_project_name = f.read().strip()
            project_task = wait.until(EC.presence_of_element_located((By.XPATH, f"//div[@class='w-full truncate' and contains(@title,'{created_project_name}')]")))
            driver.execute_script("arguments[0].scrollIntoView({block:'center', inline:'center'});", project_task)
            highlight_element(driver, project_task)
            project_task.click()
            time.sleep(2)
        except Exception as e:
            step_fail(driver, "Click project task in the list", e)
    
    with allure.step("Click 'Add new task' button"):
        try:
            add_new_task_btn = wait.until(EC.presence_of_element_located((By.XPATH, "//button[@title='Add new task']")))
            highlight_element(driver, add_new_task_btn)
            add_new_task_btn.click()
            time.sleep(1)
        except Exception as e:
            step_fail(driver, "Click 'Add new task' button", e)
        
    with allure.step("Open milestone dropdown, enter milestone name, select option"):
        try:
            milestone_file = os.path.join("data", "latest_milestone.txt")

            with open(milestone_file, "r") as f:
                created_milestone = f.read().strip()

            print(f"Using Milestone: {created_milestone}")  
            milestone_dropdown = wait.until(EC.element_to_be_clickable((By.XPATH, "(//div[@class='css-b62m3t-container'])[1]")))
            highlight_element(driver, milestone_dropdown)
            milestone_dropdown.click()

            milestone_input = driver.switch_to.active_element
            milestone_input.send_keys(created_milestone)
            time.sleep(1)

            milestone_option = wait.until(EC.element_to_be_clickable((By.XPATH, f"//div[contains(@class,'option') and normalize-space()='{created_milestone}']")))
            highlight_element(driver, milestone_option)
            milestone_option.click()
        except Exception as e:
            step_fail(driver, "Open milestone dropdown, enter milestone name, select option", e)
    
    with allure.step("Click 'Next' button"):
        try:
            next_btn = wait.until(EC.presence_of_element_located((By.XPATH, "//button[normalize-space()='Next']")))
            highlight_element(driver, next_btn)
            next_btn.click()
            time.sleep(1)
            print("✅ Project Submit clicked")
        except Exception as e:
            step_fail(driver, "Click 'Next' button", e)

    
    test_case_details = pd.read_excel(os.path.join("data", "test_case_selector.xlsx"), sheet_name=f"add_task_test_cases").fillna("")
    # test_case_details = pd.read_excel(os.path.join("data", "test_case_selector.xlsx")).fillna("")
    first_row = test_case_details.iloc[0]
    task_name = milestone_task_name if milestone_task_name else "task_name"
    # task_name = first_row.get('task_name')
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
                time.sleep(4)
                # return True
            else:
                allure.attach("Test case failed for Task Creation", name="Task Creation Validation Failed", attachment_type=allure.attachment_type.TEXT)
                return False
        except Exception as e:
            allure.attach(str(e), name="Add Task Error", attachment_type=allure.attachment_type.TEXT)
    with allure.step("Click the newly created milestone task"):
        try: 
            milestone_task_btn = wait.until(EC.presence_of_element_located((By.XPATH, f"//div[@title='{milestone_task_name}']")))
            highlight_element(driver, milestone_task_btn)
            milestone_task_fetch = milestone_task_btn .text.strip()
            milestone_task_btn.click()
            time.sleep(2)
            print(f"{milestone_task_fetch} created")
        except Exception as e:
            step_fail(driver, "Click the newly created milestone task", e)
    
    with allure.step("Click close button on task details panel"):
        try:
            close_btn = wait.until(EC.presence_of_element_located((By.XPATH, task_project_close_btn)))
            highlight_element(driver, close_btn)
            close_btn.click()
            time.sleep(1)
            print("✅ Close Submit clicked")
        except Exception as e:
            step_fail(driver, "Click close button on task details panel", e)
    with allure.step("Click Milestone close button on task details panel"):
        try:
            milestone_close_btn = wait.until(EC.presence_of_element_located((By.XPATH, milestone_cancel_btn)))
            highlight_element(driver, milestone_close_btn)
            milestone_close_btn.click()
            time.sleep(2)
            print("✅ Milestone Submit clicked")
        except Exception as e:
            step_fail(driver, "Click Milestone close button on task details panel", e)
    
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
            step_fail(driver, "Step 5: Verify created task by searching", e)
        with allure.step("Validate Project Task vs Dashboard Search Task"):

            validation_msg = f"Actual Project Task ='{milestone_task_fetch}', Expected Dashboard Search Task='{task_name}'"
            
            print(validation_msg)
            allure.attach(validation_msg, name="Task Validation", attachment_type=allure.attachment_type.TEXT)

            if milestone_task_fetch != task_name:
                print(f"❌ Mismatch: {validation_msg}")
                allure.attach("❌ FAILED", name="Status", attachment_type=allure.attachment_type.TEXT)
                pytest.fail(validation_msg)
            else:
                print(f"✅ Match: {validation_msg}")
                allure.attach("✅ PASSED", name="Status", attachment_type=allure.attachment_type.TEXT)
    with allure.step("Click close button on task details"):
        try:
            close_btn = wait.until(EC.presence_of_element_located((By.XPATH, task_project_close_btn)))
            highlight_element(driver, close_btn)
            close_btn.click()
            wait_for_loader_to_disappear(driver, wait)
            time.sleep(3)
        except Exception as e:
            step_fail(driver, "Click close button on task details", e)
    
    with allure.step("Click Search close button on task details"):
        try:
            search_close_btn = wait.until(EC.presence_of_element_located((By.XPATH,  task_search_close_btn)))
            highlight_element(driver, search_close_btn)
            search_close_btn.click()
            wait_for_loader_to_disappear(driver, wait)
            time.sleep(3)
        except Exception as e:
            step_fail(driver, "Click Search close button on task details", e)
    
    return True 