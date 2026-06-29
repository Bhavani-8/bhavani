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
from utilities.special_add_task_utils import special_task_check
from utilities.add_task_functions.format_time_if_valid import format_time_if_valid
from utilities.add_task_functions.format_date_if_valid import format_date_if_valid

from utilities.other_utils_functions.highlight import highlight_element
from selenium.common.exceptions import TimeoutException
from utilities.add_task_utils import wait_for_loader_to_disappear

def step_fail(driver, step_name, error):
    allure.attach(str(error), name=f"{step_name} Error", attachment_type=allure.attachment_type.TEXT)
    allure.attach(driver.get_screenshot_as_png(), name=f"{step_name} Screenshot", attachment_type=allure.attachment_type.PNG)
    pytest.fail(f"❌ {step_name} failed")

def configurations_special_task(driver, wait):

    with allure.step("Load locators.json"):
        try:
            with open(os.path.join("data", "locators.json"), "r") as f:
                elements_details = json.load(f)
            settings_icon = elements_details["settings_icon"]
            toast_msg = elements_details["toast_msg"]
            config_btn_elem = elements_details['config_btn_elem']
            config_submit = elements_details['config_submit']
           
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
            configurations_btn = wait.until(EC.element_to_be_clickable((By.XPATH, config_btn_elem)))
            highlight_element(driver, configurations_btn)
            configurations_btn.click()
        except Exception as e:
            step_fail(driver, "Click configurations", e)
    

    normal_switches = [
        {
            "label": "Allow task creation without assignee",
            "for_attr": "TASK_CREATE_ASSIGNEE_REQUIRED"
        },
        {
            "label": "Allow task creation without approver",
            "for_attr": "TASK_CREATE_APPROVER_REQUIRED"
        }
    ]

    for switch in normal_switches:
        try:
            with allure.step(f"Validate and Enable '{switch['label']}'"):

                switch_xpath = (f"//label[@for='{switch['for_attr']}']"f"/following::*[@role='switch'][1]")
                switch_elem = wait.until(EC.element_to_be_clickable((By.XPATH, switch_xpath)))
                driver.execute_script("arguments[0].scrollIntoView({block:'center'});",switch_elem)
                highlight_element(driver, switch_elem)
                current_status = switch_elem.get_attribute("aria-checked")
                current_status_text = ("Enabled" if current_status == "true" else "Disabled")
                print(f"Current status for '{switch['label']}': "f"{current_status_text}")
                allure.attach(f"Current Status: {current_status_text}",name=f"{switch['label']} - Before",attachment_type=allure.attachment_type.TEXT)
                # Enable if Disabled
                if current_status == "false":
                    switch_elem.click()
                    time.sleep(1)
                    print(f"✅ '{switch['label']}' enabled successfully.")
                else:
                    print(f"ℹ️ '{switch['label']}' is already enabled.")
                # Re-fetch and validate final status
                switch_elem = wait.until(EC.presence_of_element_located((By.XPATH, switch_xpath)))
                final_status = switch_elem.get_attribute("aria-checked")
                final_status_text = ("Enabled" if final_status == "true" else "Disabled")

                print(f"Final status for '{switch['label']}': "f"{final_status_text}")
                allure.attach(f"Final Status: {final_status_text}",name=f"{switch['label']} - After",attachment_type=allure.attachment_type.TEXT)

                if final_status == "true":
                    print(f"✅ Validation Passed: '{switch['label']}' is Enabled.")
                else:
                    print(f"❌ Validation Failed: '{switch['label']}' is still Disabled.")

        except Exception as e:
            print(f"❌ Failed for '{switch['label']}': {e}")

            allure.attach(str(e),name=f"{switch['label']} Error",attachment_type=allure.attachment_type.TEXT)

    # Submit once after normal task switches
    try:
        submit_btn = wait.until(EC.element_to_be_clickable((By.XPATH, config_submit)))
        highlight_element(driver, submit_btn)
        submit_btn.click()

        print("✅ Normal task configuration submitted successfully.")
        time.sleep(2)

    except Exception as e:
        print(f"❌ Failed to click submit button: {e}")


    special_switches = [
        {
            "label": "Allow special task creation without assignee",
            "for_attr": "SPECIAL_TASK_CREATE_ASSIGNEE_REQUIRED"
        },
        {
            "label": "Allow special task creation without approver",
            "for_attr": "SPECIAL_TASK_CREATE_APPROVER_REQUIRED"
        }
    ]

    for switch in special_switches:
        try:
            with allure.step(f"Validate and Disable '{switch['label']}'"):

                switch_xpath = (f"//label[@for='{switch['for_attr']}']"f"/following::*[@role='switch'][1]")

                switch_elem = wait.until(EC.element_to_be_clickable((By.XPATH, switch_xpath)))
                driver.execute_script("arguments[0].scrollIntoView({block:'center'});",switch_elem)
                highlight_element(driver, switch_elem)

                current_status = switch_elem.get_attribute("aria-checked")
                current_status_text = ("Enabled" if current_status == "true" else "Disabled")

                print(f"Current status for '{switch['label']}': "f"{current_status_text}")

                allure.attach(f"Current Status: {current_status_text}",name=f"{switch['label']} - Before",attachment_type=allure.attachment_type.TEXT)

                # Disable if Enabled
                if current_status == "true":
                    switch_elem.click()
                    time.sleep(1)
                    print(f"✅ '{switch['label']}' disabled successfully.")
                else:
                    print(f"ℹ️ '{switch['label']}' is already disabled.")

                # Re-fetch and validate final status
                switch_elem = wait.until(EC.presence_of_element_located((By.XPATH, switch_xpath)))
                final_status = switch_elem.get_attribute("aria-checked")
                final_status_text = ("Enabled" if final_status == "true" else "Disabled")
                print(f"Final status for '{switch['label']}': "f"{final_status_text}")
                allure.attach(f"Final Status: {final_status_text}",name=f"{switch['label']} - After",attachment_type=allure.attachment_type.TEXT)

                if final_status == "false":
                    print(f"✅ Validation Passed: '{switch['label']}' is Disabled.")
                else:
                    print(f"❌ Validation Failed: '{switch['label']}' is still Enabled.")

        except Exception as e:
            print(f"❌ Failed for '{switch['label']}': {e}")

            allure.attach(str(e),name=f"{switch['label']} Error",attachment_type=allure.attachment_type.TEXT)

    # Submit once after special task switches
    try:
        submit_btn = wait.until(EC.element_to_be_clickable((By.XPATH, config_submit)))
        highlight_element(driver, submit_btn)
        submit_btn.click()
        print("✅ Special task configuration submitted successfully.")
        time.sleep(2)

    except Exception as e:
        print(f"❌ Failed to click submit button: {e}")
            
        try:
            toast = wait.until(EC.presence_of_element_located((By.XPATH, toast_msg)))
            highlight_element(driver, toast)
            print(f"📢 Toast message: {toast.text.strip()}")
        except Exception:
            print("❌ No toast message found")


    test_case_details = pd.read_excel(os.path.join("data", "test_case_selector.xlsx"), sheet_name=f"special_add_task_test_cases").fillna("")
    # test_case_details = pd.read_excel(os.path.join("data", "test_case_selector.xlsx")).fillna("")
    first_row = test_case_details.iloc[0]
    # task_name = first_row.get('task_name')
    task_name = str(first_row.get('task_name', '')).strip()
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
        task_name = f"{task_name}_config_task"
        try:
            if special_task_check(driver, task_name, start_date, due_date, frequency, repeat_if_holiday, end_freq_date,
                repeat_weekday, repeat_day_month, end_time, internal_deadline, assign_to, approver, cc,
                risk_rating, license_name, task_category, description, attach_file_name, impact_details, impact_file_name,
                circular_search, test_type, task_type='mandatory', direct_task_creation=False):
                print("✅ Task creation successful")
            else:
                allure.attach("Test case failed for Task Creation", name="Task Creation Validation Failed", attachment_type=allure.attachment_type.TEXT)
                return False
        except Exception as e:
            allure.attach(str(e), name="Add Task Error", attachment_type=allure.attachment_type.TEXT)

    return True