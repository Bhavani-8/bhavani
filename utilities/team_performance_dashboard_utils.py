from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import pandas as pd
import pytest
import allure
import json
import os
from load_test_config_excel_data import load_test_config_excel_data
from utilities.other_utils_functions.highlight import highlight_element
from utilities.login_utils import login_check
from utilities.add_task_utils import wait_for_loader_to_disappear
from utilities.team_performance_functions.team_column_chooser_validation import validate_column_chooser_flow
from utilities.team_performance_functions.special_column_chooser_validation import special_column_chooser_flow
from utilities.team_performance_functions.team_column_filter_validation import column_filter_validation
from utilities.team_performance_functions.team_export_data_validation import export_data_validation
from utilities.team_performance_functions.team_count_validation import count_validation
from utilities.team_performance_functions.special_team_count_validation import special_tm_count_validation
from utilities.team_performance_functions.team_search_validation import search_validation
from utilities.team_performance_functions.special_tm_search_validation import special_search_validation
from utilities.team_performance_functions.team_date_validation import date_validation
from utilities.team_performance_functions.special_tm_date_validation import special_tm_date_validation
from utilities.team_performance_functions.project_validation import project_check
from utilities.team_performance_functions.special_project_validation import special_project_check
from utilities.search_utils import clear_search
from utilities.team_performance_functions.special_team_column_filter_validation import special_column_filter_validation


def team_performance_dashboard_check(driver, dash_type='QCC', module_name=None, test_case_id=None):
    wait = WebDriverWait(driver, 30)

    
    driver.get("https://preprodreact.compliancesutra.com/login")

    # ✅ Step 1: Login
    with allure.step("Login with valid credentials"):
       
            
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

    # ✅ Step 3: Load locators
    # with allure.step("Load locators.json"):
    try:
        with open(os.path.join("data", 'locators.json'), 'r') as f:
            elements_details = json.load(f)

        dashboard_icon = elements_details['dashboard_icon']
        special_task_icon = elements_details['special_task_icon']
        team_performance_btn = elements_details['team_performance_btn']
        print("✅ locators.json loaded successfully")
    except Exception as e:
        allure.attach(str(e), name="Locators Load Error", attachment_type=allure.attachment_type.TEXT)
        return False

   
    if dash_type == 'special':
        with allure.step("Open Special Task Dashboard → Special Team Performance"):
            try:
                print("📍 Opening Special Task Dashboard...")
                special_task_icon_elem = wait.until(EC.element_to_be_clickable((By.XPATH, special_task_icon)))
                highlight_element(driver, special_task_icon_elem)
                special_task_icon_elem.click()
                print("✅ Special Task Dashboard icon clicked")

                wait_for_loader_to_disappear(driver, wait)
                special_team_perf_elem = wait.until(EC.element_to_be_clickable((By.XPATH, team_performance_btn)))
                highlight_element(driver, special_team_perf_elem)
                special_team_perf_elem.click()
                print("✅ Special Team Performance clicked")
                wait_for_loader_to_disappear(driver, wait)
            except Exception as e:
                allure.attach(str(e), name="Dashboard Open Error", attachment_type=allure.attachment_type.TEXT)
                return False
    else:
        with allure.step("Open Dashboard → Team Performance"):
            try:
                print("📍 Opening Normal Dashboard...")
                dashboard_icon_elem = wait.until(EC.element_to_be_clickable((By.XPATH, dashboard_icon)))
                highlight_element(driver, dashboard_icon_elem)
                dashboard_icon_elem.click()
                print("✅ Dashboard icon clicked")

                wait_for_loader_to_disappear(driver, wait)
                print("⏳ Clicking Team Performance...")
                team_perf_elem = wait.until(EC.element_to_be_clickable((By.XPATH, team_performance_btn)))
                highlight_element(driver, team_perf_elem)
                team_perf_elem.click()
                print("✅ Team Performance clicked")
                wait_for_loader_to_disappear(driver, wait)
            except Exception as e:
                print(f"❌ Failed in dashboard navigation: {e}")
                allure.attach(str(e), name="Dashboard Navigation Error", attachment_type=allure.attachment_type.TEXT)
                return False


    if module_name == 'column_filter':
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

   
    if module_name == 'count_validation':
        with allure.step("count_validation"):
            try:
                count_validation(driver, wait)
                print("✅ Count validation successful")
                return True

            except AssertionError as ae:
                # 🔴 actual validation failures
                allure.attach(str(ae), name="Count Validation Failed", attachment_type=allure.attachment_type.TEXT)
                print(f"❌ Validation Failed: {ae}")
                # pytest.fail(str(ae)) 
                return False 

            except Exception as e:
                # ⚠️ unexpected errors
                allure.attach(str(e), name="Count Error", attachment_type=allure.attachment_type.TEXT)
                print(f"⚠️ Unexpected Error: {e}")
                # pytest.fail(f"Unexpected Error: {e}")
                return False 
    
    if module_name == 'special_count_validation':
        with allure.step("count_validation"):
            try:
                special_tm_count_validation(driver, wait)
                print("✅ Count validation successful")
                return True

            except AssertionError as ae:
                # 🔴 actual validation failures
                allure.attach(str(ae), name="Count Validation Failed", attachment_type=allure.attachment_type.TEXT)
                print(f"❌ Validation Failed: {ae}")
                return False 


            except Exception as e:
                # ⚠️ unexpected errors
                allure.attach(str(e), name="Count Error", attachment_type=allure.attachment_type.TEXT)
                print(f"⚠️ Unexpected Error: {e}")
                return False 


    if module_name == 'special_column_filter':
        with allure.step("Special Column Filter Validation"):
            try:
                if special_column_filter_validation(driver, wait):
                    print("✅ Special Column Filter validation successful")
                    return True
                else:
                   allure.attach("Test case failed for Special column filter", name="Column Filter Validation Failed", attachment_type=allure.attachment_type.TEXT)
                   return False
            except Exception as e:
                allure.attach(str(e), name="Column Filter Error", attachment_type=allure.attachment_type.TEXT)
   
    if module_name == 'export_data':
        with allure.step("Export Data Validation"):
            try:
                if export_data_validation(driver, wait):
                    print("✅ Export Data validation successful")
                    return True
                else:
                   allure.attach("Test case failed for Export Data", name="Export Data Validation Failed", attachment_type=allure.attachment_type.TEXT)
                   return False
            except Exception as e:
                allure.attach(str(e), name="Export Data Error", attachment_type=allure.attachment_type.TEXT)

    if module_name == 'column_chooser':
        with allure.step("Column Chooser Validation"):
            try:
                if validate_column_chooser_flow(driver, wait):
                    print("✅ Column Chooser validation successful")
                    return True
                else:
                   allure.attach("Test case failed for Column Chooser", name="Column Chooser Validation Failed", attachment_type=allure.attachment_type.TEXT)
                   return False
            except Exception as e:
                allure.attach(str(e), name="Column Chooser Error", attachment_type=allure.attachment_type.TEXT)


    if module_name == 'special_column_chooser':
        with allure.step("Column Chooser Validation"):
            try:
                if special_column_chooser_flow(driver, wait):
                    print("✅ Column Chooser validation successful")
                    return True
                else:
                   allure.attach("Test case failed for Column Chooser", name="Column Chooser Validation Failed", attachment_type=allure.attachment_type.TEXT)
                   return False
            except Exception as e:
                allure.attach(str(e), name="Column Chooser Error", attachment_type=allure.attachment_type.TEXT)

    if module_name == 'search_validation':
        with allure.step("Search Validation"):
            try:
                search_validation(driver, wait)
                print("✅ Search validation successful")
                return True

            except AssertionError as ae:  
                allure.attach(str(ae), name="Search Validation Failed", attachment_type=allure.attachment_type.TEXT)
                print(f"❌ Validation Failed: {ae}")
                return False 

            except Exception as e:
                # ⚠️ unexpected errors
                allure.attach(str(e), name="Count Error", attachment_type=allure.attachment_type.TEXT)
                print(f"⚠️ Unexpected Error: {e}")
                return False 

    
    if module_name == 'special_search_validation':
        with allure.step("Search Validation"):
            try:
                special_search_validation(driver, wait)
                print("✅ Search validation successful")
                return True

            except AssertionError as ae:  
                allure.attach(str(ae), name="Search Validation Failed", attachment_type=allure.attachment_type.TEXT)
                print(f"❌ Validation Failed: {ae}")
                return False 

            except Exception as e:
                # ⚠️ unexpected errors
                allure.attach(str(e), name="Count Error", attachment_type=allure.attachment_type.TEXT)
                print(f"⚠️ Unexpected Error: {e}")
                return False 


    if module_name == 'date_validation':
        with allure.step("Date Validation"):
            try:
                date_validation(driver, wait)
                print("✅ Date Filter validation successful")
                return True
            except AssertionError as ae:  
                allure.attach(str(ae), name="Date Filter validation Failed", attachment_type=allure.attachment_type.TEXT)
                print(f"❌ Validation Failed: {ae}")
                return False 

            except Exception as e:
                # ⚠️ unexpected errors
                allure.attach(str(e), name="Count Error", attachment_type=allure.attachment_type.TEXT)
                print(f"⚠️ Unexpected Error: {e}")
                return False 
    if module_name == 'special_date_validation':
        with allure.step("special Date Validation"):
            try:
                special_tm_date_validation(driver, wait)
                print("✅ Date Filter validation successful")
                return True
            except AssertionError as ae:  
                allure.attach(str(ae), name="Date Filter validation Failed", attachment_type=allure.attachment_type.TEXT)
                print(f"❌ Validation Failed: {ae}")
                return False 

            except Exception as e:
                # ⚠️ unexpected errors
                allure.attach(str(e), name="Count Error", attachment_type=allure.attachment_type.TEXT)
                print(f"⚠️ Unexpected Error: {e}")
                return False 

    if module_name == 'project_filter':
        with allure.step("Project Filter Validation"):
            try:
                if project_check(driver, wait):
                    print("✅ Project Filter validation successful")
                    return True
                else:
                   allure.attach("Test case failed for Project Filter", name="Project Filter Validation Failed", attachment_type=allure.attachment_type.TEXT)
                   return False
            except Exception as e:
                allure.attach(str(e), name="Project Error", attachment_type=allure.attachment_type.TEXT)
    if module_name == 'special_project_filter':
        with allure.step("Project Filter Validation"):
            try:
                if special_project_check(driver, wait):
                    print("✅ Project Filter validation successful")
                    return True
                else:
                   allure.attach("Test case failed for Project Filter", name="Project Filter Validation Failed", attachment_type=allure.attachment_type.TEXT)
                   return False
            except Exception as e:
                allure.attach(str(e), name="Project Error", attachment_type=allure.attachment_type.TEXT)
    
    
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


