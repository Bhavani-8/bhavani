import os
import time
import json
import pandas as pd
import pyautogui as pg
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import pyautogui as pg
import allure
import pytest
import json
import time
import os
import pandas as pd
from selenium.webdriver.common.action_chains import ActionChains
from utilities.other_utils_functions.license_utils import validate_license_subscription
from utilities.other_utils_functions.highlight import highlight_element
from utilities.add_task_functions.wait_for_loader_to_disappear import wait_for_loader_to_disappear
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utilities.login_utils import login_check
from selenium.webdriver import ActionChains
from selenium.common.exceptions import StaleElementReferenceException


def column_reorder(driver, wait, dropdown_selection_val_data):
    try:
        with open(os.path.join("data", "locators.json"), "r") as f:
            locators = json.load(f)
            logout_icon = locators["logout_icon"]
            dash_total_btn = locators["dash_total_btn"]
            column_chooser_btn = locators["column_chooser_btn"]
            select_all_checkbox = locators["select_all_checkbox"]
            column_chooser_save_btn = locators["column_chooser_save_btn"]
            toast_msg = locators["toast_msg"]
    except Exception as e:
        print(f"❌ Failed to load locators.json: {e}")
        return False
    
    with allure.step("Click Total tab"):
        try:
            total_btn = wait.until(EC.element_to_be_clickable((By.XPATH, dash_total_btn)))
            highlight_element(driver, total_btn)
            total_btn.click()
            wait_for_loader_to_disappear(driver, wait)
            print("✅ Opened Dashboard → Total tab")
        except Exception as e:
            print(f"❌ Failed to open Total tab: {e}")
            return False
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

    with allure.step("Verify column headers BEFORE reorder"):
        try:
            headers = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//tr[contains(@class,'dx-header-row')]//td[@aria-label]")))
            before_reorder_columns = [h.get_attribute("aria-label").strip() for h in headers]
            print(f"📊 Columns BEFORE reorder:\n{before_reorder_columns}")
            headers_text = str(before_reorder_columns)
            allure.attach(headers_text,name="Columns Before Reorder",attachment_type=allure.attachment_type.TEXT)
        except Exception as e:
            print(f"❌ Failed to capture columns before reorder: {e}")
            return False

    with allure.step("Reorder columns using drag & drop"):
        try:
            header_xpath = "//tr[contains(@class,'dx-header-row')]//td[@aria-label]"
            headers = wait.until(EC.presence_of_all_elements_located((By.XPATH, header_xpath)))

            if len(headers) < 4:
                pytest.fail("❌ Not enough columns available for reorder")

            source_label = headers[0].get_attribute("aria-label")
            target_label = headers[2].get_attribute("aria-label")

            source_col = wait.until(EC.presence_of_element_located((By.XPATH, f"{header_xpath}[@aria-label='{source_label}']")))
            target_col = wait.until(EC.presence_of_element_located((By.XPATH, f"{header_xpath}[@aria-label='{target_label}']")))

            highlight_element(driver, source_col)
            highlight_element(driver, target_col)

            actions = ActionChains(driver)

            actions.move_to_element(source_col).pause(0.2).click_and_hold() \
                .pause(0.4) \
                .move_to_element(target_col) \
                .pause(0.4) \
                .release() \
                .perform()

            wait_for_loader_to_disappear(driver, wait)
            time.sleep(1)

            print(f"🔀 Dragged '{source_label}' → '{target_label}'")

        except StaleElementReferenceException:
            pytest.fail("❌ Column DOM refreshed during drag – element went stale")

        except Exception as e:
            print(f"❌ Drag & drop failed: {e}")
            return False
        
    with allure.step("Verify column headers AFTER reorder"):
        try:
            headers = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//tr[contains(@class,'dx-header-row')]//td[@aria-label]")))
            after_reorder_columns = [h.get_attribute("aria-label").strip() for h in headers]
            print(f"📊 Columns AFTER reorder:\n{after_reorder_columns}")
            headers_text = str(after_reorder_columns)
            allure.attach(headers_text,name="Columns After Reorder",attachment_type=allure.attachment_type.TEXT)
            if before_reorder_columns == after_reorder_columns:
                pytest.fail("❌ Column order did not change after drag & drop")
        except Exception as e:
            print(f"❌ Failed to capture columns after reorder: {e}")
            return False
        
    with allure.step("Logout from application"):
        try:
            logout_btn = wait.until(EC.element_to_be_clickable((By.XPATH, logout_icon)))
            highlight_element(driver, logout_btn)
            logout_btn.click()
            yes_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[.//span[text()='Yes']]")))
            yes_btn.click()
            print("🚪 Logged out successfully")
        except Exception as e:
            print(f"❌ Logout failed: {e}")
            return False

    with allure.step("Login again with same credentials"):
        try:
            creds = pd.read_excel(os.path.join("data", "test_case_selector.xlsx"),sheet_name="credentials")
            login_check(
                driver,
                waittime=10,
                trial=1,
                username=str(creds["username"][0]),
                password=str(creds["password"][0]),
                user_validation=False
            )

            wait_for_loader_to_disappear(driver, wait)
            print("🔐 Re-login successful")
        except Exception as e:
            print(f"❌ Re-login failed: {e}")
            return False
        
    with allure.step("Verify column headers AFTER login"):
        try:
            headers = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//tr[contains(@class,'dx-header-row')]//td[@aria-label]")))
            after_login_columns = [h.get_attribute("aria-label").strip() for h in headers]
            print(f"📊 Columns AFTER login:\n{after_login_columns}")
            headers_text = str(after_login_columns)
            allure.attach(headers_text,name="After login column headers",attachment_type=allure.attachment_type.TEXT)
        except Exception as e:
            print(f"❌ Failed to capture columns after login: {e}")
            return False
    with allure.step("Validate column reorder functionality"):
        if after_reorder_columns == after_login_columns:
            print("🎯 Column reorder validated successfully ✅")
        else:
            pytest.fail("❌ Column order failed - order changed after drag & drop but is different after logout/login")


    return True
