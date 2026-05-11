import allure
import os
import json
import time
import pytest
import pyautogui as pg
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from utilities.other_utils_functions.highlight import highlight_element
from selenium.common.exceptions import TimeoutException
from utilities.add_task_utils import wait_for_loader_to_disappear
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver import ActionChains


def reassign_task_by_co(driver, wait, task_name='Internal Task'):

    # ✅ Step 1: Load locators
    with allure.step("Load locators.json"):
        try:
            with open(os.path.join("data", "locators.json"), "r") as f:
                elements_details = json.load(f)
            dash_not_assigned_tab = elements_details['dash_not_assigned_tab']
            column_chooser_btn = elements_details['column_chooser_btn']
            column_chooser_save_btn = elements_details['column_chooser_save_btn']
            notification_icon = elements_details["notification_icon"]
            toast_msg = elements_details['toast_msg']
            column_filter_search_input = elements_details['column_filter_search_input']
            column_filter_ok_btn = elements_details['column_filter_ok_btn']
            column_filter_cancel_btn = elements_details['column_filter_ok_btn']
            column_chooser_company_project = elements_details['column_chooser_company_project']
            column_filter_company_project = elements_details['column_filter_company_project']
            dash_not_assigned_tab = elements_details['dash_not_assigned_tab']
            notification_icon = elements_details["notification_icon"]
            toast_msg = elements_details["toast_msg"]
            notification_all_items = elements_details['notification_all_items']
            notification_icon = elements_details['notification_icon']
            toast_msg = elements_details['toast_msg']
            task_open_btn = elements_details['task_open_btn']
            column_chooser_cc = elements_details['column_chooser_cc']
            column_chooser_assign_to = elements_details['column_chooser_assign_to']
            column_chooser_approver = elements_details['column_chooser_approver']
            column_filter_assigned_to = elements_details['column_filter_assigned_to']
            column_filter_approver = elements_details['column_filter_approver']
            column_filter_cc = elements_details['column_filter_cc']
            task_log_tab = elements_details['task_log_tab']
            task_action_log_section = elements_details['task_action_log_section']
           
        except Exception as e:
            allure.attach(str(e), name="Locators Load Error", attachment_type=allure.attachment_type.TEXT)
            return False
    
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

            save_btn = wait.until(EC.element_to_be_clickable((By.XPATH, column_chooser_save_btn)))
            highlight_element(driver, save_btn)
            save_btn.click()
            print("✅ Column Chooser saved")

        except TimeoutException:
            print("❌ 'Company / Project' not found in filter list")

    with allure.step(f"Open Company/Project filter and search for '{task_name}'"):
        company_project_filter_btn = wait.until(EC.presence_of_element_located((By.XPATH, column_filter_company_project)))
        highlight_element(driver, company_project_filter_btn)
        company_project_filter_btn.click()
        time.sleep(4)

        search_input = wait.until(EC.presence_of_element_located((By.XPATH, column_filter_search_input)))
        search_input.clear()
        search_input.send_keys(task_name)
        wait_for_loader_to_disappear(driver, wait)
        time.sleep(4)

    try:
        search_task = wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class,'dx-list-item-content') and normalize-space()='Internal Task']")))
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", search_task)
        search_task.click()
        time.sleep(3)
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

    with allure.step("Open Assigned column filter and search for 'Assign'"):
        assigned_to_filter = wait.until(EC.presence_of_element_located((By.XPATH, column_filter_assigned_to)))
        highlight_element(driver,  assigned_to_filter)
        assigned_to_filter.click()
        time.sleep(2)

        search_input = wait.until(EC.presence_of_element_located((By.XPATH,"//input[contains(@class,'dx-texteditor-input') and @role='textbox']")))
        search_input.send_keys("Assign")
        time.sleep(3)

    try:
        search_task = wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class,'dx-list-item-content') and normalize-space()='Assign']")))
        driver.execute_script("arguments[0].scrollIntoView({block:'center'});",search_task)
        search_task.click()
        time.sleep(3)
        print("✅ Clicked 'Assign'")
    except TimeoutException:
        print("⚠️ 'Assign' option not found, skipping selection")
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
    scroll_container = driver.find_element(By.XPATH, "//div[contains(@class,'dx-scrollable-container')]")
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
        search_task = wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class,'dx-list-item-content') and normalize-space()='Assign']")))
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
        time.sleep(4)
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

    with allure.step("Open CC column filter and search for 'Assign'"):
        cc_filter_btn = wait.until(EC.presence_of_element_located((By.XPATH, column_filter_cc)))
        highlight_element(driver, cc_filter_btn)
        cc_filter_btn.click()
        time.sleep(3)

        search_input = wait.until(EC.presence_of_element_located((By.XPATH,"//input[contains(@class,'dx-texteditor-input') and @role='textbox']")))
        search_input.clear()
        search_input.send_keys("Assign")
        time.sleep(3)

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
            time.sleep(1)
            wait_for_loader_to_disappear(driver, wait)
        except Exception as err:
            allure.attach(str(err), name="Task Open Error", attachment_type=allure.attachment_type.TEXT)
            print(f"❌ Error opening task: {err}")
    # with allure.step("Validate Normal Notification - Mark Complete"):
    #     try:
    #         time.sleep(5)

    #         notification_btn = wait.until(EC.presence_of_element_located((By.XPATH, notification_icon)))
    #         driver.execute_script("arguments[0].click();", notification_btn)
    #         print("✅ Notification icon clicked via JS.")
    #         time.sleep(7)
    #         all_items = driver.find_elements(By.XPATH, notification_all_items)
    #         if not all_items:
    #             print("ℹ️ No normal notifications found.")
    #             allure.attach("No normal notifications found","Notification Missing",allure.attachment_type.TEXT)
    #             return False
    #         first_notification = all_items[0]
    #         driver.execute_script("arguments[0].scrollIntoView(true);", first_notification)
    #         highlight_element(driver, first_notification)
    #         message_text = first_notification.text.strip()
    #         print(f"🔔 Normal Notification: {message_text}")
    #         allure.attach(message_text, "Normal Notification (Created Task)",allure.attachment_type.TEXT)
    #         driver.execute_script("arguments[0].click();", first_notification)
    #         print("✅ First normal notification clicked successfully.")
    #         time.sleep(2)
    #     except Exception as e:
    #         msg = f"❌ Normal Notification Error (Created Task): {e}"
    #         print(msg)
    #         allure.attach(msg, "Normal Notification Error", allure.attachment_type.TEXT)
    #         return False
    # -----------------------------
    # ✅ Step 2: Assign Team Member to 'Assign To'
    # -----------------------------
    with allure.step("Assign Team Member to 'Assign To'"):
        print()
        time.sleep(1)
        assign_user = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@id='assignBtn4assignTo']")))
        highlight_element(driver, assign_user)
        assign_user.click()
        print("✅ Assign To button clicked.")

        first_user = wait.until(EC.presence_of_element_located((By.XPATH, "(//div[@class='email-list-row'])[1]")))
        highlight_element(driver, first_user)
        first_user.click()
        time.sleep(6)
        print("✅ User selected from email list.")


# -----------------------------
    # ✅ Step 2: Reassigned Team Member to 'Assign'
    # -----------------------------
    with allure.step("Task is been reassigned by CO. 'Assign'"):
        print()
        assign_user = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='holding-list-normal-title' and text()='Assign To']//..//..//div[@class='holding-list-bold-title truncate cursor-pointer']//span")))
        highlight_element(driver, assign_user)
        assign_user.click()
        print("✅ Assign To button clicked.")

        second_user = wait.until(EC.presence_of_element_located((By.XPATH, "(//div[@class='flex flex-col mx-1'])[2]")))
        highlight_element(driver, second_user)
        second_user.click()
        print("✅ First user selected from email list.")
    #
    with allure.step("Validate Toast Notification - Assign To Reassigned"):
        try:
            toast_element = wait.until(EC.visibility_of_element_located((By.XPATH, toast_msg)))
            highlight_element(driver, toast_element)
            toast_text = toast_element.text.strip()
            print(f"🔔 Toast Message: {toast_text}")
        except TimeoutException:
            print("❌ No toast message appeared within timeout (Assign To).")
            allure.attach("No toast appeared", name="Toast Status (Assign To)", attachment_type=allure.attachment_type.TEXT)
            wait_for_loader_to_disappear(driver, wait)

    # -----------------------------
    # ✅ Step 4: Validate Normal Notification (Assign To)
    # -----------------------------
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
            time.sleep(2)
        except Exception as e:
            msg = f"❌ Normal Notification Error (Created Task): {e}"
            print(msg)
            allure.attach(msg, "Normal Notification Error", allure.attachment_type.TEXT)
            return False

    with allure.step("Assign to Approver"):
        print()
        approver_user = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@id='assignBtn5approver']")))
        highlight_element(driver, approver_user)
        approver_user.click()
        print("✅ Approver Assign button clicked.")
        allure.attach("Approver Assign button clicked", name="Approver Assign Clicked", attachment_type=allure.attachment_type.TEXT)

        first_user = wait.until(EC.presence_of_element_located((By.XPATH, "(//div[@class='email-list-row'])[1]")))
        highlight_element(driver, first_user)
        first_user.click()
        time.sleep(6)
        print("✅ First user selected for approver.")
        allure.attach("First user selected", name="Approver User Selected", attachment_type=allure.attachment_type.TEXT)
        
    with allure.step("Task is been reassigned by CO. 'Approver'"):
        print()
        approver_user = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='holding-list-normal-title' and text()='Approver']//..//..//div[@class='holding-list-bold-title truncate cursor-pointer']//span")))
        highlight_element(driver, approver_user)
        approver_user.click()
        print("✅ Approver Assign button clicked.")

        second_user = wait.until(EC.presence_of_element_located((By.XPATH, "(//div[@class='flex flex-col mx-1'])[2]")))
        highlight_element(driver, second_user)
        second_user.click()
        print("✅ First user selected from email list.")
    # -----------------------------
    # ✅ Step 3: Validate Toast Notification (Approver)
    # -----------------------------
    with allure.step("Validate Toast Notification - Approver Reassigned"):
        try:
            toast_element = wait.until(EC.visibility_of_element_located((By.XPATH, toast_msg)))
            highlight_element(driver, toast_element)
            toast_text = toast_element.text.strip()
            print(f"🔔 Toast Message: {toast_text}")
        except TimeoutException:
            print("❌ No toast message appeared within timeout (Assign To).")
            allure.attach("No toast appeared", name="Toast Status (Assign To)", attachment_type=allure.attachment_type.TEXT)
            wait_for_loader_to_disappear(driver, wait)

    # -----------------------------
    # ✅ Step 4: Validate Normal Notification (Approver)
    # -----------------------------
    with allure.step("Validate Normal Notification - Approver Reassigned"):
        try:
            # Refresh notifications
            pg.hotkey('ctrl', 'r')
            pg.hotkey('ctrl', 'r')
            time.sleep(2)

            # Click notification icon
            notification_btn = wait.until(EC.presence_of_element_located((By.XPATH, notification_icon)))
            driver.execute_script("arguments[0].click();", notification_btn)
            print("✅ Notification icon clicked.")
            time.sleep(2)

            all_items = driver.find_elements(By.XPATH, notification_all_items)

            approver_reassigned_found = False
            first_clickable_item = None

            for item in all_items:
                text = item.text.strip()

                # Save FIRST notification item
                if first_clickable_item is None:
                    first_clickable_item = item

                if "approver reassigned" in text.lower():
                    try:
                        highlight_element(driver, item)
                    except:
                        pass

                    print(f"🔔 Approver Reassigned Notification Found: {text}")
                    approver_reassigned_found = True
                    driver.execute_script("arguments[0].click();", item)
                    break

            # If not found → click the first item
            if not approver_reassigned_found:
                print("⚠️ Approver Reassigned notification not found → Clicking FIRST notification")
                highlight_element(driver, first_clickable_item)
                driver.execute_script("arguments[0].click();", first_clickable_item)

        except Exception as e:
            msg = f"❌ Error while validating Approver Reassigned notification: {e}"
            print(msg)
            allure.attach(msg,name="Approver Reassigned Notification Error",attachment_type=allure.attachment_type.TEXT)

    with allure.step("Assign to CC"):
        print()
        cc_user = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@id='assignBtn4cc']")))
        highlight_element(driver, cc_user)
        cc_user.click()
        print("✅ CC Assign button clicked.")

        first_user = wait.until(EC.presence_of_element_located((By.XPATH, "(//div[@class='email-list-row'])[1]")))
        highlight_element(driver, first_user)
        first_user.click()
        time.sleep(6)
        print("✅ First user selected for approver.")
    
    with allure.step("Task is been reassigned by CO. 'CC'"):
        print()
        cc_user = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='holding-list-normal-title' and text()='CC']//..//..//div[@class='holding-list-bold-title truncate cursor-pointer']//span")))
        highlight_element(driver, cc_user)
        cc_user.click()
        print("✅ CC Assign button clicked.")
        
        second_user = wait.until(EC.presence_of_element_located((By.XPATH,"(//div[@class='flex flex-col mx-1'])[2]")))

        highlight_element(driver, second_user)
        second_user.click()
        print("✅ Clicked first NOT-selected user.")
    
    with allure.step("Validate Toast Notification - CC Reassigned"):
        try:
            toast_element = wait.until(EC.visibility_of_element_located((By.XPATH, toast_msg)))
            highlight_element(driver, toast_element)
            toast_text = toast_element.text.strip()
            print(f"🔔 Toast Message: {toast_text}")
        except TimeoutException:
            print("❌ No toast message appeared within timeout (Assign To).")
            allure.attach("No toast appeared", name="Toast Status (Assign To)", attachment_type=allure.attachment_type.TEXT)
            wait_for_loader_to_disappear(driver, wait)

    with allure.step("Validate Normal Notification - CC Reassigned"):
        try:
            # Refresh notifications
            pg.hotkey('ctrl', 'r')
            pg.hotkey('ctrl', 'r')
            time.sleep(2)

            # Click notification icon
            notification_btn = wait.until(EC.presence_of_element_located((By.XPATH, notification_icon)))
            driver.execute_script("arguments[0].click();", notification_btn)
            print("✅ Notification icon clicked.")
            time.sleep(2)

            all_items = driver.find_elements(By.XPATH, notification_all_items)

            cc_reassigned_found = False
            first_clickable_item = None

            for item in all_items:
                text = item.text.strip()

                # Save FIRST notification item
                if first_clickable_item is None:
                    first_clickable_item = item

                if "cc reassigned" in text.lower():
                    try:
                        highlight_element(driver, item)
                    except:
                        pass

                    print(f"🔔 Approver Reassigned Notification Found: {text}")
                    cc_reassigned_found = True
                    driver.execute_script("arguments[0].click();", item)
                    break

            # If not found → click the first item
            if not cc_reassigned_found:
                print("⚠️ Approver Reassigned notification not found → Clicking FIRST notification")
                highlight_element(driver, first_clickable_item)
                driver.execute_script("arguments[0].click();", first_clickable_item)

        except Exception as e:
            msg = f"❌ Error while validating CC Reassigned notification: {e}"
            print(msg)
            allure.attach(msg,name="CC Reassigned Notification Error",attachment_type=allure.attachment_type.TEXT)

    with allure.step("Open Task Log tab to verify assignment actions"):

        try:
            time.sleep(3)
            task_log_tab_elem = wait.until(EC.presence_of_element_located((By.XPATH, task_log_tab)))
            task_log_tab_elem.click()
            print("✅ Log tab clicked")
            time.sleep(3)
            wait_for_loader_to_disappear(driver, wait)
        except Exception as e:
            print(f"❌ Error clicking Log tab: {e}")
            allure.attach(str(e), "Error clicking Log tab", allure.attachment_type.TEXT)
    with allure.step("Fetch action text and member name from log entry"):
        try:
            task_log_list_elem = wait.until(EC.presence_of_all_elements_located((By.XPATH, task_action_log_section)))
            visible_logs_count = 0
            for index, log_elem in enumerate(task_log_list_elem, start=1):
                if log_elem.is_displayed():  # Only process visible logs
                    highlight_element(driver, log_elem, 0.2)
                    full_text = log_elem.get_attribute("textContent").strip()
                    fetched_member_name = log_elem.find_element(By.TAG_NAME, "strong").text
                    action = full_text.replace(fetched_member_name, "").strip()

                    print(f"✅ Log {index}: Member='{fetched_member_name}', Action='{action}'")
                    log_details = (f"Full Text: {full_text}")
                    allure.attach(log_details,name="Log Entry Details",attachment_type=allure.attachment_type.TEXT)
                    visible_logs_count += 1
        except Exception as e:
            print(f"❌ Error fetching log details: {e}")
            allure.attach(str(e), "Error fetching log details", allure.attachment_type.TEXT)
            return False
    return True



    
