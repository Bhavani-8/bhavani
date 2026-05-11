import allure
import pandas as pd
import os
import json
import pytest
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from utilities.other_utils_functions.highlight import highlight_element

from utilities.login_utils import login_check
from load_test_config_excel_data import load_test_config_excel_data
from utilities.add_task_functions.wait_for_loader_to_disappear import wait_for_loader_to_disappear
from selenium.webdriver.support.ui import WebDriverWait
from utilities.compliance_history_functions.compliance_column_filter import compliance_column_filter
from utilities.compliance_history_functions.search_task_name import search_task_name
from utilities.compliance_history_functions.compliance_history_filter import compliance_history_filter
from utilities.compliance_history_functions.compliance_view import compliance_view
def step_fail(driver, step_name, error):
    allure.attach(str(error), name=f"{step_name} Error", attachment_type=allure.attachment_type.TEXT)
    allure.attach(driver.get_screenshot_as_png(), name=f"{step_name} Screenshot", attachment_type=allure.attachment_type.PNG)
    pytest.fail(f"❌ {step_name} failed")

def compliance_history_check(driver, module_name=None, test_case_id=None):
    wait = WebDriverWait(driver, 30)


    try:
        with open(os.path.join("data", 'locators.json'), 'r') as f:
            elements_details = json.load(f)
            dashboard_icon = elements_details['dashboard_icon']
            compliance_hist_icon = elements_details['compliance_hist_icon']
        print("✅ locators.json loaded successfully")
    except Exception as e:
        allure.attach(str(e), name="Locators Error", attachment_type=allure.attachment_type.TEXT)
        pytest.fail("Failed to load locators.json")

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
            allure.attach("Login failed", name="Login Status", attachment_type=allure.attachment_type.TEXT)
            step_fail(driver, "Login Failed - Unable to proceed with test", Exception("Login returned False"))
        

    wait_for_loader_to_disappear(driver, wait)

    with allure.step("Open Dashboard"):
        try:
            dashboard_icon_elem = wait.until(EC.element_to_be_clickable((By.XPATH, dashboard_icon)))
            # highlight_element(driver, dashboard_icon_elem)
            dashboard_icon_elem.click()
            print("✅ Dashboard icon clicked")
        except Exception as e:
            allure.attach(str(e), name="Dashboard Open Error", attachment_type=allure.attachment_type.TEXT)
            return False
    with allure.step("Open Compliance History Section"):
        try:
            compliance_btn = wait.until(EC.element_to_be_clickable((By.XPATH, compliance_hist_icon)))
            highlight_element(driver, compliance_btn)
            compliance_btn.click()
            time.sleep(2)
            print("✅ Compliance History icon clicked")
        except Exception as e:
            allure.attach(str(e), name="Compliance History Section Error", attachment_type=allure.attachment_type.TEXT)
            return False

    if module_name == 'compliance_column_filter':
        with allure.step("Column filter"):
            try:
                if compliance_column_filter(driver, wait):
                    print("✅ Column filter successful")
                    return True
                else:
                    allure.attach("Test case failed for Column filter",name="Column filter Validation Failed",attachment_type=allure.attachment_type.TEXT)
                    return False
            except Exception as e:
                allure.attach(str(e), name="Column filter ", attachment_type=allure.attachment_type.TEXT)
    
    if module_name == 'search_task_name':
        with allure.step("Search Task Name"):
            try:
                if search_task_name(driver, wait):
                    print("✅ Search Task Name successful")
                    return True
                else:
                    allure.attach("Test case failed for search task name",name="Search Task Name Validation Failed",attachment_type=allure.attachment_type.TEXT)
                    return False
            except Exception as e:
                allure.attach(str(e), name="Search task name ", attachment_type=allure.attachment_type.TEXT)

    if module_name == 'compliance_history_filter':
        with allure.step("Compliance History Filter"):
            try:
                if compliance_history_filter(driver, wait):
                    print("✅ Compliance filter successful")
                    return True
                else:
                    allure.attach("Test case failed for compliance history filter failed",name="Compliance History Filter Validation Failed",attachment_type=allure.attachment_type.TEXT)
                    return False
            except Exception as e:
                allure.attach(str(e), name="Compliance history filter ", attachment_type=allure.attachment_type.TEXT)
    
    if module_name == 'compliance_view':
        with allure.step("Compliance History Filter"):
            try:
                if compliance_view(driver, wait):
                    print("✅ Compliance view successful")
                    return True
                else:
                    allure.attach("Test case failed for Compliance View",name="Compliance View Validation Failed",attachment_type=allure.attachment_type.TEXT)
                    return False
            except Exception as e:
                allure.attach(str(e), name="Compliance view ", attachment_type=allure.attachment_type.TEXT)
    
    
    
    step_fail(driver, "Unknown module name", f"Unknown module name: {module_name}")


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


    