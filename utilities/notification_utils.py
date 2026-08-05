import time
import json
import os
import allure
import pytest
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utilities.login_utils import login_check
from utilities.other_utils_functions.highlight import highlight_element
from load_test_config_excel_data import load_test_config_excel_data
from utilities.notification_functions.search_task import _search_task_flow
from utilities.notification_functions.notification_filter_flow import execute_filter_and_validate


def step_fail(driver, step_name, error):
    allure.attach(str(error), name=f"{step_name} Error", attachment_type=allure.attachment_type.TEXT)
    allure.attach(driver.get_screenshot_as_png(), name=f"{step_name} Screenshot", attachment_type=allure.attachment_type.PNG)
    pytest.fail(f"❌ {step_name} failed")


def notification_check(driver, module_name=None, test_case_id=None):
    wait = WebDriverWait(driver, 30)

    # driver.get("https://preprodreact.compliancesutra.com/login")
    target_url = None
    
    if "192.168.30.11:8081" in driver.current_url:
        target_url = "http://192.168.30.11:8081/login"
    elif "preprodreact.compliancesutra.com" in driver.current_url:
        target_url = "https://preprodreact.compliancesutra.com/login"
    else:
        # Default login URL
        target_url = "https://preprodreact.compliancesutra.com/login"

    driver.get(target_url)
    with allure.step("Login with valid credentials"):
        try:
            print("🔐 Logging in with valid credentials...")
            credentials_df = pd.read_excel(os.path.join('data', 'test_case_selector.xlsx'), sheet_name='credentials').fillna("")
            
            # 🚨 Grabbing the email directly from the username column
            user_email = str(credentials_df['username'].iloc[0]).strip()
            pwd = str(credentials_df['password'].iloc[0]).strip()
            
            print(f"👤 Logged in as: {user_email}")
            
            login_check_success = login_check(driver, waittime=10, trial=1, username=user_email, password=pwd)
            if not login_check_success:
                raise Exception("❌ Login failed")
        except Exception as e:
            step_fail(driver, "Login failed", e)

    
    try:
        with open(os.path.join("data", 'locators.json'), 'r') as f:
            elements_details = json.load(f)
            locators = elements_details["notification_elements"]
    except Exception as e:
        step_fail(driver, "Locators Load Error", e)

    with allure.step("Open Notifications Icon"):
        try:
            notification_btn = wait.until(EC.presence_of_element_located((By.XPATH, locators["notification_icon"])))
            highlight_element(driver, notification_btn)
            notification_btn.click()
            time.sleep(3)
        except Exception as e:
            msg = f"Failed to open notifications button: {str(e)}"
            print(msg)
            allure.attach(msg, name="Notifications Error", attachment_type=allure.attachment_type.TEXT)
            return False
    

    # module_name = str(module_name).strip().lower()

    
    # module_name = str(module_name).strip().lower()

    
    filter_map = {
        'assigned_task':     {'locator_key': 'drop_down_assignd',   'inner_label': None,  'notification_text': None},
        'tasks_filter':      {'locator_key': 'drop_down_tsks',      'inner_label': None,  'notification_text': None},
        'rejected_filter':   {'locator_key': 'drop_down_rjtd',   'inner_label': None,  'notification_text': None},
        'reassigned_filter': {'locator_key': 'drop_down_rasignd', 'inner_label': None,  'notification_text': None},
        'comment_filter':    {'locator_key': 'drop_down_cmmt',   'inner_label': None,  'notification_text': None},
        'approved_filter':   {'locator_key': 'drop_down_apprvd',  'inner_label': 'Task Approved', 'notification_text': 'Task Approved by'}
    }

    
    if module_name == 'search_task':
        with allure.step("Notification Search Task Validation"):
            try:
                
                return _search_task_flow(driver, wait, locators)
            except Exception as e:
                step_fail(driver, "Search Task Error", e)
          

   
    if module_name in filter_map:
        config = filter_map[module_name]

        with allure.step(f"Notification Validation for: {module_name}"):
            try:
                return execute_filter_and_validate(
                    driver=driver,
                    wait=wait,
                    locators=locators,
                    logged_in_email=user_email,
                    filter_key=config['locator_key'],
                    filter_name=module_name,
                    expected_inner_status=config['inner_label'],
                    notification_text=config['notification_text']
                )
            except Exception as e:
                step_fail(driver, f"{module_name.capitalize()} Error", e)
                return False
                
    else:
        msg = f"❌ Unknown module name: {module_name}"
        allure.attach(msg,name="Unknown Module Error",attachment_type=allure.attachment_type.TEXT)
        raise Exception(msg) 

def get_test_case_list(module=None):
    try:
        config = load_test_config_excel_data()
        if not config:
            pytest.fail("test_case_selector.xlsx file not found")

        test_details = config.get("module_to_test", {})
        
        raw_test_types = test_details.get(module, [])
        if isinstance(raw_test_types, str):
            raw_test_types = [raw_test_types]
        
        
        selected_test_types = [str(x).strip().lower() for x in raw_test_types]

        print(f"🎯 Master Config says run these types for '{module}': {selected_test_types}")

        test_case_details = pd.read_excel(
            os.path.join("data", "test_case_selector.xlsx"),
            sheet_name=f"{module}_test_cases"
        ).fillna("")    

        test_case_list = []

        for _, row in test_case_details.iterrows():
              # ----------------------------
            # 1. Testcase execution check
            # ----------------------------
            test_case_execution = str(row.get("test_case_execution", "n")).strip().lower()

            if test_case_execution != "y":
                print(f"Skipping {row.get('test_case_id')} -> test_case_execution = n")
                continue
            
            row_test_type = str(row.get("test_type", "")).strip().lower()

            if row_test_type not in selected_test_types:
                continue  

            marks = []
            if row_test_type in ["positive", "negative"]:
                marks.append(getattr(pytest.mark, row_test_type))

            test_case_list.append(
                pytest.param(
                    row.get("test_case_id"),
                    row.get("module_name"),
                    row.get("test_case_description"),
                    row_test_type,
                    row.get("test_case_execution"),
                    marks=marks
                )
            )

        if not test_case_list:
            pytest.skip("⏭️ No test cases matched the Master Config criteria", allow_module_level=True)
        return test_case_list

    except FileNotFoundError:
        pytest.fail("❌ test_case_selector.xlsx file not found")
    except Exception as e:
        pytest.fail(f"❌ Error reading test cases: {str(e)}")