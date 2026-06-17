import time
import pytest
import os
import json
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from utilities.other_utils_functions.highlight import highlight_element
import pyautogui as pg
from selenium.common.exceptions import TimeoutException
from utilities.add_task_functions.wait_for_loader_to_disappear import wait_for_loader_to_disappear


def department_export_all_data(driver, wait):
   

    # ✅ Load locators
    with allure.step("Load locators.json for Export Data Validation"):
        try:
            with open(os.path.join("data", 'locators.json'), 'r') as f:
                elements_details = json.load(f)
                settings_icon = elements_details["settings_icon"]
            
            print("✅ locators.json loaded successfully")
        except FileNotFoundError as e:
            print("❌ locators.json file not found")
            allure.attach(str(e), name="Locators_FileNotFound", attachment_type=allure.attachment_type.TEXT)
            pytest.fail("locators.json file not found")
        except json.JSONDecodeError as e:
            print("❌ Invalid JSON in locators.json")
            allure.attach(str(e), name="Invalid_JSON", attachment_type=allure.attachment_type.TEXT)
            pytest.fail("Invalid JSON in locators.json")

    
    with allure.step("Click Settings"):
        try:
            settings_btn = wait.until(EC.presence_of_element_located((By.XPATH, settings_icon)))
            highlight_element(driver, settings_btn)
            settings_btn.click()
        except TimeoutException:
            print("ℹ️ Settings Failed")

    with allure.step("Click on Department"):
        try:
            department_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[normalize-space()='Department']")))
            highlight_element(driver, department_btn)
            department_btn.click()
        except TimeoutException:
            print("ℹ️ Department Failed")
    wait_for_loader_to_disappear(driver, wait)
    time.sleep(2)

    # ✅ Export → All Data
    with allure.step("Export All Data from Dashboard"):
        try:
            export_data_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "(//button[@data-slot='dropdown-menu-trigger'])[1]")))
            export_data_btn.click()
            export_all = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[text()='Export all data']")))
            export_all.click()
            print("✅ Exported All Data")
            wait_for_loader_to_disappear(driver, wait)
            time.sleep(3)
        except Exception as e:
            print("❌ Failed to export all data")
            allure.attach(str(e), name="Export_All_Error", attachment_type=allure.attachment_type.TEXT)
            raise
    # ✅ Select All Rows
    with allure.step("Select all rows in Dashboard Table"):
        try:
            dash_col_all_selection_btn_elem = wait.until(EC.element_to_be_clickable((By.XPATH, "//th//span[@role='checkbox']")))
            highlight_element(driver, dash_col_all_selection_btn_elem)
            dash_col_all_selection_btn_elem.click()
            print("✅ Selected all rows in Dashboard")
            time.sleep(3)
            wait_for_loader_to_disappear(driver, wait)
        except Exception as e:
            print("❌ Failed to select all rows in Dashboard")
            allure.attach(str(e), name="Select_All_Error", attachment_type=allure.attachment_type.TEXT)
            raise
    
    # ✅ Export → Selected Rows (after selection)
    with allure.step("Export Selected Rows after selecting rows"):
        try:
            wait_for_loader_to_disappear(driver, wait)
            time.sleep(2)
            export_data_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "(//button[@data-slot='dropdown-menu-trigger'])[1]")))
            export_data_btn.click()
            export_selected_rows = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@role='menuitem' and contains(text(),'Export selected rows')]")))
            export_selected_rows.click()
            print("✅ Exported Selected Rows (after selecting rows)")
            pg.press('esc')
            wait_for_loader_to_disappear(driver, wait)
            time.sleep(3)  # wait for download to complete
            pg.press('esc')
            return True
        except Exception as e:
            print("❌ Failed to export selected rows after selection")
            allure.attach(str(e), name="Export_Selected_After", attachment_type=allure.attachment_type.TEXT)
            raise

