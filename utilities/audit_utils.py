import allure
import pandas as pd
import os
import json
import pytest
import allure
from utilities.login_utils import login_check
from utilities.add_task_functions.wait_for_loader_to_disappear import wait_for_loader_to_disappear
from selenium.webdriver.support.ui import WebDriverWait
from load_test_config_excel_data import load_test_config_excel_data
from utilities.audit_company_functions.audit_company import AuditCompanyTask
from utilities.audit_company_functions.new_branch import AuditBranchTask
from utilities.audit_company_functions.export_data import ExportData
from utilities.audit_company_functions.search_company_name import SearchCompanyTask
from utilities.audit_company_functions.view_company import ViewColumnHeaders
from utilities.audit_template_functions.create_template import CreateTemplate
from utilities.audit_template_functions.search_template import SearchTemplateTask
from utilities.audit_template_functions.template_export_data import CustomExportData
from utilities.audit_template_functions.custom_view import CustomViewColumnHeaders
from utilities.audit_template_functions.create_audit_assignment import CreateAssignment
from utilities.audit_company_functions.edit_company import EditCompanyTask
from utilities.audit_assignment_functions.search_assignment import SearchAssignmentTask
from utilities.audit_assignment_functions.assignment_export import AssignExportData
from utilities.audit_assignment_functions.view_assign import AssignViewColumnHeaders
from utilities.audit_template_functions.edit_template import EditTemplate
from utilities.audit_template_functions.add_questionnaire import CreateQuestionnaire
def audit_check(driver, module_name=None, task_details=None):
    wait = WebDriverWait(driver, 30)

    # driver.get("http://192.168.30.11:8081/login")
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
            # allure.attach("Login failed", name="Login Timeout", attachment_type=allure.attachment_type.TEXT)
            allure.attach(str(e), name="Delete Task and Restore", attachment_type=allure.attachment_type.TEXT)

    wait_for_loader_to_disappear(driver, wait)
   

    if module_name == 'audit_company':
        email_id = task_details.get("email_id")

        with allure.step("Verify Audit Company"):
            try:
                audit_company_task = AuditCompanyTask(driver, wait, email_id)
                if audit_company_task.audit_company():
                    print("✅ Audit company details successful")
                    return True
                else:
                    allure.attach("Test case failed for Audit Company details",name="Audit Company details Validation Failed",attachment_type=allure.attachment_type.TEXT)
                    return False
            except Exception as e:
                 allure.attach(str(e), name="Audit Company details", attachment_type=allure.attachment_type.TEXT)

    if module_name == 'audit_branch':
        with allure.step("Verify Audit Branch"):
            try:
                audit_branch_task = AuditBranchTask(driver, wait)
                if audit_branch_task.audit_branch():
                    print("✅ Audit Branch details successful")
                    return True
                else:
                    allure.attach("Test case failed for Audit Branch details",name="Audit Branch details Validation Failed",attachment_type=allure.attachment_type.TEXT)
                    return False
            except Exception as e:
                    allure.attach(str(e), name="Audit Branch details", attachment_type=allure.attachment_type.TEXT)

    if module_name == 'company_export_data':
        with allure.step("Verify Export Data"):
            try:
                company_export = ExportData(driver, wait)
                if company_export.export_data():
                    print("✅ Export data details successful")
                    return True
                else:
                    allure.attach("Test case failed for Export data details",name="Export data details Validation Failed",attachment_type=allure.attachment_type.TEXT)
                    return False
            except Exception as e:
                    allure.attach(str(e), name="Export data details", attachment_type=allure.attachment_type.TEXT)


    if module_name == 'search_company_name':
        with allure.step("Verify Search Company name"):
            try:
                search_company_task = SearchCompanyTask(driver, wait)
                if search_company_task.search_company_name():
                    print("✅ Search company name successful")
                    return True
                else:
                    allure.attach("Test case failed for Search company name",name="Search company name Validation Failed",attachment_type=allure.attachment_type.TEXT)
                    return False
            except Exception as e:
                    allure.attach(str(e), name="Search company name", attachment_type=allure.attachment_type.TEXT)

    if module_name == 'view_column_headers':
        with allure.step("Verify Column Headers"):
            try:
                view_column_header = ViewColumnHeaders(driver, wait)
                if view_column_header.view_column_headers():
                    print("✅ View column headers name successful")
                    return True
                else:
                    allure.attach("Test case failed for View column headers",name="View column headers name Validation Failed",attachment_type=allure.attachment_type.TEXT)
                    return False
            except Exception as e:
                    allure.attach(str(e), name="View column headers name", attachment_type=allure.attachment_type.TEXT)
    if module_name == "create_template":
        with allure.step("Create Template"):
            try:
                create_template_task = CreateTemplate(driver, wait)
                if create_template_task.create_template():
                    print("✅ Create Template successful")
                    return True
                else:
                    allure.attach("Test case failed for Create Template",name="Create Template Validation Failed",attachment_type=allure.attachment_type.TEXT)
                    return False

            except Exception as e:
                allure.attach(str(e),name="Create Template Error",attachment_type=allure.attachment_type.TEXT)
                return False

    if module_name == 'search_template_name':
        with allure.step("Verify Search Template name"):
            try:
                search_template_task = SearchTemplateTask(driver, wait)
                if search_template_task.search_template_name():
                    print("✅ Search template name successful")
                    return True
                else:
                    allure.attach("Test case failed for Search template name",name="Search company name Validation Failed",attachment_type=allure.attachment_type.TEXT)
                    return False
            except Exception as e:
                    allure.attach(str(e), name="Search template name", attachment_type=allure.attachment_type.TEXT)

    if module_name == 'custom_export_data':
        with allure.step("Export Custom Export Data"):
            try:
                custom_export = CustomExportData(driver, wait)
                if custom_export.custom_export_data():
                    print("✅ Search template name successful")
                    return True
                else:
                    allure.attach("Test case failed for Search template name",name="Search company name Validation Failed",attachment_type=allure.attachment_type.TEXT)
                    return False
            except Exception as e:
                    allure.attach(str(e), name="Search template name", attachment_type=allure.attachment_type.TEXT)

    if module_name == 'custom_view_column_headers':
        with allure.step("Verify Column Headers"):
            try:
                custom_view_column_header = CustomViewColumnHeaders(driver, wait)
                if custom_view_column_header.custom_view_column_headers():
                    print("✅ View column headers name successful")
                    return True
                else:
                    allure.attach("Test case failed for View column headers",name="View column headers name Validation Failed",attachment_type=allure.attachment_type.TEXT)
                    return False
            except Exception as e:
                    allure.attach(str(e), name="View column headers name", attachment_type=allure.attachment_type.TEXT)

    if module_name == 'create_assignment':
        with allure.step("Verify Assignment"):
            try:
                create_assignment = CreateAssignment(driver, wait)
                if create_assignment.create_audit_assignment():
                    print("Create Assignment successful")
                    return True
                else:
                    allure.attach("Test case failed for Create Assignment",name="Create Assignment Validation Failed",attachment_type=allure.attachment_type.TEXT)
                    return False
            except Exception as e:
                    allure.attach(str(e), name="Create Assignment", attachment_type=allure.attachment_type.TEXT)

    if module_name == 'edit_company_name':
        with allure.step("Verify Edit Company"):
            try:
                edit_company_name = EditCompanyTask(driver, wait)
                if edit_company_name.edit_company():
                    print("Edit Company name successful")
                    return True
                else:
                    allure.attach("Test case failed for edit company",name="Edit Company name Validation Failed",attachment_type=allure.attachment_type.TEXT)
                    return False
            except Exception as e:
                    allure.attach(str(e), name="Edit Company name", attachment_type=allure.attachment_type.TEXT)

    if module_name == 'assignment_name':
        with allure.step("Verify Assignment"):
            try:
                assignment_task = SearchAssignmentTask(driver, wait)
                if assignment_task.assigment_name():
                    print("Assignment successful")
                    return True
                else:
                    allure.attach("Test case failed for ",name="Edit Company name Validation Failed",attachment_type=allure.attachment_type.TEXT)
                    return False
            except Exception as e:
                    allure.attach(str(e), name="Edit Company name", attachment_type=allure.attachment_type.TEXT)

    if module_name == 'assign_export_data':
        with allure.step("Verify Assign Export Data"):
            try:
                assign_export = AssignExportData(driver, wait)
                if assign_export.assign_export_data():
                    print("Assign Export data details successful")
                    return True
                else:
                    allure.attach("Test case failed for Assign Export data details",name="Assign Export data details Validation Failed",attachment_type=allure.attachment_type.TEXT)
                    return False
            except Exception as e:
                    allure.attach(str(e), name="Assign Export data details", attachment_type=allure.attachment_type.TEXT)

    if module_name == 'assign_view_column_headers':
        with allure.step("Verify Column Headers"):
            try:
                assign_view_column_header = AssignViewColumnHeaders(driver, wait)
                if assign_view_column_header.assing_view_column_headers():
                    print("✅ View column headers name successful")
                    return True
                else:
                    allure.attach("Test case failed for View column headers",name="View column headers name Validation Failed",attachment_type=allure.attachment_type.TEXT)
                    return False
            except Exception as e:
                    allure.attach(str(e), name="View column headers name", attachment_type=allure.attachment_type.TEXT)
    
    if module_name == 'edit_inside_template':
        with allure.step("Verify Edit Inside Template"):
            try:
                edit_inside_template = EditTemplate(driver, wait)
                if edit_inside_template.edit_inside_template_name():
                    print("✅ View Edit Template successful")
                    return True
                else:
                    allure.attach("Test case failed for Edit Template",name="Edit Template Validation Failed",attachment_type=allure.attachment_type.TEXT)
                    return False
            except Exception as e:
                    allure.attach(str(e), name="Edit Template name", attachment_type=allure.attachment_type.TEXT)

    if module_name == 'add_questionnaire':
        with allure.step("Verify Questionnaire"):
            try:
                create_add_questionnaire = CreateQuestionnaire(driver, wait)
                if create_add_questionnaire.add_questionnaire():
                    print("✅ View Creating Questionnaire successful")
                    return True
                else:
                    allure.attach("Test case failed for Creating Questionnaire",name="Creating Questionnaire Validation Failed",attachment_type=allure.attachment_type.TEXT)
                    return False
            except Exception as e:
                    allure.attach(str(e), name="Creating Questionnaire", attachment_type=allure.attachment_type.TEXT)

            
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
