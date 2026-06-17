
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
from selenium.common.exceptions import TimeoutException
from utilities.add_task_utils import wait_for_loader_to_disappear
from utilities.add_task_functions.format_time_if_valid import format_time_if_valid
from utilities.add_task_functions.format_date_if_valid import format_date_if_valid
from utilities.add_task_utils import add_task_check

def step_fail(driver, step_name, error):
    allure.attach(str(error), name=f"{step_name} Error", attachment_type=allure.attachment_type.TEXT)
    allure.attach(driver.get_screenshot_as_png(), name=f"{step_name} Screenshot", attachment_type=allure.attachment_type.PNG)
    pytest.fail(f"❌ {step_name} failed")
   
def project_task_restore_delete(driver, wait):

    with allure.step("Load locators.json"):
        try:
            with open(os.path.join("data", "locators.json"), "r") as f:
                elements_details = json.load(f)

            project_icon = elements_details["project_icon"]
            toast_msg = elements_details['toast_msg']
            trash_icon = elements_details['trash_icon']
            milestone_cancel_btn = elements_details['milestone_cancel_btn']

            print("✅ locators.json loaded")
        except Exception as e:
            step_fail(driver, "Load locators.json", e)
        
    with allure.step("Click project icon"):
        try:
            project_btn = wait.until(EC.presence_of_element_located((By.XPATH, project_icon)))
            highlight_element(driver, project_btn)
            project_btn.click()
            time.sleep(2)
        except Exception as e:
            step_fail(driver, "Click project icon", e)
    with allure.step("Click Project Task"):
        try:
            time.sleep(1)
            project_file = os.path.join("data", "latest_project.txt")
            with open(project_file, "r") as f:
                created_project_name = f.read().strip()
            project_task = wait.until(EC.presence_of_element_located((By.XPATH, f"//div[@class='w-full truncate' and contains(@title,'{created_project_name}')]")))
            driver.execute_script("arguments[0].scrollIntoView({block:'center', inline:'center'});", project_task)
            highlight_element(driver, project_task)
            project_task.click()
            time.sleep(2)
        except Exception as e:
            step_fail(driver, "Click Project Task", e)
    with allure.step("Click 'Add new task' button"):
        try:
            add_new_task_btn = wait.until(EC.presence_of_element_located((By.XPATH, "//button[@title='Add new task']")))
            highlight_element(driver, add_new_task_btn)
            add_new_task_btn.click()
            time.sleep(1)
        except Exception as e:
            step_fail(driver, "Click 'Add new task' button", e)
    with allure.step("Click 'Next' button"):
        try:
            next_btn = wait.until(EC.presence_of_element_located((By.XPATH, "//button[normalize-space()='Next']")))
            highlight_element(driver, next_btn)
            next_btn.click()
            print("✅ Project Submit clicked")
        except Exception as e:
            step_fail(driver, "Click 'Next' button", e)

    test_case_details = pd.read_excel(os.path.join("data", "test_case_selector.xlsx"), sheet_name=f"add_task_test_cases").fillna("")
    # test_case_details = pd.read_excel(os.path.join("data", "test_case_selector.xlsx")).fillna("")
    first_row = test_case_details.iloc[0]
    task_name = first_row.get('task_name')
    # task_name = project_task_name if project_task_name else "task_name"
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
        task_name = f"{task_name}_delete_check"
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
            allure.attach(str(e), name="Add Task Error", attachment_type=allure.attachment_type.TEXT)
    with allure.step("Verify Project Task Creation"):
        try:
            time.sleep(3)
            task_name_element = wait.until(EC.visibility_of_element_located((By.XPATH, f"//div[contains(text(),'{task_name}')]")))
            highlight_element(driver, task_name_element)
            fetch_task_name = task_name_element.text.strip()
            print(f"✅ Task '{fetch_task_name}' created successfully")
        except Exception as e:
            step_fail(driver, "Verify Project Task Creation", e)
    with allure.step("Click three dots menu"):
        try:
            three_dots_btn = wait.until(EC.presence_of_element_located((By.XPATH, f"//tr[contains(@class,'dx-data-row')][.//div[contains(@class,'font-weight-normal') and @title='{task_name}']]//button")))
            driver.execute_script("arguments[0].scrollIntoView({block:'center', inline:'center'});", three_dots_btn)
            highlight_element(driver, three_dots_btn)
            three_dots_btn.click()
            time.sleep(0.5)
        except Exception as e:
            step_fail(driver, "Click three dots menu", e)
    with allure.step("Click Delete Task"):
        try:
            delete_btn = wait.until(EC.presence_of_element_located((By.XPATH, "//button[@title='Delete']")))
            highlight_element(driver, delete_btn)
            delete_btn.click()
            print("🗑️ Delete button clicked")

            yes_btn = wait.until(EC.presence_of_element_located((By.XPATH,"//button//span[text()='Yes']")))
            highlight_element(driver, yes_btn)
            yes_btn.click()
            time.sleep(2)
            print("☑️ YES clicked — Task delete confirmed")

        except Exception as e:
            step_fail(driver, "Click Delete Task", e)
    
   
    with allure.step("Click Milestone close button on task details panel"):
        try:
            milestone_close_btn = wait.until(EC.presence_of_element_located((By.XPATH, milestone_cancel_btn)))
            highlight_element(driver, milestone_close_btn)
            milestone_close_btn.click()
            time.sleep(2)
            print("✅ Milestone Submit clicked")
        except Exception as e:
            step_fail(driver, "Click Milestone close button on task details panel", e)
    with allure.step("Click Trash Icon"):
        try:
            print()
            trash_btn = wait.until(EC.presence_of_element_located((By.XPATH, trash_icon)))
            highlight_element(driver, trash_btn)
            trash_btn.click()
            print("🗑️ Trash icon clicked")

        except Exception as e:
            step_fail(driver, "Click Trash Icon", e)

    with allure.step("Click Tasks Tab"):
        try:
            time.sleep(3)
            tasks_tab = wait.until(EC.presence_of_element_located((By.XPATH, "//button[text()='Tasks']")))
            highlight_element(driver, tasks_tab)
            tasks_tab.click()
            print("📌 Tasks tab clicked")

        except Exception as e:
            step_fail(driver, "Click Tasks Tab", e)
    
    with allure.step("Verify Project Task in Trash"):
        try:
            task_name_elem = wait.until(EC.visibility_of_element_located((By.XPATH, f"//span[@title='{task_name}']")))
            highlight_element(driver, task_name_elem)
            fetch_task_name_elem = task_name_elem.text.strip()
            print(f"✅ Task '{fetch_task_name_elem}' found in Trash")
        except Exception as e:
            step_fail(driver, "Verify Project Task in Trash", e)
    
    with allure.step("Click Restore Task"):
        try:
            time.sleep(3)
            restore_elem = wait.until(EC.presence_of_element_located((By.XPATH, f"//tr[@data-slot='table-row'][.//span[@title='{task_name}']]//button[@title='Restore Task']")))
            highlight_element(driver, restore_elem)
            restore_elem.click()
            time.sleep(3)
            print("📌 Restore Task button clicked")

        except Exception as e:
           step_fail(driver, "Click Project Task", e)

    with allure.step("Click project icon"):
        try:
            project_btn = wait.until(EC.presence_of_element_located((By.XPATH, project_icon)))
            highlight_element(driver, project_btn)
            project_btn.click()
            time.sleep(2)
        except Exception as e:
            step_fail(driver, "Click project icon", e)

    with allure.step("Click Project Task"):
        try:
            time.sleep(1)
            project_file = os.path.join("data", "latest_project.txt")
            with open(project_file, "r") as f:
                created_project_name = f.read().strip()
            project_task = wait.until(EC.presence_of_element_located((By.XPATH, f"//div[@class='w-full truncate' and contains(@title,'{created_project_name}')]")))
            driver.execute_script("arguments[0].scrollIntoView({block:'center', inline:'center'});", project_task)
            highlight_element(driver, project_task)
            project_task.click()
            time.sleep(2)
        except Exception as e:
            step_fail(driver, "Click Project Task", e)
    
    with allure.step("Click project task three dots menu"):
        try:
            three_dots_btn = wait.until(EC.presence_of_element_located((By.XPATH, f"//tr[contains(@class,'dx-data-row')][.//div[contains(@class,'font-weight-normal') and @title='{task_name}']]//button")))
            driver.execute_script("arguments[0].scrollIntoView({block:'center', inline:'center'});", three_dots_btn)
            highlight_element(driver, three_dots_btn)
            three_dots_btn.click()
            time.sleep(1)
        except Exception as e:
            step_fail(driver, "Click project task three dots menu", e)
    with allure.step("Click Delete Task"):
        try:
            delete_btn = wait.until(EC.presence_of_element_located((By.XPATH, "//button[@title='Delete']")))
            highlight_element(driver, delete_btn)
            delete_btn.click()
            print("🗑️ Delete button clicked")

            yes_btn = wait.until(EC.presence_of_element_located((By.XPATH,"//button//span[text()='Yes']")))
            highlight_element(driver, yes_btn)
            yes_btn.click()
            time.sleep(3)
            print("☑️ YES clicked — Task delete confirmed")

        except Exception as e:
            step_fail(driver, "Click Delete Task", e)
    with allure.step("Click Milestone close button on task details"):
        try:
            milestone_close_btn = wait.until(EC.presence_of_element_located((By.XPATH, milestone_cancel_btn)))
            highlight_element(driver, milestone_close_btn)
            milestone_close_btn.click()
            print("✅ Milestone Submit clicked")
        except Exception as e:
            step_fail(driver, "Click Milestone close button on task details", e)
    
    return True