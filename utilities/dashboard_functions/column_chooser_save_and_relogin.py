from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import pyautogui as pg
import allure
import pytest
import json
import time
import os
import pandas as pd
from utilities.add_task_functions.wait_for_loader_to_disappear import wait_for_loader_to_disappear
from utilities.other_utils_functions.highlight import highlight_element
from utilities.login_utils import login_check




def column_chooser_relogin(driver, wait):

    wait_less = WebDriverWait(driver, 5)
    
    try:
        with open(os.path.join("data", "locators.json"), "r") as f:
            locators = json.load(f)

        dash_total_btn = locators["dash_total_btn"]
        toast_msg = locators["toast_msg"]
        logout_icon = locators["logout_icon"]
        column_chooser_btn = locators["column_chooser_btn"]
        select_all_checkbox = locators["select_all_checkbox"]
        column_chooser_save_btn = locators["column_chooser_save_btn"]
    except FileNotFoundError:
        pytest.fail("❌ locators.json file not found")
    except json.JSONDecodeError:
        pytest.fail("❌ Invalid JSON in locators.json")

    with allure.step("Clicking Dashboard Total button"):       
        total_btn = wait.until(EC.element_to_be_clickable((By.XPATH, dash_total_btn)))
        highlight_element(driver, total_btn)
        total_btn.click()
        wait_for_loader_to_disappear(driver, wait)
        print("✅ Clicked Dashboard Total tab")

    with allure.step("Open Column Chooser"):
        chooser_btn = wait.until(EC.element_to_be_clickable((By.XPATH, column_chooser_btn)))
        highlight_element(driver, chooser_btn)
        chooser_btn.click()
        wait_for_loader_to_disappear(driver, wait)
        print("✅ Opened Column Chooser")

    with allure.step("Select all columns in Column Chooser"):
        select_all = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, select_all_checkbox)))
        if select_all.get_attribute("aria-checked") != "true":
            driver.execute_script("arguments[0].click();", select_all)
            print("☑️ Selected all columns")
        else:
            print("✅ Select All already enabled")

        save_btn = wait.until(EC.element_to_be_clickable((By.XPATH, column_chooser_save_btn)))
        highlight_element(driver, save_btn)
        save_btn.click()
        
        toast = wait.until(EC.presence_of_element_located((By.XPATH, toast_msg)))
        print(f"📢 Toast: {toast.text.strip()}")

    with allure.step("Verify column headers before logout"):
        headers = wait.until(EC.presence_of_all_elements_located((By.XPATH,"//tr[contains(@class,'dx-header-row')]//td[@aria-label]")))
        before_columns = [h.get_attribute("aria-label").strip() for h in headers]
        print(f"📊 Columns BEFORE logout: {before_columns}")
        allure.attach(str(before_columns),name="Columns Before Logout",attachment_type=allure.attachment_type.TEXT)

    with allure.step("Logout from application"):
        pg.hotkey("ctrl", "-")
        pg.hotkey("ctrl", "-")
        time.sleep(1)

        logout_btn = wait.until(EC.element_to_be_clickable((By.XPATH, logout_icon)))
        highlight_element(driver, logout_btn)
        logout_btn.click()
        print("🚪 Logged out successfully")

        yes_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[.//span[text()='Yes']]")))
        yes_btn.click()

    with allure.step("Login again with valid credentials"):
        creds = pd.read_excel(os.path.join("data", "test_case_selector.xlsx"),sheet_name="credentials")
        login_check(driver,waittime=10,trial=1,username=str(creds["username"][0]),password=str(creds["password"][0]),user_validation=False)
        wait_for_loader_to_disappear(driver, wait)
        print("🔐 Re-login successful")

        wait_for_loader_to_disappear(driver, wait)
        
    with allure.step("Verify column headers after login"):
        headers = wait.until(EC.presence_of_all_elements_located((By.XPATH,"//tr[contains(@class,'dx-header-row')]//td[@aria-label]")))
        after_columns = [h.get_attribute("aria-label").strip() for h in headers]
        print(f"📊 Columns AFTER login: {after_columns}")

        allure.attach(str(after_columns),name="Columns After Login",attachment_type=allure.attachment_type.TEXT)


        
    with allure.step("Verify column chooser save and restore functionality"):
        try:
            validation_msg = f"BEFORE: {before_columns}\nAFTER: {after_columns}"
            if before_columns == after_columns:
                print("✅ Columns persisted correctly after re-login")
                allure.attach(validation_msg,name="Column Persistence Validation",attachment_type=allure.attachment_type.TEXT)

            else:
                print("❌ Columns mismatch after re-login")
                allure.attach(validation_msg,name="Column Mismatch",attachment_type=allure.attachment_type.TEXT)
                pytest.fail("❌ Column mismatch after re-login")
        
        except Exception as e:
            allure.attach(str(e),name="Validation Error",attachment_type=allure.attachment_type.TEXT)
            pytest.fail(str(e))

    return True


