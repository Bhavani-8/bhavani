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




def export_data_validation(driver, wait):
    
    with allure.step("Load locators.json for Export Data Validation"):
        try:
            with open(os.path.join("data", 'locators.json'), 'r') as f:
                elements_details = json.load(f)
                toast_msg = elements_details['toast_msg']
                error_toast_msg = elements_details['error_toast_msg']
            print("✅ locators.json loaded successfully")
        except FileNotFoundError as e:
            print("❌ locators.json file not found")
            allure.attach(str(e), name="Locators_FileNotFound", attachment_type=allure.attachment_type.TEXT)
            pytest.fail("locators.json file not found")
        except json.JSONDecodeError as e:
            print("❌ Invalid JSON format in locators.json")
            allure.attach(str(e), name="Invalid_JSON", attachment_type=allure.attachment_type.TEXT)
            pytest.fail("Invalid JSON in locators.json")

    with allure.step("Attempt to Export All Team Performance Data"):
        try:
            wait.until(EC.invisibility_of_element_located((By.XPATH, toast_msg)))
            export_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@role='button' and @aria-label='Export all data']")))
            highlight_element(driver, export_btn)
            export_btn.click()
            print("📤 Clicked on 'Export All Data' button")
            wait_for_loader_to_disappear(driver, wait)
           
        except Exception as e:
            print("❌ Export Team Performance Data action failed.")
            allure.attach(str(e), name="Export_Failure", attachment_type=allure.attachment_type.TEXT)
            raise
    
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
