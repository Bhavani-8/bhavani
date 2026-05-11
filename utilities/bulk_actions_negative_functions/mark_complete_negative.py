import pytest
import os
import json
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from utilities.other_utils_functions.highlight import highlight_element
from selenium.webdriver import ActionChains
import pyautogui as pg
import time
import allure
from selenium.common.exceptions import TimeoutException
from utilities.add_task_functions.wait_for_loader_to_disappear import wait_for_loader_to_disappear


try:
    with open(os.path.join("data", 'locators.json'), 'r') as f:
        elements_details = json.load(f)
        dash_col_all_selection_btn = elements_details['dash_col_all_selection_btn']
        dash_bulk_task_dropdown_btn = elements_details['dash_bulk_task_dropdown_btn']
        dash_total_btn = elements_details['dash_total_btn']
        dash_col_selected_label = elements_details['dash_col_selected_label']
        dash_bulk_task_dropdown_form_label = elements_details['dash_bulk_task_dropdown_form_label']
        dash_bulk_task_dropdown_form_input = elements_details['dash_bulk_task_dropdown_form_input']
        dash_bulk_task_dropdown_form_member_confirmation = elements_details['dash_bulk_task_dropdown_form_member_confirmation']
        dash_assign_to_me_tab = elements_details['dash_assign_to_me_tab']
        scroller = elements_details['scroller']
        toast_msg = elements_details['toast_msg']
        error_toast_msg = elements_details['error_toast_msg']

except FileNotFoundError:
    pytest.fail("❌ locators.json file not found")
except json.JSONDecodeError:
    pytest.fail("❌ Invalid JSON in locators.json")


def mark_complete_negative(driver, wait, dropdown_selection_val_data, dropdown_selection_val=None, text_case_id=None):

    wait_less = WebDriverWait(driver, 5)
    with allure.step("Clicking Dashboard Total button"):
        try:
            total_tab = wait.until(EC.element_to_be_clickable((By.XPATH, dash_total_btn)))
            highlight_element(driver, total_tab)
            total_tab.click()
            wait_for_loader_to_disappear(driver, wait)
            print("✅ Clicked Total tab")
        except Exception as err:
            allure.attach(str(err), "Total tab error", allure.attachment_type.TEXT)
            pytest.fail("Failed to click Total tab")
    with allure.step("Select All tasks from task list"):
        try:
            select_all = wait.until(EC.element_to_be_clickable((By.XPATH, dash_col_all_selection_btn)))
            highlight_element(driver, select_all)
            select_all.click()
            wait_for_loader_to_disappear(driver, wait)
            print("✅ Selected all tasks")
        except Exception as err:
            allure.attach(str(err), "Select all error", allure.attachment_type.TEXT)
            pytest.fail("Failed to select all tasks")

    try:
        selected_label = wait.until(EC.presence_of_element_located((By.XPATH, dash_col_selected_label)))
        selected_text = selected_label.text.strip()
        selected_count = int("".join(filter(str.isdigit, selected_text)))
        print(f"Selected count: {selected_count}")
    except Exception as err:
        allure.attach(str(err), "Count fetch error", allure.attachment_type.TEXT)
        pytest.fail("Failed to fetch selected count")

    if selected_count > 100:
        with allure.step(f" Performing bulk action validation for {selected_count} tasks (>100)"):
            print("🔹 Performing bulk action validation for >100 tasks")
        with allure.step("Open Bulk Action and select 'Mark Complete'"): 
            bulk_dd = wait.until(EC.element_to_be_clickable((By.XPATH, dash_bulk_task_dropdown_btn)))
            highlight_element(driver, bulk_dd)
            bulk_dd.click()

            mark_complete = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@class,'dx-list-item-content') and text()='Mark Complete']")))
            highlight_element(driver, mark_complete)
            mark_complete.click()
        with allure.step("Verify toast notifications"):
            try:
                toast = wait.until(EC.presence_of_element_located((By.XPATH,f"{toast_msg} | {error_toast_msg}")))
                highlight_element(driver, toast)
                toast_class = toast.get_attribute("class")
                if "Toastify__toast--success" in toast_class:
                    print(f"❌ Success Toast shown unexpectedly: {toast.text.strip()}")
                    return True   # ❌ BUG FOUND
                elif "Toastify__toast--error" in toast_class:
                    print(f"✅ Error Toast shown as expected: {toast.text.strip()}")
                    return False  # ✅ EXPECTED
            except TimeoutException:
                print("❌ No toast found — unexpected behavior")
    return True
    