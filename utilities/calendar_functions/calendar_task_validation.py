import allure
import time
import pyautogui as pg
import pytest
import random
import os
import json
from datetime import datetime
import pandas as pd
from utilities.add_task_functions.show_toast import show_toast
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from utilities.add_task_functions.task_validation import task_validation
from utilities.add_task_functions.format_time_if_valid import format_time_if_valid
from utilities.add_task_functions.format_date_if_valid import format_date_if_valid
from utilities.add_task_utils import add_task_check
from utilities.add_task_functions.wait_for_loader_to_disappear import wait_for_loader_to_disappear
from utilities.other_utils_functions.highlight import highlight_element


def validate_today_task(driver, wait, calendar_task_name):
    with allure.step("Loading locators from JSON"):
        try:
            with open(os.path.join("data", 'locators.json'), 'r') as f:
                elements_details = json.load(f)
                calendar_icon = elements_details["calendar_icon"]
                calendar_filter_btn = elements_details['calendar_filter_btn']
                calendar_today_btn = elements_details['calendar_today_btn']
                calendar_day_btn = elements_details['calendar_day_btn']
            print("✅ locators.json loaded successfully")
        except FileNotFoundError as e:
            print("❌ locators.json file not found")
            allure.attach(str(e), name="Locators_FileNotFound", attachment_type=allure.attachment_type.TEXT)
            pytest.fail("locators.json file not found")
        except json.JSONDecodeError as e:
            print("❌ Invalid JSON in locators.json")
            allure.attach(str(e), name="Invalid_JSON", attachment_type=allure.attachment_type.TEXT)
            pytest.fail("Invalid JSON in locators.json")

    test_case_details = pd.read_excel(os.path.join("data", "test_case_selector.xlsx"), sheet_name=f"add_task_test_cases").fillna("")
    # test_case_details = pd.read_excel(os.path.join("data", "test_case_selector.xlsx")).fillna("")
    first_row = test_case_details.iloc[0]
    task_name = (calendar_task_name if calendar_task_name else f"task_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
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

        try:
            if add_task_check(driver, task_name, start_date, due_date, frequency, repeat_if_holiday, end_freq_date,
                repeat_weekday, repeat_day_month, end_time, internal_deadline, assign_to, approver, cc,
                risk_rating, license_name, description, attach_file_name, impact_details, impact_file_name,
                circular_search, test_type, task_type='mandatory', direct_task_creation=False):
                print("✅ Task creation successful")
                time.sleep(6)
                # return True
            else:
                allure.attach("Test case failed for Task Creation", name="Task Creation Validation Failed", attachment_type=allure.attachment_type.TEXT)
                return False
        except Exception as e:
            allure.attach(str(e), name="Add Task Error", attachment_type=allure.attachment_type.TEXT)
    
    with allure.step("Click Calendar Icon"):
        try:
            calendar_btn = wait.until(EC.presence_of_element_located((By.XPATH, calendar_icon)))
            highlight_element(driver, calendar_btn)
            calendar_btn.click()
            time.sleep(3)
        except Exception as e:
            msg = f"failed to click Calender button: {str(e)}"
            print(msg)
            allure.attach(msg, name="Calendar Button Error", attachment_type=allure.attachment_type.TEXT)
            return False
    
    with allure.step("Click Day Button in Calendar"):
        try:
            day_btn = wait.until(EC.presence_of_element_located((By.XPATH, calendar_day_btn)))
            highlight_element(driver, day_btn)
            day_btn.click()
            wait_for_loader_to_disappear(driver, wait)
            time.sleep(3)
        except Exception as e:
            msg = f"failed to click Day button: {str(e)}"
            print(msg)
            allure.attach(msg, name="Day Button Error", attachment_type=allure.attachment_type.TEXT)
            return False
    with allure.step("Click Date Calendar"): 
        try:
            calendar_date_btn = wait.until(EC.presence_of_element_located((By.XPATH, calendar_filter_btn)))
            highlight_element(driver, calendar_date_btn)
            calendar_date_btn.click()
            time.sleep(3)
        except Exception as e:
            msg = f"failed to click Calender Date button: {str(e)}"
            print(msg)
            allure.attach(msg, name="Calendar Date Button Error", attachment_type=allure.attachment_type.TEXT)
            return False
    
    with allure.step("Click Today Day Button in Calendar"):
        try:
            today_btn = wait.until(EC.presence_of_element_located((By.XPATH, calendar_today_btn)))
            highlight_element(driver, today_btn)
            today_btn.click()
            time.sleep(3)
        except Exception as e:
            msg = f"failed to click Calender Today button: {str(e)}"
            print(msg)
            allure.attach(msg, name="Calendar Today Button Error", attachment_type=allure.attachment_type.TEXT)
            return False
    with allure.step("Click Today Task Button in Calendar"):
        try:
            click_task_btn = wait.until(EC.presence_of_element_located((By.XPATH, f"//h2[text()='{task_name}']")))
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", click_task_btn)
            time.sleep(2)
            highlight_element(driver, click_task_btn)
            click_task_btn.click()
            time.sleep(3)
            print("Cicked Today Task")
        except Exception as e:
            msg = f"failed to click Today Task button: {str(e)}"
            print(msg)
            allure.attach(msg, name="Today Task Button Error", attachment_type=allure.attachment_type.TEXT)
            return False

    # with allure.step("Validate Task Details After Submission"):
    #     print(f"Validate Task Details After Submission:")
    #     validation_success = task_validation(driver, wait)
    #     if validation_success:
    #         # allure.attach("Validate Task Details After Submission successfull", name="Validation Status", attachment_type=allure.attachment_type.TEXT)
    #         print("✅ Validate Task Details After Submission successful.")
    #         return True
    #     else:
    #         msg = "❌ Failed to Validate Task Details After Submission."
    #         print(msg)
    #         allure.attach(msg, name="Validation Status", attachment_type=allure.attachment_type.TEXT)
    #         show_toast(driver, msg)
    #         time.sleep(2)
    #         return False  
    return True
    