from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import allure
import json
import os
import time
import pytest
from datetime import datetime, timedelta

import pandas as pd
import pyautogui as pg
import glob
from utilities.add_task_functions.add_task_common import task_value_store
from utilities.add_task_functions.add_task_common import task_value_get
from utilities.add_task_functions.format_time_if_valid import format_time_if_valid
from utilities.add_task_functions.format_date_if_valid import format_date_if_valid
from utilities.add_task_utils import add_task_check
from utilities.other_utils_functions.highlight import highlight_element
from utilities.add_task_functions.wait_for_loader_to_disappear import wait_for_loader_to_disappear



def update_internal_deadline(driver, wait, internal_deadline):
    with allure.step("Loading locators from JSON"):
        try:
            with open(os.path.join("data", 'locators.json'), 'r') as f:
                elements_details = json.load(f)
                task_deadline_label = elements_details['task_deadline_label']
                

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

    test_case_details = pd.read_excel(os.path.join("data", "test_case_selector.xlsx"), sheet_name=f"add_task_test_cases").fillna("")
    # test_case_details = pd.read_excel(os.path.join("data", "test_case_selector.xlsx")).fillna("")
    first_row = test_case_details.iloc[0]
    # task_name = (new_compliance_task if new_compliance_task else f"task_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
    # task_name = project_task_name or first_row.get('task_name')
    current_task_name = internal_deadline.strip() if internal_deadline else "task_name"
    task_name = current_task_name
    task_value_store("task_name", task_name)

    start_date = datetime.today().strftime("%d %B %Y")
    due_date = (datetime.today() + timedelta(days=7)).strftime("%d %B %Y")
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
                created_task = task_value_get("task_name")
                print(f"Update Internal Deadline {created_task}")
            else:
                    allure.attach("Test case failed for Task Creation", name="Task Creation Validation Failed", attachment_type=allure.attachment_type.TEXT)
                    return False
        except Exception as e:
            allure.attach(str(e), name="Add Task Error", attachment_type=allure.attachment_type.TEXT)
        
    with allure.step("Verify Internal Deadline Before Update"):
        try:
            task_deadline_label_elem = wait.until(EC.visibility_of_element_located((By.XPATH, task_deadline_label)))
            highlight_element(driver, task_deadline_label_elem)
            task_deadline_text = task_deadline_label_elem.text.strip()

            fetched_deadline = datetime.strptime(task_deadline_text,"%d %b %Y %I:%M %p")
            print(f"Fetched Deadline: {fetched_deadline}")

            allure.attach(fetched_deadline.strftime("%d %b %Y %I:%M %p"),name="Before Update - Internal Deadline (Date & Time)",attachment_type=allure.attachment_type.TEXT)
    
        except Exception as e:
            msg = f"Failed to Fetch Internal Deadline: {str(e)}"
            print(msg)
            allure.attach(msg, name="Internal Deadline Fetch Error", attachment_type=allure.attachment_type.TEXT)
            raise Exception(msg)
    with allure.step("Edit Internal Deadline"):
        try:
            edit_internal_deadline=wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class,'holding-list-bold-title')]//button")))
            highlight_element(driver, edit_internal_deadline)
            edit_internal_deadline.click()
        except Exception as e:
            msg = f"Failed to Click Edit Internal deadline button: {str(e)}"
            print(msg)
            allure.attach(msg, name="Internal Deadline Button Error", attachment_type=allure.attachment_type.TEXT)
            raise Exception(msg)
        
        try:
            calendar_btn=wait.until(EC.presence_of_element_located((By.XPATH, "(//div[contains(@class,'ant-picker-input')])[1]")))
            highlight_element(driver, calendar_btn)
            calendar_btn.click()
            future_date = (datetime.today() + timedelta(days=2)).day
            future_date_ele = wait.until(EC.element_to_be_clickable((By.XPATH, f"//div[text()='{future_date}']")))
            highlight_element(driver, future_date_ele)
            future_date_ele.click()
        except Exception as e:
            msg = f"Failed to click Calendar Button: {str(e)}"
            print(msg)
            allure.attach(msg, name="Calendar Button Error", attachment_type=allure.attachment_type.TEXT)
            raise Exception(msg)
        
    with allure.step("Edit Time"):
        
        try:
            time_btn=wait.until(EC.presence_of_element_located((By.XPATH, "(//div[contains(@class,'ant-picker-input')])[2]")))
            highlight_element(driver, time_btn)
            time_btn.click()
            # presnt_time = (datetime.today() + timedelta(days=2)).day
            present_time = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[text()='Now']")))
            highlight_element(driver, present_time)
            present_time.click()
        except Exception as e:
            msg = f"Failed to click Time Button: {str(e)}"
            print(msg)
            allure.attach(msg, name="Time Button Error", attachment_type=allure.attachment_type.TEXT)
            raise Exception(msg)
            
        try: 
            confirm_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[span[text()='Confirm']]")))
            highlight_element(driver, confirm_btn)
            confirm_btn.click()
            time.sleep(2)
        except Exception as e:
            msg = f"Failed to click Confirm Button: {str(e)}"
            print(msg)
            allure.attach(msg, name="Confirm Button Error", attachment_type=allure.attachment_type.TEXT)
            raise Exception(msg)
    
    with allure.step("Verify Internal Deadline After Update"):
        try:
            task_deadline_label_elem = wait.until(EC.visibility_of_element_located((By.XPATH, task_deadline_label)))
            highlight_element(driver, task_deadline_label_elem)
            task_deadline_text = task_deadline_label_elem.text.strip()

            fetched_deadline = datetime.strptime(task_deadline_text,"%d %b %Y %I:%M %p")
            print(f"Fetched Deadline: {fetched_deadline}")

            allure.attach(fetched_deadline.strftime("%d %b %Y %I:%M %p"),name="After Update - Internal Deadline (Date & Time)",attachment_type=allure.attachment_type.TEXT)
    
        except Exception as e:
            msg = f"Failed to Fetch Internal Deadline: {str(e)}"
            print(msg)
            allure.attach(msg, name="Internal Deadline Fetch Error", attachment_type=allure.attachment_type.TEXT)
            raise Exception(msg)
    return True
        
    
    
    