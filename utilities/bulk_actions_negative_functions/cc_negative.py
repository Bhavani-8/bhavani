import pytest
import os
import json
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from utilities.other_utils_functions.highlight import highlight_element
from selenium.webdriver import ActionChains
import time
import allure
from utilities.add_task_functions.wait_for_loader_to_disappear import wait_for_loader_to_disappear


def cc_negative(driver, wait):

    try:
        with open(os.path.join("data", 'locators.json'), 'r') as f:
            elements_details = json.load(f)
            dash_bulk_task_dropdown_btn = elements_details['dash_bulk_task_dropdown_btn']
            dash_total_btn = elements_details['dash_total_btn']
            dash_bulk_task_dropdown_form_label = elements_details['dash_bulk_task_dropdown_form_label']
            dash_bulk_task_dropdown_form_input = elements_details['dash_bulk_task_dropdown_form_input']
            dash_bulk_task_dropdown_form_member_confirmation = elements_details['dash_bulk_task_dropdown_form_member_confirmation']
            column_chooser_btn = elements_details['column_chooser_btn']
            column_chooser_save_btn = elements_details['column_chooser_save_btn']
            toast_msg = elements_details['toast_msg']
            error_toast_msg = elements_details['error_toast_msg']
            column_filter_search_input = elements_details['column_filter_search_input']
            column_filter_ok_btn = elements_details['column_filter_ok_btn']
            select_first_checkbox = elements_details['select_first_checkbox']
            dash_bulk_options_first_member = elements_details['dash_bulk_options_first_member']
            column_chooser_company_project = elements_details['column_chooser_company_project']
            column_chooser_creator = elements_details['column_chooser_creator']
            column_filter_creator = elements_details['column_filter_creator']
            dash_bulk_options_add_cc = elements_details['dash_bulk_options_add_cc']

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
    with allure.step("Clicking Dashboard Total button"):
        try:
            wait_for_loader_to_disappear(driver, wait)
            total_tab = wait.until(EC.element_to_be_clickable((By.XPATH, dash_total_btn)))
            highlight_element(driver, total_tab)
            total_tab.click()
            wait_for_loader_to_disappear(driver, wait)
            print("✅ Clicked Total tab")
        except Exception as e:
            msg = f"Failed to Click Total tab: {str(e)}"
            print(msg)
            allure.attach(msg, name="Total tab Error", attachment_type=allure.attachment_type.TEXT)
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
        except Exception as e:
            msg = f"Failed to Selecting all: {str(e)}"
            print(msg)
            allure.attach(msg, name="Selecting all Error", attachment_type=allure.attachment_type.TEXT)
            raise Exception(msg)
    with allure.step("Select 'CC' from Column Chooser"):
        try:

            company_project_option_elm = wait.until(EC.presence_of_element_located((By.XPATH, column_chooser_company_project)))
            actions = ActionChains(driver)
            actions.move_to_element(company_project_option_elm).perform()
            time.sleep(0.5)
            company_project_option_elm.click()

            creator_option = wait.until(EC.presence_of_element_located((By.XPATH, column_chooser_creator)))
            actions = ActionChains(driver)
            actions.move_to_element(creator_option).perform()
            time.sleep(0.5)
            creator_option.click()

            save_btn = wait.until(EC.element_to_be_clickable((By.XPATH, column_chooser_save_btn)))
            highlight_element(driver, save_btn)
            save_btn.click()

        except Exception as e:
            msg = f"Failed to Clicking CC option: {str(e)}"
            print(msg)
            allure.attach(msg, name="CC Option Error", attachment_type=allure.attachment_type.TEXT)
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
        wait_for_loader_to_disappear(driver, wait, "Toastify__toast-body")

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

            time.sleep(2)
        except Exception as e:
            msg = f"Failed to Open Creator filter: {str(e)}"
            print(msg)
            allure.attach(msg, name="Creator filter Error", attachment_type=allure.attachment_type.TEXT)
            raise Exception(msg)
    try:
        search_task = wait.until(EC.element_to_be_clickable((By.XPATH,f"//div[contains(@class,'dx-list-item-content') and normalize-space()=\"{username}\"]")))
        search_task.click()
    except Exception as e:
        msg = f"Failed to Search Task: {str(e)}"
        print(msg)
        allure.attach(msg, name="Search Task Error", attachment_type=allure.attachment_type.TEXT)
        return False

    try:
        column_filter_ok = wait.until(EC.presence_of_element_located((By.XPATH, column_filter_ok_btn)))
        column_filter_ok.click()
        time.sleep(2)
    except Exception as e:
        msg = f"Failed to Click Column Filter OK Button: {str(e)}"
        print(msg)
        allure.attach(msg, name="Column Filter OK Button Error", attachment_type=allure.attachment_type.TEXT)
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
    with allure.step("Open Bulk Action and select 'Add CC'"): 
        try:
            bulk_dd = wait.until(EC.element_to_be_clickable((By.XPATH, dash_bulk_task_dropdown_btn)))
            highlight_element(driver, bulk_dd)
            bulk_dd.click()

            cc_option = wait.until(EC.element_to_be_clickable((By.XPATH, dash_bulk_options_add_cc)))
            highlight_element(driver, cc_option)
            cc_option.click()

            title_elem = wait.until(EC.presence_of_element_located((By.XPATH, dash_bulk_task_dropdown_form_label)))
            highlight_element(driver, title_elem)
            time.sleep(1)
        except Exception as e:
            msg = f"Failed to Click Bulk action Dropdown: {str(e)}"
            print(msg)
            allure.attach(msg, name="Bulk action Error", attachment_type=allure.attachment_type.TEXT)
            raise Exception(msg)
    with allure.step("Attempt to assign the same user as CC who is already assigned"):
        try: 
            input_elem = wait.until(EC.presence_of_element_located((By.XPATH, dash_bulk_task_dropdown_form_input)))
            highlight_element(driver, input_elem)    
            input_elem.send_keys(f"{username}")
            time.sleep(3)
                
            member_elem = wait.until(EC.element_to_be_clickable((By.XPATH, dash_bulk_options_first_member)))
            highlight_element(driver, member_elem)
            member_elem.click()

            confirm_btn = wait.until(EC.element_to_be_clickable((By.XPATH, dash_bulk_task_dropdown_form_member_confirmation)))
            confirm_btn.click()
        except Exception as e:
            msg = f"Failed to Click Team Member: {str(e)}"
            print(msg)
            allure.attach(msg, name="Team Member Error", attachment_type=allure.attachment_type.TEXT)
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