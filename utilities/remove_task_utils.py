import allure
from selenium.webdriver.support.ui import WebDriverWait
import pytest
import os
import pandas as pd
from utilities.add_task_functions.wait_for_loader_to_disappear import wait_for_loader_to_disappear
from utilities.login_utils import login_check
from load_test_config_excel_data import load_test_config_excel_data
from utilities.remove_task_functions.delete_only_once_task import delete_only_once_task
from utilities.remove_task_functions.delete_daily_this_event_task import delete_daily_this_event_task
from utilities.remove_task_functions.delete_daily_this_and_following_events import delete_daily_this_and_following_events
from utilities.remove_task_functions.delete_weekly_all_events import delete_weekly_all_events
from utilities.remove_task_functions.delete_monthly_all_future_events import delete_monthly_all_future_events
from utilities.remove_task_functions.delete_quarterly_all_events_task import delete_quarterly_all_events_task
from utilities.remove_task_functions.delete_half_yearly_all_events_task import delete_half_yearly_all_events_task
from utilities.remove_task_functions.delete_yearly_all_events_task import delete_yearly_all_events_task
from utilities.remove_task_functions.delete_fortnightly_all_events_task import delete_fortnightly_all_events_task


    
def remove_task_check(driver, module_name=None):
    
    wait = WebDriverWait(driver, 10)
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
                    
    wait_for_loader_to_disappear(driver, wait, loader_class="dx-loadpanel-content")

    if module_name == 'delete_only_once_task':
        with allure.step("Delete Only once task"):
            try:
                if delete_only_once_task(driver, wait):
                    print("Delete Only once task successful")
                    return True
                else:
                    allure.attach("Test case failed for Delete only once task", name=" Delete only once task Validation Failed",attachment_type=allure.attachment_type.TEXT)
                    return False
            except Exception as e:
                 allure.attach(str(e), name="Delete only once task", attachment_type=allure.attachment_type.TEXT)

    if module_name == 'delete_daily_this_event_task':
        with allure.step("Delete Daily this event task"):
            try:
                if delete_daily_this_event_task(driver, wait):
                    print("Delete Daily this event task successful")
                    return True
                else:
                    allure.attach("Test case failed for Delete Daily this event task", name=" Delete Daily this event task Validation Failed",attachment_type=allure.attachment_type.TEXT)
                    return False
            except Exception as e:
                 allure.attach(str(e), name="Delete Daily this event task", attachment_type=allure.attachment_type.TEXT)

    if module_name == 'delete_daily_this_and_following_events':
        with allure.step("Delete Daily task"):
            try:
                if delete_daily_this_and_following_events(driver, wait):
                    print("Delete Only once task successful")
                    return True
                else:
                    allure.attach("Test case failed for Delete only once task", name=" Delete only once task Validation Failed",attachment_type=allure.attachment_type.TEXT)
                    return False
            except Exception as e:
                 allure.attach(str(e), name="Delete only once task", attachment_type=allure.attachment_type.TEXT)

    if module_name == 'delete_weekly_all_events':
        with allure.step("Delete all events task"):
            try:
                if delete_weekly_all_events(driver, wait):
                    print("Delete all events task successful")
                    return True
                else:
                    allure.attach("Test case failed for Delete all events task", name=" Delete all events task Validation Failed",attachment_type=allure.attachment_type.TEXT)
                    return False
            except Exception as e:
                allure.attach(str(e), name="Delete all events task", attachment_type=allure.attachment_type.TEXT)

    if module_name == 'delete_monthly_all_future_events':
        with allure.step("Delete All future events task"):
            try:
                if delete_monthly_all_future_events(driver, wait):
                    print("Delete all future events task successful")
                    return True
                else:
                    allure.attach("Test case failed for Delete all future events task", name=" Delete all future events task Validation Failed",attachment_type=allure.attachment_type.TEXT)
                    return False
            except Exception as e:
                allure.attach(str(e), name="Delete all future events task", attachment_type=allure.attachment_type.TEXT)

    if module_name == 'delete_quarterly_all_events_task':
        with allure.step("Delete Quarterly task"):
            try:
                if delete_quarterly_all_events_task(driver, wait):
                    print("Delete Quarterly task successful")
                    return True
                else:
                    allure.attach("Test case failed for Delete Quarterly task", name=" Delete Quarterly task Validation Failed",attachment_type=allure.attachment_type.TEXT)
                    return False
            except Exception as e:
                 allure.attach(str(e), name="Delete Quarterly task", attachment_type=allure.attachment_type.TEXT)

    if module_name == 'delete_half_yearly_all_events_task':
        with allure.step("Delete Quarterly task"):
            try:
                if delete_half_yearly_all_events_task(driver, wait):
                    print("Delete Half Yearly task successful")
                    return True
                else:
                    allure.attach("Test case failed for Delete Half Yearly task", name=" Delete Half Yearly task Validation Failed",attachment_type=allure.attachment_type.TEXT)
                    return False
            except Exception as e:
                 allure.attach(str(e), name="Delete Half Yearly task", attachment_type=allure.attachment_type.TEXT)

    if module_name == 'delete_yearly_all_events_task':
        with allure.step("Delete Yearly task"):
            try:
                if delete_yearly_all_events_task(driver, wait):
                    print("Delete Yearly task successful")
                    return True
                else:
                    allure.attach("Test case failed for Delete Yearly task", name=" Delete Yearly task Validation Failed",attachment_type=allure.attachment_type.TEXT)
                    return False
            except Exception as e:
                 allure.attach(str(e), name="Delete Yearly task", attachment_type=allure.attachment_type.TEXT)
    
    if module_name == 'delete_fortnightly_all_events_task':
        with allure.step("Delete Fortnightly task"):
            try:
                if delete_fortnightly_all_events_task(driver, wait):
                    print("Delete Fortnightly task successful")
                    return True
                else:
                    allure.attach("Test case failed for Delete Fortnightly task", name=" Delete Fortnightly task Validation Failed",attachment_type=allure.attachment_type.TEXT)
                    return False
            except Exception as e:
                 allure.attach(str(e), name="Delete Fortnightly task", attachment_type=allure.attachment_type.TEXT)

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
