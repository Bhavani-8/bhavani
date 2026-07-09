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




def rejected_complied_bulk_action(driver, wait):
    wait_less = WebDriverWait(driver, 5)
    try:
        with open(os.path.join("data", 'locators.json'), 'r') as f:
            elements_details = json.load(f)
            dash_rejected_task_btn = elements_details['dash_rejected_task_btn']
            dash_bulk_task_dropdown_btn = elements_details['dash_bulk_task_dropdown_btn']
            dash_assign_to_others_tab = elements_details['dash_assign_to_others_tab']
            toast_msg = elements_details['toast_msg']
            select_first_checkbox = elements_details['select_first_checkbox']
            dash_bulk_options_complied = elements_details['dash_bulk_options_complied']
            dash_bulk_options_confirm_btn = elements_details['dash_bulk_options_confirm_btn']

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
    with allure.step("Clicking Rejected button"):
        try:
            rejected_task_tab = wait.until(EC.presence_of_element_located((By.XPATH, dash_rejected_task_btn)))
            highlight_element(driver, rejected_task_tab)
            driver.execute_script("arguments[0].click();", rejected_task_tab)
            wait_for_loader_to_disappear(driver, wait)
            print("✅ Clicked rejected task tab")
        except Exception as e:
            msg = f"Failed to Click Rejected Task tab: {str(e)}"
            print(msg)
            allure.attach(msg, name="Rejected Task tab Error", attachment_type=allure.attachment_type.TEXT)
            raise Exception(msg)
    with allure.step("➡️ Clicking Assigned To Others"):
        try:
            assigned_to_others_btn_tab = wait_less.until(EC.presence_of_element_located((By.XPATH, dash_assign_to_others_tab)))
            assigned_to_others_btn_tab.click()
            highlight_element(driver, assigned_to_others_btn_tab)
            time.sleep(3)           
            wait_for_loader_to_disappear(driver, wait)
        except Exception as e:
            msg = f"Failed to click Assigned to Others tab: {str(e)}"
            print(msg)
            allure.attach(msg, name="Assigned to Others tab Error", attachment_type=allure.attachment_type.TEXT)
            raise Exception(msg)
    with allure.step("Select first task from task list"):
        try:
            first_checkbox = wait.until(EC.presence_of_element_located((By.XPATH, select_first_checkbox)))
            first_checkbox.click()
            time.sleep(2)
        except Exception as e:
            msg = f"Failed to Selecting first task: {str(e)}"
            print(msg)
            allure.attach(msg, name="Selecting first task Error", attachment_type=allure.attachment_type.TEXT)
            raise Exception(msg)

    with allure.step("Open Bulk Action and select 'Complied'"):
        try:
            bulk_dd = wait.until(EC.element_to_be_clickable((By.XPATH, dash_bulk_task_dropdown_btn)))
            highlight_element(driver, bulk_dd)
            bulk_dd.click()

            complied_option = wait.until(EC.element_to_be_clickable((By.XPATH, dash_bulk_options_complied)))
            highlight_element(driver, complied_option)
            complied_option.click()
        except Exception as e:
            msg = f"Failed to Click Bulk action Dropdown: {str(e)}"
            print(msg)
            allure.attach(msg, name="Bulk action Error", attachment_type=allure.attachment_type.TEXT)
            raise Exception(msg)

    try:
        confirm_btn = wait.until(EC.element_to_be_clickable((By.XPATH, dash_bulk_options_confirm_btn)))
        highlight_element(driver, confirm_btn)
        confirm_btn.click()
        print("✅ Confirm button clicked")
    except Exception as e:
        msg = f"Failed to Click Confirm Button: {str(e)}"
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

