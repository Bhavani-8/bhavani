import pytest
import os
import json
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from utilities.other_utils_functions.highlight import highlight_element
import pyautogui as pg
import time
import allure
from selenium.common.exceptions import TimeoutException
from utilities.add_task_functions.wait_for_loader_to_disappear import wait_for_loader_to_disappear
from selenium.common.exceptions import StaleElementReferenceException


try:
    with open(os.path.join("data", 'locators.json'), 'r') as f:
        elements_details = json.load(f)
        dash_total_btn = elements_details['dash_total_btn']
        dash_approval_pending_btn = elements_details['dash_approval_pending_btn']
        dash_bulk_task_dropdown_btn = elements_details['dash_bulk_task_dropdown_btn']
        notification_icon = elements_details['notification_icon']
        task_open_btn = elements_details['task_open_btn']
        toast_msg = elements_details['toast_msg']
        error_toast_msg = elements_details['error_toast_msg']
        dash_approval_pending_by_me = elements_details['dash_approval_pending_by_me']
        notification_all_items = elements_details['notification_all_items']
        select_first_checkbox = elements_details['select_first_checkbox']
        task_action_log_section = elements_details['task_action_log_section']

except FileNotFoundError:
    pytest.fail("❌ locators.json file not found")
except json.JSONDecodeError:
    pytest.fail("❌ Invalid JSON in locators.json")

def reject_bulk_action(driver, wait, dropdown_selection_val_data, dropdown_selection_val=None, test_case_id=None):
    wait_less = WebDriverWait(driver, 5)

    try:
        wait_for_loader_to_disappear(driver, wait)
        approval_pending_tab = wait.until(EC.presence_of_element_located((By.XPATH, dash_approval_pending_btn)))
        highlight_element(driver, approval_pending_tab)
        driver.execute_script("arguments[0].click();", approval_pending_tab)
        wait_for_loader_to_disappear(driver, wait)
        print("✅ Clicked Approval Pending tab")
    except Exception as err:
        allure.attach(str(err), "Approval Pending tab error", allure.attachment_type.TEXT)
        pytest.fail("Failed to click Approval Pending tab")
    with allure.step("➡️ Clicking Approval Pending by me"):
        approval_pending_by_me_tab = wait_less.until(EC.presence_of_element_located((By.XPATH, dash_approval_pending_by_me)))
        approval_pending_by_me_tab.click()
        highlight_element(driver,  approval_pending_by_me_tab)
        time.sleep(3)           
        wait_for_loader_to_disappear(driver, wait)
    with allure.step("Select first task from task list"):
        first_checkbox = wait.until(EC.presence_of_element_located((By.XPATH, select_first_checkbox)))
        first_checkbox.click()

    with allure.step("Open Bulk Action dropdown"): 
        bulk_dd = wait.until(EC.element_to_be_clickable((By.XPATH, dash_bulk_task_dropdown_btn)))
        highlight_element(driver, bulk_dd)
        bulk_dd.click()
    with allure.step("Select 'Reject' option in Bulk Action"):
        reject_option = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@class,'dx-item-content') and normalize-space()='Reject']")))
        driver.execute_script("arguments[0].click();", reject_option)
    with allure.step("Click Confirm button"):
        try:
            confirm_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[.//span[normalize-space()='Confirm']]")))
            highlight_element(driver, confirm_btn)
            confirm_btn.click()
            time.sleep(3)
            print("✅ Confirm button clicked")
        except Exception as e:
            print("ℹ️ Confirm button not available / not clickable")
            cancel_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[.//span[normalize-space()='Cancel']]")))
            highlight_element(driver, cancel_btn)
            cancel_btn.click()
            print("✅ Cancel button clicked")



    with allure.step("Validate Normal Notification - Assigned to"):
        try:
            pg.hotkey('ctrl', 'r')
            pg.hotkey('ctrl', 'r')
            time.sleep(7)
            notification_btn = wait.until(EC.presence_of_element_located((By.XPATH, notification_icon)))
            driver.execute_script("arguments[0].click();", notification_btn)
            print("✅ Notification icon clicked via JS.")
            time.sleep(3)
            all_items = driver.find_elements(By.XPATH, notification_all_items)
            if not all_items:
                print("ℹ️ No normal notifications found.")
                allure.attach("No normal notifications found",
                            "Notification Missing",
                            allure.attachment_type.TEXT)
                return False
            first_notification = all_items[0]
            driver.execute_script("arguments[0].scrollIntoView(true);", first_notification)
            try:
                highlight_element(driver, first_notification)
            except:
                pass
            message_text = first_notification.text.strip()
            print(f"🔔 Normal Notification: {message_text}")
            allure.attach(message_text, "Normal Notification (Created Task)",
                        allure.attachment_type.TEXT)
            driver.execute_script("arguments[0].click();", first_notification)
            print("✅ First normal notification clicked successfully.")
        except Exception as e:
            msg = f"❌ Normal Notification Error (Created Task): {e}"
            print(msg)
            allure.attach(msg, "Normal Notification Error", allure.attachment_type.TEXT)
            return False    
    with allure.step("Open Task Log tab to verify assignment actions"):
        try:
            task_log_tab_elem = wait.until(EC.presence_of_element_located((By.XPATH, "//div[text()='Log']")))
            task_log_tab_elem.click()
            print("✅ Log tab clicked")
            time.sleep(3)
        except Exception as e:
            print(f"❌ Error clicking Log tab: {e}")
            allure.attach(str(e), "Error clicking Log tab", allure.attachment_type.TEXT)
    with allure.step("Fetch action text and member name from log entry"):
        try:
            p_elem = driver.find_element(By.XPATH, task_action_log_section)
            highlight_element(driver, p_elem)
            full_text = p_elem.get_attribute("textContent").strip()  # e.g. "Comment Piyush Gala"
            fetched_member_name = p_elem.find_element(By.TAG_NAME, "strong").text  # e.g. "Piyush Gala"
            action = full_text.replace(fetched_member_name, "").strip()  # e.g. "Comment"

            print(f"✅ Log details fetched: Action='{action}', Member='{fetched_member_name}'")
            log_details = (f"Action: {action}\n"f"Member: {fetched_member_name}\n"f"Full Text: {full_text}")

            allure.attach(log_details,name="Log Entry Details",attachment_type=allure.attachment_type.TEXT)
        except Exception as e:
            print(f"❌ Error fetching log details: {e}")
            allure.attach(str(e), "Error fetching log details", allure.attachment_type.TEXT)
            return False

    return True

