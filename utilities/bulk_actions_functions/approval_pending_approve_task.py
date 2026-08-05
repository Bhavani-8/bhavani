import os
import json
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from utilities.other_utils_functions.highlight import highlight_element
import time
import allure
from utilities.add_task_functions.wait_for_loader_to_disappear import wait_for_loader_to_disappear



def approve_bulk_action(driver, wait):
    wait_less = WebDriverWait(driver, 5)
    try:
        with open(os.path.join("data", 'locators.json'), 'r') as f:
            elements_details = json.load(f)
            dash_approval_pending_btn = elements_details['dash_approval_pending_btn']
            dash_bulk_task_dropdown_btn = elements_details['dash_bulk_task_dropdown_btn']
            notification_icon = elements_details['notification_icon']
            dash_approval_pending_by_me = elements_details['dash_approval_pending_by_me']
            notification_all_items = elements_details['notification_all_items']
            task_action_log_section = elements_details['task_action_log_section']
            toast_msg = elements_details['toast_msg'] 
            task_log_tab = elements_details['task_log_tab']
            select_first_checkbox = elements_details['select_first_checkbox']
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

    with allure.step("Clicking Approval Pending Tab"):
        try:
            wait_for_loader_to_disappear(driver, wait)
            approval_pending_tab = wait.until(EC.presence_of_element_located((By.XPATH, dash_approval_pending_btn)))
            highlight_element(driver, approval_pending_tab)
            driver.execute_script("arguments[0].click();", approval_pending_tab)
            wait_for_loader_to_disappear(driver, wait)
            print("✅ Clicked Approval Pending tab")
        except Exception as e:
            msg = f"Failed to click Approval Pending tab: {str(e)}"
            print(msg)
            allure.attach(msg, name="Approval Pending tab Error", attachment_type=allure.attachment_type.TEXT)
            raise Exception(msg)
    with allure.step("Clicking Approval Pending by me"):
        try:
            approval_pending_by_me_tab = wait_less.until(EC.presence_of_element_located((By.XPATH, dash_approval_pending_by_me)))
            approval_pending_by_me_tab.click()
            highlight_element(driver,  approval_pending_by_me_tab)
            time.sleep(3)           
            wait_for_loader_to_disappear(driver, wait)
        except Exception as e:
            msg = f"Failed to click Approval Pending By me tab: {str(e)}"
            print(msg)
            allure.attach(msg, name="Approval Pending By me tab Error", attachment_type=allure.attachment_type.TEXT)
            raise Exception(msg)
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
        

    with allure.step("Open Bulk Action dropdown"):
        try:
            bulk_dd = wait.until(EC.element_to_be_clickable((By.XPATH, dash_bulk_task_dropdown_btn)))
            driver.execute_script("arguments[0].click();", bulk_dd)
            time.sleep(1)

            approve_option = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@class,'dx-item-content') and normalize-space()='Approve']")))
            driver.execute_script("arguments[0].click();", approve_option)
        except Exception as e:
            msg = f"Failed to Click Bulk action Dropdown: {str(e)}"
            print(msg)
            allure.attach(msg, name="Bulk action Error", attachment_type=allure.attachment_type.TEXT)
            raise Exception(msg)
    with allure.step("Click Confirm button"):
        try:
            confirm_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[.//span[normalize-space()='Confirm']]")))
            highlight_element(driver, confirm_btn)
            confirm_btn.click()
            time.sleep(3)
            print("✅ Confirm button clicked")
        except Exception as e:
            msg = f"Failed to Click Confirm Button : {str(e)}"
            print(msg)
            allure.attach(msg, name="Confirm Button Error", attachment_type=allure.attachment_type.TEXT)
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
    with allure.step("Validate Normal Notification - Mark Complete"):
        try:
            time.sleep(5)

            notification_btn = wait.until(EC.presence_of_element_located((By.XPATH, notification_icon)))
            driver.execute_script("arguments[0].click();", notification_btn)
            print("✅ Notification icon clicked via JS.")
            time.sleep(7)
            all_items = driver.find_elements(By.XPATH, notification_all_items)
            if not all_items:
                print("ℹ️ No normal notifications found.")
                allure.attach("No normal notifications found","Notification Missing",allure.attachment_type.TEXT)
                return False
            first_notification = all_items[0]
            driver.execute_script("arguments[0].scrollIntoView(true);", first_notification)
            highlight_element(driver, first_notification)
            message_text = first_notification.text.strip()
            print(f"🔔 Normal Notification: {message_text}")
            allure.attach(message_text, "Normal Notification (Created Task)",allure.attachment_type.TEXT)
            driver.execute_script("arguments[0].click();", first_notification)
            print("✅ First normal notification clicked successfully.")
            time.sleep(5)
        except Exception as e:
            msg = f"❌ Normal Notification Error (Created Task): {e}"
            print(msg)
            allure.attach(msg, "Normal Notification Error", allure.attachment_type.TEXT)
            raise Exception(msg)
    with allure.step("Open Task Log tab to verify assignment actions"):
        try:
            time.sleep(3)
            task_log_tab_elem = wait.until(EC.presence_of_element_located((By.XPATH, task_log_tab)))
            task_log_tab_elem.click()
            print("✅ Log tab clicked")
            time.sleep(3)
            wait_for_loader_to_disappear(driver, wait)
        except Exception as e:
            msg = f"❌ Error clicking Log tab: {e}"
            allure.attach(msg, "Error clicking Log tab", allure.attachment_type.TEXT)
            raise Exception(msg)
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
            msg = f"❌ Error fetching log details: {e}"
            allure.attach(msg, "Error fetching log details", allure.attachment_type.TEXT)
            raise Exception(msg)

    return True



    

