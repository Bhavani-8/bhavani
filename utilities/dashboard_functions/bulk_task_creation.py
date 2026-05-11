from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
import pandas as pd
import allure
import os
import json
import pytest
import time

from utilities.add_task_utils import wait_for_loader_to_disappear
from utilities.highlight import highlight_element
from utilities.search_utils import perform_search, clear_search


def bulk_task_creation_check(driver, wait, filename='bulk_task_creation_valid.xlsx', task_name='trial'):
    wait_less = WebDriverWait(driver, 5)

    # -------------------------
    # Load locators
    # -------------------------
    try:
        with allure.step("➡️ Loading locators from data/locators.json"):
            with open(os.path.join("data", 'locators.json'), 'r') as f:
                elements_details = json.load(f)
                add_task_float = elements_details['add_task_float']
                add_task_btn = elements_details['add_task_btn']
                toast_msg = elements_details['toast_msg']
                create_bulk_task_btn = elements_details['create_bulk_task_btn']
                create_bulk_task_label = elements_details['create_bulk_task_label']
                dash_bulk_task_dropdown_file_input = elements_details['dash_bulk_task_dropdown_file_input']
                bulk_task_error_file_btn = elements_details['bulk_task_error_file_btn']
                dash_total_btn = elements_details['dash_total_btn']
                task_close_btn = elements_details['task_close_btn']
                form_cancel_btn = elements_details['form_cancel_btn']
                create_tasks_btn = elements_details['create_tasks_btn']
                task_open_btn = elements_details['task_open_btn']
            print("✅ Loaded locators from locators.json")
    except FileNotFoundError as err:
        allure.attach(str(err), name="locators.json not found", attachment_type=allure.attachment_type.TEXT)
        pytest.fail("locators.json file not found")
    except json.JSONDecodeError as err:
        allure.attach(str(err), name="Invalid JSON in locators.json", attachment_type=allure.attachment_type.TEXT)
        pytest.fail("Invalid JSON in locators.json")
    except Exception as err:
        allure.attach(str(err), name="Unexpected error loading locators", attachment_type=allure.attachment_type.TEXT)
        pytest.fail(f"Unexpected error loading locators: {err}")

    # -------------------------
    # Dashboard total button
    # -------------------------
    try:
        with allure.step("➡️ Clicking Dashboard Total button"):
            dash_total_btn_elem = wait.until(EC.presence_of_element_located((By.XPATH, dash_total_btn)))
            highlight_element(driver, dash_total_btn_elem)
            dash_total_btn_elem.click()
            wait_for_loader_to_disappear(driver, wait)
            print("✅ Clicked Dashboard Total button")
    except Exception as err:
        allure.attach(str(err), name="Dashboard Button Error", attachment_type=allure.attachment_type.TEXT)
        print(f"❌ Error clicking Dashboard Total button: {err}")

    # -------------------------
    # Add Task Float
    # -------------------------
    try:
        with allure.step("➡️ Opening Add Task Float"):
            add_task_float_btn = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, add_task_float)))
            highlight_element(driver, add_task_float_btn)
            add_task_float_btn.click()
            wait_for_loader_to_disappear(driver, wait)
            print("✅ Opened Add Task Float")
    except Exception as err:
        allure.attach(str(err), name="Add Task Float Error", attachment_type=allure.attachment_type.TEXT)
        print(f"❌ Error opening Add Task Float: {err}")

    # -------------------------
    # Add Task Button
    # -------------------------
    try:
        with allure.step("➡️ Clicking Add Task Button"):
            add_task_button = wait.until(EC.presence_of_element_located((By.XPATH, add_task_btn)))
            highlight_element(driver, add_task_button)
            add_task_button.click()
            wait_for_loader_to_disappear(driver, wait)
            print("✅ Clicked Add Task Button")
    except Exception as err:
        allure.attach(str(err), name="Add Task Button Error", attachment_type=allure.attachment_type.TEXT)
        print(f"❌ Error clicking Add Task Button: {err}")

    # -------------------------
    # Bulk Task Creation
    # -------------------------
    try:
        with allure.step("➡️ Opening Bulk Task Creation form"):
            create_bulk_task_btn_elem = wait.until(EC.element_to_be_clickable((By.XPATH, create_bulk_task_btn)))
            create_bulk_task_btn_elem = wait.until(EC.presence_of_element_located((By.XPATH, create_bulk_task_btn)))
            highlight_element(driver, create_bulk_task_btn_elem)
            create_bulk_task_btn_elem.click()
            wait_for_loader_to_disappear(driver, wait)
            print("✅ Bulk Task Creation form opened")
    except Exception as err:
        allure.attach(str(err), name="Bulk Task Form Error", attachment_type=allure.attachment_type.TEXT)
        print(f"❌ Error opening Bulk Task Creation form: {err}")

    try:
        with allure.step("➡️ Verifying Bulk Task Creation form title"):
            create_bulk_task_label_elem = wait.until(EC.presence_of_element_located((By.XPATH, create_bulk_task_label)))
            highlight_element(driver, create_bulk_task_label_elem)
            if create_bulk_task_label_elem.text == 'Bulk Task Creation':
                print("✅ Bulk Task Creation form title verified")
            else:
                print("❌ Bulk Task Creation form title mismatch")
                allure.attach("Form title mismatch", name="Form Title Error", attachment_type=allure.attachment_type.TEXT)
    except Exception as err:
        allure.attach(str(err), name="Form Title Error", attachment_type=allure.attachment_type.TEXT)
        print(f"❌ Error verifying Bulk Task Creation form: {err}")

    try:
        with allure.step("➡️ Uploading bulk task file"):
            file_input_elem = wait.until(EC.presence_of_element_located((By.XPATH, dash_bulk_task_dropdown_file_input)))
            highlight_element(driver, file_input_elem)
            file_path = os.path.abspath(os.path.join('data', filename))
            file_input_elem.send_keys(file_path)
            wait_for_loader_to_disappear(driver, wait)
            print(f"✅ Uploaded file: {file_path}")
    except Exception as err:
        allure.attach(str(err), name="File Upload Error", attachment_type=allure.attachment_type.TEXT)
        print(f"❌ Error uploading file: {err}")

    try:
        with allure.step("➡️ Handling validation results"):
            try:
                bulk_task_error_file_btn_elem = wait_less.until(EC.presence_of_element_located((By.XPATH, bulk_task_error_file_btn)))
                highlight_element(driver, bulk_task_error_file_btn_elem)
                bulk_task_error_file_btn_elem.click()

                form_cancel_btn_elem = wait_less.until(EC.presence_of_element_located((By.XPATH, form_cancel_btn)))
                highlight_element(driver, form_cancel_btn_elem)
                form_cancel_btn_elem.click()
                wait_for_loader_to_disappear(driver, wait)
                print("ℹ️ Error file found and form closed")
            except TimeoutException:
                print("ℹ️ No error file found, proceeding with task creation")
                create_tasks_btn_elem = wait_less.until(EC.presence_of_element_located((By.XPATH, create_tasks_btn)))
                highlight_element(driver, create_tasks_btn_elem)
                if create_tasks_btn_elem.is_enabled():
                    create_tasks_btn_elem.click()
                    print("✅ Clicked Create Tasks button")
                else:
                    form_cancel_btn_elem = wait_less.until(EC.presence_of_element_located((By.XPATH, form_cancel_btn)))
                    highlight_element(driver, form_cancel_btn_elem)
                    form_cancel_btn_elem.click()
                    print("❌ Create button disabled. Form closed")
                    allure.attach("Create button disabled. Form closed", name="Create Tasks Error", attachment_type=allure.attachment_type.TEXT)
                wait_for_loader_to_disappear(driver, wait)
    except Exception as err:
        allure.attach(str(err), name="Validation Handling Error", attachment_type=allure.attachment_type.TEXT)
        print(f"❌ Error handling validation: {err}")

    try:
        with allure.step("➡️ Checking for toast message"):
            try:
                toast_msg_elem = wait.until(EC.presence_of_element_located((By.XPATH, toast_msg)))
                highlight_element(driver, toast_msg_elem)
                msg = toast_msg_elem.text
                print(f"✅ Toast message displayed: {msg}")
                wait.until(EC.invisibility_of_element_located((By.XPATH, toast_msg)))
                wait_for_loader_to_disappear(driver, wait)
            except TimeoutException:
                print("ℹ️ No toast message found")
            except Exception as e:
                allure.attach(str(e), name="Toast Error", attachment_type=allure.attachment_type.TEXT)
                print(f"❌ Error fetching toast: {e}")
    except Exception as err:
        allure.attach(str(err), name="Toast Handling Error", attachment_type=allure.attachment_type.TEXT)
        print(f"❌ Unexpected error while handling toast: {err}")

    # --------------------------
    # Search Task
    # --------------------------
    try:
        with allure.step("➡️ Searching Task"):
            perform_search(driver, wait, task_name)
            wait_for_loader_to_disappear(driver, wait)
            print("✅ Search executed")
    except Exception as err:
        allure.attach(str(err), name="Search Error", attachment_type=allure.attachment_type.TEXT)
        print(f"❌ Error performing search: {err}")

    try:
        with allure.step("➡️ Opening task from table"):
            task_open_btn_elem = wait.until(
                EC.element_to_be_clickable((By.XPATH, task_open_btn))
            )
            highlight_element(driver, task_open_btn_elem)
            try:
                task_open_btn_elem.click()
            except Exception:
                driver.execute_script("arguments[0].scrollIntoView(true);", task_open_btn_elem)
                driver.execute_script("arguments[0].click();", task_open_btn_elem)
            print("✅ Task opened from table")
            time.sleep(1)
            wait_for_loader_to_disappear(driver, wait)
    except Exception as err:
        allure.attach(str(err), name="Task Open Error", attachment_type=allure.attachment_type.TEXT)
        print(f"❌ Error opening task: {err}")

    try:
        with allure.step("➡️ Closing task window"):
            task_close_btn_elem = wait.until(EC.presence_of_element_located((By.XPATH, task_close_btn)))
            highlight_element(driver, task_close_btn_elem)
            task_close_btn_elem.click()
            wait_for_loader_to_disappear(driver, wait)
            print("✅ Task closed")
    except Exception as err:
        allure.attach(str(err), name="Task Close Error", attachment_type=allure.attachment_type.TEXT)
        print(f"❌ Error closing task: {err}")

    try:
        with allure.step("➡️ Clearing search input"):
            clear_search(driver, wait)
            time.sleep(2)
            wait_for_loader_to_disappear(driver, wait)
            print("✅ Search cleared")
    except Exception as err:
        allure.attach(str(err), name="Clear Search Error", attachment_type=allure.attachment_type.TEXT)
        print(f"❌ Error clearing search: {err}")

    return True
