import time
import pytest
import os
import json
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from utilities.other_utils_functions.highlight import highlight_element
from selenium.webdriver import ActionChains
from utilities.add_task_functions.wait_for_loader_to_disappear import wait_for_loader_to_disappear
def special_comment_task(driver, wait, task_name='Internal Task'):

    # ✅ Load locators
    with allure.step("Load locators.json for Export Data Validation"):
        try:
            with open(os.path.join("data", 'locators.json'), 'r') as f:
                elements_details = json.load(f)
                settings_icon = elements_details['settings_icon']
                special_task_icon = elements_details['special_task_icon']
                column_chooser_save_btn = elements_details['column_chooser_save_btn']
                toast_msg = elements_details['toast_msg']
                dash_total_btn = elements_details['dash_total_btn']
                column_chooser_btn = elements_details['column_chooser_btn']
                column_chooser_company_project = elements_details['column_chooser_company_project']
                dash_total_btn = elements_details['dash_total_btn']
                column_filter_search_input = elements_details['column_filter_search_input']
                column_filter_ok_btn = elements_details['column_filter_ok_btn']
                column_chooser_btn = elements_details['column_chooser_btn']
                column_chooser_save_btn = elements_details['column_chooser_save_btn']
                column_filter_company_project = elements_details['column_filter_company_project']
                task_open_btn = elements_details['task_open_btn']    
                task_log_tab = elements_details['task_log_tab'] 
                task_action_log_section = elements_details['task_action_log_section']
                
                
            print("✅ locators.json loaded successfully")
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

    with allure.step("Editing Personal Details"):
        try:
            print()
            time.sleep(2)  # Wait for page to load completely
            # Click Project Icon
            settings_btn = wait.until(EC.presence_of_element_located((By.XPATH, settings_icon)))
            highlight_element(driver, settings_btn)
            settings_btn.click()
            time.sleep(2)
            print("✅ Settings Icon Clicked")
        except Exception as e:
            msg = f"Failed to Click Total tab: {str(e)}"
            print(msg)
            allure.attach(msg, name="Total tab Error", attachment_type=allure.attachment_type.TEXT)
            raise Exception(msg)

    with allure.step("Click on Task Category"):
        try:
            task_category_btn = wait.until(EC.presence_of_element_located((By.XPATH, "//span[text()='Task Category']")))
            highlight_element(driver, task_category_btn)
            task_category_btn.click()
        except Exception as e:
            msg = f"Failed to Click task category: {str(e)}"
            print(msg)
            allure.attach(msg, name="Task Category Error", attachment_type=allure.attachment_type.TEXT)
            raise Exception(msg)
        wait_for_loader_to_disappear(driver, wait)
        time.sleep(3)

    with allure.step("Click on Edit button"):
        try:
            edit_btn = wait.until(EC.presence_of_element_located((By.XPATH, "//button[@data-slot='button' and .//*[name()='svg' and contains(@class,'lucide-pencil')]]")))
            highlight_element(driver, edit_btn)
            edit_btn.click()
        except Exception as e:
            msg = f"Failed to Click Edit Button: {str(e)}"
            print(msg)
            allure.attach(msg, name="Edit Button Error", attachment_type=allure.attachment_type.TEXT)
            raise Exception(msg)

    with allure.step("Verify Disable Comments checkbox is disabled"):
        try:
            disable_btn = wait.until(EC.presence_of_element_located((By.XPATH, "//span[@role='checkbox' and @aria-labelledby='task-category-disable-comments-label']")))
            highlight_element(driver, disable_btn)
            is_checked = disable_btn.get_attribute("aria-checked")

            if is_checked == "true":
                print("☑️ Checkbox is enabled. Disabling it...")
                disable_btn.click()
                print("✅ Checkbox disabled successfully.")
                allure.attach("Checkbox was enabled and has been disabled.",name="Disable Checkbox",attachment_type=allure.attachment_type.TEXT)

            else:
                print("✅ Checkbox is already disabled.")
                allure.attach("Checkbox is already disabled.",name="Disable Checkbox",attachment_type=allure.attachment_type.TEXT)

        except Exception as e:
            msg = f"Failed to click Disable checkbox: {str(e)}"
            print(msg)
            allure.attach(msg,name="Disable Checkbox Error",attachment_type=allure.attachment_type.TEXT)
            raise Exception(msg)
    try:
        update_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit' and text()='Update']")))
        highlight_element(driver, update_btn)
        update_btn.click()
    except Exception as e:
        msg = f"Failed to click Update Button: {str(e)}"
        print(msg)
        allure.attach(msg,name="Update Button Error",attachment_type=allure.attachment_type.TEXT)
        raise Exception(msg)
        
    with allure.step("Open Dashboard"):
        try:
            time.sleep(2)
            special_task_icon_elem = wait.until(EC.element_to_be_clickable((By.XPATH, special_task_icon)))
            highlight_element(driver, special_task_icon_elem)
            special_task_icon_elem.click()
        except Exception as e:
            msg = f"Failed to click Special Task Icon: {str(e)}"
            print(msg)
            allure.attach(msg,name="Special Task Icon Error",attachment_type=allure.attachment_type.TEXT)
            raise Exception(msg)

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

        except Exception as e:
            msg = f"Failed to Selecting all: {str(e)}"
            print(msg)
            allure.attach(msg, name="Selecting all Error", attachment_type=allure.attachment_type.TEXT)
            raise Exception(msg)
    with allure.step("Select 'Company / Project, Approver, CC, Creator' from Column Chooser"): 
        try:

            company_project_option_elm = wait.until(EC.presence_of_element_located((By.XPATH, column_chooser_company_project)))
            actions = ActionChains(driver)
            actions.move_to_element(company_project_option_elm).perform()
            time.sleep(0.5)
            company_project_option_elm.click()

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
            company_project_filter_btn = wait.until(EC.presence_of_element_located((By.XPATH, column_filter_company_project)))
            highlight_element(driver, company_project_filter_btn)
            company_project_filter_btn.click()
            time.sleep(2)

            search_input = wait.until(EC.presence_of_element_located((By.XPATH, column_filter_search_input)))
            search_input.clear()
            search_input.send_keys(task_name)
            wait_for_loader_to_disappear(driver, wait)
            time.sleep(4)
        except Exception as e:
            msg = f"Failed to Open Company Project filter: {str(e)}"
            print(msg)
            allure.attach(msg, name="Company Project filter Error", attachment_type=allure.attachment_type.TEXT)
            raise Exception(msg)

    try:
        search_task = wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class,'dx-list-item-content') and normalize-space()='Internal Task']")))
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", search_task)
        search_task.click()
        time.sleep(3)
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
    time.sleep(6)

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
    
        try:
            comment_tab = wait.until(EC.presence_of_element_located((By.XPATH, "//h1[text()='Comment']")))
            highlight_element(driver, comment_tab)
            comment_tab.click()
            time.sleep(1)
        except Exception as e:
            msg = f"failed to Click Comment tab: {str(e)}"
            print(msg)
            allure.attach(msg, name = "comment Tab Error", attachment_type=allure.attachment_type.TEXT)
            raise Exception(msg)
    comment_text = "This is a special test comment"
    with allure.step(f"Open Comment box and enter comment '{comment_text}'"):
        try: 
            comment_input = wait.until(EC.presence_of_element_located((By.XPATH, "//textarea[contains(@placeholder, 'Add a comment')]")))
            highlight_element(driver, comment_input)
            comment_input.send_keys(comment_text)
            entered_comment = comment_input.get_attribute("value").strip()
            time.sleep(1)
            print(f"Comment Input: {entered_comment}") 
        except Exception as e:
            msg = f"failed to cick Comment Input : {str(e)}"
            print(msg)
            allure.attach(msg, name = "Comment Input Error", attachment_type=allure.attachment_type.TEXT)
            raise Exception(msg)
        
    try:
        comment_arrow = wait.until(EC.presence_of_element_located((By.XPATH, "//img[@alt='arrow-right']")))
        highlight_element(driver, comment_arrow)
        comment_arrow.click()
        time.sleep(1)
    except Exception as e:
        msg = f"failed to cick Comment Arrow : {str(e)}"
        print(msg)
        allure.attach(msg, name = "Comment Arrow Error", attachment_type=allure.attachment_type.TEXT)
        raise Exception(msg)
    with allure.step("Validate entered comment against displayed comment"):
        try:
            comment_text_elem = wait.until(EC.visibility_of_element_located((By.XPATH, "(//p[contains(@class,'_fileTitleText')])[1]")))
            highlight_element(driver, comment_text_elem)
            # comment_date = wait.until(EC.visibility_of_element_located((By.XPATH, "(//p[contains(@class,'_fileTimestampText')])[1]")))
            # highlight_element(driver, comment_date)
            displayed_comment = comment_text_elem.text.strip()
            print(f"Displayed Comment: {displayed_comment}")
            if entered_comment == displayed_comment:
                msg = (f"✅ Comment matched successfully.\n\n" f"Entered Comment : {entered_comment}\n" f"Displayed Comment: {displayed_comment}")
                print(msg)
                allure.attach(msg,name="Comment Validation",attachment_type=allure.attachment_type.TEXT)
            else:
                msg = (f"❌ Comment mismatch.\n\n"f"Entered Comment : {entered_comment}\n"f"Displayed Comment: {displayed_comment}")
                print(msg)
                allure.attach(msg,name="Comment Validation",attachment_type=allure.attachment_type.TEXT)
                raise Exception(msg)
        except Exception as e:
            msg = f"failed to validate Comment Text : {str(e)}"
            print(msg)
            allure.attach(msg, name = "Validate Comment Text Error", attachment_type=allure.attachment_type.TEXT)
            raise Exception(msg)
    
    with allure.step("Open Task Log tab to verify assignment actions"):
        try:
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
            full_text = wait.until(EC.visibility_of_element_located((By.XPATH, "//p[contains(@class,'holding-list-bold-title') and contains(.,'Comment')]")))
            highlight_element(driver, full_text)
            log_details = full_text.text.strip()
            print(f"Log Entry: {log_details}")
            allure.attach(log_details,name="Log Entry Details",attachment_type=allure.attachment_type.TEXT)

        except Exception as e:
            msg = f"❌ Error fetching log details: {e}"
            allure.attach(msg, "Error fetching log details", allure.attachment_type.TEXT)
            raise Exception(msg)


        return True

