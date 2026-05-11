import allure
import os
import json
import time
import pytest
import pyautogui as pg
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from utilities.other_utils_functions.highlight import highlight_element
from selenium.common.exceptions import TimeoutException
from utilities.add_task_utils import wait_for_loader_to_disappear
from selenium.common.exceptions import StaleElementReferenceException

def delete_tasks(driver, wait):

    with allure.step("Load locators.json"):
        try:
            with open(os.path.join("data", "locators.json"), "r") as f:
                elements_details = json.load(f)
            dashboard_icon = elements_details["dashboard_icon"]
            dash_total_btn = elements_details["dash_total_btn"]
            trash_icon = elements_details["trash_icon"]
            notification_icon = elements_details["notification_icon"]
            column_filter_search_input = elements_details['column_filter_search_input']
            column_filter_ok_btn = elements_details['column_filter_ok_btn']
            column_filter_cancel_btn = elements_details['column_filter_ok_btn']
            column_chooser_btn = elements_details['column_chooser_btn']
            column_chooser_save_btn = elements_details['column_chooser_save_btn']
            notification_icon = elements_details['notification_icon']
            toast_msg = elements_details['toast_msg']
            task_open_btn = elements_details['task_open_btn']
            creator_filter = elements_details['creator_filter']
            print("✅ locators.json loaded")

        except Exception as e:
            allure.attach(str(e), name="Locators Load Error", attachment_type=allure.attachment_type.TEXT)
            return False
    
    with allure.step("Open Dashboard"):
        try:
            print()
            dashboard_icon_elem = wait.until(EC.presence_of_element_located((By.XPATH, dashboard_icon)))
            highlight_element(driver, dashboard_icon_elem)
            dashboard_icon_elem.click()
            print("✅ Dashboard icon clicked")
        except Exception as e:
            allure.attach(str(e), name="Dashboard Open Error", attachment_type=allure.attachment_type.TEXT)
            return False 
    # Dashboard total button
    
    with allure.step("➡️ Clicking Dashboard Total button"):
        dash_total_btn_elem = wait.until(EC.presence_of_element_located((By.XPATH, dash_total_btn)))
        highlight_element(driver, dash_total_btn_elem)
        dash_total_btn_elem.click()
        wait_for_loader_to_disappear(driver, wait)
        print("✅ Clicked Dashboard Total button")
    
    with allure.step("Clicking Column Chooser"):
        column_chooser_btn_elem = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@role='button' and @aria-label='columnchooser']")))
        highlight_element(driver, column_chooser_btn_elem)
        column_chooser_btn_elem.click()
        print("✅ Opened Column Chooser")

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

    with allure.step("Select Creator column "):
        creator_option = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='dx-item-content dx-list-item-content' and normalize-space()='Creator']")))
        actions = ActionChains(driver)
        actions.move_to_element(creator_option).perform()
        time.sleep(0.5)
        # wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='dx-item-content dx-list-item-content' and normalize-space()='Creator']")))
        creator_option.click()


        save_btn = wait.until(EC.element_to_be_clickable((By.XPATH, column_chooser_save_btn)))
        highlight_element(driver, save_btn)
        save_btn.click()
        print("✅ Column Chooser saved")
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
        creator_filter_btn = wait.until(EC.presence_of_element_located((By.XPATH, creator_filter)))
        highlight_element(driver, creator_filter_btn)
        creator_filter_btn.click()
        time.sleep(2)

        search_input = wait.until(EC.presence_of_element_located((By.XPATH, column_filter_search_input)))
        highlight_element(driver, search_input)
        search_input.clear()

        # 🔥 Dynamic search value
        search_input.send_keys(username)

        print(f"🔍 Searching Creator filter using username: {username}")
        allure.attach(username, "Creator Filter Search Value", allure.attachment_type.TEXT)

        time.sleep(1)

    try:
        search_task = wait.until(EC.element_to_be_clickable((By.XPATH,f"//div[contains(@class,'dx-list-item-content') and normalize-space()=\"{username}\"]")))
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
    time.sleep(0.8)
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
    # STEP 1: DELETE TASK
    with allure.step("Step 1: Delete Task"):
        try:
            print()
            time.sleep(2)
            delete_btn = wait.until(EC.presence_of_element_located((By.XPATH, "//button[@title='Delete']")))
            highlight_element(driver, delete_btn)
            delete_btn.click()
            print("🗑️ Delete button clicked")

            yes_btn = wait.until(EC.presence_of_element_located((By.XPATH,"//button[span='Delete']")))
            highlight_element(driver, yes_btn)
            yes_btn.click()
            print("☑️ YES clicked — Task delete confirmed")

        except Exception as e:
            allure.attach(str(e), name="Delete Task Error", attachment_type=allure.attachment_type.TEXT)
            return False

    with allure.step("Verify toast Popup"):
        try:
            toast = wait.until(EC.presence_of_element_located((By.XPATH, toast_msg)))
            highlight_element(driver, toast)
            print(f"📢 Toast message: {toast.text.strip()}")
            time.sleep(6)
        except Exception:
            print("❌ No toast message found")

    wait_for_loader_to_disappear(driver, wait)

    # STEP 3: CHECK NOTIFICATION
    with allure.step("Step 3: Check Notification for Deleted Task"):
        try:
            # Refresh once to load new notifications
            pg.hotkey('ctrl', 'r')
            pg.hotkey('ctrl','r')
            notification_btn = wait.until(EC.presence_of_element_located((By.XPATH, notification_icon)))
            highlight_element(driver, notification_btn)
            notification_btn.click()
            print("🔔 Notification icon clicked")
            time.sleep(2)
            all_notifications = driver.find_elements(By.XPATH, "//li[contains(@class,'styles_normalText__')]")

            found = False
            for notif in all_notifications:
                if "deleted" in notif.text.lower():
                    highlight_element(driver, notif)
                    print(f"🔔 Notification Found: {notif.text.strip()}")
                    found = True
                    break

            if not found:
                print("ℹ️ Deleted task notification not present")

        except Exception as e:
            print(f"❌ Error reading notifications: {e}")
            allure.attach(str(e), name="Notification Error", attachment_type=allure.attachment_type.TEXT)

    with allure.step("Step 4: Click Trash Icon"):
        try:
            print()
            trash_btn = wait.until(EC.presence_of_element_located((By.XPATH, trash_icon)))
            highlight_element(driver, trash_btn)
            trash_btn.click()
            print("🗑️ Trash icon clicked")

        except Exception as e:
            allure.attach(str(e), name="Trash Icon Error", attachment_type=allure.attachment_type.TEXT)
            return False

    with allure.step("Step 5: Click Tasks Tab"):
        try:
            time.sleep(3)
            tasks_tab = wait.until(EC.presence_of_element_located((By.XPATH, "//p[normalize-space()='Tasks'] | //span[normalize-space()='Tasks']")))
            highlight_element(driver, tasks_tab)
            tasks_tab.click()
            print("📌 Tasks tab clicked")

        except Exception as e:
            allure.attach(str(e), name="Tasks Tab Error", attachment_type=allure.attachment_type.TEXT)
            return False

    with allure.step("Step 6: Delete Created Task Again"):
        try:
            delete_elem_btn = wait.until(EC.presence_of_element_located((By.XPATH, "(//button[@title='Delete Task'])")))
            highlight_element(driver, delete_elem_btn)
            delete_elem_btn.click()
            print("🗑️ Delete Created Task clicked")

            yes_elem_btn = wait.until(EC.presence_of_element_located((By.XPATH,"//button[contains(@class,'project-management__button--primary')]")))
            highlight_element(driver, yes_elem_btn)
            yes_elem_btn.click()
            pg.hotkey('ctrl', 'r')
            time.sleep(0.5)
            print("☑️ YES clicked for 2nd delete")

        except Exception as e:
            allure.attach(str(e), name="Second Delete Error", attachment_type=allure.attachment_type.TEXT)
            return False
        
    with allure.step("Verify toast Popup"):
        try:
            toast = wait.until(EC.presence_of_element_located((By.XPATH, toast_msg)))
            highlight_element(driver, toast)
            print(f"📢 Toast message: {toast.text.strip()}")
        except Exception:
            print("❌ No toast message found")

    wait_for_loader_to_disappear(driver, wait)

    # STEP 3: CHECK NOTIFICATION
    with allure.step("Step 3: Check Notification for Deleted Task"):
        try:
            # Refresh once to load new notifications
            pg.hotkey('ctrl', 'r')
            time.sleep(1)
            notification_btn = wait.until(EC.presence_of_element_located((By.XPATH, notification_icon)))
            highlight_element(driver, notification_btn)
            notification_btn.click()
            print("🔔 Notification icon clicked")
            time.sleep(2)
            all_notifications = driver.find_elements(By.XPATH, "//li[contains(@class,'styles_normalText__')]")

            found = False
            for notif in all_notifications:
                if "deleted" in notif.text.lower():
                    highlight_element(driver, notif)
                    print(f"🔔 Notification Found: {notif.text.strip()}")
                    found = True
                    break

            if not found:
                print("ℹ️ Deleted task notification not present")

        except Exception as e:
            print(f"❌ Error reading notifications: {e}")
            allure.attach(str(e), name="Notification Error", attachment_type=allure.attachment_type.TEXT)

    return True