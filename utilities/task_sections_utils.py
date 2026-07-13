# task_sections_utils.py

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import pandas as pd
import pytest
import allure
import json
import time
import os

from utilities.other_utils_functions.highlight import highlight_element
from utilities.login_utils import login_check
from utilities.add_task_utils import wait_for_loader_to_disappear
from utilities.other_utils_functions.license_utils import validate_license_subscription
from utilities.task_functions.comment_tab import comment_check
from utilities.task_functions.file_tab import file_check
from utilities.task_functions.note_tab import note_check
from utilities.task_functions.update_tab import update_check
from utilities.task_functions.log_tab import log_check
from load_test_config_excel_data import load_test_config_excel_data


def task_sections_check(driver, dash_type='QCC', module_name=None, test_case_id=None):
    wait = WebDriverWait(driver, 30)

    # LOGIN
    with allure.step("Login with valid credentials"):
        try:
            credentials_df = pd.read_excel(
                os.path.join('data', 'test_case_selector.xlsx'),
                sheet_name='credentials'
            ).fillna("")

            user = str(credentials_df['username'].iloc[0]).strip()
            pwd = str(credentials_df['password'].iloc[0]).strip()

            login_success = login_check(driver, waittime=10, trial=1,
                                        username=user, password=pwd,
                                        user_validation=False)

            if not login_success:
                raise Exception("❌ Login failed")

            print("✅ Login successful")

        except Exception as e:
            allure.attach(str(e), name="Login Error", attachment_type=allure.attachment_type.TEXT)
            return False

    wait_for_loader_to_disappear(driver, wait)

   
    with allure.step("Load locators.json"):
        try:
            with open(os.path.join("data", 'locators.json'), 'r') as f:
                elements_details = json.load(f)

            dashboard_icon = elements_details['dashboard_icon']
            special_task_icon = elements_details['special_task_icon']

            # print("✅ locators.json loaded successfully")

        except Exception as e:
            allure.attach(str(e), name="Locators Error", attachment_type=allure.attachment_type.TEXT)
            return False

    # OPEN DASHBOARD
    with allure.step("Open Dashboard"):
        try:
            if dash_type == 'special':
                print("🔍 Opening SPECIAL TASK dashboard...")
                special_task_icon_elem = wait.until(EC.presence_of_element_located((By.XPATH, special_task_icon)))
                highlight_element(driver, special_task_icon_elem)
                special_task_icon_elem.click()
                print("✅ Special Task Dashboard icon clicked")
            else:
                print("🔍 Opening QCC dashboard...")
                dashboard_icon_elem = wait.until(EC.presence_of_element_located((By.XPATH, dashboard_icon)))
                highlight_element(driver, dashboard_icon_elem)
                dashboard_icon_elem.click()
                print("✅ QCC Dashboard icon clicked")

        except Exception as e:
            allure.attach(str(e), name="Dashboard Open Error", attachment_type=allure.attachment_type.TEXT)
            return False

    if module_name == 'comment_check':
    # # ✅ Step 4: Comment Section
        with allure.step("Comment Section Validation"):
            try:
                if comment_check(driver, wait):
                    print("✅ Comment Section validation successful")
                else:
                    raise Exception("❌ Comment Section validation failed")
            except Exception as e:
                allure.attach(str(e), name="Comment Section Error", attachment_type=allure.attachment_type.TEXT)

    #  ✅ Step 4: File Section
    if module_name == 'file_check': 
        with allure.step("File Tab Section Validation"):
            try:
                if file_check(driver, wait, dash_type):
                    print("✅ File Section validation successful")
                else:
                    raise Exception("❌ File Section validation failed")
            except Exception as e:
                allure.attach(str(e), name="File Section Error", attachment_type=allure.attachment_type.TEXT)
    
    if module_name == 'note_check':
        with allure.step("Note Tab Section Validation"):
            try:
                if note_check(driver, wait, dash_type):
                    print("✅ Note Tab Section validation successful")
                else:
                    raise Exception("❌ Note Tab Section validation failed")
            except Exception as e:
                allure.attach(str(e), name="Note Tab Section Error", attachment_type=allure.attachment_type.TEXT)
    if module_name == 'update_check':
        with allure.step("Update Tab Section Validation"):
            try:
                if update_check(driver, wait, dash_type):
                    print("✅ Update Tab Section validation successful")
                else:
                    raise Exception("❌ Update Tab Section validation failed")
            except Exception as e:
                allure.attach(str(e), name="Update Tab Section Error", attachment_type=allure.attachment_type.TEXT)

    if module_name == 'log_check':
        with allure.step("Log Tab Section Validation"):
            try:
                if log_check(driver, wait, dash_type):
                    print("✅ Log Tab Section validation successful")
                else:
                    raise Exception("❌ Log Tab Section validation failed")
            except Exception as e:
                allure.attach(str(e), name="Log Tab Section Error", attachment_type=allure.attachment_type.TEXT)

    
    allure.attach(str(e), name="Delete Task and Restore", attachment_type=allure.attachment_type.TEXT)
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

        # 🔹 Load test cases sheet (NO execution columns here)
        test_case_details = pd.read_excel(
            os.path.join("data", "test_case_selector.xlsx"),
            sheet_name=f"{module}_test_cases"
        ).fillna("")

        test_case_list = []

        for _, row in test_case_details.iterrows():
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
                    row.get("test_case_id"),
                    row.get("module_name"),
                    row.get("test_case_description"),
                    row_test_type,
                    row.get("test_case_execution"),
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
