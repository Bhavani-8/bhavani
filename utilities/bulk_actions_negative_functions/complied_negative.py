import pytest
import os
import json
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from utilities.other_utils_functions.highlight import highlight_element
import time
import allure
from selenium.common.exceptions import TimeoutException
from utilities.add_task_functions.wait_for_loader_to_disappear import wait_for_loader_to_disappear



def complied_negative(driver, wait, dropdown_selection_val_data, dropdown_selection_val=None, text_case_id=None):

    try:
        with open(os.path.join("data", 'locators.json'), 'r') as f:
            elements_details = json.load(f)
            dash_col_all_selection_btn = elements_details['dash_col_all_selection_btn']
            dash_bulk_task_dropdown_btn = elements_details['dash_bulk_task_dropdown_btn']
            dash_total_btn = elements_details['dash_total_btn']
            dash_col_selected_label = elements_details['dash_col_selected_label']
            toast_msg = elements_details['toast_msg']  
            dash_bulk_options_complied = elements_details['dash_bulk_options_complied']
    except FileNotFoundError as e:
        msg = f"locators.json file not found: {str(e)}"
        print(msg)
        allure.attach(msg, name="Locators File Missing", attachment_type=allure.attachment_type.TEXT)
        return False
    except json.JSONDecodeError as e:
        msg = f"Invalid JSON in locators.json: {str(e)}"
        print(msg)
        allure.attach(msg, name="Locators JSON Error", attachment_type=allure.attachment_type.TEXT)
        return False
    wait_less = WebDriverWait(driver, 5)
    with allure.step("Clicking Dashboard Total button"):
        try:
            total_tab = wait.until(EC.element_to_be_clickable((By.XPATH, dash_total_btn)))
            highlight_element(driver, total_tab)
            total_tab.click()
            wait_for_loader_to_disappear(driver, wait)
            print("✅ Clicked Total tab")
        except Exception as e:
            msg = f"Failed to Click Total tab: {str(e)}"
            print(msg)
            allure.attach(msg, name="Total tab Error", attachment_type=allure.attachment_type.TEXT)
            raise Exception(msg)
    with allure.step("Select All tasks from task list"):
        try:
            select_all = wait.until(EC.element_to_be_clickable((By.XPATH, dash_col_all_selection_btn)))
            highlight_element(driver, select_all)
            select_all.click()
            wait_for_loader_to_disappear(driver, wait)
            print("✅ Selected all tasks")
        except Exception as e:
            msg = f"Failed to Selecting all from the task list: {str(e)}"
            print(msg)
            allure.attach(msg, name="Selecting all from the task list Error", attachment_type=allure.attachment_type.TEXT)
            raise Exception(msg)

    try:
        selected_label = wait.until(EC.presence_of_element_located((By.XPATH, dash_col_selected_label)))
        selected_text = selected_label.text.strip()
        selected_count = int("".join(filter(str.isdigit, selected_text)))
        print(f"Selected count: {selected_count}")
    except Exception as e:
        msg = f"Failed to fetch selected count: {str(e)}"
        print(msg)
        allure.attach(msg, name="Count fetch Error", attachment_type=allure.attachment_type.TEXT)
        raise Exception(msg)

    if selected_count > 100:
        with allure.step(f" Performing bulk action validation for {selected_count} tasks (>100)"):
            print("🔹 Performing bulk action validation for >100 tasks")
        with allure.step("Open Bulk Action and select 'Complied'"): 
            try: 
                bulk_dd = wait.until(EC.element_to_be_clickable((By.XPATH, dash_bulk_task_dropdown_btn)))
                highlight_element(driver, bulk_dd)
                bulk_dd.click()

                complied = wait.until(EC.element_to_be_clickable((By.XPATH, dash_bulk_options_complied)))
                highlight_element(driver, complied)
                complied.click()
            except Exception as e:
                msg = f"Failed to Click Bulk action Dropdown: {str(e)}"
                print(msg)
                allure.attach(msg, name="Bulk action Error", attachment_type=allure.attachment_type.TEXT)
                raise Exception(msg)
        
        try:
            toast = wait.until(EC.presence_of_element_located((By.XPATH, toast_msg)))
            highlight_element(driver, toast)
            print(f"📢 Toast message: {toast.text.strip()}")
        except Exception as e:
            msg = f"Toast message not found: {str(e)}"
            print(msg)
            allure.attach(str(e), name="Toast message Error", attachment_type=allure.attachment_type.TEXT)
            raise Exception(msg)
    