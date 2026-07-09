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



def update_due_date_negative(driver, wait):
    try:
        with open(os.path.join("data", 'locators.json'), 'r') as f:
            elements_details = json.load(f)
            dash_bulk_task_dropdown_btn = elements_details['dash_bulk_task_dropdown_btn']
            dash_total_btn = elements_details['dash_total_btn']
            column_chooser_btn = elements_details['column_chooser_btn']
            column_chooser_save_btn = elements_details['column_chooser_save_btn']
            toast_msg = elements_details['toast_msg']
            error_toast_msg = elements_details['error_toast_msg']
            dash_bulk_options_confirm_btn = elements_details['dash_bulk_options_confirm_btn']
            select_first_checkbox = elements_details['select_first_checkbox']
            update_due_date_btn = elements_details['update_due_date_btn']
            column_chooser_due_date = elements_details['column_chooser_due_date']
            dash_bulk_task_dropdown_form_label = elements_details['dash_bulk_task_dropdown_form_label']
    except FileNotFoundError as e:
        msg = f"locators.json file not found: {str(e)}"
        print(msg)
        allure.attach(msg, name="Locators File Missing", attachment_type=allure.attachment_type.TEXT)
        return False
    except json.JSONDecodeError as e:
        msg = f"Invalid JSON in locators.json: {str(e)}"
        print(msg)
        allure.attach(msg, name="Locators JSON Error", attachment_type=allure.attachment_type.TEXT)
        return False

    wait_less = WebDriverWait(driver, 5)
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
        try:     
            column_chooser_btn_elem = wait.until(EC.presence_of_element_located((By.XPATH, column_chooser_btn)))
            highlight_element(driver, column_chooser_btn_elem)
            driver.execute_script("arguments[0].click();", column_chooser_btn_elem)
            print("Clicked Column Chooser button")
            wait_for_loader_to_disappear(driver, wait)
        except Exception as e:
            msg = f"Failed to Click Column chooser button: {str(e)}"
            print(msg)
            allure.attach(msg, name="Column chooser Error", attachment_type=allure.attachment_type.TEXT)
            raise Exception(msg)
        
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
        except Exception as e:
            msg = f"Failed to Selecting all: {str(e)}"
            print(msg)
            allure.attach(msg, name="Selecting all Error", attachment_type=allure.attachment_type.TEXT)
            raise Exception(msg)
    with allure.step("Select 'Due Date' from Column Chooser"):
        try:
            due_date_option = wait.until(EC.presence_of_element_located((By.XPATH, column_chooser_due_date)))
            actions = ActionChains(driver)
            actions.move_to_element(due_date_option).perform()
            time.sleep(0.5)
            wait.until(EC.element_to_be_clickable((By.XPATH, column_chooser_due_date)))
            due_date_option.click()

            save_btn = wait.until(EC.element_to_be_clickable((By.XPATH, column_chooser_save_btn)))
            highlight_element(driver, save_btn)
            save_btn.click()
        except Exception as e:
            msg = f"Failed to Clicking Due Date option: {str(e)}"
            print(msg)
            allure.attach(msg, name="Due Date Option Error", attachment_type=allure.attachment_type.TEXT)
            raise Exception(msg)

        try:
            toast = wait.until(EC.presence_of_element_located((By.XPATH,f"{toast_msg} | {error_toast_msg}")))
            highlight_element(driver, toast)
            toast_class = toast.get_attribute("class")

            if "Toastify__toast--success" in toast_class:
                print(f"📢 Success Toast: {toast.text.strip()}")
            elif "Toastify__toast--error" in toast_class:
                print(f"❌ Error Toast: {toast.text.strip()}")
        except Exception as e:
            msg = f"Toast message not found: {str(e)}"
            print(msg)
            allure.attach(str(e), name="Toast message Error", attachment_type=allure.attachment_type.TEXT)
            raise Exception(msg)
        wait_for_loader_to_disappear(driver, wait)
    with allure.step("Select first task from task list"):
        try:
            first_checkbox = wait.until(EC.presence_of_element_located((By.XPATH, select_first_checkbox)))
            first_checkbox.click()
            time.sleep(2)
       
        except Exception as e:
            msg = f"Failed to Selecting first task: {str(e)}"
            print(msg)
            allure.attach(msg, name="Selecting first task Error", attachment_type=allure.attachment_type.TEXT)
            raise Exception(msg)
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

            title_elem = wait.until(EC.presence_of_element_located((By.XPATH, dash_bulk_task_dropdown_form_label)))
            highlight_element(driver, title_elem)
            time.sleep(1)
        
        except Exception as e:
            msg = f"Failed to Click Bulk action Dropdown: {str(e)}"
            print(msg)
            allure.attach(msg, name="Bulk action Error", attachment_type=allure.attachment_type.TEXT)
            raise Exception(msg)
        
    with allure.step("Open calendar"):   
        try:
            calendar_btn = wait.until(EC.presence_of_element_located((By.XPATH, "//span[contains(@class,'ant-picker-suffix')]//img[@alt='calander']")))
            highlight_element(driver, calendar_btn)
            driver.execute_script("arguments[0].click();", calendar_btn)
            print("📅 Calendar opened")
            time.sleep(1)
        except Exception as e:
            print(f"❌ Calendar not opened → {e}")
        
        except Exception as e:
            msg = f"Failed to Click Calendar: {str(e)}"
            print(msg)
            allure.attach(msg, name="Bulk action Error", attachment_type=allure.attachment_type.TEXT)
            raise Exception(msg)
    with allure.step("Select target date 10 days from today"):
        try:
            today_cell = wait.until(EC.element_to_be_clickable((By.XPATH, "//td[contains(@class,'ant-picker-cell-today')]//div")))
            selected_date_text = datetime.today().strftime("%d/%m/%Y")
            today_cell.click()
            print(f"📅 Today's date selected → {selected_date_text}")
            time.sleep(1)
        except Exception as e:
            msg = f"Failed to Click Today Date: {str(e)}"
            print(msg)
            allure.attach(msg, name="Bulk action Error", attachment_type=allure.attachment_type.TEXT)
            raise Exception(msg)
        try:
            confirm_btn = wait.until(EC.element_to_be_clickable((By.XPATH, dash_bulk_options_confirm_btn)))
            highlight_element(driver, confirm_btn)
            confirm_btn.click()
            time.sleep(2)
            print("✅ Confirm clicked")
            time.sleep(1)
        except Exception as e:
            msg = f"Failed to Click Confirm Button: {str(e)}"
            print(msg)
            allure.attach(msg, name="Bulk action Error", attachment_type=allure.attachment_type.TEXT)
            raise Exception(msg)
        
    try:
        toast = wait.until(EC.presence_of_element_located((By.XPATH, toast_msg)))
        highlight_element(driver, toast)
        print(f"📢 Toast message: {toast.text.strip()}")
    except Exception as e:
        msg = f"Toast message not found: {str(e)}"
        print(msg)
        allure.attach(str(e), name="Toast message Error", attachment_type=allure.attachment_type.TEXT)
        raise Exception(msg)
    
    
    