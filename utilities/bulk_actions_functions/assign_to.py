import pytest
import os
import json
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from utilities.other_utils_functions.highlight import highlight_element
from selenium.webdriver import ActionChains
import pyautogui as pg
import time
import allure
from selenium.common.exceptions import TimeoutException
from utilities.add_task_functions.wait_for_loader_to_disappear import wait_for_loader_to_disappear
from selenium.common.exceptions import StaleElementReferenceException


try:
    with open(os.path.join("data", 'locators.json'), 'r') as f:
        elements_details = json.load(f)
        dash_col_selected_label = elements_details['dash_col_selected_label']
        dash_bulk_task_dropdown_btn = elements_details['dash_bulk_task_dropdown_btn']
        dash_bulk_task_dropdown_form_label = elements_details['dash_bulk_task_dropdown_form_label']
        dash_bulk_task_dropdown_form_input = elements_details['dash_bulk_task_dropdown_form_input']
        dash_bulk_task_dropdown_form_member_confirmation = elements_details['dash_bulk_task_dropdown_form_member_confirmation']
        dash_total_btn = elements_details['dash_total_btn']
        column_filter_search_input = elements_details['column_filter_search_input']
        column_filter_ok_btn = elements_details['column_filter_ok_btn']
        column_filter_cancel_btn = elements_details['column_filter_ok_btn']
        column_chooser_btn = elements_details['column_chooser_btn']
        column_chooser_save_btn = elements_details['column_chooser_save_btn']
        column_filter_company_project = elements_details['column_filter_company_project']
        dash_not_assigned_tab = elements_details['dash_not_assigned_tab']
        notification_icon = elements_details['notification_icon']
        toast_msg = elements_details['toast_msg']
        task_open_btn = elements_details['task_open_btn']
        column_filter_creator = elements_details['column_filter_creator']
        notification_all_items = elements_details['notification_all_items']
        select_first_checkbox = elements_details['select_first_checkbox']
        dash_bulk_options_confirm_btn = elements_details['dash_bulk_options_confirm_btn']
        dash_bulk_options_cancel_btn = elements_details['dash_bulk_options_cancel_btn']
        task_action_log_section =elements_details['task_action_log_section']
        column_chooser_cc = elements_details['column_chooser_cc']
        column_chooser_assign_to = elements_details['column_chooser_assign_to']
        column_chooser_approver = elements_details['column_chooser_approver']
        column_chooser_creator = elements_details['column_chooser_creator']
        column_filter_assigned_to = elements_details['column_filter_assigned_to']
        column_filter_approver = elements_details['column_filter_approver']
        column_filter_cc = elements_details['column_filter_cc']
        dash_bulk_options_assign_to = elements_details['dash_bulk_options_assign_to']
        dash_bulk_options_first_member = elements_details['dash_bulk_options_first_member']
        column_chooser_company_project = elements_details['column_chooser_company_project']
        task_log_tab = elements_details['task_log_tab']

except FileNotFoundError:
    pytest.fail("❌ locators.json file not found")
except json.JSONDecodeError:
    pytest.fail("❌ Invalid JSON in locators.json")


def assign_to_bulk_action(driver, wait, dropdown_selection_val_data, dropdown_selection_val=None, task_name='Internal Task', text_case_id=None):

    wait_less = WebDriverWait(driver, 5)
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
    with allure.step("Clicking Not Assigned Tab"):
        not_assigned_tab = wait.until(EC.element_to_be_clickable((By.XPATH, dash_not_assigned_tab)))
        not_assigned_tab.click()
        time.sleep(1)
        wait_for_loader_to_disappear(driver, wait)
        
    with allure.step("Open Column Chooser from task list"):
        column_chooser_btn_elem = wait.until(EC.presence_of_element_located((By.XPATH, column_chooser_btn)))
        highlight_element(driver, column_chooser_btn_elem)
        driver.execute_script("arguments[0].click();", column_chooser_btn_elem)
        print("Clicked Column Chooser button")
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

    with allure.step("Select 'Company / Project, Approver, CC, Creator' from Column Chooser"): 
        try:

            cc_option = wait.until(EC.presence_of_element_located((By.XPATH, column_chooser_cc)))
            actions = ActionChains(driver)
            actions.move_to_element(cc_option).perform()
            time.sleep(0.5)
            # wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='dx-item-content dx-list-item-content' and normalize-space()='CC']")))
            cc_option.click()

            company_project_option_elm = wait.until(EC.presence_of_element_located((By.XPATH, column_chooser_company_project)))
            actions = ActionChains(driver)
            actions.move_to_element(company_project_option_elm).perform()
            time.sleep(0.5)
            company_project_option_elm.click()

            assign_to_option = wait.until(EC.presence_of_element_located((By.XPATH, column_chooser_assign_to)))
            actions = ActionChains(driver)
            actions.move_to_element(assign_to_option).perform()
            time.sleep(0.5)
            assign_to_option.click()

            approver_option = wait.until(EC.presence_of_element_located((By.XPATH, column_chooser_approver)))
            actions = ActionChains(driver)
            actions.move_to_element(approver_option).perform()
            time.sleep(0.5)
            approver_option.click()

            creator_option = wait.until(EC.presence_of_element_located((By.XPATH, column_chooser_creator)))
            actions = ActionChains(driver)
            actions.move_to_element(creator_option).perform()
            time.sleep(0.5)
            creator_option.click()


            save_btn = wait.until(EC.element_to_be_clickable((By.XPATH, column_chooser_save_btn)))
            highlight_element(driver, save_btn)
            save_btn.click()
            print("✅ Column Chooser saved")

        except TimeoutException:
            print("❌ 'Company / Project' not found in filter list")

    try:
        toast = wait.until(EC.presence_of_element_located((By.XPATH, toast_msg)))
        highlight_element(driver, toast)
        print(f"📢 Toast message: {toast.text.strip()}")
    except Exception:
        print("❌ No toast message found")

    wait_for_loader_to_disappear(driver, wait)

    with allure.step(f"Open Company/Project filter and search for '{task_name}'"):
        company_project_filter_btn = wait_less.until(EC.presence_of_element_located((By.XPATH, column_filter_company_project)))
        company_project_filter_btn.click()
        highlight_element(driver, company_project_filter_btn)
        time.sleep(2)

        search_input = wait.until(EC.presence_of_element_located((By.XPATH, column_filter_search_input)))
        search_input.clear()
        search_input.send_keys(task_name)
        wait_for_loader_to_disappear(driver, wait)
        time.sleep(4)

    try:
        search_task = wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class,'dx-list-item-content') and normalize-space()='Internal Task']")))
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", search_task)
        search_task.click()
        time.slee(3)
        print("✅ Clicked 'Internal Task'")

    except TimeoutException:
        print("❌ 'Internal Task' not found in filter list")
    button_clicked = False

    try:
        column_filter_ok = wait.until(EC.presence_of_element_located((By.XPATH, column_filter_ok_btn)))
        column_filter_ok.click()
        button_clicked = True
    except TimeoutException:
        print("ℹ️ Ok button not available / not clickable")
    if not button_clicked:
        try:
            column_filter_cancel = wait.until(EC.presence_of_element_located((By.XPATH, column_filter_cancel_btn)))
            column_filter_cancel.click()
        except TimeoutException:
            print("ℹ️ Close/Cancel button not present")
    
    wait_for_loader_to_disappear(driver, wait)
    time.sleep(6)

    with allure.step("👤 Reading User Title from Dashboard"):
        try:
            user_title_elem = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='user-title']")))
            highlight_element(driver, user_title_elem)

            username = user_title_elem.text.strip()
            username = user_title_elem.text.strip()

            username = (username.replace('Hi', '').replace('Hello', '').replace(',', '').replace(';', '').strip())
            username = " ".join(username.split())
            print(f"✅ Username detected: {username}")
            allure.attach(username, "Logged-in Username", allure.attachment_type.TEXT)

        except Exception as e:
            allure.attach(str(e), name="User Title Error", attachment_type=allure.attachment_type.TEXT)
            pytest.fail("❌ Failed to read user title")
    scroll_container = driver.find_element(By.XPATH, "//div[contains(@class,'dx-scrollable-container')]")
    driver.execute_script("arguments[0].scrollLeft += 400;", scroll_container)
    time.sleep(1)       
    with allure.step("Open Creator column filter and enter logged-in username"):
        creator_filter_btn = wait_less.until(EC.presence_of_element_located((By.XPATH, column_filter_creator)))
        highlight_element(driver, creator_filter_btn)
        creator_filter_btn.click()
        time.sleep(2)

        search_input = wait.until(EC.presence_of_element_located((By.XPATH, column_filter_search_input)))
        highlight_element(driver, search_input)
        search_input.clear()
        search_input.send_keys(username)

        print(f"🔍 Searching Creator filter using username: {username}")
        allure.attach(username, "Creator Filter Search Value", allure.attachment_type.TEXT)
        time.sleep(3)

    try:
        search_task = wait.until(EC.element_to_be_clickable((By.XPATH,f"//div[contains(@class,'dx-list-item-content') and normalize-space()='{username}']")))
        search_task.click()

    except TimeoutException:
        print("❌ 'User' not found in filter list")
    button_clicked = False

    try:
        column_filter_ok = wait.until(EC.presence_of_element_located((By.XPATH, column_filter_ok_btn)))
        column_filter_ok.click()
        button_clicked = True
    except TimeoutException:
        print("ℹ️ Ok button not available / not clickable")
    if not button_clicked:
        try:
            column_filter_cancel = wait.until(EC.presence_of_element_located((By.XPATH, column_filter_cancel_btn)))
            column_filter_cancel.click()
        except TimeoutException:
            print("ℹ️ Close/Cancel button not present")
    
    wait_for_loader_to_disappear(driver, wait)
    driver.execute_script("arguments[0].scrollLeft -= 400;", scroll_container)
    time.sleep(0.8)
    with allure.step("Open Assigned column filter and search for 'Assign'"):
        assigned_to_filter = wait_less.until(EC.presence_of_element_located((By.XPATH, column_filter_assigned_to)))
        assigned_to_filter.click()
        highlight_element(driver,  assigned_to_filter)
        time.sleep(1)

        search_input = wait.until(EC.presence_of_element_located((By.XPATH,"//input[contains(@class,'dx-texteditor-input') and @role='textbox']")))
        search_input.send_keys("Assign")
        time.sleep(3)

    try:
        search_task = wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class,'dx-list-item-content') and text()='Assign']")))
        driver.execute_script("arguments[0].scrollIntoView({block:'center'});",search_task)
        search_task.click()
        time.sleep(2)
        print("✅ Clicked 'Assign'")
    except TimeoutException:
        print("⚠️ 'Assign' option not found, skipping selection")
    button_clicked = False

    try:
        column_filter_ok = wait.until(EC.presence_of_element_located((By.XPATH, column_filter_ok_btn)))
        column_filter_ok.click()
        time.sleep(3)
        button_clicked = True
    except TimeoutException:
        print("ℹ️ Ok button not available / not clickable")
    if not button_clicked:
        try:
            column_filter_cancel = wait.until(EC.presence_of_element_located((By.XPATH, column_filter_cancel_btn)))
            column_filter_cancel.click()
        except TimeoutException:
            print("ℹ️ Close/Cancel button not present")
    
    wait_for_loader_to_disappear(driver, wait)
    driver.execute_script("arguments[0].scrollLeft += 400;", scroll_container)
    with allure.step("Open Approver column filter and search for 'Assign'"):
        time.sleep(2)
        approver_filter = wait.until(EC.presence_of_element_located((By.XPATH, column_filter_approver)))
        approver_filter.click()
        highlight_element(driver,  approver_filter)
        time.sleep(2)

        search_input = wait.until(EC.presence_of_element_located((By.XPATH,"//input[contains(@class,'dx-texteditor-input') and @role='textbox']")))
        search_input.send_keys("Assign")
        time.sleep(3)

    try:
        search_task = wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class,'dx-list-item-content') and text()='Assign']")))
        driver.execute_script("arguments[0].scrollIntoView({block:'center'});",search_task)
        search_task.click()
        time.sleep(2)
        print("✅ Clicked 'Assign'")
    except TimeoutException:
        print("⚠️ 'Assign' option not found, skipping selection")
    button_clicked = False

    try:
        ok_btn = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@aria-label='OK']")))
        ok_btn.click()
        time.sleep(3)
        button_clicked = True
    except TimeoutException:
        print("ℹ️ Ok button not available / not clickable")
    if not button_clicked:
        try:
            cancel_btn = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@aria-label='Cancel']")))
            cancel_btn.click()
            time.sleep(6)
        except TimeoutException:
            print("ℹ️ Close/Cancel button not present")

        
    wait_for_loader_to_disappear(driver, wait)
    # driver.execute_script("arguments[0].scrollLeft -= 400;", scroll_container)
    with allure.step("Open CC column filter and search for 'Assign'"):
        cc_filter_btn = wait_less.until(EC.presence_of_element_located((By.XPATH, column_filter_cc)))
        driver.execute_script("arguments[0].scrollIntoView({block:'center', inline:'center'});", cc_filter_btn)
        cc_filter_btn.click()
        highlight_element(driver, cc_filter_btn)
        time.sleep(2)

        search_input = wait.until(EC.presence_of_element_located((By.XPATH,"//input[contains(@class,'dx-texteditor-input') and @role='textbox']")))
        search_input.clear()
        search_input.send_keys("Assign")
        time.sleep(3)

    try:
        search_task = wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class,'dx-list-item-content') and text()='Assign']")))
        driver.execute_script("arguments[0].scrollIntoView({block:'center'});",search_task)
        search_task.click()
        print("✅ Clicked 'Assign'")
    except TimeoutException:
        print("⚠️ 'Assign' option not found, skipping selection")
    button_clicked = False

    try:
        column_filter_ok = wait.until(EC.presence_of_element_located((By.XPATH, column_filter_ok_btn)))
        column_filter_ok.click()
        time.sleep(3)
        button_clicked = True
    except TimeoutException:
        print("ℹ️ Ok button not available / not clickable")
    if not button_clicked:
        try:
            column_filter_cancel = wait.until(EC.presence_of_element_located((By.XPATH, column_filter_cancel_btn)))
            column_filter_cancel.click()
        except TimeoutException:
            print("ℹ️ Close/Cancel button not present")
    
    wait_for_loader_to_disappear(driver, wait)
    driver.execute_script("arguments[0].scrollLeft -= 400;", scroll_container)
    with allure.step("Select first task from task list"):
        first_checkbox = wait.until(EC.presence_of_element_located((By.XPATH, select_first_checkbox)))
        driver.execute_script( "arguments[0].scrollIntoView({block:'center', inline:'start'});", first_checkbox)
        first_checkbox.click()
    with allure.step("Open Bulk Action and select 'Assign'"): 
        bulk_dd = wait.until(EC.element_to_be_clickable((By.XPATH, dash_bulk_task_dropdown_btn)))
        highlight_element(driver, bulk_dd)
        bulk_dd.click()

        assign_to_option = wait.until(EC.element_to_be_clickable((By.XPATH, dash_bulk_options_assign_to)))
        highlight_element(driver, assign_to_option)
        assign_to_option.click()

        title_elem = wait.until(EC.presence_of_element_located((By.XPATH, dash_bulk_task_dropdown_form_label)))
        highlight_element(driver, title_elem)
        time.sleep(1)
        
        input_elem = wait.until(EC.presence_of_element_located((By.XPATH, dash_bulk_task_dropdown_form_input)))
        highlight_element(driver, input_elem)     
        time.sleep(0.5)
    with allure.step("Select the first user displayed"):
        first_member = wait.until(EC.element_to_be_clickable((By.XPATH, dash_bulk_options_first_member)))
        highlight_element(driver, first_member)
        first_member.click()

        confirm_btn = wait.until(EC.element_to_be_clickable((By.XPATH, dash_bulk_task_dropdown_form_member_confirmation)))
        confirm_btn.click()
        time.sleep(3)
        print("✅ Assignment confirmed")

    with allure.step("Validate Normal Notification - Assign To"):
        try:
            notification_btn = wait.until(EC.element_to_be_clickable((By.XPATH, notification_icon)))
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
            return False
    with allure.step("Open Task Log tab to verify assignment actions"):
        try:
            task_log_tab_elem = wait.until(EC.presence_of_element_located((By.XPATH, task_log_tab)))
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