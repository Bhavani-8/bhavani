import allure
import pytest
from utilities.bulk_actions_functions.assign_to import assign_to_bulk_action
from utilities.bulk_actions_negative_functions.assign_to_negative import assign_to_negative
from utilities.bulk_actions_functions.add_approver import approver_bulk_action
from utilities.bulk_actions_negative_functions.approver_negative import approver_negative
from utilities.bulk_actions_functions.cc import cc_bulk_action
from utilities.bulk_actions_negative_functions.cc_negative import cc_negative
from utilities.bulk_actions_functions.comment_bulk import comment_bulk_action
from utilities.bulk_actions_negative_functions.comment_negative import comment_negative
from utilities.bulk_actions_functions.upload_file import upload_file_bulk_action
from utilities.bulk_actions_negative_functions.upload_file_negative import upload_file_negative
from utilities.bulk_actions_functions.update_due_date import update_due_date_bulk_action
from utilities.bulk_actions_negative_functions.update_due_date_negative import update_due_date_negative
from utilities.bulk_actions_functions.mark_complete import mark_complete_bulk_action
from utilities.bulk_actions_negative_functions.mark_complete_negative import mark_complete_negative
from utilities.bulk_actions_functions.approval_pending_complied import approval_complied_bulk_action
from utilities.bulk_actions_functions.approval_pending_not_complied import approval_not_complied_bulk_action
from utilities.bulk_actions_functions.rejected_complied import rejected_complied_bulk_action
from utilities.bulk_actions_functions.rejected_not_complied import rejected_not_complied_bulk_action
from utilities.bulk_actions_functions.approval_pending_approve_task import approve_bulk_action
from utilities.bulk_actions_functions.approval_pending_reject_task import reject_bulk_action
from utilities.bulk_actions_functions.rejected_task import rejected_bulk_action
from utilities.bulk_actions_functions.completed_task import completed_task_bulk_action
from utilities.search_utils import clear_search

def bulk_actions_module(driver, wait, module_name=None, dash_type='QCC', test_case_id=None, task_name=None):  
    if module_name == 'assign_to_bulk_action':
        with allure.step("Verify 'Assign To' bulk action functionality"):
            try:
                if assign_to_bulk_action(driver, wait, dash_type):
                    print("✅ Assign To bulk action validation successful")
                    return True
                else:
                    allure.attach("Test case failed for Assign To Bulk Action", name=" assign_to_bulk_action Failed", attachment_type=allure.attachment_type.TEXT)
                    return False
            except Exception as e:
                allure.attach(str(e), name="Bulk Action Error", attachment_type=allure.attachment_type.TEXT)

    if module_name == 'assign_to_bulk_action_negative':
        with allure.step("Verify 'Assign To' bulk action negative functionality"):
            try:
                if assign_to_negative(driver, wait, dash_type):
                    print("✅ Negative scenario validated successfully")
                    return True
                else:
                    allure.attach("Test case failed for Bulk Action", name=" assign_to_bulk_action Failed", attachment_type=allure.attachment_type.TEXT)
                    return False
            except Exception as e:
                allure.attach(str(e), name="Bulk Action Error", attachment_type=allure.attachment_type.TEXT)

    if module_name == 'add_approver_bulk_action':
        with allure.step("Verify 'Approver' bulk action functionality"):
            try:
                if approver_bulk_action(driver, wait, dash_type):
                    print("✅ Bulk Action validation successful")
                    return True
                else:
                    allure.attach("Test case failed for Bulk Action", name="approver_bulk_action Failed", attachment_type=allure.attachment_type.TEXT)
                    return False
            except Exception as e:
                allure.attach(str(e), name="Bulk Action Error", attachment_type=allure.attachment_type.TEXT)
    
    if module_name == 'add_approver_bulk_action_negative':
        with allure.step("Verify 'Approver' bulk action Negative functionality"):
            try:
                if approver_negative(driver, wait, dash_type, text_case_id=test_case_id):
                    print("✅ Negative scenario validated successfully")
                    return True
                else:
                   
                    allure.attach("Test case failed for Bulk Action", name=" approver_negative_bulk_action Failed", attachment_type=allure.attachment_type.TEXT)
                    return False
            except Exception as e:
                allure.attach(str(e), name="Bulk Action Error", attachment_type=allure.attachment_type.TEXT)
                

    
    if module_name == 'add_cc_bulk_action':
        with allure.step("Verify 'CC' bulk action functionality"):
            try:
                if  cc_bulk_action(driver, wait, dash_type):
                    print("✅ Bulk Action validation successful")
                    return True
                else:
                    allure.attach("Test case failed for Bulk Action", name="cc_bulk_action Failed", attachment_type=allure.attachment_type.TEXT)
                    return False
            except Exception as e:
                allure.attach(str(e), name="Bulk Action Error", attachment_type=allure.attachment_type.TEXT)

    if module_name == 'add_cc_bulk_action_negative':
        with allure.step("Verify 'CC' bulk action Negative functionality"):
            try:
                if cc_negative(driver, wait, dash_type, text_case_id=test_case_id):
                    print("✅ Bulk Action validation successful")
                    return True
                else:
                    allure.attach("Test case failed for Bulk Action", name=" approver_negative_bulk_action Failed", attachment_type=allure.attachment_type.TEXT)
                    return False
            except Exception as e:
                allure.attach(str(e), name="Bulk Action Error", attachment_type=allure.attachment_type.TEXT)   
    
    if module_name == 'add_comment_bulk_action':
        with allure.step("Verify 'Comment' bulk action functionality"):
            try:
                if comment_bulk_action(driver, wait, dash_type):
                    print("✅ Bulk Action validation successful")
                    return True
                else:
                    allure.attach("Test case failed for Bulk Action", name="comment_bulk_action Failed", attachment_type=allure.attachment_type.TEXT)
                    return False
            except Exception as e:
                allure.attach(str(e), name="Bulk Action Error", attachment_type=allure.attachment_type.TEXT)
    
    if module_name == 'add_comment_bulk_action_negative':
        with allure.step("Verify 'Comment' bulk action Negative functionality"):
            try:
                if comment_negative(driver, wait, dash_type, text_case_id=test_case_id):
                    print("✅ Bulk Action validation successful")
                    return True
                else:
                    allure.attach("Test case failed for Bulk Action", name=" approver_negative_bulk_action Failed", attachment_type=allure.attachment_type.TEXT)
                    return False
            except Exception as e:
                allure.attach(str(e), name="Bulk Action Error", attachment_type=allure.attachment_type.TEXT)          
    
    if module_name == 'upload_file_bulk_action':
        with allure.step("Verify 'Upload File' bulk action functionality"):
            try:
                if upload_file_bulk_action(driver, wait, dash_type):
                    print("✅ Bulk Action validation successful")
                    return True
                else:
                    allure.attach("Test case failed for Bulk Action", name="upload_file_bulk_action Failed", attachment_type=allure.attachment_type.TEXT)
                    return False
            except Exception as e:
                allure.attach(str(e), name="Bulk Action Error", attachment_type=allure.attachment_type.TEXT)
    
    if module_name == 'upload_file_bulk_action_negative':
        with allure.step("Verify 'Upload File' bulk action Negative functionality"):
            try:
                if upload_file_negative(driver, wait, dash_type):
                    print("✅ Bulk Action validation successful")
                    return True
                else:
                    allure.attach("Test case failed for Bulk Action", name="upload_file_bulk_action Failed", attachment_type=allure.attachment_type.TEXT)
                    return False
            except Exception as e:
                allure.attach(str(e), name="Bulk Action Error", attachment_type=allure.attachment_type.TEXT)
    

    if module_name == 'update_due_date_bulk_action':
        with allure.step("Verify 'Update Due Date' bulk action functionality"):
            try:
                if update_due_date_bulk_action(driver, wait, dash_type):
                    print("✅ Bulk Action validation successful")
                    return True
                else:
                    allure.attach("Test case failed for Bulk Action", name="update_due_date_bulk_action Failed", attachment_type=allure.attachment_type.TEXT)
                    return False
            except Exception as e:
                allure.attach(str(e), name="Bulk Action Error", attachment_type=allure.attachment_type.TEXT)
    
    if module_name == 'update_due_date_bulk_action_negative':
        with allure.step("Verify 'Update Due Date' bulk action Negative functionality"):
            try:
                if update_due_date_negative(driver, wait, dash_type):
                    print("✅ Bulk Action validation successful")
                    return True
                else:
                    allure.attach("Test case failed for Bulk Action", name="update_due_date_bulk_action Failed", attachment_type=allure.attachment_type.TEXT)
                    return False
            except Exception as e:
                allure.attach(str(e), name="Bulk Action Error", attachment_type=allure.attachment_type.TEXT)
    
    if module_name == 'approval_complied_bulk_action':
        with allure.step("Verify 'Approval Complied' bulk action functionality"):
            try:
                if approval_complied_bulk_action(driver, wait, task_name,dash_type):
                    print("✅ Bulk Action validation successful")
                    return True
                else:
                    allure.attach("Test case failed for Bulk Action", name="mark_complete_bulk_action Failed", attachment_type=allure.attachment_type.TEXT)
                    return False
            except Exception as e:
                allure.attach(str(e), name="Bulk Action Error", attachment_type=allure.attachment_type.TEXT)
    
    if module_name == 'approval_not_complied_bulk_action':
        with allure.step("Verify 'Approval Not Complied' bulk action functionality"):
            try:
                if approval_not_complied_bulk_action(driver, wait, task_name,dash_type):
                    print("✅ Bulk Action validation successful")
                    return True
                else:
                    allure.attach("Test case failed for Bulk Action", name="not_complied_bulk_action Failed", attachment_type=allure.attachment_type.TEXT)
                    return False
            except Exception as e:
                allure.attach(str(e), name="Bulk Action Error", attachment_type=allure.attachment_type.TEXT)
    
    if module_name == 'rejected_complied_bulk_action':
        with allure.step("Verify 'Rejected Complied' bulk action functionality"):
            try:
                if rejected_complied_bulk_action(driver, wait, task_name,dash_type):
                    print("✅ Bulk Action validation successful")
                    return True
                else:
                    allure.attach("Test case failed for Bulk Action", name="mark_complete_bulk_action Failed", attachment_type=allure.attachment_type.TEXT)
                    return False
            except Exception as e:
                allure.attach(str(e), name="Bulk Action Error", attachment_type=allure.attachment_type.TEXT)
    
    if module_name == 'rejected_not_complied_bulk_action':
        with allure.step("Verify 'Rejected Not Complied' bulk action functionality"):
            try:
                if rejected_not_complied_bulk_action(driver, wait, task_name,dash_type):
                    print("✅ Bulk Action validation successful")
                    return True
                else:
                    allure.attach("Test case failed for Bulk Action", name="mark_complete_bulk_action Failed", attachment_type=allure.attachment_type.TEXT)
                    return False
            except Exception as e:
                allure.attach(str(e), name="Bulk Action Error", attachment_type=allure.attachment_type.TEXT)
   
    if module_name == 'mark_complete_bulk_action':
        with allure.step("Verify 'Mark Complete' bulk action functionality"):
            try:
                if mark_complete_bulk_action(driver, wait, dash_type):
                    print("✅ Bulk Action validation successful")
                    return True
                else:
                    allure.attach("Test case failed for Bulk Action", name="mark_complete_bulk_action Failed", attachment_type=allure.attachment_type.TEXT)
                    return False
            except Exception as e:
                allure.attach(str(e), name="Bulk Action Error", attachment_type=allure.attachment_type.TEXT)
    
    if module_name == 'mark_complete_bulk_action_negative':
        with allure.step("Verify 'Mark Complete' bulk action Negative functionality"):
            try:
                if mark_complete_negative(driver, wait, dash_type):
                    print("✅ Bulk Action validation successful")
                    return True
                else:
                    allure.attach("Test case failed for Bulk Action", name="mark_complete_bulk_action Failed", attachment_type=allure.attachment_type.TEXT)
                    return False
            except Exception as e:
                allure.attach(str(e), name="Bulk Action Error", attachment_type=allure.attachment_type.TEXT)

    if module_name == 'approve_task_bulk_action':
        with allure.step("Verify 'Approve Task' bulk action functionality"):
            try:
                if approve_bulk_action(driver, wait, dash_type):
                    print("✅ Bulk Action validation successful")
                    return True
                else:
                    allure.attach("Test case failed for Bulk Action", name="Bulk Action Validation Failed", attachment_type=allure.attachment_type.TEXT)
                    return False
            except Exception as e:
                allure.attach(str(e), name="Bulk Action Error", attachment_type=allure.attachment_type.TEXT)
    
    if module_name == 'reject_task_bulk_action':
        with allure.step("Verify 'Reject Task' bulk action functionality"):
            try:
                if reject_bulk_action(driver, wait, dash_type):
                    print("✅ Bulk Action validation successful")
                    return True
                else:
                    allure.attach("Test case failed for Bulk Action", name="Bulk Action Validation Failed", attachment_type=allure.attachment_type.TEXT)
                    return False
            except Exception as e:
                allure.attach(str(e), name="Bulk Action Error", attachment_type=allure.attachment_type.TEXT)
    
    if module_name == 'rejected_tasks_bulk_action':
        with allure.step("Verify 'Rejected Tasks' bulk action functionality"):
            try:
                if rejected_bulk_action(driver, wait, dash_type):
                    print("✅ Bulk Action validation successful")
                    return True
                else:
                    allure.attach("Test case failed for Bulk Action", name="Bulk Action Validation Failed", attachment_type=allure.attachment_type.TEXT)
                    return False
            except Exception as e:
                allure.attach(str(e), name="Bulk Action Error", attachment_type=allure.attachment_type.TEXT)

    if module_name == 'completed_tasks_bulk_Action':
        with allure.step("Verify 'Completed Tasks' bulk action functionality"):
            try:
                if completed_task_bulk_action(driver, wait, dash_type):
                    print("✅ Bulk Action validation successful")
                    return True
                else:
                    allure.attach("Test case failed for Bulk Action", name="Bulk Action Validation Failed", attachment_type=allure.attachment_type.TEXT)
                    return False
            except Exception as e:
                allure.attach(str(e), name="Bulk Action Error", attachment_type=allure.attachment_type.TEXT)
    
