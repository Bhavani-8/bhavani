import time
import pytest
import os
import json
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from utilities.other_utils_functions.highlight import highlight_element
from utilities.add_task_functions.wait_for_loader_to_disappear import wait_for_loader_to_disappear


def project_export_all_data(driver, wait):
    wait_less = WebDriverWait(driver, 5)

    # ✅ Load locators
    with allure.step("Load locators.json for Export Data Validation"):
        try:
            with open(os.path.join("data", 'locators.json'), 'r') as f:
                elements_details = json.load(f)
                export_all_data_btn = elements_details['export_all_data_btn']
                project_icon = elements_details["project_icon"]
            print("✅ locators.json loaded successfully")
        except FileNotFoundError as e:
            print("❌ locators.json file not found")
            allure.attach(str(e), name="Locators_FileNotFound", attachment_type=allure.attachment_type.TEXT)
            pytest.fail("locators.json file not found")
        except json.JSONDecodeError as e:
            print("❌ Invalid JSON in locators.json")
            allure.attach(str(e), name="Invalid_JSON", attachment_type=allure.attachment_type.TEXT)
            pytest.fail("Invalid JSON in locators.json")

    with allure.step("Click project icon"):
        try:
            project_btn = wait.until(EC.presence_of_element_located((By.XPATH, project_icon)))
            highlight_element(driver, project_btn)
            project_btn.click()
            time.sleep(2)
        
        except Exception as e:
            msg = f"Failed to Click Project Icon: {str(e)}"
            print(msg)
            allure.attach(msg, name="Project Icon Error", attachment_type=allure.attachment_type.TEXT)
            raise Exception(msg)

    # ✅ Export → All Data
    with allure.step("Export All Data from Dashboard"):
        try:
            export_all = wait_less.until(EC.presence_of_element_located((By.XPATH, export_all_data_btn)))
            export_all.click()
            print("✅ Exported All Data")
            wait_for_loader_to_disappear(driver, wait)
            time.sleep(3)
            return True
        except Exception as e:
            print("❌ Failed to export all data")
            allure.attach(str(e), name="Export_All_Error", attachment_type=allure.attachment_type.TEXT)
            raise Exception(msg)
  
    
