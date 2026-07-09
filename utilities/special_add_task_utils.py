# add_task_utils.py
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from datetime import datetime, date, time as dt_time
from dateutil.parser import parse
from calendar import monthrange
from dateutil import parser
import pyautogui as pg
import pandas as pd
import pytest
import allure
import random
import time
import json
import re
import os
from utilities.add_task_functions.show_toast import show_toast
from utilities.add_task_functions.add_task_common import task_value_get
from utilities.add_task_functions.format_date_if_valid import format_date_if_valid
from utilities.add_task_functions.format_time_if_valid import format_time_if_valid
from utilities.add_task_functions.normalize_date import normalize_date
from utilities.add_task_functions.normalize_day_and_month import normalize_day_and_month
from utilities.add_task_functions.wait_for_loader_to_disappear import wait_for_loader_to_disappear
from utilities.add_task_functions.set_task_name import set_task_name
from utilities.add_task_functions.set_start_date import set_start_date
from utilities.add_task_functions.set_due_date import set_due_date
from utilities.add_task_functions.set_frequency import set_frequency
from utilities.add_task_functions.set_end_time import set_end_time
from utilities.add_task_functions.set_deadline_input import set_deadline_input
from utilities.add_task_functions.set_assign_to import set_assign_to
from utilities.add_task_functions.set_approver import set_approver
from utilities.add_task_functions.set_cc import set_cc
from utilities.add_task_functions.set_risk_rating import set_risk_rating
from utilities.add_task_functions.set_license import set_license
from utilities.add_task_functions.set_task_category import set_task_category
from utilities.add_task_functions.add_description import add_description
from utilities.add_task_functions.attach_file import attach_file
from utilities.add_task_functions.add_impact_details import add_impact_details
from utilities.add_task_functions.search_and_add_circulars import search_and_add_circulars
from utilities.add_task_functions.add_circulars import add_circulars
from utilities.add_task_functions.validate_search_task import validate_search_task
from utilities.add_task_functions.submit_task import submit_task
from utilities.add_task_functions.open_task import open_task
from utilities.add_task_functions.special_task_validation import special_task_validation
from utilities.other_utils_functions.license_utils import validate_license_subscription
from utilities.other_utils_functions.highlight import highlight_element
from utilities.login_utils import login_check
from load_test_config_excel_data import load_test_config_excel_data



def special_task_check(driver, task_name, start_date, due_date, frequency, repeat_if_due_date_is_on_holiday, end_frequency_date, weekday_name, repeat_day_and_month, end_time, internal_deadline, assign_to, approver, cc, risk_rating, license_name, task_category, description, attach_file_name, impact_details, impact_file_name, circular_search, test_type, task_type=None, refresh=False, login_required=True, direct_task_creation = False, module="default"):
    # Get all arguments as a local variable dictionary
    args = locals()

    # Replace NaN values with empty strings
    for key in args:
        if pd.isna(args[key]):
            args[key] = ""

    # Optionally, unpack updated variables back (if needed)
    task_name = args["task_name"]
    start_date = args["start_date"]
    due_date = args["due_date"]
    frequency = args["frequency"]
    repeat_if_due_date_is_on_holiday = args["repeat_if_due_date_is_on_holiday"]
    end_frequency_date = args["end_frequency_date"]
    weekday_name = args["weekday_name"]
    end_time = args["end_time"]
    internal_deadline = args["internal_deadline"]
    assign_to = args["assign_to"]
    approver = args["approver"]
    cc = args["cc"]
    risk = args["risk_rating"]
    license_name = args["license_name"]
    task_category = args["task_category"]
    description = args["description"]
    attach_file_name = args["attach_file_name"]
    impact_details = args["impact_details"]
    impact_file_name = args["impact_file_name"]
    circular_search = args["circular_search"]
    test_type = args["test_type"]

    wait = WebDriverWait(driver, 30)
    try:
        with open(os.path.join("data", 'locators.json'), 'r') as f:
            elements_details = json.load(f)
            add_task_float = elements_details['add_task_float']
            add_task_btn = elements_details['add_task_btn']
            task_input_error_msg = elements_details['task_input_error_msg']
            task_name_input = elements_details['task_name_input']
            start_date_input = elements_details['start_date_input']
            due_date_input = elements_details['due_date_input']
            frequency_option = elements_details['freq_option']
            frequency_value_check = elements_details['freq_value_check']
            end_time_input = elements_details['end_time_input']
            deadline_input = elements_details['deadline_input']
            assign_to_dropdown = elements_details['assign_to_dropdown']
            approver_dropdown = elements_details['approver_dropdown']
            cc_dropdown = elements_details['cc_dropdown']
            risk_rating_dropdown = elements_details['risk_rating_dropdown']
            license_input = elements_details['license_input']
            task_category_dropdown = elements_details['task_category_dropdown']
            description_btn = elements_details['desc_btn']
            description_input = elements_details['desc_input']
            desc_save_btn = elements_details['desc_save_btn']
            desc_view = elements_details['desc_view']
            attach_file_btn = elements_details['attach_file_btn']
            attach_file_input = elements_details['file_input']
            attach_file_save_btn = elements_details['attach_file_save_btn']
            attach_file_view = elements_details['attach_file_view']
            impact_button = elements_details['impact_button']
            fine_amount_editor = elements_details['fine_amount_editor']
            impact_file_save_btn = elements_details['impact_file_save_btn']
            impact_fine_amount_view = elements_details['impact_fine_amount_view']
            impact_file_view = elements_details['impact_file_view']
            regulatory_btn = elements_details['regulatory_btn']
            regulatory_search_btn = elements_details['regulatory_search_btn']
            regulatory_checkboxes = elements_details['regulatory_checkboxes']
            regulatory_save_btn = elements_details['regulatory_save_btn']
            regulatory_cancel_btn = elements_details['regulatory_cancel_btn']
            submit_button = elements_details['task_submit_btn']
            err_msg_toast = elements_details['err_msg_toast']
            toast_msg = elements_details['toast_msg']
            



    except FileNotFoundError:
        pytest.fail("locators.json file not found")
    except json.JSONDecodeError:
        pytest.fail("Invalid JSON in locators.json")
    if login_required:

        # if refresh:
        #     driver.get('https://preprodreact.compliancesutra.com/dashboard-view')
        # if not "dashboard-view" in driver.current_url:
        target_url = None
        if "project-management" in driver.current_url:
            target_url = "https://preprodreact.compliancesutra.com/project-management"
        elif "dashboard-view" in driver.current_url:
            target_url = "https://preprodreact.compliancesutra.com/dashboard-view"
        elif "updates" in driver.current_url:
            target_url = "https://preprodreact.compliancesutra.com/updates"
        elif "settings" in driver.current_url:
            target_url = "https://preprodreact.compliancesutra.com/settings"
        else:
            # Default target
            target_url = "https://preprodreact.compliancesutra.com/dashboard-view"
        if refresh and target_url:driver.get(target_url)

    # Only login if not already on dashboard or project page
        if not any(x in driver.current_url for x in ["dashboard-view", "project-management", "updates", "settings"]):

            driver.get("https://preprodreact.compliancesutra.com/login")
        # driver.get("https://preprodreact.compliancesutra.com/login")

        
        # ✅ Step 1: Login Check
            with allure.step("Login with valid credentials"):
                print("🔐 Logging in with valid credentials...")
                credentials_df = pd.read_excel(os.path.join('data', 'test_case_selector.xlsx'), sheet_name='credentials').fillna("")
                user = str(credentials_df['username'].iloc[0]).strip()
                pwd = str(credentials_df['password'].iloc[0]).strip()
                login_check_success = login_check(driver, waittime=10, trial=1, username=user, password=pwd, user_validation=False)
                if login_check_success:
                    allure.attach("Login successful", name="Login Status", attachment_type=allure.attachment_type.TEXT)
                else:
                    allure.attach("Login failed", name="Login Status", attachment_type=allure.attachment_type.TEXT)
                    return False
            
    #     wait_for_loader_to_disappear(driver, wait, loader_class="dx-loadpanel-content")

    # # ✅ Step 2: Ensure dashboard loaded
    #     if "dashboard-view" not in driver.current_url:
    #         driver.get("https://preprodreact.compliancesutra.com/dashboard-view")
    #         wait_for_loader_to_disappear(driver, wait)
    #         time.sleep(2)

    #     print("✅ Dashboard loaded")
        
    
                
    wait_for_loader_to_disappear(driver, wait)
    time.sleep(3)
    # ✅ Step 2: Locate and click on Add Task Float
    if direct_task_creation:
        with allure.step("Task form is already open"):
            print("ℹ️ Direct task creation mode: skipping button clicks.")
    else:
        with allure.step("Opening Add Task Float"):
            try:
                add_task_float_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, add_task_float)))
                highlight_element(driver, add_task_float_btn)
                add_task_float_btn.click()
            
            except Exception as err:
                add_task_float_btns = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, add_task_float)))
                for btn in add_task_float_btns:
                    highlight_element(driver, btn)
                    btn.click()
                allure.attach(err, name="Add task float button error", attachment_type=allure.attachment_type.TEXT)
    if direct_task_creation:
        with allure.step("Task form is already open"):
            print("ℹ️ Direct task creation mode: skipping button clicks.")
    else:
        with allure.step("Clicking on Add Task Button"):
            try:
                add_task_button = wait.until(EC.element_to_be_clickable((By.XPATH, add_task_btn)))
                highlight_element(driver, add_task_button)
                add_task_button.click()
            
            except TimeoutException:
                add_comment_task_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "(//button[@aria-label='Add' and not(ancestor::div[@hidden])])[last()]")))
                highlight_element(driver, add_comment_task_btn)
                add_comment_task_btn.click()


    # ✅ Step 3: Set Task Name
    with allure.step(f"Entering Task Name: '{task_name}'"):
        print()
        task_name_success = set_task_name(driver, task_name_input, task_name, wait)
        if task_name_success == 'blank':
            msg = "Task name input is blank."
            allure.attach(msg, name="Task Name Status", attachment_type=allure.attachment_type.TEXT)
            print(msg)
            show_toast(driver, msg)
            time.sleep(2)
            return False
        
        elif task_name_success:
            msg = "✅ Task name set successfully"
            allure.attach(msg, name="Task Name Status", attachment_type=allure.attachment_type.TEXT)
            print(msg)
            # return True
        
        else:
            msg = "❌ Failed to set task name."
            print(msg)
            allure.attach(msg, name="Task Name Status", attachment_type=allure.attachment_type.TEXT)
            show_toast(driver, msg)
            time.sleep(2)
            return False

    # ✅ Step 4: Set Start Date
    with allure.step(f"Selecting Start Date: '{start_date}'"):
        print()
        print(f"Setting start date to: {start_date}")
        start_date_success = set_start_date(driver, start_date_input, start_date, wait)
        if start_date_success == 'blank':
            msg = "Start date input is blank."
            print(msg)
            allure.attach(msg, name="Start Date Status", attachment_type=allure.attachment_type.TEXT)
            show_toast(driver, msg)
            time.sleep(2)
            return False
        
        elif start_date_success:
            allure.attach("Start date set successfully", name="Start Date Status", attachment_type=allure.attachment_type.TEXT)
            print("✅ Start date set successfully.")
            # return True
        
        else:
            msg = "❌ Failed to set start date."
            print(msg)
            allure.attach(msg, name="Start Date Status", attachment_type=allure.attachment_type.TEXT)
            show_toast(driver, msg)
            time.sleep(2)
            return False

    # ✅ Step 5: Set Due Date
    with allure.step(f"Selecting Due Date: '{due_date}'"):
        print()
        print(f"Setting due date to: {due_date}")
        due_date_success = set_due_date(driver, due_date_input, start_date_input, due_date, task_input_error_msg, wait)
        if due_date_success == 'blank':
            msg = "Due date input is blank."
            print(msg)
            allure.attach(msg, name="Due Date Status", attachment_type=allure.attachment_type.TEXT)
            show_toast(driver, msg)
            time.sleep(2)
            # return False
        
        elif due_date_success:
            allure.attach("Due date set successfully", name="Due Date Status", attachment_type=allure.attachment_type.TEXT)
            print("✅ Due date set successfully.")
            # return True
        
        else:
            msg = "❌ Failed to set due date."
            print(msg)
            allure.attach(msg, name="Due Date Status", attachment_type=allure.attachment_type.TEXT)
            show_toast(driver, msg)
            time.sleep(2)
            return False
    
    # ✅ Step 6: Set Frequency
    with allure.step(f"Selecting Frequency: '{frequency}'"):
        print()
        print(f"Setting frequency to: {frequency}")
        frequency_success = set_frequency(driver, frequency_option, frequency, repeat_if_due_date_is_on_holiday, end_frequency_date, weekday_name, repeat_day_and_month, frequency_value_check, wait)
        if frequency_success == 'blank':
            msg = "Frequency input is blank."
            print(msg)
            allure.attach(msg, name="Frequency Status", attachment_type=allure.attachment_type.TEXT)
            show_toast(driver, msg)
            time.sleep(2)
            return False
        
        elif frequency_success:
            allure.attach("Frequency set successfully", name="Frequency Status", attachment_type=allure.attachment_type.TEXT)
            print("✅ Frequency set successfully.")
            # return True
        
        else:
            msg = "❌ Failed to set frequency."
            print(msg)
            allure.attach(msg, name="Frequency Status", attachment_type=allure.attachment_type.TEXT)
            show_toast(driver, msg)
            time.sleep(2)
            return False

    if task_type == 'mandatory':
        with allure.step(f"Selecting Task Category: '{task_category}'"):
            print()
            print(f"Setting task category: {task_category}")
            allure.attach(f"Setting task category: {task_category}", name="Task Category", attachment_type = allure.attachment_type.TEXT)
            task_category_success = set_task_category(driver, task_category_dropdown, task_category, wait)
            if task_category_success == 'blank':
                msg = "Task category input is blank."
                print(msg)
                allure.attach(msg, name="Category Status", attachment_type=allure.attachment_type.TEXT)
                show_toast(driver, msg)
                time.sleep(2)
                # return False
            
            if task_category_success:
                allure.attach("Task category set successfully", name="Task Category Status", attachment_type=allure.attachment_type.TEXT)
                print("✅ Task category set successfully.")
                # return True
            else:
                msg = "❌ Failed to set task category."
                print(msg)
                allure.attach(msg, name="Category Status", attachment_type=allure.attachment_type.TEXT)
                show_toast(driver, msg)
                time.sleep(2)
                return False
    
    if task_type == 'mandatory':
        with allure.step(f"Selecting Assign To: '{assign_to}'"):
            print()
            print(f"Setting assign to: {assign_to}")
            allure.attach(f"Setting assign to: {assign_to}", name="Assign To", attachment_type=allure.attachment_type.TEXT)
            assign_to_success = set_assign_to(driver, assign_to_dropdown, assign_to, wait)
            if assign_to_success == 'blank':
                msg = "Assign to input is blank."
                print(msg)
                allure.attach(msg, name="Assign To Status", attachment_type=allure.attachment_type.TEXT)
                show_toast(driver, msg)
                time.sleep(2)
                # return False
            
            elif assign_to_success:
                allure.attach("Assign to set successfully", name="Assign To Status", attachment_type=allure.attachment_type.TEXT)
                print("✅ Assign to set successfully.")
                # return True
            
            else:
                msg = "❌ Failed to set assign to."
                print(msg)
                allure.attach(msg, name="Assign To Status", attachment_type=allure.attachment_type.TEXT)
                show_toast(driver, msg)
                time.sleep(2)
                return False
    if task_type == 'mandatory':  
        # ✅ Step 10: Set Approver
        with allure.step(f"Selecting Approver: '{approver}'"):
            print()
            print(f"Setting approver: {approver}")
            allure.attach(f"Setting approver: {approver}", name="Approver", attachment_type=allure.attachment_type.TEXT)
            approver_success = set_approver(driver, approver_dropdown, approver, wait, module)
            if approver_success == 'blank':
                msg = "Approver input is blank."
                print(msg)
                allure.attach(msg, name="Approver Status", attachment_type=allure.attachment_type.TEXT)
                show_toast(driver, msg)
                time.sleep(2)
                # return False
            
            elif approver_success:
                allure.attach("Approver set successfully", name="Approver Status", attachment_type=allure.attachment_type.TEXT)
                print("✅ Approver set successfully.")
                # return True
            
            else:
                msg = "❌ Failed to set approver."
                print(msg)
                allure.attach(msg, name="Approver Status", attachment_type=allure.attachment_type.TEXT)
                show_toast(driver, msg)
                time.sleep(2)
                return False  
    
    # ✅ Step 7: Set End Time
    if task_type == 'mandatory':
        print(f'Only mandatory fields added')
        with allure.step(f"Click Submit button: '{submit_button}'"):
            print()
            print(f"Submitting Task:")
            submit_task_success = submit_task(driver, submit_button, toast_msg, wait)
            wait_for_loader_to_disappear(driver, wait)
            time.sleep(3)
            if submit_task_success:
                allure.attach("Task submitted successfully", name="Submit Task Status", attachment_type=allure.attachment_type.TEXT)
                print("✅ Task submitted successfully.")
                time.sleep(3)
                return True
            else:
                msg = "❌ Failed to submit Task."
                print(msg)
                allure.attach(msg, name="Submit Task Status", attachment_type=allure.attachment_type.TEXT)
                show_toast(driver, msg)
                time.sleep(2)
                return False
    else:
        # ✅ Step 7: Set End Time
        with allure.step(f"Selecting End Time: '{end_time}'"):
            print()
            print(f"Setting end time: {end_time}")
            end_time_success = set_end_time(driver, end_time_input, end_time, wait)
            if end_time_success == 'blank':
                msg = "End time input is blank."
                print(msg)
                allure.attach(msg, name="End Time Status", attachment_type=allure.attachment_type.TEXT)
                show_toast(driver, msg)
                time.sleep(2)
                return False
            
            elif end_time_success:
                allure.attach("✅ End time set successfully", name="End Time Status", attachment_type=allure.attachment_type.TEXT)
                print("✅ End time set successfully.")
                # return True
            
            else:
                msg = "❌ Failed to set end time."
                print(msg)
                allure.attach(msg, name="End Time Status", attachment_type=allure.attachment_type.TEXT)
                show_toast(driver, msg)
                time.sleep(2)
                return False
        
        # ✅ Step 8: Set Internal Deadline
        with allure.step(f"Selecting Internal Deadline: '{internal_deadline}'"):
            print()
            print(f"Setting internal deadline: {internal_deadline}")
            internal_deadline_success = set_deadline_input(driver, start_date_input, due_date_input, deadline_input, internal_deadline, wait)
            if internal_deadline_success == 'blank':
                msg = "Internal deadline input is blank."
                print("Internal deadline input is blank.") 
                allure.attach(msg, name="Internal Deadline Status", attachment_type=allure.attachment_type.TEXT)
                show_toast(driver, msg)
                time.sleep(2)
                # return True
            
            elif internal_deadline_success:
                print("✅ Internal deadline set successfully.")
                allure.attach("✅ Internal deadline set successfully", name="Internal Deadline Status", attachment_type=allure.attachment_type.TEXT)
                # return True
            
            else:
                msg = "❌ Failed to set internal deadline."
                print(msg)
                allure.attach(msg, name="Internal Deadline Status", attachment_type=allure.attachment_type.TEXT)
                show_toast(driver, msg)
                time.sleep(2)
                return False
        
        # ✅ Step 11: Set CC
        with allure.step(f"Selecting CC: '{cc}'"):
            print()
            print(f"Setting CC: {cc}")
            allure.attach(f"Setting CC: {cc}", name="CC", attachment_type=allure.attachment_type.TEXT)
            cc_success = set_cc(driver, cc_dropdown, cc, wait)
            if cc_success == 'blank':
                msg = "CC input is blank."
                print(msg)
                allure.attach(msg, name="CC Status", attachment_type=allure.attachment_type.TEXT)
                show_toast(driver, msg)
                time.sleep(2)
                # return False
            
            elif cc_success:
                allure.attach("CC set successfully", name="CC Status", attachment_type=allure.attachment_type.TEXT)
                print("✅ CC set successfully.")
                # return True 
            
            else:
                msg = "❌ Failed to set CC."
                print(msg)
                allure.attach(msg, name="CC Status", attachment_type=allure.attachment_type.TEXT)
                show_toast(driver, msg)
                time.sleep(2)
                return False

        # ✅ Step 9: Set Assign To
        with allure.step(f"Selecting Assign To: '{assign_to}'"):
            print()
            print(f"Setting assign to: {assign_to}")
            allure.attach(f"Setting assign to: {assign_to}", name="Assign To", attachment_type=allure.attachment_type.TEXT)
            assign_to_success = set_assign_to(driver, assign_to_dropdown, assign_to, wait)
            if assign_to_success == 'blank':
                msg = "Assign to input is blank."
                print(msg)
                allure.attach(msg, name="Assign To Status", attachment_type=allure.attachment_type.TEXT)
                show_toast(driver, msg)
                time.sleep(2)
                # return False
            
            elif assign_to_success:
                allure.attach("Assign to set successfully", name="Assign To Status", attachment_type=allure.attachment_type.TEXT)
                print("✅ Assign to set successfully.")
                # return True
            
            else:
                msg = "❌ Failed to set assign to."
                print(msg)
                allure.attach(msg, name="Assign To Status", attachment_type=allure.attachment_type.TEXT)
                show_toast(driver, msg)
                time.sleep(2)
                return False
            
        # ✅ Step 10: Set Approver
        with allure.step(f"Selecting Approver: '{approver}'"):
            print()
            print(f"Setting approver: {approver}")
            allure.attach(f"Setting approver: {approver}", name="Approver", attachment_type=allure.attachment_type.TEXT)
            approver_success = set_approver(driver, approver_dropdown, approver, wait, module)
            if approver_success == 'blank':
                msg = "Approver input is blank."
                print(msg)
                allure.attach(msg, name="Approver Status", attachment_type=allure.attachment_type.TEXT)
                show_toast(driver, msg)
                time.sleep(2)
                # return False
            
            elif approver_success:
                allure.attach("Approver set successfully", name="Approver Status", attachment_type=allure.attachment_type.TEXT)
                print("✅ Approver set successfully.")
                # return True
            
            else:
                msg = "❌ Failed to set approver."
                print(msg)
                allure.attach(msg, name="Approver Status", attachment_type=allure.attachment_type.TEXT)
                show_toast(driver, msg)
                time.sleep(2)
                return False    
            
        
        
        # ✅ Step 12: Set Priority
        with allure.step(f"Selecting Priority: '{risk}'"):
            print()
            print(f"Setting priority: {risk}")
            allure.attach(f"Setting priority: {risk}", name="Priority", attachment_type=allure.attachment_type.TEXT)
            priority_success = set_risk_rating(driver, risk_rating_dropdown, risk, wait)
            if priority_success == 'blank':
                msg = "Risk rating input is blank."
                print(msg)
                allure.attach(msg, name="Priority Status", attachment_type=allure.attachment_type.TEXT)
                show_toast(driver, msg)
                time.sleep(2)
                return False
            
            if priority_success:
                print("✅ Priority set successfully.")
                allure.attach("Priority set successfully", name="Priority Status", attachment_type=allure.attachment_type.TEXT)
                # return True
            
            else:
                msg = "❌ Failed to set priority."
                print(msg)
                allure.attach(msg, name="Priority Status", attachment_type=allure.attachment_type.TEXT)
                show_toast(driver, msg)
                time.sleep(2)
                return False
        
        # ✅ Step 13: Set License
        with allure.step(f"Entering License Name: '{license_name}'"):
            print()
            print(f"Setting license: {license_name}")
            allure.attach(f"Setting license: {license_name}", name="License", attachment_type=allure.attachment_type.TEXT)
            license_success = set_license(driver, license_input, license_name, wait)
            if license_success == 'blank':
                msg = "License input is blank."
                print(msg)
                allure.attach(msg, name="License Status", attachment_type=allure.attachment_type.TEXT)
                show_toast(driver, msg)
                time.sleep(2)
                # return False
            
            elif license_success:
                allure.attach("License set successfully", name="License Status", attachment_type=allure.attachment_type.TEXT)
                print("✅ License set successfully.")
                # return True
            else:
                msg = "❌ Failed to set license."
                print(msg)
                allure.attach(msg, name="License Status", attachment_type=allure.attachment_type.TEXT)
                show_toast(driver, msg)
                time.sleep(2)
                return False
        
        # ✅ Step 14: Set Task Category
        with allure.step(f"Selecting Task Category: '{task_category}'"):
            print()
            print(f"Setting task category: {task_category}")
            allure.attach(f"Setting task category: {task_category}", name="Task Category", attachment_type = allure.attachment_type.TEXT)
            task_category_success = set_task_category(driver, task_category_dropdown, task_category, wait)
            if task_category_success == 'blank':
                msg = "Task category input is blank."
                print(msg)
                allure.attach(msg, name="Category Status", attachment_type=allure.attachment_type.TEXT)
                show_toast(driver, msg)
                time.sleep(2)
                # return False
            
            if task_category_success:
                allure.attach("Task category set successfully", name="Task Category Status", attachment_type=allure.attachment_type.TEXT)
                print("✅ Task category set successfully.")
                # return True
            else:
                msg = "❌ Failed to set task category."
                print(msg)
                allure.attach(msg, name="Category Status", attachment_type=allure.attachment_type.TEXT)
                show_toast(driver, msg)
                time.sleep(2)
                return False
        
        # ✅ Step 15: Add description
        with allure.step(f"Adding description: '{description}'"):
            print()
            print(f"Adding description: {description}")
            allure.attach(f"Adding description: {description}", name="Description", attachment_type=allure.attachment_type.TEXT)
            description_success = add_description(driver, description_btn, description_input, str(description), desc_save_btn, desc_view, wait)
            if description_success == 'blank':
                msg = "Description input is blank."
                print(msg)
                allure.attach(msg, name="Description Status", attachment_type=allure.attachment_type.TEXT)
                show_toast(driver, msg)
                time.sleep(2)
                # return False

            if description_success:
                print("✅ Description added successfully.")
                allure.attach("Description added successfully", name="Description Status", attachment_type=allure.attachment_type.TEXT)
                # return True
            
            else:
                msg = "❌ Failed to add description."
                print(msg)
                allure.attach(msg, name="Description Status", attachment_type=allure.attachment_type.TEXT)
                show_toast(driver, msg)
                time.sleep(2)
                return False
        
        # ✅ Step 16: Add attachments
        with allure.step(f"Adding attachments: '{attach_file_name}'"):
            print()
            print(f"Adding attachments: {attach_file_name}")
            allure.attach(f"Attaching file: {attach_file_name}", name="Attachments", attachment_type=allure.attachment_type.TEXT)
            attachment_success = attach_file(driver, attach_file_btn, attach_file_input, attach_file_name, attach_file_save_btn, attach_file_view, wait)
            if attachment_success == 'blank':
                msg = "Attachment input is blank."
                print(msg)
                allure.attach(msg, name="File Attach Status", attachment_type=allure.attachment_type.TEXT)
                show_toast(driver, msg)
                time.sleep(2)
                # return False
            
            if attachment_success:
                allure.attach("Attachments added successfully", name="Attachments Status", attachment_type=allure.attachment_type.TEXT)
                print("✅ Attachments added successfully.")
                # return True
            else:
                msg = "❌ Failed to add attachments."
                print(msg)
                allure.attach(msg, name="Attachments Status", attachment_type=allure.attachment_type.TEXT)
                show_toast(driver, msg)
                time.sleep(2)
                return False
        
        # ✅ Step 17: Add Impact Details and File
        # with allure.step(f"Adding Impact Details and File: '{impact_file_name}'"):
        #     print()
        #     print(f"Adding Impact Details and File: {impact_file_name}")
        #     impact_details_success = add_impact_details(driver, impact_button, fine_amount_editor, str(impact_details), str(impact_file_name), attach_file_input, impact_file_save_btn, impact_fine_amount_view, impact_file_view, wait)
        #     if impact_details_success:
        #         print("✅ Impact Details and File added successfully.")
        #         allure.attach("Impact Details and File added successfully", name="Impact Status", attachment_type=allure.attachment_type.TEXT)
        #         # return False
        #     else:
        #         msg = "❌ Failed to add Impact Details and File."
        #         print(msg)
        #         allure.attach(msg, name="Impact Status", attachment_type=allure.attachment_type.TEXT)
        #         show_toast(driver, msg)
        #         time.sleep(2)
        #         return False
        # ✅ Step 17: Add Impact Details and File
        with allure.step(f"Adding Impact Details and File: '{impact_file_name}'"):
            print()
            print(f"Adding Impact Details and File: {impact_file_name}")
            impact_details_success = add_impact_details(driver, impact_button, fine_amount_editor, impact_details, impact_file_name, attach_file_input, impact_file_save_btn, impact_fine_amount_view, impact_file_view, wait)
            if impact_details_success:
                print("✅ Impact Details and File added successfully.")
                # allure.attach("Impact Details and File added successfully", name="Impact Status", attachment_type=allure.attachment_type.TEXT)
                # return True
            else:
                msg = "❌ Failed to add Impact Details and File."
                print(msg)
                allure.attach(msg, name="Impact Status", attachment_type=allure.attachment_type.TEXT)
                show_toast(driver, msg)
                time.sleep(2)
                return False
        
        # ✅ Step 18: Adding Circulars
        with allure.step(f"Adding Circulars: '{circular_search}'"):
            print()
            print(f"Adding Circulars:")
            if circular_search and (circular_search.strip() != ''):
                circular_search_success = search_and_add_circulars(driver, regulatory_btn, regulatory_checkboxes, circular_search, regulatory_save_btn, regulatory_cancel_btn, regulatory_search_btn, wait)
                if circular_search_success:
                    print("✅ Circulars added successfully.")
                    allure.attach("Circulars added successfully", name="Circulars Search Status", attachment_type=allure.attachment_type.TEXT)
                    # return False
                else:
                    msg = "❌ Failed to search and add Circulars."
                    print(msg)
                    allure.attach(msg, name="Circulars Search Status", attachment_type=allure.attachment_type.TEXT)
                    show_toast(driver, msg)
                    time.sleep(2)
                    # return False
            
            else:
                circulars_success = add_circulars(driver, regulatory_btn, regulatory_checkboxes, regulatory_save_btn, 3, wait)
                if circulars_success:
                    print("✅ Circulars added successfully.")
                    allure.attach("Circulars added successfully", name="Circulars Search Status", attachment_type=allure.attachment_type.TEXT)
                    # return False
                else:
                    msg = "❌ Failed to add Circulars."
                    print(msg)
                    allure.attach(msg, name="Circulars Search Status", attachment_type=allure.attachment_type.TEXT)
                    show_toast(driver, msg)
                    time.sleep(2)
                    return False

        # ✅ Step 19: Submitting Task
        with allure.step(f"Click Submit button: '{submit_button}'"):
            print()
            print(f"Submitting Task:")
            submit_task_success = submit_task(driver, submit_button, toast_msg, wait)
            wait_for_loader_to_disappear(driver, wait)
            time.sleep(3)
            if submit_task_success:
                allure.attach("Task submitted successfully", name="Submit Task Status", attachment_type=allure.attachment_type.TEXT)
                print("✅ Task submitted successfully.")
                time.sleep(3)
                # return False
            else:
                msg = "❌ Failed to submit Task."
                print(msg)
                allure.attach(msg, name="Submit Task Status", attachment_type=allure.attachment_type.TEXT)
                show_toast(driver, msg)
                time.sleep(2)
                return False
        
        with allure.step(f"Click Open Task"):
            print()
            print(f"Opening Task:")
            open_task_success = open_task(driver, wait, task_name)
            time.sleep(3)
            if open_task_success:
                allure.attach("Task Opened successfully", name="Open Task Status", attachment_type=allure.attachment_type.TEXT)
                print("✅ Task Opened successfully.")
                time.sleep(3)
                # return False
            else:
                msg = "❌ Failed to Open Task."
                print(msg)
                allure.attach(msg, name="Open Task Status", attachment_type=allure.attachment_type.TEXT)
                show_toast(driver, msg)
                time.sleep(2)
                return False

            
        # ✅ Step 20: Validation After Submitting Task
        with allure.step("Validate Task Details After Submission"):
            print()
            print(f"Validate Task Details After Submission:")
            validation_success = special_task_validation(driver, wait)
            if validation_success:
                allure.attach("Validate Task Details After Submission successful", name="Validation Status", attachment_type=allure.attachment_type.TEXT)
                print("✅ Validate Task Details After Submission successful.")
                time.sleep(1)
                # return True
            else:
                msg = "❌ Failed to validate after submitting task."
                print(msg)
                allure.attach(msg, name="Validation Status", attachment_type=allure.attachment_type.TEXT)
                show_toast(driver, msg)
                time.sleep(2)
                return False
        
        

        with allure.step("Verify created task is displayed in the task list using the search functionality"):
            print(f"Verify created task is displayed in the task list using the search functionality")
            created_task_name = task_value_get("task_name")
            search_task_success = validate_search_task(driver, wait, created_task_name)
            if search_task_success:
                print("✅ Verify created task is displayed in the task list using the search functionality successfull")
                return True
            else:
                msg = "❌ Failed to Verify created task is displayed in the task list using the search functionality successfull"
                print(msg)
                allure.attach(msg, name="Validation Status", attachment_type=allure.attachment_type.TEXT)
                show_toast(driver, msg)
                time.sleep(2)
                return False 
                        


def get_test_case_list(module=None):
    try:
        # with open(os.path.join("data", "test_data.json")) as f:
        #     config = json.load(f)
        config = load_test_config_excel_data()
        print(f'Configurations: {config}')
        if not config:
            pytest.fail("test_case_selector.xlsx file not found")
        
       
        test_details = config.get("module_to_test", {})
        print(f'Module fetched: {test_details}')
        selected_test_types = test_details.get(module, [])
        print(f'Selected test types: {selected_test_types}')

        # 🔹 Load test cases sheet (NO execution columns here)
        test_case_details = pd.read_excel(
            os.path.join("data", "test_case_selector.xlsx"),
            sheet_name=f"{module}_test_cases"
        ).fillna("")

        test_case_list = []
        for _, row in test_case_details.iterrows():
            end_time_val = row.get("end_time")
            end_time = format_time_if_valid(end_time_val) if pd.notna(end_time_val) else None
            # ----------------------------
            # 1. Testcase execution check
            # ----------------------------
            test_case_execution = str(row.get("test_case_execution", "n")).strip().lower()

            if test_case_execution != "y":
                print(f"Skipping {row.get('test_case_id')} -> test_case_execution = n")
                continue
            row_test_type = str(row.get("test_type", "")).strip().lower()

            if row_test_type not in selected_test_types:
                continue  # skip

            marks = []

            # Add the positive/negative mark based on test_type
            if row_test_type in ["positive", "negative"]:
                marks.append(getattr(pytest.mark, row_test_type))
            test_case_list.append(
                pytest.param(
                    row['test_case_id'],
                    row['task_name'],
                    row['test_case_description'],
                    format_date_if_valid(row['start_date']),
                    format_date_if_valid(row['due_date']),
                    row['frequency'],
                    row['repeat_if_due_date_is_on_holiday[For Daily: Yes/No][For Others: Before/After/Yes]'],
                    row['end_frequency_date(YYYY-MM-DD)'],
                    row['repeat_on_every(weekdays_name)'],
                    row['repeat_on_every(DD/MM)[Except For: Daily and Weekly]'],
                    end_time,
                    row['internal_deadline'],
                    row['assign_to'],
                    row['approver'],
                    row['cc'],
                    row['risk_rating'],
                    row['license_name'],
                    row['task_category'],
                    row['description'],
                    row['attach_file_name'],
                    row['impact_details'],
                    row['impact_file_name'],
                    row['circular_search'],
                    row['test_type'],
                    row['test_case_execution'],
                    marks=marks
                )
            )
        if not test_case_list:
            pytest.skip("No test cases matched the selected criteria", allow_module_level=True)
        return test_case_list
    
    except FileNotFoundError:
        pytest.fail("test_case_selector.xlsx file not found")
    except Exception as e:
        pytest.fail(f"Error reading test cases: {str(e)}")
