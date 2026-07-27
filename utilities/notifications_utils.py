import allure
import pandas as pd
import os
import pytest

from utilities.login_utils import login_check
from utilities.add_task_functions.format_time_if_valid import format_time_if_valid
from utilities.add_task_functions.format_date_if_valid import format_date_if_valid
from utilities.add_task_functions.wait_for_loader_to_disappear import wait_for_loader_to_disappear
from selenium.webdriver.support.ui import WebDriverWait
from utilities.other_utils_functions.license_utils import validate_license_subscription
from utilities.add_task_utils import add_task_check
from load_test_config_excel_data import load_test_config_excel_data
# from utilities.add_task_utils import get_test_case_list
from utilities.notifications_functions.create_individual_task import create_individual_task
from utilities.notifications_functions.assign_task_by_co import assign_task_by_co
from utilities.notifications_functions.reassign_task_by_co import reassign_task_by_co
from utilities.notifications_functions.update_created_task import update_created_task
from utilities.notifications_functions.notification_project import create_project
from utilities.notifications_functions.delete_task import delete_tasks
from utilities.notifications_functions.create_company import create_company
from utilities.notifications_functions.edit_personal_details import edit_personal_details
from utilities.notifications_functions.task_approved_by_approver import task_approved_by_approver
from utilities.notifications_functions.bulk_task import bulk_task_not_assigned 
from utilities.notifications_functions.reference_added import reference_added_by_co
from utilities.notifications_functions.pending_approval import pending_approval


def notifications_check(driver, module_name=None, test_case_id=None):
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
            return False
        

    wait_for_loader_to_disappear(driver, wait)

    # 🧩 Load first test case data

    # # ✅ Step 3: Create Task
    if module_name == 'add_task':
        test_case_details = pd.read_excel(os.path.join("data", "test_case_selector.xlsx"), sheet_name=f"{module_name}_test_cases").fillna("")
        # test_case_details = pd.read_excel(os.path.join("data", "test_case_selector.xlsx")).fillna("")
        first_row = test_case_details.iloc[0]
        task_name = first_row.get('task_name')
        start_date = format_date_if_valid(first_row.get('start_date'))
        due_date = format_date_if_valid(first_row.get('due_date'))
        frequency = first_row.get('frequency')
        repeat_if_holiday = first_row.get('repeat_if_holiday')
        end_freq_date = first_row.get('end_freq_date')
        repeat_weekday = first_row.get('repeat_weekday')
        repeat_day_month = first_row.get('repeat_day_month')
        # end_time = first_row.get('end_time')
        end_time = format_time_if_valid(first_row.get('end_time')) if pd.notna(first_row.get('end_time')) else None
        internal_deadline = first_row.get('internal_deadline')
        assign_to = first_row.get('assign_to')
        approver = first_row.get('approver')
        cc = first_row.get('cc')
        risk_rating = first_row.get('risk_rating')
        license_name = first_row.get('license_name')
        description = first_row.get('description')
        attach_file_name= first_row.get('attach_file_name')
        impact_details = first_row.get('impact_details')
        impact_file_name = first_row.get('impact_file_name')
        circular_search = first_row.get('circular_search')
        test_type = first_row.get('test_type')


        print(f"🧠 Running notification test for task: {task_name}")
        print(f"Assigned to: {assign_to} | Approver: {approver} | CC: {cc}")
        with allure.step("Add Task Check"):
            try:
                if add_task_check(driver, task_name, start_date, due_date, frequency, repeat_if_holiday, end_freq_date,
                    repeat_weekday, repeat_day_month, end_time, internal_deadline, assign_to, approver, cc,
                    risk_rating, license_name, description, attach_file_name, impact_details, impact_file_name,
                    circular_search, test_type, task_type='mandatory'):
                    print("✅ Task creation successful")
                    return True
                else:
                   allure.attach("Test case failed for Task Creation", name="Task Creation Validation Failed", attachment_type=allure.attachment_type.TEXT)
                   return False
            except Exception as e:
                allure.attach(str(e), name="Add Task Error", attachment_type=allure.attachment_type.TEXT)

    # Step 6: Assign task by Co
    if module_name == 'assign_task_by_co':
        with allure.step("Create a task without assignee, then assign it to a user"):
        # Step 1: Create a task without assigning to anyone
        # Step 2: After creation, assign the task to a user
            try:
                if assign_task_by_co(driver, wait):
                    print("✅ Assign task by Co successful")
                    return True
                else:
                    allure.attach("Test case failed for Assign Task By Co", name=" Assign Task By Co Validation Failed", attachment_type=allure.attachment_type.TEXT)
                    return False
            except Exception as e:
                allure.attach(str(e), name="Assign task by Co", attachment_type=allure.attachment_type.TEXT)

     # Step 6: Re_Assign task by Co
    if module_name == 'reassign_task_by_co':
        with allure.step("Create a task without assignee, then assign it to a user"):
        # Step 1: Create a task without assigning to anyone
        # Step 2: After creation, assign the task to a user
            try:
                if reassign_task_by_co(driver, wait):
                    print("✅ Assign task by Co successful")
                    return True
                else:
                    allure.attach("Test case failed for Reassign Task By Co", name="Reassign Task By Co Validation Failed", attachment_type=allure.attachment_type.TEXT)
                    return False
            except Exception as e:
                allure.attach(str(e), name="Assign task by Co", attachment_type=allure.attachment_type.TEXT)
    
    
    # # Step 7: Create individual task
    if module_name == 'create_individual_task':
        with allure.step("Create individual task"):
            try:
                if create_individual_task(driver, wait):
                    print("✅ Create individual task successful")
                    return True
                else:
                    allure.attach("Test case failed for Lower Dashboard", name="Lower Dashboard Validation Failed", attachment_type=allure.attachment_type.TEXT)
                    return False
            except Exception as e:
                allure.attach(str(e), name="Create individual task", attachment_type=allure.attachment_type.TEXT)
    
    # # Step 7: Create individual task
    if module_name == 'update_created_task':
        with allure.step("Create individual task"):
            try:
                if update_created_task(driver, wait):
                    print("✅ Create individual task successful")
                    return True
                else:
                    allure.attach("Test case failed for Lower Dashboard", name="Lower Dashboard Validation Failed", attachment_type=allure.attachment_type.TEXT)
                    return False
            except Exception as e:
                allure.attach(str(e), name="Create individual task", attachment_type=allure.attachment_type.TEXT)
    
    
    # # Step 8: Create Project
    if module_name == 'create_project':
        with allure.step("Create Project"):
            try:
                if create_project(driver, wait):
                    print("✅ Create Project successful")
                    return True
                else:
                    allure.attach("Test case failed for Create Project", name="Create Project Validation Failed", attachment_type=allure.attachment_type.TEXT)
                    return False
            except Exception as e:
                allure.attach(str(e), name="Create Project", attachment_type=allure.attachment_type.TEXT)
   
    # Step 9: Delete Tasks
    if module_name == 'delete_tasks':
        with allure.step("Delete Tasks"):
            try:
                if delete_tasks(driver, wait):
                    print("✅ Delete Tasks successful")
                    return True
                else:
                    allure.attach("Test case failed for Delete Tasks", name="Delete Tasks Validation Failed", attachment_type=allure.attachment_type.TEXT)
                    return False
            except Exception as e:
                allure.attach(str(e), name="Delete Tasks", attachment_type=allure.attachment_type.TEXT)
        
    
    # # Step 10: Edit Personal Detials
    if module_name == 'edit_personal_details':
        with allure.step("Edit Personal Detials"):
            try:
                if edit_personal_details(driver, wait):
                    print("✅ Edit Personal Detials successful")
                    return True
                else:
                    allure.attach("Test case failed for Edit Personal Detials", name="Edit Personal Detials Validation Failed", attachment_type=allure.attachment_type.TEXT)
                    return False
            except Exception as e:
                allure.attach(str(e), name="Edit Personal Detials", attachment_type=allure.attachment_type.TEXT)
    
     # # Step 10: Edit Personal Detials
    if module_name == 'company_details':
        with allure.step("Edit Personal Detials"):
            try:
                if create_company(driver, wait):
                    print("✅ Edit Personal Detials successful")
                    return True
                else:
                    allure.attach("Test case failed for Edit Personal Detials", name="Edit Personal Detials Validation Failed", attachment_type=allure.attachment_type.TEXT)
                    return False
            except Exception as e:
                allure.attach(str(e), name="Edit Personal Detials", attachment_type=allure.attachment_type.TEXT)
   
    # # Step 12: Reject Task by CO
    if module_name == 'reject_task_by_co':
        with allure.step("Reject Task by CO"):
            try:
                if task_approved_by_approver(driver, wait):
                    print("✅ Reject Task successful")
                    return True
                else:
                    allure.attach("Test case failed for Lower Dashboard", name="Lower Dashboard Validation Failed", attachment_type=allure.attachment_type.TEXT)
                    return False
            except Exception as e:
                allure.attach(str(e), name="Reject Task Detials", attachment_type=allure.attachment_type.TEXT)
    
    # Step 13: Bulk Task Not Assigned to Team Member
    if module_name == 'bulk_task_not_assigned_to_team_member':
        with allure.step("Bulk Task Not Assigned to Team Member"):
            try:
                if  bulk_task_not_assigned(driver, wait):
                    print("✅ Bulk Task Not Assigned to Team Member successful")
                    return True
                else:
                    allure.attach("Test case failed for Lower Dashboard", name="Lower Dashboard Validation Failed", attachment_type=allure.attachment_type.TEXT)
                    return False
            except Exception as e:
                allure.attach(str(e), name="Bulk Task Not Assigned to Team Member Detials", attachment_type=allure.attachment_type.TEXT)
   
    # # Step 14: Reference Added
    if module_name == 'reference_added':
        with allure.step("Reference added"):
            try:
                if reference_added_by_co(driver, wait):
                    print("✅ Reference Added successful")
                    return True
                else:
                    allure.attach("Test case failed for Lower Dashboard", name="Lower Dashboard Validation Failed", attachment_type=allure.attachment_type.TEXT)
                    return False
            except Exception as e:
                allure.attach(str(e), name=" Reference Added Detials", attachment_type=allure.attachment_type.TEXT)
   
    # Step 15: Task completed by the team member and pendig for approval
    if module_name == 'pending_approval':
        with allure.step("Task completed by the team member and pendig for approval"):
            try:
                if pending_approval(driver, wait):
                    print("✅ Task completed successfully")
                    return True
                else:
                    allure.attach("Test case failed for Bulk Action", name="Bulk Action Validation Failed", attachment_type=allure.attachment_type.TEXT)
                    return False
            except Exception as e:
                allure.attach(str(e), name="Mark completed Detials", attachment_type=allure.attachment_type.TEXT)
   
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


    