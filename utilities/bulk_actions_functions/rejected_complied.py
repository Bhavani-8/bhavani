import pytest
import os
import json
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from utilities.other_utils_functions.highlight import highlight_element
import pyautogui as pg
import time
import allure
from selenium.common.exceptions import TimeoutException
from utilities.add_task_functions.wait_for_loader_to_disappear import wait_for_loader_to_disappear
from selenium.common.exceptions import StaleElementReferenceException


try:
    with open(os.path.join("data", 'locators.json'), 'r') as f:
        elements_details = json.load(f)
        dash_rejected_task_btn = elements_details['dash_rejected_task_btn']
        dash_bulk_task_dropdown_btn = elements_details['dash_bulk_task_dropdown_btn']
        notification_icon = elements_details['notification_icon']
        dash_assign_to_others_tab = elements_details['dash_assign_to_others_tab']
        toast_msg = elements_details['toast_msg']
        error_toast_msg = elements_details['error_toast_msg']
        task_open_btn = elements_details['task_open_btn']
        select_first_checkbox = elements_details['select_first_checkbox']
        dash_bulk_options_complied = elements_details['dash_bulk_options_complied']
        dash_bulk_options_confirm_btn = elements_details['dash_bulk_options_confirm_btn']
        dash_bulk_options_cancel_btn = elements_details['dash_bulk_options_cancel_btn']


except FileNotFoundError:
    pytest.fail("❌ locators.json file not found")
except json.JSONDecodeError:
    pytest.fail("❌ Invalid JSON in locators.json")

def rejected_complied_bulk_action(driver, wait):
    wait_less = WebDriverWait(driver, 5)
    with allure.step("Clicking Rejected button"):
        try:
            rejected_task_tab = wait.until(EC.presence_of_element_located((By.XPATH, dash_rejected_task_btn)))
            highlight_element(driver, rejected_task_tab)
            driver.execute_script("arguments[0].click();", rejected_task_tab)
            wait_for_loader_to_disappear(driver, wait)
            print("✅ Clicked rejected task tab")
        except Exception as err:
            allure.attach(str(err), "Approval Pending tab error", allure.attachment_type.TEXT)
            pytest.fail("Failed to click Approval Pending tab")
    with allure.step("➡️ Clicking Assigned To Others"):
        assigned_to_others_btn_tab = wait_less.until(EC.presence_of_element_located((By.XPATH, dash_assign_to_others_tab)))
        assigned_to_others_btn_tab.click()
        highlight_element(driver, assigned_to_others_btn_tab)
        time.sleep(3)           
        wait_for_loader_to_disappear(driver, wait)
    with allure.step("Select first task from task list"):
        first_checkbox = wait.until(EC.presence_of_element_located((By.XPATH, select_first_checkbox)))
        first_checkbox.click()

    with allure.step("Open Bulk Action and select 'Complied'"):
        bulk_dd = wait.until(EC.element_to_be_clickable((By.XPATH, dash_bulk_task_dropdown_btn)))
        highlight_element(driver, bulk_dd)
        bulk_dd.click()

        complied_option = wait.until(EC.element_to_be_clickable((By.XPATH, dash_bulk_options_complied)))
        highlight_element(driver, complied_option)
        complied_option.click()

    try:
        confirm_btn = wait.until(EC.element_to_be_clickable((By.XPATH, dash_bulk_options_confirm_btn)))
        highlight_element(driver, confirm_btn)
        confirm_btn.click()
        print("✅ Confirm button clicked")
    except Exception as e:
        print("ℹ️ Confirm button not available / not clickable")
        cancel_btn = wait.until(EC.element_to_be_clickable((By.XPATH, dash_bulk_options_cancel_btn)))
        highlight_element(driver, cancel_btn)
        cancel_btn.click()
        print("✅ Cancel button clicked")

    try:
        toast = wait.until(EC.presence_of_element_located((By.XPATH,f"{toast_msg} | {error_toast_msg}")))
        highlight_element(driver, toast)
        toast_class = toast.get_attribute("class")
        if "Toastify__toast--success" in toast_class:
            print(f"📢 Success Toast: {toast.text.strip()}")
        elif "Toastify__toast--error" in toast_class:
            print(f"❌ Error Toast: {toast.text.strip()}")
    except TimeoutException:
        print("ℹ️ No toast found")
    
    return True

