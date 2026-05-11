# note_tab.py
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import pytest
import allure
import time
import pandas as pd
import json
import os

from utilities.other_utils_functions.highlight import highlight_element
from utilities.add_task_utils import wait_for_loader_to_disappear
from utilities.add_task_utils import add_task_check
from utilities.add_task_utils import load_test_config_excel_data
from utilities.add_task_utils import get_test_case_list
from utilities.add_task_functions.show_toast import show_toast
from utilities.add_task_functions.format_date_if_valid import format_date_if_valid
from utilities.add_task_functions.format_time_if_valid import format_time_if_valid
from utilities.add_task_functions.set_task_name import set_task_name
from utilities.add_task_functions.set_start_date import set_start_date
from utilities.add_task_functions.set_due_date import set_due_date
from utilities.add_task_functions.set_frequency import set_frequency
from utilities.add_task_functions.add_description import add_description
from utilities.add_task_functions.attach_file import attach_file
from utilities.add_task_functions.submit_task import submit_task

def note_check(driver,task_name=None, start_date=None, due_date=None, frequency=None,
                  repeat_if_due_date_is_on_holiday=None, end_frequency_date=None,
                  weekday_name=None, repeat_day_and_month=None, dash_type=''):
    wait = WebDriverWait(driver, 30)
   
    

    # ✅ Step 3: Load locators
    with allure.step("Load locators.json"):
        try:
            with open(os.path.join("data", 'locators.json'), 'r') as f:
                elements_details = json.load(f)

            add_task_float = elements_details['add_task_float']
            add_task_btn = elements_details['add_task_btn']
            task_close_btn = elements_details['task_close_btn']
            task_input_error_msg = elements_details['task_input_error_msg']
            task_name_input = elements_details['task_name_input']
            task_note_tab = elements_details['task_note_tab']
            start_date_input = elements_details['start_date_input']
            due_date_input = elements_details['due_date_input']
            frequency_option = elements_details['freq_option']
            frequency_value_check = elements_details['freq_value_check']
            description_btn = elements_details['desc_btn']
            description_input = elements_details['desc_input']
            desc_save_btn = elements_details['desc_save_btn']
            desc_view = elements_details['desc_view']
            attach_file_btn = elements_details['attach_file_btn']
            attach_file_input = elements_details['file_input']
            attach_file_save_btn = elements_details['attach_file_save_btn']
            attach_file_view = elements_details['attach_file_view']
            submit_button = elements_details['task_submit_btn']
            

            print("✅ locators.json loaded successfully")
        except Exception as e:
            allure.attach(str(e), name="Locators Load Error", attachment_type=allure.attachment_type.TEXT)
            return False
    # 🧩 Load first test case data
    test_cases = get_test_case_list()
    first_case = test_cases[0]
    task_data = first_case.values

    (task_name, start_date, due_date, frequency, repeat_if_holiday, end_freq_date,
     repeat_weekday, repeat_day_month, end_time, internal_deadline, assign_to,
     approver, cc, risk_rating, license_name, description, attach_file_name,
     impact_details, impact_file_name, circular_search, expected_success,
     level_of_testing) = task_data
    

    print(f"🧠 Running Comment test for task: {task_name}")
    print(f"Assigned to: {assign_to} | Approver: {approver} | CC: {cc}")

    # # ✅ Step 3: Create Task
    with allure.step("Add Task Check"):
        try:
            if add_task_check(driver, task_name, start_date, due_date, frequency, repeat_if_holiday, end_freq_date,
                   repeat_weekday, repeat_day_month, end_time, internal_deadline, assign_to, approver, cc,
                   risk_rating, license_name, description, attach_file_name, impact_details, impact_file_name,
                   circular_search, expected_success, level_of_testing, task_type='mandatory'):
                print("✅ Task creation successful")
            else:
                raise Exception("❌ Task creation failed")
        except Exception as e:
            allure.attach(str(e), name="Add Task Error", attachment_type=allure.attachment_type.TEXT)
     # ✅ Step 4: Load Config Data
    with allure.step("Load test config excel data"):
        try:
            if load_test_config_excel_data(driver, wait):
                print("✅ Load test config excel data successful")
            else:
                raise Exception("❌ Load test config excel data failed")
        except Exception as e:
            allure.attach(str(e), name="Load Config Error", attachment_type=allure.attachment_type.TEXT)

    # Validate toast message
    with allure.step("Validate toast notification for creation of a task without an assignee"):
        toast = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//div[contains(@class,'Toastify__toast-body')]")
            )
        )
        highlight_element(driver, toast)
        print(f"📢 Toast message: {toast.text.strip()}")
    #Edit Task Details
    with allure.step("Click Edit Button"):
        print()
        time.sleep(7)
        edit_btn = wait.until(EC.presence_of_element_located((By.XPATH, "//button[@title='Edit']")))
        highlight_element(driver, edit_btn)
        edit_btn.click()
        print("✅ Edit button clicked successfully")
    
     # ✅ Step 15: Add description
    with allure.step("Adding description..."):
        print()
        print(f"Adding description: {description}")
        allure.attach(f"Adding description: {description}", name="Description", attachment_type=allure.attachment_type.TEXT)
        description_success = add_description(driver, description_btn, description_input, str(description), desc_save_btn, desc_view, wait)
        if description_success == 'blank':
            msg = "Description input is blank."
            print(msg)
            allure.attach(msg, name="Description Status", attachment_type=allure.attachment_type.TEXT)
            show_toast(driver, msg)
            time.sleep(2)
            # return True

        if description_success:
            print("✅ Description added successfully.")
            # allure.attach("Description added successfully", name="Description Status", attachment_type=allure.attachment_type.TEXT)
            # return True
        
        else:
            msg = "❌ Failed to add description."
            print(msg)
            allure.attach(msg, name="Description Status", attachment_type=allure.attachment_type.TEXT)
            show_toast(driver, msg)
            time.sleep(2)
            return False
    
    # ✅ Step 16: Add attachments
    with allure.step("Adding attachments..."):
        print()
        print(f"Adding attachments: {attach_file_name}")
        allure.attach(f"Attaching file: {attach_file_name}", name="Attachments", attachment_type=allure.attachment_type.TEXT)
        attachment_success = attach_file(driver, attach_file_btn, attach_file_input, attach_file_name, attach_file_save_btn, attach_file_view, wait)
        if attachment_success == 'blank':
            msg = "Attachment input is blank."
            print(msg)
            allure.attach(msg, name="File Attach Status", attachment_type=allure.attachment_type.TEXT)
            show_toast(driver, msg)
            time.sleep(2)
            # return True
        
        if attachment_success:
            # allure.attach("Attachments added successfully", name="Attachments Status", attachment_type=allure.attachment_type.TEXT)
            print("✅ Attachments added successfully.")
            # return True
        else:
            msg = "❌ Failed to add attachments."
            print(msg)
            allure.attach(msg, name="Attachments Status", attachment_type=allure.attachment_type.TEXT)
            show_toast(driver, msg)
            time.sleep(2)
            return False
    
    #Click Update Button
    with allure.step("Click Update Button"):
        save_btn = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Save') or contains(., 'Update')]"))
        )
        highlight_element(driver, save_btn)
        save_btn.click()
        print("✅ Save/Update button clicked successfully.")
    
     # Validate toast message
    with allure.step("Validate toast notification for creation of a task without an assignee"):
        toast = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//div[contains(@class,'Toastify__toast-body')]")
            )
        )
        highlight_element(driver, toast)
        print(f"📢 Toast message: {toast.text.strip()}")
    # ✅ Step 5: Note added by User (Team Member)
    with allure.step("Click on Note Tab"):
        print()
    # Click Log tab
        time.sleep(3)
        note_user = wait.until(EC.presence_of_element_located((By.XPATH, task_note_tab)))
        highlight_element(driver, note_user)
        note_user.click()
        print("✅ Note tab clicked successfully.")

    #  Click Add Task Float Button
# ============================
    with allure.step("➕ Open Add Task Float"):
        try:
            print()
            time.sleep(10)
            # Wait for re-render after comment
            add_task_float_btn = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, add_task_float))
            )
            highlight_element(driver, add_task_float_btn)
            add_task_float_btn.click()
            print("✅ Add Task Float button clicked")

        except Exception:
            # Fallback: sometimes multiple buttons exist
            print("⚠️ Primary click failed → Trying fallback method")

            add_task_float_btns = WebDriverWait(driver, 20).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, add_task_float))
            )

            clicked = False
            for btn in add_task_float_btns:
                try:
                    highlight_element(driver, btn)
                    btn.click()
                    print("✅ Add Task Float clicked using fallback")
                    clicked = True
                    break
                except:
                    continue

            if not clicked:
                pytest.fail("❌ Could not click Add Task Float button")


    # ============================
    # Click 'Add Task' Button
    # ============================
    with allure.step("🆕 Click Add Task button"):
        try:
            # Wait for modal/popup to appear
            wait.until(EC.presence_of_element_located((By.XPATH, add_task_btn)))

            # Try to find ALL matching Add Task buttons (multiple possibilities)
            buttons = driver.find_elements(By.XPATH, add_task_btn)

            if not buttons:
                pytest.fail("❌ No Add Task button found in DOM")

            clicked = False

            for btn in buttons:
                try:
                    # Scroll into view (sometimes it's low in popup)
                    driver.execute_script("arguments[0].scrollIntoView(true);", btn)
                    time.sleep(0.5)

                    # Wait until clickable
                    WebDriverWait(driver, 5).until(EC.element_to_be_clickable(btn))

                    highlight_element(driver, btn)
                    btn.click()
                    print("✅ Add Task button clicked")
                    clicked = True
                    break

                except Exception:
                    continue

            if not clicked:
                pytest.fail("❌ Add Task button was found but not clickable")

        except Exception as e:
            allure.attach(str(e), name="AddTaskButtonError", attachment_type=allure.attachment_type.TEXT)
            pytest.fail("❌ Failed to click Add Task button (final catch)")

    # ✅ Step 3: Set Task Name
    with allure.step("Setting Task Name..."):
        print()
        task_name = f'{task_name}_new'
        task_name_success = set_task_name(driver, task_name_input, task_name, wait)
        if task_name_success == 'blank':
            msg = "Task name input is blank."
            allure.attach(msg, name="Task Name Failure", attachment_type=allure.attachment_type.TEXT)
            print(msg)
            show_toast(driver, msg)
            time.sleep(2)
            return False
        
        elif task_name_success:
            # msg = "✅ Task name set successfully"
            # allure.attach(msg, name="Task Name Status", attachment_type=allure.attachment_type.TEXT)
            print("✅ Task name set successfully")
            # return True
        
        else:
            msg = "❌ Failed to set task name."
            print(msg)
            allure.attach(msg, name="Task Name Failure", attachment_type=allure.attachment_type.TEXT)
            show_toast(driver, msg)
            time.sleep(2)
            return False

    # ✅ Step 4: Set Start Date
    with allure.step("Setting Start Date..."):
        print()
        print(f"Setting start date to: {start_date}")
        start_date_success = set_start_date(driver, start_date_input, start_date, wait)
        if start_date_success == 'blank':
            msg = "Start date input is blank."
            print(msg)
            allure.attach(msg, name="Start Date Failure", attachment_type=allure.attachment_type.TEXT)
            show_toast(driver, msg)
            time.sleep(2)
            return False
        
        elif start_date_success:
            # allure.attach("Start date set successfully", name="Start Date Status", attachment_type=allure.attachment_type.TEXT)
            print("✅ Start date set successfully.")
            # return True
        
        else:
            msg = "❌ Failed to set start date."
            print(msg)
            allure.attach(msg, name="Start Date Failure", attachment_type=allure.attachment_type.TEXT)
            show_toast(driver, msg)
            time.sleep(2)
            return False

    # ✅ Step 5: Set Due Date
    with allure.step("Setting Due Date..."):
        print()
        print(f"Setting due date to: {due_date}")
        due_date_success = set_due_date(driver, due_date_input, start_date_input, due_date, task_input_error_msg, wait)
        if due_date_success == 'blank':
            msg = "Due date input is blank."
            print(msg)
            allure.attach(msg, name="Due Date Status", attachment_type=allure.attachment_type.TEXT)
            show_toast(driver, msg)
            time.sleep(2)
            return False
        
        elif due_date_success:
            # allure.attach("Due date set successfully", name="Due Date Status", attachment_type=allure.attachment_type.TEXT)
            print("✅ Due date set successfully.")
            # return True
        
        else:
            msg = "❌ Failed to set due date."
            print(msg)
            allure.attach(msg, name="Due Date Status", attachment_type=allure.attachment_type.TEXT)
            show_toast(driver, msg)
            time.sleep(2)
            return False
    
    # ✅ Step 6: Set Frequency
    with allure.step("Setting Frequency..."):
        print()
        time.sleep(2)
        print(f"Setting frequency to: {frequency}")
        if not frequency or frequency.strip() == '':
            frequency = 'Only once'
        frequency_option = "//div[text()='Frequency*']"
        frequency_success = set_frequency(driver, frequency_option, frequency, repeat_if_due_date_is_on_holiday, end_frequency_date, weekday_name, repeat_day_and_month, frequency_value_check, wait)
        if frequency_success == 'blank':
            msg = "Frequency input is blank."
            print(msg)
            allure.attach(msg, name="Frequency Status", attachment_type=allure.attachment_type.TEXT)
            show_toast(driver, msg)
            time.sleep(2)
            # return False
        
        elif frequency_success:
            # allure.attach("Frequency set successfully", name="Frequency Status", attachment_type=allure.attachment_type.TEXT)
            print("✅ Frequency set successfully.")
            # return True
        
        else:
            msg = "❌ Failed to set frequency."
            print(msg)
            allure.attach(msg, name="Frequency Status", attachment_type=allure.attachment_type.TEXT)
            show_toast(driver, msg)
            time.sleep(2)
            return False
    
     # ✅ Step 19: Submitting Task
    with allure.step("Submitting Task..."):
        print(f"Submitting Task:")
        submit_task_success = submit_task(driver, submit_button, wait)
        if submit_task_success:
            msg = "Task submitted successfully."
            print(msg)
            allure.attach(msg, name="Submit Task Status", attachment_type=allure.attachment_type.TEXT)
            time.sleep(1)
            # return False
        else:
            msg = "❌ Failed to submit Task."
            print(msg)
            allure.attach(msg, name="Submit Task Status", attachment_type=allure.attachment_type.TEXT)
            time.sleep(1)
            return False

     # Validate toast message
    with allure.step("Validate toast notification for creation of a task without an assignee"):
        toast = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//div[contains(@class,'Toastify__toast-body')]")
            )
        )
        highlight_element(driver, toast)
        print(f"📢 Toast message: {toast.text.strip()}")
    #Edit Task Details
    with allure.step("Click Edit Button"):
        print()
        time.sleep(7)
        edit_btn = wait.until(EC.presence_of_element_located((By.XPATH, "//button[@title='Edit']")))
        highlight_element(driver, edit_btn)
        edit_btn.click()
        print("✅ Edit button clicked successfully")

     # ✅ Step 15: Add description
    with allure.step("Adding description..."):
        print()
        description = f'{description}_new'
        print(f"Adding description: {description}")
        allure.attach(f"Adding description: {description}", name="Description", attachment_type=allure.attachment_type.TEXT)
        description_success = add_description(driver, description_btn, description_input, str(description), desc_save_btn, desc_view, wait)
        if description_success == 'blank':
            msg = "Description input is blank."
            print(msg)
            allure.attach(msg, name="Description Status", attachment_type=allure.attachment_type.TEXT)
            show_toast(driver, msg)
            time.sleep(2)
            # return True

        if description_success:
            print("✅ Description added successfully.")
            # allure.attach("Description added successfully", name="Description Status", attachment_type=allure.attachment_type.TEXT)
            # return True
        
        else:
            msg = "❌ Failed to add description."
            print(msg)
            allure.attach(msg, name="Description Status", attachment_type=allure.attachment_type.TEXT)
            show_toast(driver, msg)
            time.sleep(2)
            return False
    
    # ✅ Step 16: Add attachments
    with allure.step("Adding attachments..."):
        print()
        print(f"Adding attachments: {attach_file_name}")
        allure.attach(f"Attaching file: {attach_file_name}", name="Attachments", attachment_type=allure.attachment_type.TEXT)
        attachment_success = attach_file(driver, attach_file_btn, attach_file_input, attach_file_name, attach_file_save_btn, attach_file_view, wait)
        if attachment_success == 'blank':
            msg = "Attachment input is blank."
            print(msg)
            allure.attach(msg, name="File Attach Status", attachment_type=allure.attachment_type.TEXT)
            show_toast(driver, msg)
            time.sleep(2)
            # return True
        
        if attachment_success:
            # allure.attach("Attachments added successfully", name="Attachments Status", attachment_type=allure.attachment_type.TEXT)
            print("✅ Attachments added successfully.")
            # return True
        else:
            msg = "❌ Failed to add attachments."
            print(msg)
            allure.attach(msg, name="Attachments Status", attachment_type=allure.attachment_type.TEXT)
            show_toast(driver, msg)
            time.sleep(2)
            return False
    
    #Click Update Button
    with allure.step("Click Update Button"):
        save_btn = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Save') or contains(., 'Update')]"))
        )
        highlight_element(driver, save_btn)
        save_btn.click()
        print("✅ Save/Update button clicked successfully.")
    
     # Validate toast message
    with allure.step("Validate toast notification for creation of a task without an assignee"):
        toast = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//div[contains(@class,'Toastify__toast-body')]")
            )
        )
        highlight_element(driver, toast)
        print(f"📢 Toast message: {toast.text.strip()}")
    # ✅ Step 5: Note added by User (Team Member)
    with allure.step("Click on Note Tab"):
        print()
    # Click Log tab
        time.sleep(3)
        note_user = wait.until(EC.presence_of_element_located((By.XPATH, task_note_tab)))
        highlight_element(driver, note_user)
        note_user.click()
        print("✅ Note tab clicked successfully.")
        time.sleep(7)
    close_btn = wait.until((EC.presence_of_element_located((By.XPATH, task_close_btn))))
    highlight_element(driver, close_btn)
    close_btn.click()
    return True
    