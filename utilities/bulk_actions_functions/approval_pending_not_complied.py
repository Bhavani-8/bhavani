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





def approval_not_complied_bulk_action(driver, wait):
    wait_less = WebDriverWait(driver, 5)
    try:
        with open(os.path.join("data", 'locators.json'), 'r') as f:
            elements_details = json.load(f)
            dash_approval_pending_btn = elements_details['dash_approval_pending_btn']
            dash_approval_pending_by_me = elements_details['dash_approval_pending_by_me']
            dash_bulk_task_dropdown_btn = elements_details['dash_bulk_task_dropdown_btn']
            toast_msg = elements_details['toast_msg']
            error_toast_msg = elements_details['error_toast_msg']
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

    with allure.step("Clicking Approval Pending Tab"):
        try:
    
            wait_for_loader_to_disappear(driver, wait)
            approval_pending_tab = wait.until(EC.presence_of_element_located((By.XPATH, dash_approval_pending_btn)))
            highlight_element(driver, approval_pending_tab)
            driver.execute_script("arguments[0].click();", approval_pending_tab)
            wait_for_loader_to_disappear(driver, wait)
            print("✅ Clicked Approval Pending tab")
        except Exception as e:
            msg = f"Failed to click Approval Pending tab: {str(e)}"
            print(msg)
            allure.attach(msg, name="Approval Pending tab Error", attachment_type=allure.attachment_type.TEXT)
            raise Exception(msg)
    with allure.step("Clicking Approval Pending by me"):
        try:
            approval_pending_by_me_tab = wait_less.until(EC.presence_of_element_located((By.XPATH, dash_approval_pending_by_me)))
            approval_pending_by_me_tab.click()
            highlight_element(driver,  approval_pending_by_me_tab)
            time.sleep(3)           
            wait_for_loader_to_disappear(driver, wait)
        except Exception as e:
            msg = f"Failed to click Approval Pending By me tab: {str(e)}"
            print(msg)
            allure.attach(msg, name="Approval Pending By me tab Error", attachment_type=allure.attachment_type.TEXT)
            raise Exception(msg)

    with allure.step("Select first task from task list"):
        try:
            first_checkbox = wait.until(EC.presence_of_element_located((By.XPATH, "(//td[@aria-colindex='1']//span[contains(@class,'dx-checkbox-icon')])[2]")))
            first_checkbox.click()
        except Exception as e:
            msg = f"Failed to Selecting first task: {str(e)}"
            print(msg)
            allure.attach(msg, name="Selecting first task Error", attachment_type=allure.attachment_type.TEXT)
            raise Exception(msg)

    with allure.step("Open Bulk Action dropdown"):
        try:
            bulk_dd = wait.until(EC.element_to_be_clickable((By.XPATH, dash_bulk_task_dropdown_btn)))
            highlight_element(driver, bulk_dd)
            bulk_dd.click()

            not_complied_option = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='dx-item-content dx-list-item-content' and text()='Not Complied']")))
            highlight_element(driver, not_complied_option)
            not_complied_option.click()
        except Exception as e:
            msg = f"Failed to Click Bulk action Dropdown: {str(e)}"
            print(msg)
            allure.attach(msg, name="Bulk action Error", attachment_type=allure.attachment_type.TEXT)
            raise Exception(msg)
    with allure.step("Click Confirm button"):
        try:
            confirm_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[.//span[normalize-space()='Confirm']]")))
            highlight_element(driver, confirm_btn)
            confirm_btn.click()
            time.sleep(2)
            print("✅ Confirm button clicked")
        except Exception as e:
            msg = f"Failed to Click Confirm Button : {str(e)}"
            print(msg)
            allure.attach(msg, name="Confirm Button Error", attachment_type=allure.attachment_type.TEXT)
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


    return True

