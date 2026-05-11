# dashboard_utils.py

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import pandas as pd
import pytest
import allure
import json
import os
import time
import pyautogui as pg

from utilities.dashboard_functions.search_task_by_non_existing_task_name import search_task_by_non_existing_task_name
from utilities.other_utils_functions.highlight import highlight_element
from utilities.login_utils import login_check
from utilities.add_task_utils import wait_for_loader_to_disappear
from utilities.other_utils_functions.license_utils import validate_license_subscription
from utilities.dashboard_functions.upper_dashboard_validation import upper_dashboard_validation
from utilities.dashboard_functions.lower_dashboard_validation import lower_dashboard_validation
from utilities.dashboard_functions.column_filter_validation import column_filter_validation
from utilities.dashboard_functions.column_filter_negative import column_filter_negative
from utilities.bulk_actions_functions.bulk_actions_module import bulk_actions_module
from utilities.dashboard_functions.column_chooser_save_and_relogin import column_chooser_relogin
from utilities.dashboard_functions.column_reorder import column_reorder
from utilities.dashboard_functions.export_all_data_validation import export_all_data
from utilities.dashboard_functions.export_without_selecting_data import export_without_selecting_data
from utilities.dashboard_functions.column_chooser_validation import column_chooser_validation
from utilities.dashboard_functions.upper_dashboard_date_filter import upper_dashboard_date_filter
from utilities.dashboard_functions.lower_dashboard_date_fiter import lower_dashboard_date_filter
from utilities.dashboard_functions.copy_task_link import copy_task_link
from utilities.dashboard_functions.search_task_by_existing_task_name import search_task_by_existing_task_name
from utilities.dashboard_graph_functions.graph_count import dashboard_graph_count
from utilities.search_utils import clear_search
from load_test_config_excel_data import load_test_config_excel_data
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains


def dashboard_check(driver, dash_type='QCC', module_name=None, test_case_id=None):
    wait = WebDriverWait(driver, 30)

    # ✅ Step 1: Login
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
                    
    wait_for_loader_to_disappear(driver, wait)

    # ✅ Step 2: Load locators
    # with allure.step("Load locators.json"):
    try:
        with open(os.path.join("data", 'locators.json'), 'r') as f:
            elements_details = json.load(f)
            dashboard_icon = elements_details['dashboard_icon']
            special_task_icon = elements_details['special_task_icon']
        # print("✅ locators.json loaded successfully")
    except FileNotFoundError as e:
        allure.attach("locators.json file not found", name="Locators Error", attachment_type=allure.attachment_type.TEXT)
        pytest.fail(str(e))
    except json.JSONDecodeError as e:
        allure.attach("Invalid JSON in locators.json", name="Locators Error", attachment_type=allure.attachment_type.TEXT)
        pytest.fail(str(e))

    # ✅ Step 3: Open Dashboard
    if dash_type == 'special':
        with allure.step("Open Dashboard"):
            try:
                time.sleep(2)
                special_task_icon_elem = wait.until(EC.presence_of_element_located((By.XPATH, special_task_icon)))
                highlight_element(driver, special_task_icon_elem)
                special_task_icon_elem.click()
                print("✅ Special Task Dashboard icon clicked")
            except Exception as e:
                allure.attach(str(e), name="Dashboard Open Error", attachment_type=allure.attachment_type.TEXT)
                return False
    else:
        with allure.step("Open Dashboard"):
            try:
                time.sleep(2)
                dashboard_icon_elem = wait.until(EC.presence_of_element_located((By.XPATH, dashboard_icon)))
                highlight_element(driver, dashboard_icon_elem)
                dashboard_icon_elem.click()
                print("✅ Dashboard icon clicked")
            except Exception as e:
                allure.attach(str(e), name="Dashboard Open Error", attachment_type=allure.attachment_type.TEXT)
                return False

    task_name = 'Automation_bulk_task_creation_27_Nov2'

    if module_name == 'bulk_task_creation':
        # ✅ Step 4: Read Excel bulk task creation file
        with allure.step("Read Bulk Task Creation Excel File"):
            try:
                filename = 'bulk_task_creation_valid_preprod.xlsx' if dash_type == 'QCC' else 'bulk_special_task_creation_valid_preprod.xlsx'

                df = pd.read_excel(f'data/{filename}', skiprows=[1])
                task_name = str(df['Task Name*'].iloc[0])
                print(f'📄 Fetched task name: {task_name}')
            except Exception as e:
                allure.attach(str(e), name="Excel Read Error", attachment_type=allure.attachment_type.TEXT)
                task_name = None

    # ✅ Step 6: Upper Dashboard Validation
    if module_name == 'upper_dashboard_count':
        with allure.step("Upper Dashboard Count Validation"):
            try:
                if upper_dashboard_validation(driver, wait, dash_type):
                    print("✅ Upper Dashboard validation successful")
                    return True
                else:
                    allure.attach("Test case failed for Upper Dashboard", name="Upper Dashboard Validation Failed", attachment_type=allure.attachment_type.TEXT)
                    return False
            except Exception as e:
                allure.attach(str(e), name="Upper Dashboard Error", attachment_type=allure.attachment_type.TEXT)

    # ✅ Step 6: Upper Dashboard Validation
    if module_name == 'lower_dashboard_count':
        with allure.step("Lower Dashboard Count Validation"):
            try:
                if lower_dashboard_validation(driver, wait, dash_type):
                    print("✅ Lower Dashboard validation successful")
                    return True
                else:
                    allure.attach("Test case failed for Lower Dashboard", name="Lower Dashboard Validation Failed", attachment_type=allure.attachment_type.TEXT)
                    return False
            except Exception as e:
                allure.attach(str(e), name="Lower Dashboard Error", attachment_type=allure.attachment_type.TEXT)

    # # ✅ Step 7: Lower Dashboard Validation
    if module_name == 'lower_dashboard_date_filter_count':
        with allure.step("Lower Dashboard Date Filter Validation"):
            try:
                if lower_dashboard_date_filter(driver, wait, dash_type):
                    print("✅ Lower Dashboard Date Filter validation successful")
                    return True
                else:
                    allure.attach("Test case failed for Lower Dashboard Date Filter", name="Lower Dashboard Date Filter Validation Failed", attachment_type=allure.attachment_type.TEXT)
                    return False
            except Exception as e:
                allure.attach(str(e), name="Lower Dashboard Error", attachment_type=allure.attachment_type.TEXT)

    if module_name == 'upper_dashboard_date_filter_count':
        with allure.step("Upper Dashboard Filter Validation"):
            try:
                if upper_dashboard_date_filter(driver, wait, dash_type):
                    print("✅ Dashboard Filter successful")
                    return True
                else:
                    allure.attach("Test case failed for Dashboard Filter", name="Dashboard Filter Validation Failed", attachment_type=allure.attachment_type.TEXT)
                    return False
            except Exception as e:
                allure.attach(str(e), name="Dashboard Filter Error", attachment_type=allure.attachment_type.TEXT)

   
    if module_name == 'column_filter_functionality_valid_values':
        with allure.step("Column Filter Validation"):
            try:
                if column_filter_validation(driver, wait):
                    print("✅ Column Filter validation successful")
                    return True
                else:
                    allure.attach("Test case failed for Column Filter", name="Column Filter Validation Failed", attachment_type=allure.attachment_type.TEXT)
                    return False
            except Exception as e:
                allure.attach(str(e), name="Column Filter Error", attachment_type=allure.attachment_type.TEXT)

    
    if module_name == 'column_filter_functionality_invalid_values':
        with allure.step("Verify column filter behavior with invalid values"):
            try:
                if column_filter_negative(driver, wait):
                    print("✅Column filter works correctly with invalid values")
                    return True
                else:
                    allure.attach("Column filter did not handle invalid values as expected.", name="Column Filter Invalid Values Failed", attachment_type=allure.attachment_type.TEXT)
                    return False
            except Exception as e:
                allure.attach(str(e), name="Column Filter Invalid Values Error", attachment_type=allure.attachment_type.TEXT)

    if module_name == 'column_chooser_relogin':
        with allure.step("Verify column chooser selections are unchanged after relogin"):
            try:
                if column_chooser_relogin(driver, wait, dash_type):
                    print("✅ Bulk Action validation successful")
                    return True
                else:
                    allure.attach("Test case failed for Bulk Action", name="Bulk Action Validation Failed", attachment_type=allure.attachment_type.TEXT)
                    return False
            except Exception as e:
                allure.attach(str(e), name="Bulk Action Error", attachment_type=allure.attachment_type.TEXT)

    if module_name == 'column_filter_reorder':
        with allure.step("Column Filter Reorder Validation"):
            try:
                if column_reorder(driver, wait, dash_type):
                    print("✅ Column Filter validation Reorder successful")
                    return True
                else:
                    allure.attach("Test case failed for Column Filter Reorder", name="Column Filter Reorder Validation Failed", attachment_type=allure.attachment_type.TEXT)
                    return False
            except Exception as e:
                allure.attach(str(e), name="Bulk Action Error", attachment_type=allure.attachment_type.TEXT)

    
    # ✅ Step 10: Export Data Validation
    if module_name == 'export_all_data':
        with allure.step("Export Data Validation"):
            try:
                if export_all_data(driver, wait, dash_type):
                    print("✅ Export Data validation successful")
                    return True
                else:
                    allure.attach("Test case failed for Export Data", name="Export Data Validation Failed", attachment_type=allure.attachment_type.TEXT)
                    return False
            except Exception as e:
                allure.attach(str(e), name="Export Data Error", attachment_type=allure.attachment_type.TEXT)

    # ✅ Step 10: Export Data Validation
    if module_name == 'export_without_selecting_data':
        with allure.step("Export Without Selectig Data Validation"):
            try:
                if export_without_selecting_data(driver, wait, dash_type):
                    print("✅ Export Without Selectig Data Validation successful")
                    return True
                else:
                    allure.attach("Test case failed for Export Without Selectig Data", name="Export Without Selectig Data Validation Failed", attachment_type=allure.attachment_type.TEXT)
                    return False
            except Exception as e:
                allure.attach(str(e), name="Export Data Error", attachment_type=allure.attachment_type.TEXT)

    # ✅ Step 11: Column Chooser Validation
    if module_name == 'column_chooser':
        with allure.step("Column Chooser Validation"):
            try:
                if column_chooser_validation(driver, wait):
                    print("✅ Column Chooser validation successful")
                    return True
                else:
                    allure.attach("Test case failed for Column Chooser", name="Column Chooser Validation Failed", attachment_type=allure.attachment_type.TEXT)
                    return False
            except Exception as e:
                allure.attach(str(e), name="Column Chooser Error", attachment_type=allure.attachment_type.TEXT)

    # ✅ Step 11: Column Chooser Validation
    if module_name == 'search_existing_task':
        clear_search(driver, wait)
        with allure.step("Verify search functionality with existing task name"):
            try:
                if search_task_by_existing_task_name(driver, wait):
                    print("✅ Search with existing task name validation successful")
                    return True
                else:
                    allure.attach("Test case failed for an existing task name.", name="Search Existing Task Validation Failed", attachment_type=allure.attachment_type.TEXT)
                    return False
            except Exception as e:
                allure.attach(str(e), name="Search Existing Task Error", attachment_type=allure.attachment_type.TEXT)

    # ✅ Step 11: Column Chooser Validation
    if module_name == 'search_existing_task_with_spaces':
        with allure.step("Verify search with existing task name containing extra spaces"):
            try:
                if search_task_by_non_existing_task_name(driver, wait):
                    print("✅ Search with existing task name and extra spaces validation successful")
                    return True
                else:
                    allure.attach("Search did not return results for an existing task name with extra spaces.", name="Search Existing Task With Spaces Failed", attachment_type=allure.attachment_type.TEXT)
                    return False
            except Exception as e:
                allure.attach(str(e), name="Search Existing Task With Spaces Failed", attachment_type=allure.attachment_type.TEXT)
    
    if module_name == 'copy_task_link':
        with allure.step("Validate Copy Task Link functionality"):
            try:
                if copy_task_link(driver, wait, dash_type):
                    print("✅ Copy Task Link validation successful")
                    return True
                else:
                    allure.attach("Test case failed for Copy Task Link", name="Copy Task Link Failed", attachment_type=allure.attachment_type.TEXT)
                    return False
            except Exception as e:
                allure.attach(str(e), name="Bulk Action Error", attachment_type=allure.attachment_type.TEXT)
   
    if module_name in [
    'assign_to_bulk_action','assign_to_bulk_action_negative','add_approver_bulk_action','add_approver_bulk_action_negative','add_cc_bulk_action','add_cc_bulk_action_negative','add_comment_bulk_action',
    'add_comment_bulk_action_negative','upload_file_bulk_action','upload_file_bulk_action_negative','update_due_date_bulk_action','update_due_date_bulk_action_negative','approval_complied_bulk_action',
    'approval_not_complied_bulk_action','rejected_complied_bulk_action','rejected_not_complied_bulk_action','mark_complete_bulk_action','mark_complete_bulk_action_negative','approve_task_bulk_action',
    'reject_task_bulk_action','rejected_tasks_bulk_action','completed_tasks_bulk_Action']:
        with allure.step("Bulk Action Validation"):
            try:
                if bulk_actions_module(driver, wait, module_name, dash_type, test_case_id, task_name):
                    print("✅ Bulk Action validation successful")
                    return True
                else:
                    # print("❌ Bulk Action validation failed")
                    allure.attach("Test case failed for Bulk Action", name="Bulk Action Validation Failed", attachment_type=allure.attachment_type.TEXT)
                    return False
            except Exception as e:
                allure.attach(str(e), name="Bulk Action Error", attachment_type=allure.attachment_type.TEXT)
    if module_name == 'graph_count':
        with allure.step("Dashboard Graph Count Validation"):
            try:
                if dashboard_graph_count(driver, wait):
                    print("✅ Dashboard Graph Count validation successful")
                    return True
                else:
                    allure.attach("Test case failed for Dashboard Graph Count", name="Dashboard Graph Count Validation Failed", attachment_type=allure.attachment_type.TEXT)
                    return False
            except Exception as e:
                allure.attach(str(e), name="Dashboard Graph Count Error", attachment_type=allure.attachment_type.TEXT)
                
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
