import allure
import pandas as pd
import os
import json
import pytest

from utilities.login_utils import login_check
from utilities.add_task_functions.wait_for_loader_to_disappear import wait_for_loader_to_disappear
from selenium.webdriver.support.ui import WebDriverWait
from load_test_config_excel_data import load_test_config_excel_data
from utilities.project_functions.add_project import create_project
from utilities.project_functions.add_milestone import create_milestone
from utilities.project_functions.add_task_list import create_task_list
from utilities.project_functions.add_coowner import add_coowner
from utilities.project_functions.create_project_task import create_project_task
from utilities.project_functions.create_milestone_task import create_milestone_task
from utilities.project_functions.create_task_list_task import create_task_list_task
from utilities.project_functions.project_task_restore_delete import project_task_restore_delete
from utilities.project_functions.project_restore_delete import project_restore_delete
from utilities.project_functions.task_list_delete import task_list_delete
from utilities.project_functions.milestone_delete import milestone_delete
from utilities.project_functions.project_filter import project_filter
from utilities.project_functions.project_column_chooser import project_column_chooser_validation
from utilities.project_functions.project_export import project_export_all_data
from utilities.project_functions.project_search_name import project_search_name
from utilities.project_functions.project_graph_filter import graph_filter


def create_project_check(driver, module_name=None, test_case_id=None, test_type=None, task_details=None):
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

    if module_name == 'create_project' and task_details:
        project_name = task_details.get("project_name")
        project_description = task_details.get("project_description")

        with allure.step("Create Project"):
            try:
                if create_project(driver, wait, project_name, project_description):
                    print("✅ Create Project successful")
                    return True
                else:
                    allure.attach("Test case failed for Create Project",name="Create Project Validation Failed",attachment_type=allure.attachment_type.TEXT)
                    return False
            except Exception as e:
                 allure.attach(str(e), name="Delete Task and Restore", attachment_type=allure.attachment_type.TEXT)
    if module_name == 'project_filter':

        with allure.step("Project Filter"):
            try:
                if project_filter(driver, wait):
                    print("✅ Project Filter successful")
                    return True
                else:
                    allure.attach("Test case failed for Project Filter",name="Project Filter Validation Failed",attachment_type=allure.attachment_type.TEXT)
                    return False
            except Exception as e:
                allure.attach(str(e), name="Delete Task and Restore", attachment_type=allure.attachment_type.TEXT)
    if module_name == 'project_column_chooser':

        with allure.step("Project Column Chooser"):
            try:
                if project_column_chooser_validation(driver, wait):
                    print("✅ Project Column Chooser successful")
                    return True
                else:
                    allure.attach("Test case failed for Project Column Chooser",name="Project Column Chooser Validation Failed",attachment_type=allure.attachment_type.TEXT)
                    return False
            except Exception as e:
                allure.attach(str(e), name="Delete Task and Restore", attachment_type=allure.attachment_type.TEXT)
    
    if module_name == 'project_export_all_data':

        with allure.step("Project Export All Data"):
            try:
                if project_export_all_data(driver, wait):
                    print("✅ Project Export All Data successful")
                    return True
                else:
                    allure.attach("Test case failed for Project Export All Data",name="Project Export All Data Validation Failed",attachment_type=allure.attachment_type.TEXT)
                    return False
            except Exception as e:
                allure.attach(str(e), name="Delete Task and Restore", attachment_type=allure.attachment_type.TEXT)
    
    if module_name == 'project_search_name':
        
        with allure.step("Project Search by Name"):
            try:
                if project_search_name(driver, wait):
                    print("✅ Project Search by Name successful")
                    return True
                else:
                    allure.attach("Test case failed for Project Search by Name",name="Project Search by Name Validation Failed",attachment_type=allure.attachment_type.TEXT)
                    return False
            except Exception as e:
                allure.attach(str(e), name="Delete Task and Restore", attachment_type=allure.attachment_type.TEXT)
    if module_name == 'project_graph_filter':
        
        with allure.step("Project Graph Filter"):
            try:
                if graph_filter(driver, wait):
                    print("✅ Project Graph Filter successful")
                    return True
                else:
                    allure.attach("Test case failed for Project Graph Filter",name="Project Graph Filter Validation Failed",attachment_type=allure.attachment_type.TEXT)
                    return False
            except Exception as e:
                allure.attach(str(e), name="Delete Task and Restore", attachment_type=allure.attachment_type.TEXT)
                  
                  

    if module_name == 'create_milestone' and task_details:
        project_name = task_details.get("project_name")
        milestone = task_details.get("milestone")

        with allure.step("Create Milestone"):
            try:
                if create_milestone(driver, wait, project_name, milestone):
                    print("✅ Create Milestone successful")
                    return True
                else:
                    allure.attach("Test case failed for Create Milestone",name="Create Milestone Validation Failed",attachment_type=allure.attachment_type.TEXT)
                    return False
            except Exception as e:
                allure.attach(str(e), name="Delete Task and Restore", attachment_type=allure.attachment_type.TEXT)
    if module_name == 'create_task_list' and task_details:
        project_name = task_details.get("project_name")
        milestone = task_details.get("milestone")
        task_list = task_details.get("task_list")
        with allure.step("Create Task List"):
            try:
                if create_task_list(driver, wait, project_name, milestone, task_list):
                    print("✅ Create Task List successful")
                    return True
                else:
                    allure.attach("Test case failed for Create Task List",name="Create Task List Validation Failed",attachment_type=allure.attachment_type.TEXT)
                    return False
            except Exception as e:
                allure.attach(str(e), name="Delete Task and Restore", attachment_type=allure.attachment_type.TEXT)
    if module_name == 'add_coowner' and task_details:
        coowner_name = task_details.get("coowner_name")
        project_name = task_details.get("project_name")
        with allure.step("Add Co-owner"):
            try:
                if add_coowner(driver, wait, project_name, coowner_name):
                    print("✅ Add Co-owner successful")
                    return True
                else:
                    allure.attach("Test case failed for Add Co-owner",name="Add Co-owner Validation Failed",attachment_type=allure.attachment_type.TEXT)
                    return False
            except Exception as e:
                allure.attach(str(e), name="Delete Task and Restore", attachment_type=allure.attachment_type.TEXT)
    if module_name == 'create_project_task' and task_details:
        project_name = task_details.get("project_name")
        project_task_name = task_details.get("project_task_name")

        print("📌 Data from Excel JSON:", task_details)

        with allure.step("Create Project Task"):
            
            try:
                if create_project_task(driver, wait, project_name, project_task_name):
                    print("✅ Create Project successful")
                    return True
                else:
                    allure.attach("Test case failed for Create Project",name="Create project Validation Failed",attachment_type=allure.attachment_type.TEXT)
                    return False
            except Exception as e:
                allure.attach(str(e), name="Delete Task and Restore", attachment_type=allure.attachment_type.TEXT)
                
    if module_name == 'create_milestone_task_list' and task_details:
        milestone_task_name = task_details.get("milestone_task_name")
        milestone = task_details.get("milestone")
        project_name = task_details.get("project_name")

        print("📌 Data from Excel JSON:", task_details)

        with allure.step("Create Milestone"):
            
            try:
                if create_milestone_task(driver, wait, project_name, milestone, milestone_task_name):
                    print("✅ Create Milestone Task successful")
                    return True
                else:
                    allure.attach("Test case failed for Invite Team Member",name="Invite Team Member Validation Failed",attachment_type=allure.attachment_type.TEXT)
                    return False
            except Exception as e:
                allure.attach(str(e), name="Delete Task and Restore", attachment_type=allure.attachment_type.TEXT)
                 
    if module_name == 'create_task_list_task' and task_details:
        project_name = task_details.get("project_name")
        milestone = task_details.get("milestone")
        task_list = task_details.get("task_list")
        task_list_task_name = task_details.get("task_list_task_name")
        print("📌 Data from Excel JSON:", task_details)
        with allure.step("Create Task from task list"):
            
            try:
                if create_task_list_task(driver, wait, project_name, milestone, task_list, task_list_task_name):
                    print("✅ Create Task from task list successful")
                    return True
                else:
                    allure.attach("Test case failed for Create Task from task list",name="Create Task from task list ListValidation Failed",attachment_type=allure.attachment_type.TEXT)
                    return False
            except Exception as e:
                allure.attach(str(e), name="Delete Task and Restore", attachment_type=allure.attachment_type.TEXT)
    if module_name == 'project_task_restore_delete':
        project_name = task_details.get("project_name")
        with allure.step("Delete Task and Restore"):
            
            try:
                if project_task_restore_delete(driver, wait, project_name):
                    print("✅ Delete Task and Restore successful")
                    return True
                else:
                    allure.attach("Test case failed for Lower Dashboard", name="Lower Dashboard Validation Delete Task and Restore Failed", attachment_type=allure.attachment_type.TEXT)
                    return False
            except Exception as e:
                allure.attach(str(e), name="Delete Task and Restore", attachment_type=allure.attachment_type.TEXT)
    
    if module_name == 'task_list_delete':
        project_name = task_details.get("project_name")
        milestone = task_details.get("milestone")
        task_list = task_details.get("task_list")
        with allure.step("Delete Task list and Restore"):
            
            try:
                if task_list_delete(driver, wait, project_name, milestone, task_list):
                    print("✅Delete Task list and Restore successful")
                    return True
                else:
                    allure.attach("Test case failed for Delete Task list and Restore", name="Delete Task list and Restore Failed", attachment_type=allure.attachment_type.TEXT)
                    return False
            except Exception as e:
                allure.attach(str(e), name="Delete Task list and Restore", attachment_type=allure.attachment_type.TEXT)
    
    if module_name == 'milestone_delete':
        project_name = task_details.get("project_name")
        milestone = task_details.get("milestone")
        with allure.step("Delete Milestone and Restore"): 
            try:
                if milestone_delete(driver, wait, project_name, milestone):
                    print("✅ Delete Milestone and Restore successful")
                    return True
                else:
                    allure.attach("Test case failed for Delete Milestone and Restore", name="Delete Milestone and Restore Failed", attachment_type=allure.attachment_type.TEXT)
                    return False
            except Exception as e:
                allure.attach(str(e), name="Delete Milestone and Restore", attachment_type=allure.attachment_type.TEXT)
     
 
    if module_name == 'project_restore_delete':
        project_name = task_details.get("project_name")
       
        with allure.step("Delete Project and Restore"):     
            try:
                if project_restore_delete(driver, wait, project_name):
                    print("✅ Delete Project and Restore successful")
                    return True
                else:
                    allure.attach("Test case failed for Delete Project and Restore", name="Delete Project and Restore Failed", attachment_type=allure.attachment_type.TEXT)
                    return False
            except Exception as e:
                allure.attach(str(e), name="Delete Project and Restore ", attachment_type=allure.attachment_type.TEXT)
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
