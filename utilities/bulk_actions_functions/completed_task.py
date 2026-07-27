import pytest
import os
import json
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from utilities.other_utils_functions.highlight import highlight_element
import pyautogui as pg
from selenium.webdriver import ActionChains

import time
import allure
from selenium.common.exceptions import TimeoutException
from utilities.add_task_functions.wait_for_loader_to_disappear import wait_for_loader_to_disappear
from selenium.common.exceptions import StaleElementReferenceException

try:
    with open(os.path.join("data", 'locators.json'), 'r') as f:
        elements_details = json.load(f)
        dash_approval_pending_btn = elements_details['dash_approval_pending_btn']
        dash_bulk_task_dropdown_btn = elements_details['dash_bulk_task_dropdown_btn']
        column_filter_search_input = elements_details['column_filter_search_input']
        toast_msg = elements_details['toast_msg']
        dash_completed_btn = elements_details['dash_completed_btn']
        dash_bulk_task_dropdown_btn = elements_details['dash_bulk_task_dropdown_btn']
        column_chooser_btn = elements_details['column_chooser_btn']
        column_chooser_save_btn = elements_details['column_chooser_save_btn']
        toast_msg = elements_details['toast_msg']
        error_toast_msg = elements_details['error_toast_msg']
        task_open_btn = elements_details['task_open_btn']
        column_filter_ok_btn = elements_details['column_filter_ok_btn']
        column_filter_creator = elements_details['column_filter_creator']
        task_log_tab = elements_details['task_log_tab']
        column_filter_cancel_btn = elements_details['column_filter_cancel_btn']
        task_action_log_section = elements_details['task_action_log_section']
        column_chooser_company_project = elements_details['column_chooser_company_project']
        column_filter_company_project = elements_details['column_filter_company_project']
        column_chooser_creator = elements_details['column_chooser_creator']
        column_filter_company_project_internal_task = elements_details['column_filter_company_project_internal_task']

except FileNotFoundError:
    pytest.fail("❌ locators.json file not found")
except json.JSONDecodeError:
    pytest.fail("❌ Invalid JSON in locators.json")


def completed_task_bulk_action(driver, wait, task_name='Internal Task'):
    wait_less = WebDriverWait(driver, 5)
    with allure.step("Clicking Completed button"):
        try:
            wait_for_loader_to_disappear(driver, wait)
            completed_task_tab = wait.until(EC.presence_of_element_located((By.XPATH, dash_completed_btn)))
            highlight_element(driver, completed_task_tab)
            driver.execute_script("arguments[0].click();", completed_task_tab)
            wait_for_loader_to_disappear(driver, wait)
            print("✅ Clicked Completed Task tab")
        except Exception as e:
            msg = f"Failed to click Completed tab: {str(e)}"
            print(msg)
            allure.attach(msg, name="Completed tab Error", attachment_type=allure.attachment_type.TEXT)
            raise Exception(msg)

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
                return "mixed"   

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
    with allure.step("Select 'Company / Project, Creator' from Column Chooser"):
        try:
            company_project_option_elm = wait.until(EC.presence_of_element_located((By.XPATH, column_chooser_company_project)))
            actions = ActionChains(driver)
            actions.move_to_element(company_project_option_elm).perform()
            time.sleep(0.5)
            wait.until(EC.element_to_be_clickable((By.XPATH, column_chooser_company_project)))
            company_project_option_elm.click()
            
            creator_option = wait.until(EC.presence_of_element_located((By.XPATH, column_chooser_creator)))
            actions = ActionChains(driver)
            actions.move_to_element(creator_option).perform()
            time.sleep(0.5)
            wait.until(EC.element_to_be_clickable((By.XPATH, column_chooser_creator)))
            creator_option.click()

        
        except Exception as e:
            msg = f"Failed to Clicking Approver option: {str(e)}"
            print(msg)
            allure.attach(msg, name="Approver Option Error", attachment_type=allure.attachment_type.TEXT)
            raise Exception(msg)
    try:
        save_btn = wait.until(EC.element_to_be_clickable((By.XPATH, column_chooser_save_btn)))
        highlight_element(driver, save_btn)
        save_btn.click()
        print("✅ Column Chooser saved")
    except Exception as e:
        msg = f"Failed to Save Button: {str(e)}"
        print(msg)
        allure.attach(msg, name="Save Button Error", attachment_type=allure.attachment_type.TEXT)
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

    wait_for_loader_to_disappear(driver, wait)
    with allure.step(f"Open Company/Project filter and search for '{task_name}'"):
        try:
            company_project_filter_btn = wait_less.until(EC.presence_of_element_located((By.XPATH, column_filter_company_project)))
            highlight_element(driver, company_project_filter_btn)
            company_project_filter_btn.click()
            time.sleep(2)

            search_input = wait.until(EC.presence_of_element_located((By.XPATH, column_filter_search_input)))
            search_input.clear()
            search_input.send_keys(task_name)
            time.sleep(5)
        except Exception as e:
            msg = f"Failed to Open Company Project filter: {str(e)}"
            print(msg)
            allure.attach(msg, name="Company Project filter Error", attachment_type=allure.attachment_type.TEXT)
            raise Exception(msg)

    try:
        search_task = wait.until(EC.presence_of_element_located((By.XPATH, column_filter_company_project_internal_task)))
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", search_task)
        time.sleep(1)
        search_task.click()
        time.sleep(2)
        print("✅ Clicked 'Internal Task'")
    except Exception as e:
        msg = f"Failed to Search Task: {str(e)}"
        print(msg)
        allure.attach(msg, name="Search Task Error", attachment_type=allure.attachment_type.TEXT)
        raise Exception(msg)

    try:
        column_filter_ok = wait.until(EC.presence_of_element_located((By.XPATH, column_filter_ok_btn)))
        column_filter_ok.click()
        time.sleep(3)
    except Exception as e:
        msg = f"Failed to Click Column Filter OK Button: {str(e)}"
        print(msg)
        allure.attach(msg, name="Column Filter OK Button Error", attachment_type=allure.attachment_type.TEXT)
        raise Exception(msg)
    
    wait_for_loader_to_disappear(driver, wait)
    with allure.step("👤 Reading User Title from Dashboard"):
        try:
            user_title_elem = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='user-title']")))
            highlight_element(driver, user_title_elem)
            username = user_title_elem.text.strip()
            username = (username.replace('Hi', '').replace('Hello', '').replace(',', '').replace(';', '').strip())
            username = " ".join(username.split())
            print(f"✅ Username detected: {username}")
            allure.attach(username, "Logged-in Username", allure.attachment_type.TEXT)

        except Exception as e:
            msg = f"Failed to Reading user title: {str(e)}"
            print(msg)
            allure.attach(msg, name="Reading user title Error", attachment_type=allure.attachment_type.TEXT)
            raise Exception(msg)
    with allure.step("Open Creator column filter and enter logged-in username"):
        try: 
            creator_filter_btn = wait.until(EC.presence_of_element_located((By.XPATH, column_filter_creator)))
            highlight_element(driver, creator_filter_btn)
            creator_filter_btn.click()
            time.sleep(2)

            search_input = wait.until(EC.presence_of_element_located((By.XPATH, column_filter_search_input)))
            highlight_element(driver, search_input)
            search_input.clear()
            search_input.send_keys(username)
            time.sleep(4)
            print(f"🔍 Searching Creator filter using username: {username}")
            allure.attach(username, "Creator Filter Search Value", allure.attachment_type.TEXT)

        except Exception as e:
            msg = f"Failed to Open Creator filter: {str(e)}"
            print(msg)
            allure.attach(msg, name="Creator filter Error", attachment_type=allure.attachment_type.TEXT)
            raise Exception(msg)

    try:
        search_task = wait.until(EC.element_to_be_clickable((By.XPATH,f"//div[contains(@class,'dx-list-item-content') and normalize-space()=\"{username}\"]")))
        search_task.click()
        time.sleep(2)
    except Exception as e:
        msg = f"Failed to Search Task: {str(e)}"
        print(msg)
        allure.attach(msg, name="Search Task Error", attachment_type=allure.attachment_type.TEXT)
        return False
    try:
        column_filter_ok = wait.until(EC.presence_of_element_located((By.XPATH, column_filter_ok_btn)))
        column_filter_ok.click()
        time.sleep(3)
    except Exception as e:
        msg = f"Failed to Click Column Filter OK Button: {str(e)}"
        print(msg)
        allure.attach(msg, name="Column Filter OK Button Error", attachment_type=allure.attachment_type.TEXT)
        raise Exception(msg)
    
    wait_for_loader_to_disappear(driver, wait)
        
    with allure.step("Opening task from table"):
        try:
            task_open_btn_elem = wait.until(EC.element_to_be_clickable((By.XPATH, task_open_btn)))
            highlight_element(driver, task_open_btn_elem)
            try:
                task_open_btn_elem.click()
            except Exception:
                driver.execute_script("arguments[0].scrollIntoView(true);", task_open_btn_elem)
                driver.execute_script("arguments[0].click();", task_open_btn_elem)
            print("✅ Task opened from table")
            time.sleep(3)
            wait_for_loader_to_disappear(driver, wait)
        except Exception as e:
            msg = f"Failed to open Task Button : {str(e)}"
            print(msg)
            allure.attach(msg, name="Task Open Button Error", attachment_type=allure.attachment_type.TEXT)
            raise Exception(msg)
    with allure.step("Clicking Re-open Button"):
        try:
            reopen_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[span[text()='Re-Open']]")))
            highlight_element(driver, reopen_btn)
            reopen_btn.click()
            reopen_reason = wait.until(EC.presence_of_element_located((By.XPATH, '//textarea[@placeholder="Enter the reason to re-open this task."]')))
            # Scroll into view (optional)
            driver.execute_script("arguments[0].scrollIntoView(true);", reopen_reason)
            time.sleep(0.2)

            # Enter text
            reopen_reason.send_keys("Testing reopening of completed task.")

        except Exception as e:
            msg = f"Failed to click Re-open Button : {str(e)}"
            print(msg)
            allure.attach(msg, name="Re-open Button Error", attachment_type=allure.attachment_type.TEXT)
            raise Exception(msg)
    try:
        confirm_btn = wait.until(EC.presence_of_element_located((By.XPATH, "//button[.//span[normalize-space()='Confirm']]")))
        highlight_element(driver, confirm_btn)
        confirm_btn.click()
        time.sleep(2)
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

