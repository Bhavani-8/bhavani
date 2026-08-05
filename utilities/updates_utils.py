from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import pandas as pd
import allure
import os
import json
import pytest

from utilities.add_task_utils import wait_for_loader_to_disappear
from utilities.login_utils import login_check
from utilities.other_utils_functions.highlight import highlight_element
from utilities.highlight import highlight_element
from utilities.updates_functions.send_email import send_circular_to_user
from utilities.updates_functions.add_task_updates import updates_add_task
from utilities.updates_functions.compliance_events import compliance_events
from utilities.updates_functions.issuer_link_downloads import issuer_link_downloads
from utilities.updates_functions.export_circulars import export_circulars
from utilities.updates_functions.check_filters import check_filters
from utilities.updates_functions.mark_actionable import mark_actionable
from load_test_config_excel_data import load_test_config_excel_data


def updates_check(driver, module_name=None, test_case_id=None, task_details=None):
    wait = WebDriverWait(driver, 30)

    try:
        with open(os.path.join("data", 'locators.json'), 'r') as f:
            elements_details = json.load(f)
            dashboard_icon = elements_details['dashboard_icon']
            updates_icon = elements_details['updates_icon']
        print("✅ locators.json loaded successfully")
    except Exception as e:
        allure.attach(str(e), name="Locators Error", attachment_type=allure.attachment_type.TEXT)
        pytest.fail("Failed to load locators.json")
    # ------------------------------------------
    # STEP 1: LOGIN
    # ------------------------------------------
    driver.get("http://192.168.30.11:8081/login")
    with allure.step("Login with valid credentials"):
        try:
            print("🔐 Logging in with valid credentials...")
            credentials_df = pd.read_excel(os.path.join('data', 'test_case_selector.xlsx'), sheet_name='credentials').fillna("")
            user = str(credentials_df['username'].iloc[0]).strip()
            pwd = str(credentials_df['password'].iloc[0]).strip()

            login_check_success = login_check(driver, waittime=10, trial=1, username=user, password=pwd, user_validation=False)
            if login_check_success:
                print("✅ Login successful")
            else:
                raise Exception("❌ Login failed")
        except Exception as e:
            allure.attach(str(e), name="Login Error", attachment_type=allure.attachment_type.TEXT)
            return False

    wait_for_loader_to_disappear(driver, wait)

    # ------------------------------------------
    with allure.step("Open Dashboard"):
        try:
            dashboard_icon_elem = wait.until(EC.element_to_be_clickable((By.XPATH, dashboard_icon)))
            # highlight_element(driver, dashboard_icon_elem)
            dashboard_icon_elem.click()
            print("✅ Dashboard icon clicked")
        except Exception as e:
            allure.attach(str(e), name="Dashboard Open Error", attachment_type=allure.attachment_type.TEXT)
            return False
    with allure.step("Open Updates Section"):
        try:
            updates_btn = wait.until(EC.element_to_be_clickable((By.XPATH, updates_icon)))
            highlight_element(driver, updates_btn)
            updates_btn.click()
            print("✅ Updates icon clicked")
        except Exception as e:
            allure.attach(str(e), name="Updates Section Error", attachment_type=allure.attachment_type.TEXT)
            return False
    
    if module_name == 'send_circular_to_user':
        user_name = task_details.get("user_name")
        with allure.step("Send Circular to User Validation"):
            try:
                if send_circular_to_user(driver, wait, user_name):
                    print("✅ Send Circular to User successful")
                    return True
                else:
                    raise Exception("❌ Send Circular to User failed")
            except Exception as e:
                allure.attach(str(e), name="Send Circular to User Error", attachment_type=allure.attachment_type.TEXT)

    # ✅ Step 11: Column Chooser Validation
    if module_name == 'updates_add_task':
        updates_task_name = task_details.get("updates_task_name")
        with allure.step("Updates Add Task Validation"):
            try:
                if updates_add_task(driver, wait, updates_task_name):
                    print("✅ Updates Add Task validation successful")
                    return True
                else:
                    allure.attach("Test case failed for Updates Add Task", name="Updates Add Task Failed", attachment_type=allure.attachment_type.TEXT)
                    return False
            except Exception as e:
                allure.attach(str(e), name="Updates Add Task Error", attachment_type=allure.attachment_type.TEXT)
    module_name = module_name.strip().lower()
    if module_name == 'updates_compliance_events':
        with allure.step("Updates Compliance Events Validation"):
            try:
                if compliance_events(driver, wait):
                    print("✅ Compliance Events validation successful")
                    return True
                else:
                    raise Exception("❌ Compliance Events validation failed")
            except Exception as e:
                allure.attach(str(e), name="Compliance Events Error", attachment_type=allure.attachment_type.TEXT)
    if module_name == 'issuer_link_downloads':
        with allure.step("Issuer Link and Download files Validation"):
            try:
                if issuer_link_downloads(driver, wait):
                    print("✅ Issuer Link Downloads validation successful")
                    return True
                else:
                    raise Exception("❌ Issuer Link Downloads validation failed")
            except Exception as e:
                allure.attach(str(e), name="Issuer Link Downloads Error", attachment_type=allure.attachment_type.TEXT)
    
    
    if module_name == 'export_circulars':
        with allure.step("Export Circulars Validation"):
            try:
                if export_circulars(driver, wait):
                    print("✅ Export Circulars validation successful")
                    return True
                else:
                    raise Exception("❌ Export Circulars validation failed")
            except Exception as e:
                allure.attach(str(e), name="Export Circulars Error", attachment_type=allure.attachment_type.TEXT)
    
    if module_name == 'check_filters':
        with allure.step("Check Filters Validation"):
            try:
                if check_filters(driver, wait):
                    print("✅ Check Filters validation successful")
                    return True
                else:
                    raise Exception("❌ Check Filters validation failed")
            except Exception as e:
                allure.attach(str(e), name="Check Filters Error", attachment_type=allure.attachment_type.TEXT)


    if module_name == 'mark_actionable':
        with allure.step("Mark Actionable Validation"):
            try:
                if mark_actionable(driver, wait):
                    print("✅ Mark Actionable validation successful")
                    return True
                else:
                    raise Exception("❌ Mark Actionable validation failed")
            except Exception as e:
                allure.attach(str(e), name="Mark Actionable Error", attachment_type=allure.attachment_type.TEXT)


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

        # 🔹 Load test cases sheet (NO execution columns here)
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
                continue  # skip

            marks = []

            # Add the positive/negative mark based on test_type
            if row_test_type in ["positive", "negative"]:
                marks.append(getattr(pytest.mark, row_test_type))
            task_details_raw = row.get("task_details", "")
            task_details = {}

            if task_details_raw:
                try:
                    task_details = json.loads(task_details_raw)
                except Exception as e:
                    print(f"❌ JSON error in task_details for {row.get('test_case_id')}: {e}")


            test_case_list.append(
                pytest.param(
                    row.get("test_case_id"),
                    row.get("module_name"),
                    row.get("test_case_description"),
                    row_test_type,
                    task_details,
                    row.get('testcase_execution'),
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
