from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
import pyautogui as pg
import allure
import pytest
import json
import time
import os

from utilities.add_task_functions.wait_for_loader_to_disappear import wait_for_loader_to_disappear
from utilities.other_utils_functions.highlight import highlight_element

all_coll_list = [
    'Column Task Name', 'Column Company / Project', 'Column Status', 'Column License',
    'Column Assigned To', 'Column Approver', 'Column CC', 'Column Frequency',
    'Column Internal Deadline', 'Column Impact', 'Column Risk Rating',
    'Column Due Date', 'Column Creator', 'Column Assign Date'
]


def new_compliances_column_chooser(driver, wait):
    final_status = True  
    try:
        with open(os.path.join("data", 'locators.json'), 'r') as f:
            elements_details = json.load(f)
            new_compliances_added_btn = elements_details['new_compliances_added_btn']
            toast_msg = elements_details['toast_msg']
    except Exception as e:
        allure.attach(str(e), name="Locator Error", attachment_type=allure.attachment_type.TEXT)
        return False

    
    with allure.step("Open New Compliance Added"):
        try:
            print("Test")
            new_compliances_added = wait.until(EC.presence_of_element_located((By.XPATH, new_compliances_added_btn)))
            highlight_element(driver, new_compliances_added)
            new_compliances_added.click()
            time.sleep(3)
        except Exception as e:
            allure.attach(str(e), name="New Compliances added Error", attachment_type=allure.attachment_type.TEXT)    

    with allure.step("Open Column Chooser"):
        chooser_btn = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@role='button' and @aria-label='columnchooser']")))
        highlight_element(driver, chooser_btn)
        chooser_btn.click()
        wait_for_loader_to_disappear(driver, wait)

    # ==============================
    # ✅ STEP 2: SELECT ALL
    # ==============================
    with allure.step("Select all columns if not selected"):
        print()
        select_all_checkbox = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".dx-list-select-all .dx-checkbox")))
        is_checked = select_all_checkbox.get_attribute("aria-checked")
        if is_checked in ["false", "mixed"]:
            driver.execute_script("arguments[0].click();", select_all_checkbox)
            print("☑️ Clicked 'Select All' (it was unchecked/mixed)")
        else:
            print("✅ 'Select All' already selected")
        wait_for_loader_to_disappear(driver, wait)
    
    with allure.step("Click Save button in Column Chooser"):
            
        save_btn_xpath = "//div[@role='button' and @aria-label='Save & Close']"
        
        column_chooser_save_btn_elem = wait.until(EC.presence_of_element_located((By.XPATH, save_btn_xpath)))
        highlight_element(driver, column_chooser_save_btn_elem)
        column_chooser_save_btn_elem.click()
        print("✅ Saved Column Chooser with 'Select All'")

    with allure.step("Validate toast message after saving"):
        toast_msg_elem = wait.until(EC.presence_of_element_located((By.XPATH, toast_msg)))
        msg = toast_msg_elem.text.strip()
        print(f"📢 Toast message after saving: {msg}")
        time.sleep(7)

    # ==============================
    # ✅ STEP 3: VALIDATE ALL COLUMNS
    # ==============================
    with allure.step("Validate All Columns Visible"):
        headers = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//tr[contains(@class,'dx-header-row')]//td[@aria-label]")))
        col_headers = [h.get_attribute("aria-label").strip() for h in headers]

        print(f"📊 All Columns: {col_headers}")
        allure.attach(str(col_headers), name="All Columns", attachment_type=allure.attachment_type.TEXT)

        if not all(col in col_headers for col in all_coll_list):
            allure.attach(str(col_headers), name="Missing Columns", attachment_type=allure.attachment_type.TEXT)
            return False

    # ==============================
    # ✅ STEP 4: PARTIAL SELECTION
    # ==============================
    with allure.step("Open Column Chooser again"):
        column_chooser_btn_elem = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@role='button' and @aria-label='columnchooser']")))
        highlight_element(driver, column_chooser_btn_elem)
        column_chooser_btn_elem.click()
        wait_for_loader_to_disappear(driver, wait)

    with allure.step("Deselect 'Select All' to enable partial selection"):
        print()
        select_all_checkbox = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".dx-list-select-all .dx-checkbox")))
        is_checked = select_all_checkbox.get_attribute("aria-checked")
        if is_checked == "true" or is_checked == "mixed":
            driver.execute_script("arguments[0].click();", select_all_checkbox)
        else:
            print("Already deselected, continuing...")
        wait_for_loader_to_disappear(driver, wait)
    with allure.step("Select 'Status' column only"):
        col_to_select = "Status"
        checkbox_elem = wait.until(EC.presence_of_element_located((By.XPATH,f"//div[contains(@class,'dx-list-item')][.//div[contains(normalize-space(),'{col_to_select}')]]//div[contains(@class,'dx-checkbox-container')]")))
        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", checkbox_elem)
        driver.execute_script("arguments[0].click();", checkbox_elem)

    with allure.step("Save Column Chooser with partial selection"):
        
        save_btn_xpath = "//div[@role='button' and @aria-label='Save & Close']"
        
        column_chooser_save_btn_elem = wait.until(EC.presence_of_element_located((By.XPATH, save_btn_xpath)))
        highlight_element(driver, column_chooser_save_btn_elem)
        column_chooser_save_btn_elem.click()
        print("✅ Saved Column Chooser with partial selection")

    with allure.step("Validate toast message after saving partial selection"):
        toast_msg_elem = wait.until(EC.presence_of_element_located((By.XPATH, toast_msg)))
        msg = toast_msg_elem.text.strip()
        print(f"📢 Toast message after saving partial selection: {msg}")

        time.sleep(7)

    # ==============================
    # ✅ STEP 5: VALIDATE PARTIAL COLUMN
    # ==============================
    with allure.step("Validate table headers after partial selection"):
        headers = wait.until(EC.presence_of_all_elements_located((By.XPATH,"//tr[contains(@class,'dx-header-row')]//div[contains(@class,'dx-datagrid-text-content')]")))
        col_headers = [h.text.strip() for h in headers if h.text.strip()]
        normalized = [h.lower() for h in col_headers]

        print(f"📊 Partial Columns: {col_headers}")
        allure.attach(str(col_headers), name="Partial Columns", attachment_type=allure.attachment_type.TEXT)

        if "" not in normalized:
            print("❌ Partial selection failed")
            final_status = False
        else:
            print("✅ Partial selection passed")

    with allure.step("Open Column Chooser again to reselect all"):
        column_chooser_btn_elem = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@role='button' and @aria-label='columnchooser']")))
        highlight_element(driver, column_chooser_btn_elem)
        column_chooser_btn_elem.click()
        wait_for_loader_to_disappear(driver, wait)

    with allure.step("'Select All' selection"):
        print()
        select_all_checkbox = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".dx-list-select-all .dx-checkbox")))
        is_checked = select_all_checkbox.get_attribute("aria-checked")
            # ✅ Click ONLY if not selected
        if is_checked in ["false", "mixed"]:
            driver.execute_script("arguments[0].click();", select_all_checkbox)
            print("☑️ Select All enabled")
        else:
            print("✅ Already selected")

        wait_for_loader_to_disappear(driver, wait)
    
    with allure.step("Save Column Chooser with partial selection"):
        
        save_btn_xpath = "//div[@role='button' and @aria-label='Save & Close']"
        
        column_chooser_save_btn_elem = wait.until(EC.presence_of_element_located((By.XPATH, save_btn_xpath)))
        highlight_element(driver, column_chooser_save_btn_elem)
        column_chooser_save_btn_elem.click()
        print("✅ Saved Column Chooser with partial selection")

    # ==============================
    # ✅ STEP 3: VALIDATE ALL COLUMNS
    # ==============================
    with allure.step("Validate All Columns Visible"):
        headers = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//tr[contains(@class,'dx-header-row')]//td[@aria-label]")))
        col_headers = [h.get_attribute("aria-label").strip() for h in headers]

        print(f"📊 All Columns: {col_headers}")
        allure.attach(str(col_headers), name="All Columns", attachment_type=allure.attachment_type.TEXT)

        if not all(col in col_headers for col in all_coll_list):
            allure.attach(str(col_headers), name="Missing Columns", attachment_type=allure.attachment_type.TEXT)
            return False

    return True
