from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import allure 
import pandas as pd
import pyautogui as pg
import os
import json
import pytest
import time

from utilities.add_task_functions.wait_for_loader_to_disappear import wait_for_loader_to_disappear
from utilities.other_utils_functions.highlight import highlight_element

def issuer_link_downloads(driver, wait):
    wait_less = WebDriverWait(driver, 5)
    # ------------------------------------------
    # STEP 1: LOAD LOCATORS
    # ------------------------------------------
    with allure.step("Load locators.json"):
        try:
            with open(os.path.join("data", 'locators.json'), 'r') as f:
                elements_details = json.load(f)
            print("✅ locators.json loaded successfully")
        except Exception as e:
            allure.attach(str(e), name="Locators Error", attachment_type=allure.attachment_type.TEXT)
            pytest.fail("Failed to load locators.json")

    with allure.step("Select Update Checkbox"):
        try:
            select_elem = wait.until(EC.presence_of_element_located((By.XPATH, "(//div[@class='flex flex-col min-w-0 flex-1 gap-1'])[5]")))
            highlight_element(driver, select_elem)
            select_elem.click()
            print("🟦 First checkbox clicked")
            time.sleep(2)
        except Exception as e:
            allure.attach(str(e), name="Updates Section Error", attachment_type=allure.attachment_type.TEXT)
            return False
        
    with allure.step("Click on Issuer Link"):
        try:
            main_window = driver.current_window_handle
            issuer_link = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[text()='Issuer Link']")))
            highlight_element(driver, issuer_link)
            issuer_link.click()
            time.sleep(2)
            print("🟦 Issuer Link clicked")
             # Get all windows
            all_windows = driver.window_handles

            # Switch to new window
            for window in all_windows:
                if window != main_window:
                    driver.switch_to.window(window)
                    print("🟢 Switched to new window")
                    break

            time.sleep(3)
             # Close new window
            driver.close()
            print("🔴 New window closed")

            # Switch back to main window
            driver.switch_to.window(main_window)
            print("🟡 Switched back to main window")
        except Exception as e:
            allure.attach(str(e), name="Issuer Link Click Error", attachment_type=allure.attachment_type.TEXT)
            return False

    with allure.step("Click on the Download File"):
        try:
            downloads = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Download Files']")))
            highlight_element(driver, downloads)
            downloads.click()
            time.sleep(2)
            print("🟦 Downloads button clicked")
        except Exception as e:
            print("❌ Failed to click downloads button")
            allure.attach(str(e), name="Export_Selected_After_Error", attachment_type=allure.attachment_type.TEXT)
            return False
    
    return True