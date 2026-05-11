import pytest
import os
import json
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from utilities.other_utils_functions.highlight import highlight_element
from selenium.webdriver import ActionChains
from datetime import datetime, timedelta
import time
import allure
from selenium.common.exceptions import TimeoutException
from utilities.add_task_functions.wait_for_loader_to_disappear import wait_for_loader_to_disappear
from selenium.common.exceptions import StaleElementReferenceException


try:
    with open(os.path.join("data", 'locators.json'), 'r') as f:
        elements_details = json.load(f)
        dash_col_all_selection_btn = elements_details['dash_col_all_selection_btn']
        dash_bulk_task_dropdown_btn = elements_details['dash_bulk_task_dropdown_btn']
        dash_total_btn = elements_details['dash_total_btn']
        dash_col_selected_label = elements_details['dash_col_selected_label']
        dash_bulk_task_dropdown_form_label = elements_details['dash_bulk_task_dropdown_form_label']
        dash_bulk_task_dropdown_form_input = elements_details['dash_bulk_task_dropdown_form_input']
        dash_bulk_task_dropdown_form_member_confirmation = elements_details['dash_bulk_task_dropdown_form_member_confirmation']
        dash_assign_to_me_tab = elements_details['dash_assign_to_me_tab']
        column_chooser_btn = elements_details['column_chooser_btn']
        column_chooser_save_btn = elements_details['column_chooser_save_btn']
        scroller = elements_details['scroller']
        toast_msg = elements_details['toast_msg']
        error_toast_msg = elements_details['error_toast_msg']
        dash_bulk_options_confirm_btn = elements_details['dash_bulk_options_confirm_btn']
        dash_bulk_options_cancel_btn = elements_details['dash_bulk_options_cancel_btn']
        select_first_checkbox = elements_details['select_first_checkbox']
        update_due_date_btn = elements_details['update_due_date_btn']
        column_chooser_due_date = elements_details['column_chooser_due_date']

except FileNotFoundError:
    pytest.fail("❌ locators.json file not found")
except json.JSONDecodeError:
    pytest.fail("❌ Invalid JSON in locators.json")

def update_due_date_negative(driver, wait, dropdown_selection_val_data, dropdown_selection_val=None, text_case_id=None):

    wait_less = WebDriverWait(driver, 5)
    # date_selected = False
    # retry_required = False
    selected_date_text = ""
    with allure.step("Clicking Dashboard Total button"):
        try:
            wait_for_loader_to_disappear(driver, wait)
            total_tab = wait.until(EC.element_to_be_clickable((By.XPATH, dash_total_btn)))
            highlight_element(driver, total_tab)
            total_tab.click()
            wait_for_loader_to_disappear(driver, wait)
            print("✅ Clicked Total tab")
        except Exception as err:
            allure.attach(str(err), "Total tab error", allure.attachment_type.TEXT)
            pytest.fail("Failed to click Total tab")
    with allure.step("Open Column Chooser from task list"):
        column_chooser_btn_elem = wait.until(EC.presence_of_element_located((By.XPATH, column_chooser_btn)))
        highlight_element(driver, column_chooser_btn_elem)
        driver.execute_script("arguments[0].click();", column_chooser_btn_elem)
        
        def get_state(elem):
            """
            Returns: 'selected', 'deselected', 'mixed'
            """
            aria = elem.get_attribute("aria-checked")
            if aria == "true":
                return "selected"
            elif aria == "false":
                return "deselected"
            else:
                return "mixed"   # usually 'mixed' or None
        try:
            
            select_all_checkbox = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".dx-list-select-all-checkbox")))
            driver.execute_script("arguments[0].scrollIntoView(true);", select_all_checkbox)
            time.sleep(0.2)
            state = get_state(select_all_checkbox)
            print(f"➤ Initial 'Select All' state: {state}")
            if state == "deselected":
                print("✅ Already deselected, no action needed")
            elif state == "selected":
                print("🔁 Deselecting 'Select All'")
                driver.execute_script("arguments[0].click();", select_all_checkbox)
                wait_for_loader_to_disappear(driver, wait)
                time.sleep(0.3)
            elif state == "mixed":
                print("🔁 Mixed state detected → select all → deselect")
                driver.execute_script("arguments[0].click();", select_all_checkbox)
                wait_for_loader_to_disappear(driver, wait)
                time.sleep(0.3)
                select_all_checkbox = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".dx-list-select-all-checkbox")))
                driver.execute_script("arguments[0].click();", select_all_checkbox)
                wait_for_loader_to_disappear(driver, wait)
                time.sleep(0.3)
            select_all_checkbox = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".dx-list-select-all-checkbox")))
            final_state = get_state(select_all_checkbox)
            print(f"➤ Final 'Select All' state: {final_state}")
            if final_state != "deselected":
                pytest.fail(f"❌ Select All normalization failed, state: {final_state}")
        except StaleElementReferenceException:
            pytest.fail("❌ Stale element while normalizing Select All")
    with allure.step("Select 'Due Date' from Column Chooser"):
        try:
            due_date_option = wait.until(EC.presence_of_element_located((By.XPATH, column_chooser_due_date)))
            actions = ActionChains(driver)
            actions.move_to_element(due_date_option).perform()
            time.sleep(0.5)
            wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='dx-item-content dx-list-item-content' and normalize-space()='Due Date']")))
            due_date_option.click()

            save_btn = wait.until(EC.element_to_be_clickable((By.XPATH, column_chooser_save_btn)))
            highlight_element(driver, save_btn)
            save_btn.click()
        except TimeoutException:
            print("❌ 'Due' not found in filter list")

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
        wait_for_loader_to_disappear(driver, wait)
    with allure.step("Select first task from task list"):
        first_checkbox = wait.until(EC.presence_of_element_located((By.XPATH, select_first_checkbox)))
        first_checkbox.click()
    with allure.step("Open Bulk Action and select 'Update Due Date'"): 
        try:
            bulk_dd = wait.until(EC.element_to_be_clickable((By.XPATH, dash_bulk_task_dropdown_btn)))
            highlight_element(driver, bulk_dd)
            bulk_dd.click()
            time.sleep(1)

            update_due_date = wait.until(EC.element_to_be_clickable((By.XPATH, update_due_date_btn)))
            highlight_element(driver, update_due_date)
            update_due_date.click()
            time.sleep(1)
        except Exception as e:
            print(f"❌ Failed to open bulk dropdown → {e}")
    with allure.step("Open calendar"):   
        try:
            calendar_btn = wait.until(EC.presence_of_element_located((By.XPATH, "//span[contains(@class,'ant-picker-suffix')]//img[@alt='calander']")))
            highlight_element(driver, calendar_btn)
            driver.execute_script("arguments[0].click();", calendar_btn)
            print("📅 Calendar opened")
            time.sleep(1)
        except Exception as e:
            print(f"❌ Calendar not opened → {e}")
    with allure.step("Select target date 10 days from today"):
        try:
            today_cell = wait.until(EC.element_to_be_clickable((By.XPATH, "//td[contains(@class,'ant-picker-cell-today')]//div")))
            selected_date_text = datetime.today().strftime("%d/%m/%Y")
            today_cell.click()
            date_selected = True
            print(f"📅 Today's date selected → {selected_date_text}")
            time.sleep(1)
        except Exception as e:
            
            print(f"⚠️ Today not selectable → {e}")
        try:
            confirm_btn = wait.until(EC.element_to_be_clickable((By.XPATH, dash_bulk_options_confirm_btn)))
            highlight_element(driver, confirm_btn)
            confirm_btn.click()
            time.sleep(2)
            print("✅ Confirm clicked")
            time.sleep(1)
        except Exception:
            cancel_btn = wait.until(EC.element_to_be_clickable((By.XPATH, dash_bulk_options_cancel_btn)))
            highlight_element(driver, cancel_btn)
            cancel_btn.click()
            print("ℹ️ Confirm not available → Cancel clicked")
            time.sleep(1)
    with allure.step("Verify toast notifications"):
        try:
            toast = wait.until(EC.presence_of_element_located((By.XPATH,f"{toast_msg} | {error_toast_msg}")))
            highlight_element(driver, toast)
            toast_class = toast.get_attribute("class")
            if "Toastify__toast--success" in toast_class:
                print(f"❌ Success Toast shown unexpectedly: {toast.text.strip()}")
                return True   # ❌ BUG FOUND
            elif "Toastify__toast--error" in toast_class:
                print(f"✅ Error Toast shown as expected: {toast.text.strip()}")
                return False  # ✅ EXPECTED
        except TimeoutException:
            print("❌ No toast found — unexpected behavior")
        return False
    