import allure
import pandas as pd
import os
import pytest
import json
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from utilities.login_utils import login_check
from utilities.add_task_functions.wait_for_loader_to_disappear import wait_for_loader_to_disappear
from selenium.webdriver.support.ui import WebDriverWait
from load_test_config_excel_data import load_test_config_excel_data
from utilities.other_utils_functions.highlight import highlight_element
from utilities.settings_functions.company_details import company_details
from utilities.settings_functions.check_license_task import check_license_task
from utilities.settings_functions.check_selected_license_task import check_selected_license_task
from utilities.settings_functions.personal_details import personal_details
from utilities.settings_functions.create_department import create_department
from utilities.settings_functions.create_designation import create_designation
from utilities.settings_functions.team_members import invite_team_member
from utilities.settings_functions.task_category import task_category
from utilities.settings_functions.not_applicable_tasks import not_applicable_tasks
from utilities.settings_functions.department_export_data import department_export_all_data
from utilities.settings_functions.configurations_normal_task import configurations_normal_task
from utilities.settings_functions.configurations_special_task import configurations_special_task
from utilities.settings_functions.license_task import license_task
from utilities.settings_functions.account import license_subscription
from utilities.settings_functions.account_deactivation import account_deactivation_module

def settings_check(driver, module_name=None, test_case_id=None, test_type=None, task_details=None):
    wait = WebDriverWait(driver, 30)

    module_name = str(module_name).strip()


    if module_name not in ['account_deactivation']:
        driver.get("https://preprodreact.compliancesutra.com/login")
        
        #  ✅ Step 1: Login Check (For all normal settings tests)
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
                allure.attach(str(e), name="Delete Task and Restore", attachment_type=allure.attachment_type.TEXT)
            
        wait_for_loader_to_disappear(driver, wait)
        
        try:
            with open(os.path.join("data", 'locators.json'), 'r') as f:
                elements_details = json.load(f)
                dashboard_icon = elements_details['dashboard_icon']
        except FileNotFoundError as e:
            allure.attach("locators.json file not found", name="Locators Error", attachment_type=allure.attachment_type.TEXT)
            pytest.fail(str(e))
        except json.JSONDecodeError as e:
            allure.attach(str(e), name="Delete Task and Restore", attachment_type=allure.attachment_type.TEXT)
            
        with allure.step("Open Dashboard"):
            try:
                time.sleep(2)
                dashboard_icon_elem = wait.until(EC.presence_of_element_located((By.XPATH, dashboard_icon)))
                highlight_element(driver, dashboard_icon_elem)
                dashboard_icon_elem.click()
                print("✅ Dashboard icon clicked")
            except Exception as e:
                allure.attach(str(e), name="Delete Task and Restore", attachment_type=allure.attachment_type.TEXT)

    if module_name == 'account_deactivation' and task_details:
        driver.get("https://preprodreact.compliancesutra.com/login")
        # Extract the credentials directly from the Excel task_details column!
        tm_user = task_details.get("tm_user")
        tm_pwd = task_details.get("tm_pwd")
        co_user = task_details.get("co_user")
        co_pwd = task_details.get("co_pwd")

        with allure.step("Execute Account Deactivation Request Flow"):
            try:
                # Pass the credentials into our execution module
                if account_deactivation_module(driver, wait, tm_user, tm_pwd, co_user, co_pwd):
                    print("✅ Account Deactivation Request Rejected successful")
                    return True
                else:
                    allure.attach("Test case failed for Account Deactivation Request", name="Deactivation Validation Failed", attachment_type=allure.attachment_type.TEXT)
                    
                    # 🛑 THE FIX 1: Turn the soft return into a hard crash
                    assert False, "❌ Account Deactivation Request Flow Failed!"
                    
            except Exception as e:
                allure.attach(str(e), name="Delete Task and Restore", attachment_type=allure.attachment_type.TEXT)
                
                # 🛑 THE FIX 2: Re-raise the exception to turn the step RED
                raise e

    # # Step 10: Edit Personal Detials
    if module_name == 'edit_personal_details':
        with allure.step("Edit Personal Detials"):
            try:
                if personal_details(driver, wait):
                    print("✅ Edit Personal Detials successful")
                    return True
                else:
                    allure.attach("Test case failed for Edit Personal Detials", name="Edit Personal Detials Validation Failed", attachment_type=allure.attachment_type.TEXT)
                    return False
            except Exception as e:
                allure.attach(str(e), name="Delete Task and Restore", attachment_type=allure.attachment_type.TEXT)
     # # Step 10: Edit Personal Detials
    if module_name == 'company_details':
        company_name =  task_details.get("company_name")
        # compliance_officer = task_details.get("compliance_officer")
        with allure.step("Create Company Details"):
            try:
                if company_details(driver, wait, company_name):
                    print("✅ Create Company Details successful")
                    return True
                else:
                    allure.attach("Test case failed for Create Company Details", name="Create Company Details Validation Failed", attachment_type=allure.attachment_type.TEXT)
                    return False
            except Exception as e:
                allure.attach(str(e), name="Delete Task and Restore", attachment_type=allure.attachment_type.TEXT)

    # if module_name == 'check_license_task':
    #     company_name =  task_details.get("company_name")
    #     license_name =  task_details.get("license_name")
    #     task_name =  task_details.get("task_name")  
    #     with allure.step("Check License Task"):
    #         try:
    #             if check_license_task(driver, wait, company_name, license_name, task_name):

    #                 print("✅ Check License Task successful")
    #                 return True
    #             else:
    #                 allure.attach("Test case failed for Check License Task", name="Check License Task Validation Failed", attachment_type=allure.attachment_type.TEXT)
    #                 return False
    #         except Exception as e:
    #             allure.attach(str(e), name="Delete Task and Restore", attachment_type=allure.attachment_type.TEXT)
    # if module_name == 'selected_license_name':
    #     company_name =  task_details.get("company_name")
    #     selected_license_name = task_details.get("selected_license_name")
    #     license_name =  task_details.get("license_name")
    #     task_name =  task_details.get("task_name")  
    #     with allure.step("Check License Task"):
    #         try:
    #             if check_selected_license_task(driver, wait, company_name, selected_license_name, license_name, task_name):

    #                 print("✅ Check License Task successful")
    #                 return True
    #             else:
    #                 allure.attach("Test case failed for Check License Task", name="Check License Task Validation Failed", attachment_type=allure.attachment_type.TEXT)
    #                 return False
    #         except Exception as e:
    #             allure.attach(str(e), name="Delete Task and Restore", attachment_type=allure.attachment_type.TEXT)
    if module_name == 'create_department':
       
        company_name =  task_details.get("company_name")
        department_name = task_details.get("department_name")
        hod_name = task_details.get("hod_name")
        alias =  task_details.get("department_alias")
        description =  task_details.get("description")
    
        with allure.step("Create Department Details"):
            try:
                if create_department(driver, wait, company_name, department_name, hod_name, alias,  description):
                    print("✅ Create Department Detials successful")
                    return True
                else:
                    allure.attach("Test case failed for Create Department Detials", name="Create Department Detials Validation Failed", attachment_type=allure.attachment_type.TEXT)
                    return False
            except Exception as e:
                allure.attach(str(e), name="Delete Task and Restore", attachment_type=allure.attachment_type.TEXT)
    if module_name == 'create_designation' and task_details:
        designation_name = task_details.get("designation_name")
        alias = task_details.get("designation_alias")
        description = task_details.get("description")
        hod_name = task_details.get('hod_name')

        print("📌 Data from Excel JSON:", task_details)

        with allure.step("Create Department Details"):
            try:
                if create_designation(driver,wait, designation_name, alias, description, hod_name):
                    print("✅ Create Department Details successful")
                    return True
                else:
                    allure.attach("Test case failed for Create Department Details",name="Create Department Validation Failed",attachment_type=allure.attachment_type.TEXT)
                    return False
            except Exception as e:
                allure.attach(str(e), name="Delete Task and Restore", attachment_type=allure.attachment_type.TEXT)

    
    if module_name == 'invite_team_member' and task_details:
        full_name = task_details.get("full_name")
        email = task_details.get("email")
        role = task_details.get("role")
        department_name = task_details.get("department_name")
        designation_name = task_details.get("designation_name")
        full_name_2 = task_details.get("full_name_2")
        email_2 = task_details.get("email_2")

        print("📌 Data from Excel JSON:", task_details)

        with allure.step("Invite Team Member"):
            try:
                if invite_team_member(driver, wait, full_name, email, role, department_name, designation_name, full_name_2, email_2,):
                    print("✅ Invite Team Member successful")
                    return True
                else:
                    allure.attach("Test case failed for Invite Team Member",name="Invite Team Member Validation Failed",attachment_type=allure.attachment_type.TEXT)
                    return False
            except Exception as e:
                allure.attach(str(e), name="Delete Task and Restore", attachment_type=allure.attachment_type.TEXT)

    
    if module_name == 'task_Category' and task_details:
        category_name = task_details.get("category_name")
        category_desc= task_details.get("category_desc")


        print("📌 Data from Excel JSON:", task_details)
        with allure.step("Create Task Category"):
            try:
                if task_category(driver, wait, category_name, category_desc):
                    print("✅ Create Task Category successful")
                    return True
                else:
                    allure.attach("Test case failed for Create Task Category",name="Create Task Category Validation Failed",attachment_type=allure.attachment_type.TEXT)
                    return False
            except Exception as e:
                allure.attach(str(e), name="Delete Task and Restore", attachment_type=allure.attachment_type.TEXT)
    if module_name == 'not_applicable_tasks':
        company_name =  task_details.get("company_name")
        license_name = task_details.get("license_name")
        with allure.step("Click Not Applicable"):
            try:
                if not_applicable_tasks(driver, wait, company_name, license_name):
                    print("✅ Click Not Applicable successful")
                    return True
                else:
                    allure.attach("Test case failed for Click Not Applicable", name="Click Not Applicable Validation Failed", attachment_type=allure.attachment_type.TEXT)
                    return False
            except Exception as e:
               allure.attach(str(e), name="Delete Task and Restore", attachment_type=allure.attachment_type.TEXT)
   

    if module_name == 'department_export':
        with allure.step("Export Department Data"):
            try:
                if department_export_all_data(driver, wait):
                    print("✅ Export Department Detials successful")
                    return True
                else:
                    allure.attach("Test case failed for Export Department Detials", name="Export Department Detials Validation Failed", attachment_type=allure.attachment_type.TEXT)
                    return False
            except Exception as e:
                allure.attach(str(e), name="Export All Data Button Error", attachment_type=allure.attachment_type.TEXT)
    
    if module_name == 'configurations_normal_task':
        config_normal_task_name = task_details.get("config_normal_task_name")
        with allure.step("Configurations Normal Task"):
            try:
                if configurations_normal_task(driver, wait, config_normal_task_name):
                    print("✅ Configurations  Normal Task Detials successful")
                    return True
                else:
                    allure.attach("Test case failed for Configurations Normal Task Detials", name="Configurations Normal Task Validation Failed", attachment_type=allure.attachment_type.TEXT)
                    return False
            except Exception as e:
                allure.attach(str(e), name="Configurations Normal Task Button Error", attachment_type=allure.attachment_type.TEXT)
    
    if module_name == 'configurations_special_task':
        config_special_task_name = task_details.get("config_special_task_name")
        with allure.step("Configurations Special Task"):
            try:
                if configurations_special_task(driver, wait, config_special_task_name):
                    print("✅ Configurations  Special Special Detials successful")
                    return True
                else:
                    allure.attach("Test case failed for Configurations special Task Detials", name="Configurations Special Task Validation Failed", attachment_type=allure.attachment_type.TEXT)
                    return False
            except Exception as e:
                allure.attach(str(e), name="Configurations Special Task Button Error", attachment_type=allure.attachment_type.TEXT)
   
    if module_name == 'license_task' and task_details:
        company_license_name = task_details.get("company_name")
        license_name =  task_details.get("license_name")
        with allure.step("Add Team Members in License task"):
            try:
                if license_task(driver, wait, company_license_name, license_name):
                    print("✅ Add Team Members in License task successful")
                    return True
                else:
                    allure.attach("Test case failed for Add Team Members in License task", name="Add Team Members in License task Validation Failed", attachment_type=allure.attachment_type.TEXT)
                    return False
            except Exception as e:
                allure.attach(str(e), name="Delete Task and Restore", attachment_type=allure.attachment_type.TEXT)
    
    # if module_name == 'license_subscrption' and task_details:
       
    #     with allure.step("Check License Inactive and Active"):
    #         try:
    #             if license_subscription(driver, user_validation=False):
    #                 print("✅ Add Team Members in License task successful")
    #                 return True
    #             else:
    #                 allure.attach("Test case failed for Add Team Members in License task", name="Add Team Members in License task Validation Failed", attachment_type=allure.attachment_type.TEXT)
    #                 return False
    #         except Exception as e:
    #             step_fail(driver, "License Task", e)
    # allure.attach(str(e), name="Delete Task and Restore", attachment_type=allure.attachment_type.TEXT)

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
             # ----------------------------
            # 1. Testcase execution check
            # ----------------------------
            test_case_execution = str(row.get("test_case_execution", "n")).strip().lower()

            if test_case_execution != "y":
                print(f"Skipping {row.get('test_case_id')} -> test_case_execution = n")
                continue
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
                        row.get('test_case_execution'),
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
