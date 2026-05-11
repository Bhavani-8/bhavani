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
from selenium.common.exceptions import StaleElementReferenceException



try:
    with open(os.path.join("data", 'locators.json'), 'r') as f:
        elements_details = json.load(f)
        dash_total_btn = elements_details['dash_total_btn']
        dash_approval_pending_btn = elements_details['dash_approval_pending_btn']
        dash_approval_pending_by_me = elements_details['dash_approval_pending_by_me']
        dash_bulk_task_dropdown_btn = elements_details['dash_bulk_task_dropdown_btn']
        notification_icon = elements_details['notification_icon']
        task_open_btn = elements_details['task_open_btn']
        toast_msg = elements_details['toast_msg']
        error_toast_msg = elements_details['error_toast_msg']
except FileNotFoundError:
    pytest.fail("❌ locators.json file not found")
except json.JSONDecodeError:
    pytest.fail("❌ Invalid JSON in locators.json")

def approval_complied_bulk_action(driver, wait, dropdown_selection_val_data, dropdown_selection_val=None, test_case_id=None):
    wait_less = WebDriverWait(driver, 5)

    try:
        wait_for_loader_to_disappear(driver, wait)
        approval_pending_tab = wait.until(EC.presence_of_element_located((By.XPATH, dash_approval_pending_btn)))
        highlight_element(driver, approval_pending_tab)
        driver.execute_script("arguments[0].click();", approval_pending_tab)
        wait_for_loader_to_disappear(driver, wait)
        print("✅ Clicked Approval Pending tab")
    except Exception as err:
        allure.attach(str(err), "Approval Pending tab error", allure.attachment_type.TEXT)
        pytest.fail("Failed to click Approval Pending tab")

    approval_pending_by_me_tab = wait_less.until(EC.presence_of_element_located((By.XPATH, dash_approval_pending_by_me)))
    approval_pending_by_me_tab.click()
    highlight_element(driver,  approval_pending_by_me_tab)
    time.sleep(3)           
    wait_for_loader_to_disappear(driver, wait)

    first_checkbox = wait.until(EC.presence_of_element_located((By.XPATH, "(//td[@aria-colindex='1']//span[contains(@class,'dx-checkbox-icon')])[2]")))
    first_checkbox.click()

    # Open bulk dropdown
    bulk_dd = wait.until(EC.element_to_be_clickable((By.XPATH, dash_bulk_task_dropdown_btn)))
    highlight_element(driver, bulk_dd)
    bulk_dd.click()

    complied_option = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='dx-item-content dx-list-item-content' and text()='Complied']")))
    highlight_element(driver, complied_option)
    complied_option.click()

    try:
        confirm_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[.//span[normalize-space()='Confirm']]")))
        highlight_element(driver, confirm_btn)
        confirm_btn.click()
        time.sleep(2)
        print("✅ Confirm button clicked")
    except Exception as e:
        print("ℹ️ Confirm button not available / not clickable")
        cancel_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[.//span[normalize-space()='Cancel']]")))
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

