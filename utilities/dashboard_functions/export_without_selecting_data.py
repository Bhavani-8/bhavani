import pytest
import os
import json
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from utilities.other_utils_functions.highlight import highlight_element
import pyautogui as pg
import time
from selenium.common.exceptions import TimeoutException
from utilities.add_task_functions.wait_for_loader_to_disappear import wait_for_loader_to_disappear


def export_without_selecting_data(driver, wait, dash_type):
    wait_less = WebDriverWait(driver, 5)

    # ✅ Load locators
    with allure.step("Load locators.json for Export Data Validation"):
        try:
            with open(os.path.join("data", 'locators.json'), 'r') as f:
                elements_details = json.load(f)
                dash_total_btn = elements_details['dash_total_btn']
                error_toast_msg = elements_details['error_toast_msg']
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
            dash_total_btn_elem.click()
            wait_for_loader_to_disappear(driver, wait)
            print("✅ Clicked on Total Button")
        except Exception as e:
            print("❌ Failed to click on Total Button")
            allure.attach(str(e), name="Total_Button_Error", attachment_type=allure.attachment_type.TEXT)
            raise

    # ✅ Try Export → Selected Rows (without selecting any row)
    with allure.step("Attempt Export of Selected Rows without selecting any row"):
        try:
            wait.until(EC.invisibility_of_element_located((By.XPATH, toast_msg)))
            export_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//i[contains(@class,'dx-icon-export-to')]")))
            export_btn.click()
            export_selected_rows = wait_less.until(EC.element_to_be_clickable((By.XPATH, export_selected_rows_btn)))
            export_selected_rows.click()
            wait_for_loader_to_disappear(driver, wait)

            try:
                toast = wait.until(EC.presence_of_element_located((By.XPATH, f"{toast_msg} | {error_toast_msg}")))
                highlight_element(driver, toast)
                toast_class = toast.get_attribute("class")
                if "Toastify__toast--success" in toast_class:
                    print(f"❌ Success Toast shown unexpectedly: {toast.text.strip()}")
                    return False  # ❌ BUG FOUND

                elif "Toastify__toast--error" in toast_class:
                    print(f"✅ Error Toast shown as expected: {toast.text.strip()}")
                    return True  # ✅ EXPECTED

            except TimeoutException:
                print("❌ No toast found — unexpected behavior")
                return False

        except Exception as e:
            print("❌ Export attempt without selection failed")
            allure.attach(str(e), name="Export_Without_Selection_Error",
                        attachment_type=allure.attachment_type.TEXT)
            return True

   
    
