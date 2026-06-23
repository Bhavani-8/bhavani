import allure
import os
import json
import time
import pyautogui as pg
import pytest
import random
import pandas as pd

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from utilities.add_task_utils import add_task_check
from utilities.add_task_functions.format_time_if_valid import format_time_if_valid
from utilities.add_task_functions.format_date_if_valid import format_date_if_valid

from utilities.other_utils_functions.highlight import highlight_element
from selenium.common.exceptions import TimeoutException
from utilities.add_task_utils import wait_for_loader_to_disappear

def step_fail(driver, step_name, error):
    allure.attach(str(error), name=f"{step_name} Error", attachment_type=allure.attachment_type.TEXT)
    allure.attach(driver.get_screenshot_as_png(), name=f"{step_name} Screenshot", attachment_type=allure.attachment_type.PNG)
    pytest.fail(f"❌ {step_name} failed")

def configurations_normal_task(driver, wait, config_normal_task_name):

    with allure.step("Load locators.json"):
        try:
            with open(os.path.join("data", "locators.json"), "r") as f:
                elements_details = json.load(f)
            settings_icon = elements_details["settings_icon"]
            toast_msg = elements_details["toast_msg"]
           
        except Exception as e:
            step_fail(driver, "Load locators.json", e)

    with allure.step("Click Settings"):
        try:
            settings_btn = wait.until(EC.element_to_be_clickable((By.XPATH, settings_icon)))
            highlight_element(driver, settings_btn)
            settings_btn.click()
        except Exception as e:
            step_fail(driver, "Click Settings", e)

    with allure.step("Click on configurations"):
        try:
            configurations_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[normalize-space()='Configurations']")))
            highlight_element(driver, configurations_btn)
            configurations_btn.click()
        except Exception as e:
            step_fail(driver, "Click configurations", e)
    
    with allure.step("Allow Task creation without Assignee and Approver"):
        try:
            allow_task_creation_label = wait.until(EC.visibility_of_element_located((By.XPATH, "//label[@for='TASK_CREATE_ASSIGNEE_REQUIRED']")))
            highlight_element(driver, allow_task_creation_label)
            label_text = allow_task_creation_label.text.strip()
            print(f"✅ Label Name: {label_text}")
            allure.attach(label_text,name="Allow Task Creation Label",attachment_type=allure.attachment_type.TEXT)

        except Exception as e:
            allure.attach(str(e),name="Allow Task Creation Label Error",attachment_type=allure.attachment_type.TEXT)
            print(f"❌ Failed to fetch label: {e}")
            wait_for_loader_to_disappear(driver, wait)
            time.sleep(2)

    switch_details = [
        {
            "label": "Allow task creation without assignee",
            "for_attr": "TASK_CREATE_ASSIGNEE_REQUIRED"
        },
        {
            "label": "Allow task creation without approver",
            "for_attr": "TASK_CREATE_APPROVER_REQUIRED"
        }
    ]

    for switch in switch_details:
        try:
            with allure.step(f"Validate and Disable '{switch['label']}'"):

                switch_elem = wait.until(EC.element_to_be_clickable((By.XPATH,f"//label[@for='{switch['for_attr']}']/following::*[@role='switch'][1]")))
                driver.execute_script("arguments[0].scrollIntoView({block:'center'});",switch_elem)
                highlight_element(driver, switch_elem)

                # Initial Status
                current_status = switch_elem.get_attribute("aria-checked")
                current_status_text = ("Enabled" if current_status == "true" else "Disabled")
                print(f"Current status for '{switch['label']}': {current_status_text}")
                allure.attach(f"Current Status: {current_status_text}",name=f"{switch['label']} - Before",attachment_type=allure.attachment_type.TEXT)

                # Disable if Enabled
                if current_status == "true":
                    switch_elem.click()
                    time.sleep(1)
                    print(f"✅ '{switch['label']}' disabled successfully.")
                else:
                    print(f"ℹ️ '{switch['label']}' is already disabled.")

                # Re-fetch element
                switch_elem = wait.until(EC.presence_of_element_located((By.XPATH,f"//label[@for='{switch['for_attr']}']/following::*[@role='switch'][1]")))

                final_status = switch_elem.get_attribute("aria-checked")
                final_status_text = ("Enabled" if final_status == "true" else "Disabled")

                print(f"Final status for '{switch['label']}': {final_status_text}")

                allure.attach(f"Final Status: {final_status_text}",name=f"{switch['label']} - After",attachment_type=allure.attachment_type.TEXT)

                if final_status == "false":
                    print(f"✅ Validation Passed: '{switch['label']}' is Disabled.")
                else:
                    print(f"❌ Validation Failed: '{switch['label']}' is still Enabled.")

        except Exception as e:
            print(f"❌ Failed for '{switch['label']}': {e}")
            allure.attach(str(e),name=f"{switch['label']} Error",attachment_type=allure.attachment_type.TEXT)

        try:
            submit_btn = wait.until(EC.presence_of_element_located((By.XPATH, "//button[text()='Submit']")))
            highlight_element(driver, submit_btn)
            submit_btn.click()
        except Exception as e:
            print("❌Failed to click submit button")
        
        try:
            toast = wait.until(EC.presence_of_element_located((By.XPATH, toast_msg)))
            highlight_element(driver, toast)
            print(f"📢 Toast message: {toast.text.strip()}")
        except Exception:
            print("❌ No toast message found")


    test_case_details = pd.read_excel(os.path.join("data", "test_case_selector.xlsx"), sheet_name=f"add_task_test_cases").fillna("")
    # test_case_details = pd.read_excel(os.path.join("data", "test_case_selector.xlsx")).fillna("")
    first_row = test_case_details.iloc[0]
    # task_name = updates_task_name if updates_task_name else "task_name"
    task_name = config_normal_task_name.strip() if config_normal_task_name else "task_name"

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
                circular_search, test_type, task_type='mandatory', direct_task_creation=False):
                print("✅ Task creation successful")
                # return True
            else:
                allure.attach("Test case failed for Task Creation", name="Task Creation Validation Failed", attachment_type=allure.attachment_type.TEXT)
                return False
        except Exception as e:
            step_fail(driver, "Load locators.json", e)    
    return True
