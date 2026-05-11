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
def export_all_data(driver, wait, dash_type):
    wait_less = WebDriverWait(driver, 5)

    # ✅ Load locators
    with allure.step("Load locators.json for Export Data Validation"):
        try:
            with open(os.path.join("data", 'locators.json'), 'r') as f:
                elements_details = json.load(f)
                dash_total_btn = elements_details['dash_total_btn']
                dash_col_all_selection_btn = elements_details['dash_col_all_selection_btn']
                export_btn = elements_details['export_btn']
                export_all_data_btn = elements_details['export_all_data_btn']
                export_selected_rows_btn = elements_details['export_selected_rows_btn']
                toast_msg = elements_details['toast_msg']
            print("✅ locators.json loaded successfully")
        except FileNotFoundError as e:
            print("❌ locators.json file not found")
            allure.attach(str(e), name="Locators_FileNotFound", attachment_type=allure.attachment_type.TEXT)
            pytest.fail("locators.json file not found")
        except json.JSONDecodeError as e:
            print("❌ Invalid JSON in locators.json")
            allure.attach(str(e), name="Invalid_JSON", attachment_type=allure.attachment_type.TEXT)
            pytest.fail("Invalid JSON in locators.json")

    # ✅ Click Total Button
    with allure.step("Click on Total Button"):
        try:
            wait.until(EC.invisibility_of_element_located((By.XPATH, toast_msg)))
            dash_total_btn_elem = wait.until(EC.presence_of_element_located((By.XPATH, dash_total_btn)))
            highlight_element(driver, dash_total_btn_elem)
            dash_total_btn_elem.click()
            wait_for_loader_to_disappear(driver, wait)
            print("✅ Clicked on Total Button")
        except Exception as e:
            print("❌ Failed to click on Total Button")
            allure.attach(str(e), name="Total_Button_Error", attachment_type=allure.attachment_type.TEXT)
            raise

    # ✅ Export → All Data
    with allure.step("Export All Data from Dashboard"):
        try:
            export_data_btn = wait_less.until(EC.presence_of_element_located((By.XPATH, export_btn)))
            export_data_btn.click()
            export_all = wait_less.until(EC.presence_of_element_located((By.XPATH, export_all_data_btn)))
            export_all.click()
            print("✅ Exported All Data")
            wait_for_loader_to_disappear(driver, wait)
            time.sleep(12)
        except Exception as e:
            print("❌ Failed to export all data")
            allure.attach(str(e), name="Export_All_Error", attachment_type=allure.attachment_type.TEXT)
            raise
    
    # ✅ Select All Rows
    with allure.step("Select all rows in Dashboard Table"):
        try:
            dash_col_all_selection_btn_elem = wait.until(EC.presence_of_element_located((By.XPATH, dash_col_all_selection_btn)))
            highlight_element(driver, dash_col_all_selection_btn_elem)
            dash_col_all_selection_btn_elem.click()
            print("✅ Selected all rows in Dashboard")
            time.sleep(15)
            wait_for_loader_to_disappear(driver, wait)
        except Exception as e:
            print("❌ Failed to select all rows in Dashboard")
            allure.attach(str(e), name="Select_All_Error", attachment_type=allure.attachment_type.TEXT)
            raise
    
    
    # ✅ Export → Selected Rows (after selection)
    with allure.step("Export Selected Rows after selecting rows"):
        try:
            wait_for_loader_to_disappear(driver, wait)
            time.sleep(10)
            export_data_btn = wait_less.until(EC.presence_of_element_located((By.XPATH, export_btn)))
            export_data_btn.click()
            export_selected_rows = wait_less.until(EC.presence_of_element_located((By.XPATH, export_selected_rows_btn)))
            export_selected_rows.click()
            print("✅ Exported Selected Rows (after selecting rows)")
            pg.press('esc')
            wait_for_loader_to_disappear(driver, wait)
            time.sleep(5)  # wait for download to complete
            pg.press('esc')
            return True
        except Exception as e:
            print("❌ Failed to export selected rows after selection")
            allure.attach(str(e), name="Export_Selected_After_Error", attachment_type=allure.attachment_type.TEXT)
            return False

