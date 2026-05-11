import json
import os
from utilities.add_task_functions.add_task_common import (
    task_field_dictionary,
    task_value_validation_store,
    task_field_validation_dictionary
)
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from datetime import datetime
from utilities.add_task_functions.wait_for_loader_to_disappear import wait_for_loader_to_disappear
from utilities.other_utils_functions.highlight import highlight_element
import allure
import pyautogui as pg

def special_task_validation(driver, wait):
    try:
        # with allure.step("Load locators from JSON"):
        try:
            with open(os.path.join("data", 'locators.json'), 'r') as f:
                elements_details = json.load(f)
        except FileNotFoundError:
            msg = "locators.json file not found."
            print(msg)
            allure.attach(msg, name="Locator File Error", attachment_type=allure.attachment_type.TEXT)
            return False
        except json.JSONDecodeError:
            msg = "Error decoding JSON from locators.json."
            print(msg)
            allure.attach(msg, name="Locator JSON Error", attachment_type=allure.attachment_type.TEXT)
            return False

        # Extract locators
        special_task_icon = elements_details.get('special_task_icon')
        task_title_label = elements_details.get('task_title_label')
        task_start_date_label = elements_details.get('task_start_date_label')
        task_due_date_label = elements_details.get('task_due_date_label')
        task_deadline_label = elements_details.get('task_deadline_label')
        task_frequency_label = elements_details.get('task_frequency_label')
        task_assign_to_label = elements_details.get('task_assign_to_label')
        task_approver_label = elements_details.get('task_approver_label')
        task_cc_label = elements_details.get('task_cc_label')
        task_risk_label = elements_details.get('task_risk_label')
        task_note_tab = elements_details.get('task_note_tab')
        task_update_tab = elements_details.get('task_update_tab')
        task_log_tab = elements_details.get('task_log_tab')
        task_description = elements_details.get('task_description')
        task_attached_file = elements_details.get('task_attached_file')
        task_impact_btn = elements_details.get('task_impact_btn')
        task_impact_details = elements_details.get('task_impact_details')
        task_impact_file = elements_details.get('task_impact_file')
        task_impact_close_btn = elements_details.get('task_impact_close_btn')
        task_circular_list = elements_details.get('task_circular_list')
        task_license_label = elements_details.get('task_license_label')
        task_action_log_section = elements_details.get('task_action_log_section')
        # with allure.step("Validate task title"):
        task_name_label_elem = wait.until(EC.visibility_of_element_located((By.XPATH, task_title_label)))
        highlight_element(driver, task_name_label_elem, 0.2)
        fetched_task_name = task_name_label_elem.text.strip()
        print(f"Task Title: {fetched_task_name}")
        task_value_validation_store('task_name', fetched_task_name)

        # with allure.step("Validate start date"):
        task_start_date_label_elem = wait.until(EC.visibility_of_element_located((By.XPATH, task_start_date_label)))
        highlight_element(driver, task_start_date_label_elem, 0.2)
        fetched_start_date = task_start_date_label_elem.text.strip()
        start_date_obj = datetime.strptime(fetched_start_date, "%d %b %Y")
        print(f"Start Date: {fetched_start_date}")
        task_value_validation_store('start_date', start_date_obj.strftime("%d %B %Y"))

        # with allure.step("Validate due date and end time"):
        task_due_date_label_elem = wait.until(EC.visibility_of_element_located((By.XPATH, task_due_date_label)))
        highlight_element(driver, task_due_date_label_elem, 0.2)
        fetched_due_date_time = task_due_date_label_elem.text.strip()
        if 'AM' in fetched_due_date_time or 'PM' in fetched_due_date_time:
            due_datetime = datetime.strptime(fetched_due_date_time, "%d %b %Y %I:%M %p")
        else:
            due_datetime = datetime.strptime(fetched_due_date_time, "%d %b %Y")
        fetched_due_date = due_datetime.strftime("%d %B %Y")
        fetched_end_time = due_datetime.strftime("%I:%M %p") if 'AM' in fetched_due_date_time or 'PM' in fetched_due_date_time else None
        print(f"Due Date: {fetched_due_date}")
        if fetched_end_time:
            print(f"End Time: {fetched_end_time}")
            task_value_validation_store('end_time', fetched_end_time)
        task_value_validation_store('due_date', fetched_due_date)

        # with allure.step("Validate internal deadline"):
        task_deadline_label_elem = wait.until(EC.visibility_of_element_located((By.XPATH, task_deadline_label)))
        highlight_element(driver, task_deadline_label_elem, 0.2)
        fetched_deadline = datetime.strptime(task_deadline_label_elem.text.strip(), "%d %b %Y %I:%M %p")
        date_difference = (due_datetime.date() - fetched_deadline.date()).days
        print(f"📅 Difference between Due Date and Internal Deadline: {date_difference} day(s)")
        task_value_validation_store('internal_deadline', date_difference)

        # with allure.step("Validate frequency"):
        task_frequency_label_elem = wait.until(EC.visibility_of_element_located((By.XPATH, task_frequency_label)))
        highlight_element(driver, task_frequency_label_elem, 0.2)
        fetched_frequency = task_frequency_label_elem.text.strip()
        print(f"Task Frequency: {fetched_frequency}")
        task_value_validation_store('frequency', fetched_frequency)

        task_creator_label_elem = wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@class='holding-list-bold-title truncate']")))
        highlight_element(driver, task_creator_label_elem, 0.2)
        fetched_creator = task_creator_label_elem.text.strip()
        print(f"Task Frequency: {fetched_creator}")
        task_value_validation_store('creator', fetched_creator)

        task_category_label_elem = wait.until(EC.visibility_of_element_located((By.XPATH, "//div[div[text()='Category']]/following-sibling::div/div[@class='holding-list-bold-title']")))
        highlight_element(driver, task_category_label_elem, 0.2)
        fetched_category = task_category_label_elem.text.strip()
        print(f"Task Frequency: {fetched_category}")
        task_value_validation_store('task_category', fetched_category)

        # with allure.step("Validate assign to, approver, CC, risk, license"):
            # Assign To
        task_assign_to_label_elem = wait.until(EC.visibility_of_element_located((By.XPATH, task_assign_to_label)))
        highlight_element(driver, task_assign_to_label_elem, 0.2)
        fetched_assign_to = task_assign_to_label_elem.text.strip()
        print(f"Assign To: {fetched_assign_to}")
        task_value_validation_store('assign_to', fetched_assign_to)

        # Approver
        task_approver_label_elem = wait.until(EC.visibility_of_element_located((By.XPATH, task_approver_label)))
        highlight_element(driver, task_approver_label_elem, 0.2)
        fetched_approver = task_approver_label_elem.text.strip()
        print(f"Approver: {fetched_approver}")
        task_value_validation_store('approver', fetched_approver)

        # CC
        task_cc_label_elem = wait.until(EC.visibility_of_element_located((By.XPATH, task_cc_label)))
        highlight_element(driver, task_cc_label_elem, 0.2)
        fetched_cc = task_cc_label_elem.text.strip()
        print(f"CC: {fetched_cc}")
        task_value_validation_store('cc', fetched_cc)

        # Risk
        task_risk_label_elem = wait.until(EC.visibility_of_element_located((By.XPATH, task_risk_label)))
        highlight_element(driver, task_risk_label_elem, 0.2)
        fetched_risk = task_risk_label_elem.text.strip()
        print(f"Risk: {fetched_risk}")
        task_value_validation_store('risk', fetched_risk)

            # License
        task_license_label_elem = wait.until(EC.visibility_of_element_located((By.XPATH, task_license_label)))
        highlight_element(driver, task_license_label_elem, 0.2)
        fetched_license = task_license_label_elem.text.strip()
        print(f"License: {fetched_license}")
        task_value_validation_store('license', fetched_license)

        # with allure.step("Validate note tab and description"):
        task_note_tab_elem = wait.until(EC.presence_of_element_located((By.XPATH, task_note_tab)))
        highlight_element(driver, task_note_tab_elem, 0.2)
        wait_for_loader_to_disappear(driver, wait)
        task_note_tab_elem.click()
        print(f"Clicked on note tab")

        task_description_elem = wait.until(EC.presence_of_element_located((By.XPATH, task_description)))
        highlight_element(driver, task_description_elem, 0.2)
        fetched_description = task_description_elem.text.strip()
        print(f"Description: {fetched_description}")
        task_value_validation_store('description', fetched_description)

        # with allure.step("Validate attached file"):
        task_attached_file_elem = wait.until(EC.presence_of_element_located((By.XPATH, task_attached_file)))
        highlight_element(driver, task_attached_file_elem, 0.2)
        fetched_attached_file = task_attached_file_elem.text.strip()
        print(f"File name: {fetched_attached_file}")
        task_value_validation_store('attach_file_name', fetched_attached_file)

        # with allure.step("Validate impact details and file"):
        # task_impact_btn_elem = wait.until(EC.presence_of_element_located((By.XPATH, task_impact_btn)))
        task_impact_btn_elem = wait.until(EC.element_to_be_clickable((By.XPATH, task_impact_btn)))
        highlight_element(driver, task_impact_btn_elem, 0.2)
        wait_for_loader_to_disappear(driver, wait)
        task_impact_btn_elem.click()
        print(f"Clicked on impact button")

        task_impact_details_elem = wait.until(EC.presence_of_element_located((By.XPATH, task_impact_details)))
        highlight_element(driver, task_impact_details_elem, 0.2)
        fetched_impact_description = task_impact_details_elem.text.strip()
        print(f"Impact Description: {fetched_impact_description}")
        task_value_validation_store('impact_details', fetched_impact_description)

        task_impact_file_elem = wait.until(EC.presence_of_element_located((By.XPATH, task_impact_file)))
        highlight_element(driver, task_impact_file_elem, 0.2)
        fetched_impact_file = task_impact_file_elem.text.strip()
        print(f"Impact File name: {fetched_impact_file}")
        task_value_validation_store('impact_file_name', fetched_impact_file)

        pg.press('esc')
        pg.press('esc')

        # with allure.step("Validate update tab and circulars"):
        task_update_tab_elem = wait.until(EC.presence_of_element_located((By.XPATH, task_update_tab)))
        highlight_element(driver, task_update_tab_elem, 0.2)
        wait_for_loader_to_disappear(driver, wait)
        task_update_tab_elem.click()
        print(f"Clicked on update tab")

        task_circular_list_elem = wait.until(EC.presence_of_element_located((By.XPATH, task_circular_list)))
        highlight_element(driver, task_circular_list_elem, 0.2)
        fetched_task_circular_list = task_circular_list_elem.text.strip()
        print(f"Circula Name: {fetched_task_circular_list}")
        task_value_validation_store('circular_search', fetched_task_circular_list)

        
        task_log_tab_elem = wait.until(EC.presence_of_element_located((By.XPATH, "//div[text()='Log']")))
        task_log_tab_elem.click()
        print("✅ Log tab clicked")
        

        
        task_log_list_elem = wait.until(EC.presence_of_all_elements_located((By.XPATH, task_action_log_section)))

        visible_logs_count = 0

        for index, log_elem in enumerate(task_log_list_elem, start=1):
            if log_elem.is_displayed():  # Only process visible logs
                highlight_element(driver, log_elem, 0.2)
                full_text = log_elem.get_attribute("textContent").strip()
                fetched_member_name = log_elem.find_element(By.TAG_NAME, "strong").text
                action = full_text.replace(fetched_member_name, "").strip()

                print(f"✅ Log {index}: Action='{action}', Member='{fetched_member_name}'")

                # Optionally store each log
                task_value_validation_store(f'log_{index}_action', action)
                task_value_validation_store(f'log_{index}_member', fetched_member_name)

                visible_logs_count += 1

        print(f"Total visible logs processed: {visible_logs_count}")

        if visible_logs_count == 0:
            print("❌ No visible log entries found")


        # with allure.step("Field-wise validation"):
        for task in task_field_dictionary.keys():
            expected = str(task_field_validation_dictionary.get(task, '')).strip()
            actual = str(task_field_dictionary.get(task, '')).strip()

            if expected != '':
                print(f'Validating {actual} with {expected}')
                allure.attach(f"{task}: actual='{actual}', expected='{expected}'", name=f"Validation for {task}", attachment_type=allure.attachment_type.TEXT)
                if actual.strip().lower() == expected.strip().lower() or actual.strip().lower() in expected.strip().lower() or actual.split()[0].lower() in expected.strip().lower():
                    print(f"Validation passed for {task}")
                else:
                    msg = f"Validation failed for {task}"
                    print(msg)
                    allure.attach(msg, name="Field Validation Error", attachment_type=allure.attachment_type.TEXT)
                    return False


    except Exception as e:
        print(f"Error validating task details: {str(e)}")
        allure.attach(str(e), name="Task Details Validation Error", attachment_type=allure.attachment_type.TEXT)
        return False
    return True
