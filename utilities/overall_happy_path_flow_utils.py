# login_utils.py
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import pandas as pd
import pytest
import logging
import allure
import time
import json
import os

from utilities.login_utils import login_check
from load_test_config_excel_data import load_test_config_excel_data
from utilities.settings_functions.company_details import company_details
from utilities.settings_functions.license_task import license_task
from utilities.dashboard_graph_functions.normal_task_valid_details import normal_task_valid_details
from utilities.dashboard_graph_functions.special_task_valid_details import special_task_valid_details
from utilities.settings_functions.task_category import task_category
from utilities.updates_functions.add_task_updates import updates_add_task
from utilities.project_functions.add_project import create_project
from utilities.project_functions.add_milestone import create_milestone
from utilities.project_functions.add_task_list import create_task_list
from utilities.project_functions.add_coowner import add_coowner
from utilities.project_functions.create_project_task import create_project_task
from utilities.project_functions.create_task_list_task import create_task_list_task
from utilities.project_functions.create_milestone_task import create_milestone_task
from utilities.project_functions.project_task_restore_delete import project_task_restore_delete
from utilities.project_functions.project_restore_delete import project_restore_delete
from utilities.project_functions.task_list_delete import task_list_delete
from utilities.project_functions.milestone_delete import milestone_delete
from utilities.settings_functions.personal_details import personal_details
from utilities.settings_functions.create_department import create_department
from utilities.settings_functions.create_designation import create_designation
from utilities.settings_functions.team_members import invite_team_member
from utilities.settings_functions.mark_circular_as_na import mark_circular_as_na


def overall_happy_path_check(driver, task_details):
    wait = WebDriverWait(driver=driver, timeout=15)
    task_name = task_details.get("task_name")
    with allure.step("Login"):
        username = task_details["username"]
        password = task_details["password"]
        login_check_success = login_check(driver, waittime=10, trial=1, username=username, password=password)
        time.sleep(2)
        if login_check_success:
            allure.attach("Login successful", name="Login Status", attachment_type=allure.attachment_type.TEXT)
        else:
            allure.attach("Login failed", name="Login Status", attachment_type=allure.attachment_type.TEXT)
            return False
    with allure.step("Company Creation"):
        company_name = task_details.get("company_name")
        company_add_success = company_details(driver, wait, company_name)

        if company_add_success:
            allure.attach("Company add successful", name="Company Creation", attachment_type=allure.attachment_type.TEXT)
        else:
            allure.attach("Company Creation failed", name="Company Creation", attachment_type=allure.attachment_type.TEXT)
            return False
    
    # with allure.step("Create Department Details"):
    #     company_name =  task_details.get("company_name")
    #     department_name = task_details.get("department_name")
    #     hod_name = task_details.get("hod_name")
    #     alias =  task_details.get("department_alias")
    #     description =  task_details.get("description")
    #     if create_department(driver, wait, company_name, department_name, hod_name, alias,  description):
    #         print("✅ Create Department Detials successful")
    #         # return True
    #     else:
    #         allure.attach("Test case failed for Create Department Detials", name="Create Department Detials Validation Failed", attachment_type=allure.attachment_type.TEXT)
    #         return False
    
    # with allure.step("Create Designation Details"):
    #     # department_name = task_details.get("department_name")
    #     designation_name = task_details.get("designation_name")
    #     alias = task_details.get("designation_alias")
    #     description = task_details.get("description")
    #     if create_designation(driver,wait, designation_name, alias, description):
    #         print("✅ Create Designation Details successful")
    #         # return True
    #     else: 
    #         allure.attach("Test case failed for Create Designation Details",name="Create Designation Details Validation Failed",attachment_type=allure.attachment_type.TEXT)
    #         return False
    # with allure.step("Invite Team Member"):
    #     full_name = task_details.get("full_name")
    #     email = task_details.get("email")
    #     role = task_details.get("role")
    #     department_name = task_details.get("department_name")
    #     designation_name = task_details.get("designation_name")
    #     full_name_2 = task_details.get("full_name_2")
    #     email_2 = task_details.get("email_2")

    #     if invite_team_member(driver, wait, full_name, email, role, department_name, designation_name, full_name_2, email_2,):
    #         allure.attach("Invite Team Member successful", name="Invite Team Member", attachment_type=allure.attachment_type.TEXT)
    #     else:
    #         allure.attach("Invite Team Member failed", name="Invite Team Member", attachment_type=allure.attachment_type.TEXT)
    #         return False 
    
    # with allure.step("Check License task"):
    #     company_name = task_details.get("company_name")
    #     license_name =  task_details.get("license_name")

    #     if license_task(driver, wait, company_name, license_name):
    #         print("✅ Check License task successful")
    #         # return True
    #     else:
    #         allure.attach("Test case failed for Check License task", name="Check License task Validation Failed", attachment_type=allure.attachment_type.TEXT)
    #         return False
    with allure.step("Create Normal Task"):
        normal_task = task_details.get("normal_task")
        if normal_task_valid_details(driver, wait, normal_task):
            print("✅ Create Normal Task validation successful")
            # return True
        else:
            allure.attach("Test case failed for Create Normal Task", name="Create Normal Task Failed", attachment_type=allure.attachment_type.TEXT)
            return False
    with allure.step("Create Task Category"):
        category_name = task_details.get("category_name")
        category_desc= task_details.get("category_desc")
    
        if task_category(driver, wait, category_name, category_desc):
            print("✅ Create Task Category successful")
            # return True
        else:
            allure.attach("Test case failed for Create Task Category",name="Create Task Category Validation Failed",attachment_type=allure.attachment_type.TEXT)
            return False
    with allure.step("Create Special Task functionality"):
        special_task = task_details.get("special_task")
        if special_task_valid_details(driver, wait, special_task):
            print("✅Create Special Task  successful")
            # return True
        else:
            allure.attach("Test case failed for Create Special Task ", name="Create Special Task  Failed", attachment_type=allure.attachment_type.TEXT)
            return False
   
    with allure.step("Create a Task from Updates"):
        updates_task_name = task_details.get("updates_task_name")
        if updates_add_task(driver, wait, updates_task_name):
            print("✅ Create a Task from Updates successful")
        else:
            allure.attach("Test case failed for Create a Task from Update ", name="Create a Task from Update  Failed", attachment_type=allure.attachment_type.TEXT)
            return False
        
    with allure.step("Create Project"):
        project_name = task_details.get("project_name")
        project_description = task_details.get("project_description")
        if create_project(driver, wait, project_name, project_description):
            print("✅ Create Project successful")
            # return True
        else:
            allure.attach("Test case failed for Create Project",name="Create Project Validation Failed",attachment_type=allure.attachment_type.TEXT)
            return False
         
    with allure.step("Create Milestone"):
        milestone = task_details.get("milestone")
        if create_milestone(driver, wait, milestone):
            print("✅ Create Milestone successful")
            # return True
        else:
            allure.attach("Test case failed for Create Milestone",name="Create Milestone Validation Failed",attachment_type=allure.attachment_type.TEXT)
            return False
         
    with allure.step("Create Task List"):
        task_list = task_details.get("task_list")
        if create_task_list(driver, wait, task_list):
            print("✅ Create Project successful")
            # return True
        else:
            allure.attach("Test case failed for Create Project",name="Create Project Validation Failed",attachment_type=allure.attachment_type.TEXT)
            return False
    with allure.step("Create Project Task"):
        project_task_name = task_details.get("project_task_name")
        if create_project_task(driver, wait, project_task_name):
            print("✅ Create Project successful")
        else:
            allure.attach("Test case failed for Create Project",name="Create Project Validation Failed",attachment_type=allure.attachment_type.TEXT)
            return False         
    
    with allure.step("Add Co-owner"):
        coowner_name = task_details.get("coowner_name")  
        if add_coowner(driver, wait, coowner_name):
            print("✅ Add Co-owner successful")
            # return True
        else:
            allure.attach("Test case failed for Add Co-owner",name="Add Co-owner Validation Failed",attachment_type=allure.attachment_type.TEXT)
            return False
           
    with allure.step("Create Milestone Task"):
        milestone_task_name = task_details.get("milestone_task_name")
        if create_milestone_task(driver, wait, milestone_task_name):
            print("✅ Create Milestone Task successful")
            # return True
        else:
            allure.attach("Test case failed for Create Milestone Task",name="Create Milestone Task Validation Failed",attachment_type=allure.attachment_type.TEXT)
            return False
        
    with allure.step("Create Task List"):
        task_list_task_name = task_details.get("task_list_task_name")
    
        if create_task_list_task(driver, wait, task_list_task_name):
            print("✅ Create Task List successful")
            # return True
        else:
            allure.attach("Test case failed for Create Task List",name="Create Task List Validation Failed",attachment_type=allure.attachment_type.TEXT)
            return False

    with allure.step("Delete Task and Restore"):
        if project_task_restore_delete(driver, wait):
            print("✅ Delete Task and Restore successful")
            # return True
        else:
            allure.attach("Test case failed for Delete Task and Restore", name="Delete Task and Restore Validation Failed", attachment_type=allure.attachment_type.TEXT)
            return False
    
      
    with allure.step("Delete Task list and Restore"):
        if task_list_delete(driver, wait):
            print("✅ Delete Task list and Restore successful")
            # return True
        else:
            allure.attach("Test case failed for Delete Task list and Restore", name="Delete Task list and Restore Failed", attachment_type=allure.attachment_type.TEXT)
            return False
    
    with allure.step("Delete Milestone and Restore"):
        if milestone_delete(driver, wait):
            print("✅ Delete Milestone and Restore successful")
            # return True
        else:
            allure.attach("Test case failed for Delete Milestone and Restore", name="Delete Milestone and Restore Failed", attachment_type=allure.attachment_type.TEXT)
            return False
    with allure.step("Delete Project and Restore"):
        if project_restore_delete(driver, wait):
            print("✅ Delete Project and Restore successful")
            # return True
        else:
            allure.attach("Test case failed for Delete Project and Restore", name="Delete Project and Restore Failed", attachment_type=allure.attachment_type.TEXT)
            return False
           
    with allure.step("Edit Personal Detials"):
        if personal_details(driver, wait):
            print("✅ Edit Personal Detials successful")
            # return True
        else:
            allure.attach("Test case failed for Edit Personal Detials", name="Edit Personal Detials Validation Failed", attachment_type=allure.attachment_type.TEXT)
            return False

    with allure.step("Click Not Applicable"):
        company_name = task_details.get("company_name")
        license_name = task_details.get("license_name")
        if mark_circular_as_na(driver, wait, company_name, license_name):
            print("✅ Click Not Applicable successful")
            # return True
        else:
            allure.attach("Test case failed for Click Not Applicable", name="Click Not Applicable Validation Failed", attachment_type=allure.attachment_type.TEXT)
            return False
        
def get_test_case_list(module=None):
    try:
        config = load_test_config_excel_data()
        print(f'Configurations: {config}')
        if not config:
            pytest.fail("test_case_selector.xlsx file not found")

        test_case_details = pd.read_excel(
            os.path.join("data", "test_case_selector.xlsx"),
            sheet_name=f"{module}"
        ).fillna("")

        task_details = dict(zip(test_case_details["fields"], test_case_details["values"]))

        print(task_details)

        if not task_details:
            pytest.skip("No test cases matched the selected criteria", allow_module_level=True)

        return [task_details]

    except FileNotFoundError:
        pytest.fail("test_case_selector.xlsx file not found")
    except Exception as e:
        pytest.fail(f"Error reading test cases: {str(e)}")

