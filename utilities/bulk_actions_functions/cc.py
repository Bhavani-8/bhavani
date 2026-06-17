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
        dash_col_all_selection_btn = elements_details['dash_col_all_selection_btn']
        task_search_btn = elements_details['task_search_btn']
        column_chooser_btn = elements_details['column_chooser_btn']
        column_chooser_save_btn = elements_details['column_chooser_save_btn']
        column_filter_ok_btn = elements_details['column_filter_ok_btn']
        column_filter_search_input = elements_details['column_filter_search_input']
        column_filter_creator = elements_details['column_filter_creator']
        task_log_tab = elements_details['task_log_tab']
        column_filter_cancel_btn = elements_details['column_filter_cancel_btn']
        task_search_input = elements_details['task_search_input']
        task_log_tab = elements_details['task_log_tab']
        dash_total_btn = elements_details['dash_total_btn']
        dash_not_assigned_tab = elements_details['dash_not_assigned_tab']
        notification_icon = elements_details['notification_icon']
        toast_msg = elements_details['toast_msg']
        error_toast_msg = elements_details['error_toast_msg']
        task_open_btn = elements_details['task_open_btn']
        dash_bulk_options_add_cc = elements_details['dash_bulk_options_add_cc']
        select_first_checkbox = elements_details['select_first_checkbox']
        dash_bulk_options_first_member = elements_details['dash_bulk_options_first_member']
        dash_col_filter_ok_btn = elements_details['dash_col_filter_ok_btn']
        dash_col_filter_cancel_btn = elements_details['dash_col_filter_cancel_btn']
        column_chooser_company_project = elements_details['column_chooser_company_project']
        column_chooser_approver = elements_details['column_chooser_approver']
        column_chooser_cc = elements_details['column_chooser_cc']
        column_chooser_creator = elements_details['column_chooser_creator']
        column_filter_approver = elements_details['column_filter_approver']
        column_filter_cc = elements_details['column_filter_cc']
        column_filter_company_project = elements_details['column_filter_company_project']



except FileNotFoundError:
    pytest.fail("❌ locators.json file not found")
except json.JSONDecodeError:
    pytest.fail("❌ Invalid JSON in locators.json")

def cc_bulk_action(driver, wait, task_name='Internal Task'):
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
            company_project_option_elm = wait.until(EC.presence_of_element_located((By.XPATH, column_chooser_company_project)))
            actions = ActionChains(driver)
            actions.move_to_element(company_project_option_elm).perform()
            time.sleep(0.5)
            company_project_option_elm.click()

            approver_option = wait.until(EC.presence_of_element_located((By.XPATH, column_chooser_approver)))
            actions = ActionChains(driver)
            actions.move_to_element(approver_option).perform()
            time.sleep(0.5)
            approver_option.click()

            cc_option = wait.until(EC.presence_of_element_located((By.XPATH, column_chooser_cc)))
            actions = ActionChains(driver)
            actions.move_to_element(cc_option).perform()
            time.sleep(0.5)
            cc_option.click()

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
        time.sleep(3)

    try:
        search_task = wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class,'dx-list-item-content') and normalize-space()='Internal Task']")))
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", search_task)
        time.sleep(1)
        search_task.click()
        time.sleep(2)
        print("✅ Clicked 'Internal Task'")

    except TimeoutException:
        print("❌ 'Internal Task' not found in filter list")
    button_clicked = False

    try:
        ok_btn = wait.until(EC.presence_of_element_located((By.XPATH, column_filter_ok_btn)))
        ok_btn.click()
        time.sleep(3)
        button_clicked = True
    except TimeoutException:
        print("ℹ️ Ok button not available / not clickable")
    if not button_clicked:
        try:
            cancel_btn = wait.until(EC.presence_of_element_located((By.XPATH, column_filter_cancel_btn)))
            cancel_btn.click()
        except TimeoutException:
            print("ℹ️ Close/Cancel button not present")
   
    wait_for_loader_to_disappear(driver, wait)
    with allure.step("Open Approver column filter and search for 'Assign'"):
        approver_filter = wait_less.until(EC.presence_of_element_located((By.XPATH, column_filter_approver)))
        approver_filter.click()
        highlight_element(driver,  approver_filter)
        time.sleep(2)

        search_input = wait.until(EC.presence_of_element_located((By.XPATH,"//input[contains(@class,'dx-texteditor-input') and @role='textbox']")))
        search_input.clear()
        search_input.send_keys("Assign")
        time.sleep(2)
    try:
        search_task = wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class,'dx-list-item-content') and normalize-space()='Assign']")))
        driver.execute_script("arguments[0].scrollIntoView({block:'center'});",search_task)
        search_task.click()
        time.sleep(2)
        print("✅ Clicked 'Assign'")
    except TimeoutException:
        print("⚠️ 'Assign' option not found, skipping selection")
    button_clicked = False

    try:
        ok_btn = wait.until(EC.presence_of_element_located((By.XPATH, dash_col_filter_ok_btn)))
        ok_btn.click()
        time.sleep(4)
        button_clicked = True
    except TimeoutException:
        print("ℹ️ Ok button not available / not clickable")
    if not button_clicked:
        try:
            cancel_btn = wait.until(EC.presence_of_element_located((By.XPATH, dash_col_filter_cancel_btn)))
            cancel_btn.click()
            time.sleep(6)
        except TimeoutException:
            print("ℹ️ Close/Cancel button not present")

    wait_for_loader_to_disappear(driver, wait)
    with allure.step("Open CC column filter and search for 'Assign'"):
        cc_filter = wait_less.until(EC.presence_of_element_located((By.XPATH, column_filter_cc)))
        cc_filter.click()
        highlight_element(driver,  cc_filter)
        time.sleep(2)

        search_input = wait.until(EC.presence_of_element_located((By.XPATH, column_filter_search_input)))
        search_input.clear()
        search_input.send_keys("Assign")
        time.sleep(2)

    try:
        search_task = wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class,'dx-list-item-content') and normalize-space()='Assign']")))
        search_task.click()
        time.sleep(2)
        print("✅ Clicked 'Assign'")

    except TimeoutException:
        print("❌ 'Assign' not found in filter list")
    button_clicked = False

    try:
        ok_btn = wait.until(EC.presence_of_element_located((By.XPATH, column_filter_ok_btn)))
        ok_btn.click()
        time.sleep(3)
        button_clicked = True
    except TimeoutException:
        print("ℹ️ Ok button not available / not clickable")
    if not button_clicked:
        try:
            cancel_btn = wait.until(EC.presence_of_element_located((By.XPATH, column_filter_cancel_btn)))
            cancel_btn.click()
        except TimeoutException:
            print("ℹ️ Close/Cancel button not present")
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
            allure.attach(str(e), name="User Title Error", attachment_type=allure.attachment_type.TEXT)
            pytest.fail("❌ Failed to read user title")
    with allure.step("Open Creator column filter and enter logged-in username"):
        creator_filter_btn = wait_less.until(EC.presence_of_element_located((By.XPATH, column_filter_creator)))
        highlight_element(driver, creator_filter_btn)
        creator_filter_btn.click()
        time.sleep(2)

        search_input = wait.until(EC.presence_of_element_located((By.XPATH, column_filter_search_input)))
        highlight_element(driver, search_input)
        search_input.clear()
        search_input.send_keys(username)
        time.sleep(2)

        print(f"🔍 Searching Creator filter using username: {username}")
        allure.attach(username, "Creator Filter Search Value", allure.attachment_type.TEXT)

    try:
        search_task = wait.until(EC.element_to_be_clickable((By.XPATH,f"//div[contains(@class,'dx-list-item-content') and normalize-space()=\"{username}\"]")))
        search_task.click()
        time.sleep(2)
    except TimeoutException:
        print("❌ 'Internal Task' not found in filter list")
    button_clicked = False

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

    with allure.step("Select first task from task list"):
        first_checkbox = wait.until(EC.presence_of_element_located((By.XPATH, select_first_checkbox)))
        first_checkbox.click()
    with allure.step("Open Bulk Action and select 'CC'"): 
        bulk_dd = wait.until(EC.element_to_be_clickable((By.XPATH, dash_bulk_task_dropdown_btn)))
        highlight_element(driver, bulk_dd)
        bulk_dd.click()

        cc_option = wait.until(EC.element_to_be_clickable((By.XPATH, dash_bulk_options_add_cc)))
        highlight_element(driver, cc_option)
        cc_option.click()

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
        wait_for_loader_to_disappear(driver, wait)
        time.sleep(6)
    try:
        toast = wait.until(EC.presence_of_element_located((By.XPATH, toast_msg)))
        highlight_element(driver, toast)
        print(f"📢 Toast message: {toast.text.strip()}")
        allure.attach(username, "Toast Message", allure.attachment_type.TEXT)
    except Exception:
        print("❌ No toast message found")
        
    return True


