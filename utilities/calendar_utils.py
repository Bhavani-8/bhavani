import allure
import pandas as pd
import os
import json
import pytest
import allure
import time

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from utilities.other_utils_functions.highlight import highlight_element
from utilities.login_utils import login_check
from utilities.add_task_functions.wait_for_loader_to_disappear import wait_for_loader_to_disappear
from selenium.webdriver.support.ui import WebDriverWait
from load_test_config_excel_data import load_test_config_excel_data
from utilities.project_functions.add_project import create_project
from utilities.calendar_functions.check_day_week_month_buttons import check_day_week_month_buttons
from utilities.calendar_functions.calendar_task_validation import validate_today_task

def calendar_check(driver, module_name=None, test_case_id=None, test_type=None, task_details=None):
    wait = WebDriverWait(driver, 30)

    driver.get("https://preprodreact.compliancesutra.com/login")
    # #  ✅ Step 1: Login Check
    with allure.step("Login with valid credentials"):
        print("🔐 Logging in with valid credentials...")
        credentials_df = pd.read_excel(os.path.join('data', 'test_case_selector.xlsx'), sheet_name='credentials').fillna("")
        user = str(credentials_df['username'].iloc[0]).strip()
        pwd = str(credentials_df['password'].iloc[0]).strip()
        login_check_success = login_check(driver, waittime=10, trial=1, username=user, password=pwd, user_validation=False)

        if login_check_success:
            allure.attach("Login successful", name="Login Status", attachment_type=allure.attachment_type.TEXT)
        else:
            # allure.attach("Login failed", name="Login Timeout", attachment_type=allure.attachment_type.TEXT)
            allure.attach(str(e), name="Delete Task and Restore", attachment_type=allure.attachment_type.TEXT)

    wait_for_loader_to_disappear(driver, wait)
   

    if module_name == 'check_day_week_month':

        with allure.step("Check Day, Week, Month Buttons"):
            try:
                if check_day_week_month_buttons(driver, wait):
                    print("✅ Check Day, Week, Month successful")
                    return True
                else:
                    allure.attach("Test case failed for Check Day, Week, Month",name="Check Day, Week, Month Validation Failed",attachment_type=allure.attachment_type.TEXT)
                    return False
            except Exception as e:
                 allure.attach(str(e), name="Check Day, Week, Month", attachment_type=allure.attachment_type.TEXT)
    
    if module_name == 'validate_today_task':
        calendar_task_name = task_details.get("calendar_task_name")
        with allure.step("Validate Today Task In Calendar"):
            try:
                if validate_today_task(driver, wait, calendar_task_name):
                    print("✅Validate Today Task In Calendar successful")
                    return True
                else:
                    allure.attach("Test case failed for Validate Today Task In Calendar",name="Validate Today Task In Calendar Failed",attachment_type=allure.attachment_type.TEXT)
                    return False
            except Exception as e:
                 allure.attach(str(e), name="Validate Today Task In Calendar", attachment_type=allure.attachment_type.TEXT)
   
    else:
        msg = f"❌ Unknown module name: {module_name}"
        allure.attach(msg,name="Unknown Module Error",attachment_type=allure.attachment_type.TEXT)
        raise Exception(msg)


def get_test_case_list(module=None):
    try:
        # 🔹 Load selector config
        config = load_test_config_excel_data()
        print(f'Configurations: {config}')
        if not config:
            pytest.fail("test_case_selector.xlsx file not found")

        test_details = config.get("module_to_test", {})
        print(f'Module fetched: {test_details}')
        selected_test_types = test_details.get(module, [])
        print(f'Selected test types: {selected_test_types}')

        # 🔹 Load test cases sheet
        test_case_details = pd.read_excel(
            os.path.join("data", "test_case_selector.xlsx"),
            sheet_name=f"{module}_test_cases"
        ).fillna("")

        test_case_list = []

        for _, row in test_case_details.iterrows():
            row_test_type = str(row.get("test_type", "")).strip().lower()

            if row_test_type not in selected_test_types:
                continue  # skip if not selected

    
            marks = []

            if row_test_type in ["positive", "negative"]:
                marks.append(getattr(pytest.mark, row_test_type))
                # 🔥 Convert task_details JSON string → dictionary
            task_details_raw = row.get("task_details", "")
            task_details = {}

            if task_details_raw:
                try:
                    task_details = json.loads(task_details_raw)
                except Exception as e:
                    print(f"❌ JSON error in task_details for {row.get('test_case_id')}: {e}")


            test_case_list.append(
                    pytest.param(
                        row.get('test_case_id'),
                        row.get('module_name'),
                        row.get('test_case_description'),
                        row_test_type,
                        task_details,   # ✅ send dictionary
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
