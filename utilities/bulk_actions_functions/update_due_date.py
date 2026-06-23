import pytest
import os
import json
from utilities.add_task_functions.show_toast import show_toast
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from utilities.other_utils_functions.highlight import highlight_element
from selenium.webdriver import ActionChains
from selenium.common.exceptions import StaleElementReferenceException
import pyautogui as pg
from datetime import datetime, timedelta
import time
import allure
from selenium.common.exceptions import TimeoutException
from utilities.add_task_functions.wait_for_loader_to_disappear import wait_for_loader_to_disappear

try:
    with open(os.path.join("data", 'locators.json'), 'r') as f:
        elements_details = json.load(f)
        dash_total_btn = elements_details['dash_total_btn']
        dash_bulk_task_dropdown_btn = elements_details['dash_bulk_task_dropdown_btn']
        dash_col_all_selection_btn = elements_details['dash_col_all_selection_btn']
        toast_msg = elements_details['toast_msg']
        column_chooser_btn = elements_details['column_chooser_btn']
        column_chooser_save_btn = elements_details['column_chooser_save_btn']
        column_filter_ok_btn = elements_details['column_filter_ok_btn']
        task_log_tab = elements_details['task_log_tab']
        column_filter_cancel_btn = elements_details['column_filter_cancel_btn']
        column_filter_search_input = elements_details['column_filter_search_input']
        task_search_btn = elements_details['task_search_btn']
        task_search_input = elements_details['task_search_input']
        dash_total_btn = elements_details['dash_total_btn']
        dash_not_assigned_tab = elements_details['dash_not_assigned_tab']
        notification_icon = elements_details['notification_icon']
        error_toast_msg = elements_details['error_toast_msg']
        task_open_btn = elements_details['task_open_btn']
        dash_bulk_options_confirm_btn = elements_details['dash_bulk_options_confirm_btn']
        dash_bulk_options_cancel_btn = elements_details['dash_bulk_options_cancel_btn']
        date_filter_apply_btn = elements_details['date_filter_apply_btn']
        select_first_checkbox = elements_details['select_first_checkbox']
        update_due_date_btn = elements_details['update_due_date_btn']
        column_chooser_due_date = elements_details['column_chooser_due_date']
        column_chooser_company_project = elements_details['column_chooser_company_project']
        column_filter_company_project = elements_details['column_filter_company_project']

except FileNotFoundError:
    pytest.fail("❌ locators.json file not found")
except json.JSONDecodeError:
    pytest.fail("❌ Invalid JSON in locators.json")


def update_due_date_bulk_action(driver, wait, task_name='Internal Task'):

    wait_less = WebDriverWait(driver, 5)
    selected_date_text = ""
    with allure.step("Clicking Dashboard Total button"):
        total_tab = wait.until(EC.element_to_be_clickable((By.XPATH, dash_total_btn)))
        highlight_element(driver, total_tab)
        total_tab.click()
        wait_for_loader_to_disappear(driver, wait)
    with allure.step("Open Column Chooser from task list"):
        column_chooser_btn_elem = wait.until(EC.presence_of_element_located((By.XPATH, column_chooser_btn)))
        highlight_element(driver, column_chooser_btn_elem)
        driver.execute_script("arguments[0].click();", column_chooser_btn_elem)
        wait_for_loader_to_disappear(driver, wait)
        
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
            print("✅ 'Select All' normalized successfully")
        except StaleElementReferenceException:
            pytest.fail("❌ Stale element while normalizing Select All")
        with allure.step("Select 'Due Date' from Column Chooser"): 
            try:
                due_date_option = wait.until(EC.presence_of_element_located((By.XPATH, column_chooser_due_date)))
                actions = ActionChains(driver)
                actions.move_to_element(due_date_option).perform()
                time.sleep(0.5)
                # wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='dx-item-content dx-list-item-content' and normalize-space()='Due Date']")))
                due_date_option.click()

                company_project_option_elm = wait.until(EC.presence_of_element_located((By.XPATH, column_chooser_company_project)))
                actions = ActionChains(driver)
                actions.move_to_element(company_project_option_elm).perform()
                time.sleep(0.5)
                wait.until(EC.element_to_be_clickable((By.XPATH, column_chooser_company_project)))
                company_project_option_elm.click()
                save_btn = wait.until(EC.element_to_be_clickable((By.XPATH, column_chooser_save_btn)))
                highlight_element(driver, save_btn)
                save_btn.click()

            except TimeoutException:
                print("❌ 'Due Date' not found in filter list")
            
            
        try:
            toast = wait.until(EC.presence_of_element_located((By.XPATH, toast_msg)))
            highlight_element(driver, toast)
            print(f"📢 Toast message: {toast.text.strip()}")
        except Exception:
            print("❌ No toast message found")
        wait_for_loader_to_disappear(driver, wait, "Toastify__toast-body")
        time.sleep(7)
        with allure.step(f"Open Company/Project filter and search for '{task_name}'"):
            company_project_filter_btn = wait.until(EC.presence_of_element_located((By.XPATH, column_filter_company_project)))
            company_project_filter_btn.click()
            highlight_element(driver, company_project_filter_btn)
            time.sleep(2)

            search_input = wait.until(EC.presence_of_element_located((By.XPATH, column_filter_search_input)))
            search_input.clear()
            search_input.send_keys(task_name)
            time.sleep(3)

        try:
            search_task = wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class,'dx-list-item-content') and normalize-space()='Internal Task']")))
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", search_task)
            time.sleep(1)
            search_task.click()
            print("✅ Clicked 'Internal Task'")

            column_filter_ok = wait.until(EC.presence_of_element_located((By.XPATH, column_filter_ok_btn)))
            column_filter_ok.click()
        except TimeoutException:
            print("❌ 'Internal Task' not found in filter list")
        
        wait_for_loader_to_disappear(driver, wait)
    
        with allure.step("Open Due date Filter"):
            try:
                due_date_filter = wait.until(EC.presence_of_element_located((By.XPATH, "//td[@role='columnheader' and .//span[normalize-space()='Due Date']]//button")))
                highlight_element(driver, due_date_filter)
                due_date_filter.click()
                time.sleep(3)
            except Exception as e:
                print(f"❌ Calendar not opened → {e}")
        with allure.step("Open calendar"):
            try:
                calendar_btn = wait.until(EC.element_to_be_clickable((By.XPATH,"//div[contains(@class,'ant-picker')]//span[@aria-label='calendar']")))
                highlight_element(driver, calendar_btn)
                driver.execute_script("arguments[0].click();", calendar_btn)
                time.sleep(3)
            except Exception as e:
                print(f"❌ Failed to click calendar → {e}")
                allure.attach(str(e), "Error clicking calendar", allure.attachment_type.TEXT)

        wait = WebDriverWait(driver, 10)
        today = datetime.today().strftime('%d-%m-%Y')
        with allure.step(f"Select FROM date as today ({today})"):
            try:
                from_input = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@date-range='start']")))
                driver.execute_script("arguments[0].click();", from_input)
                today_cell = wait.until(EC.element_to_be_clickable((By.XPATH, "//td[contains(@class,'ant-picker-cell-today')]//div")))
                driver.execute_script("arguments[0].click();", today_cell)
            except Exception as e:
                print(f"❌ Failed to select FROM date → {e}")
                allure.attach(str(e), "Error selecting FROM date", allure.attachment_type.TEXT)
        with allure.step(f"Select TO date as today ({today})"):
            try:
                today_cell = wait.until(EC.element_to_be_clickable((By.XPATH, "//td[contains(@class,'ant-picker-cell-today')]//div")))
                driver.execute_script("arguments[0].click();", today_cell)
            except Exception as e:
                print(f"❌ Failed to select TO date → {e}")
                allure.attach(str(e), "Error selecting TO date", allure.attachment_type.TEXT)


        apply_btn = wait.until(EC.presence_of_element_located((By.XPATH, date_filter_apply_btn)))
        driver.execute_script("arguments[0].click();", apply_btn)
        print("✅ Date range applied")
        wait_for_loader_to_disappear(driver, wait)
        time.sleep(10)

        with allure.step("Select first task from task list"):
            try:
                first_checkbox = wait.until(EC.element_to_be_clickable((By.XPATH, select_first_checkbox)))
                driver.execute_script("arguments[0].scrollIntoView({block:'center'});", first_checkbox)
                time.sleep(0.3)
                driver.execute_script("arguments[0].click();", first_checkbox)
            except Exception as e:
                print(f"❌ Failed to select first task checkbox → {e}")
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
                time.sleep(1)
            except Exception as e:
                print(f"❌ Calendar not opened → {e}")
                retry_required = True

        with allure.step("Select target date 10 days from today"):
            today_cell = wait.until(EC.presence_of_element_located((By.XPATH, "//td[contains(@class,'ant-picker-cell-today')]")))
            target_cell = today_cell
            for _ in range(10):
                target_cell = target_cell.find_element(By.XPATH,"following::td[not(contains(@class,'ant-picker-cell-disabled'))][1]")
            target_cell.find_element(By.TAG_NAME, "div").click()
            selected_date_text = (datetime.today() + timedelta(days=10)).strftime("%d/%m/%Y")
            print(f"📅 Selected date → {selected_date_text}")
            time.sleep(2)

            try:
                confirm_btn = wait.until(EC.element_to_be_clickable((By.XPATH, dash_bulk_options_confirm_btn)))
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
                toast = wait.until(EC.presence_of_element_located((By.XPATH, toast_msg)))
                print(f"📢 Final Toast: {toast.text.strip()}")
            except Exception:
                print("❌ No final toast found")
            print("🎯 Update Due Date bulk action completed")
    return True
    
  



