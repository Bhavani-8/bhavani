import allure
import os
import json
import time
import pytest
import pyautogui as pg
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from utilities.add_task_utils import wait_for_loader_to_disappear
from utilities.highlight import highlight_element
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver import ActionChains
from selenium.common.exceptions import TimeoutException


def pending_approval(driver, wait, task_name='Internal Task'):

    # ✅ Step 1: Load locators
    with allure.step("Load locators.json"):
        try:
            with open(os.path.join("data", "locators.json"), "r") as f:
                elements_details = json.load(f)
            dash_total_btn = elements_details["dash_total_btn"]
            notification_icon = elements_details["notification_icon"]
            column_chooser_btn = elements_details["column_chooser_btn"]
            toast_msg = elements_details["toast_msg"]
            column_chooser_btn = elements_details['column_chooser_btn']
            creator_filter = elements_details['creator_filter']
            column_filter_search_input = elements_details['column_filter_search_input']
            column_chooser_btn = elements_details['column_chooser_btn']
            company_project_filter = elements_details['company_project_filter']
            column_filter_search_input = elements_details['column_filter_search_input']
            notification_icon = elements_details['notification_icon']
            company_project_option = elements_details['company_project_option']
            toast_msg = elements_details['toast_msg']

            print("✅ locators.json loaded successfully")
        except Exception as e:
            allure.attach(str(e), name="Locators Load Error", attachment_type=allure.attachment_type.TEXT)
            return False
    
    
    with allure.step("➡️ Clicking Dashboard Total button"):
        dash_total_btn_elem = wait.until(EC.presence_of_element_located((By.XPATH, dash_total_btn)))
        highlight_element(driver, dash_total_btn_elem)
        dash_total_btn_elem.click()
        wait_for_loader_to_disappear(driver, wait)
        print("✅ Clicked Dashboard Total button")
        
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

    with allure.step("Select 'Approver', Creator column only"):
        try: 
            company_project_option_elm = wait.until(EC.presence_of_element_located((By.XPATH, company_project_option)))
            actions = ActionChains(driver)
            actions.move_to_element(company_project_option_elm).perform()
            time.sleep(0.5)
            company_project_option_elm.click()  

            approver_option = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='dx-item-content dx-list-item-content' and normalize-space()='Approver']")))
            actions = ActionChains(driver)
            actions.move_to_element(approver_option).perform()
            time.sleep(0.5)
            wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='dx-item-content dx-list-item-content' and normalize-space()='Approver']")))
            approver_option.click()

            creator_option = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='dx-item-content dx-list-item-content' and normalize-space()='Creator']")))
            actions = ActionChains(driver)
            actions.move_to_element(creator_option).perform()
            time.sleep(0.5)
            wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='dx-item-content dx-list-item-content' and normalize-space()='Creator']")))
            creator_option.click()
        except TimeoutException:
            print("Approver, Creator not found in filter list")
        try:
            save_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@role='button' and @aria-label='Save & Close']")))
            highlight_element(driver, save_btn)
            save_btn.click()
            time.sleep(5)
            print("✅ Saved Approver, Creator chooser")
            wait_for_loader_to_disappear(driver, wait)
        except TimeoutException:
            pytest.fail("❌ Save button not available / not clickable")
        
        try:
            toast = wait.until(EC.presence_of_element_located((By.XPATH, toast_msg)))
            highlight_element(driver, toast)
            print(f"📢 Toast message: {toast.text.strip()}")
            time.sleep(4)
        except Exception:
            print("❌ No toast message found")
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
    with allure.step("Open Approver column filter and search for 'Assign'"):
        approver_filter = wait.until(EC.presence_of_element_located((By.XPATH, "//td[@role='columnheader'][.//text()[normalize-space()='Approver']]//span[contains(@class,'dx-header-filter')]")))
        approver_filter.click()
        highlight_element(driver,  approver_filter)
        time.sleep(2)

        search_input = wait.until(EC.presence_of_element_located((By.XPATH, column_filter_search_input)))
        highlight_element(driver, search_input)
        search_input.clear()
        search_input.send_keys(username)
        time.sleep(3)
    
        search_task = wait.until(EC.element_to_be_clickable((By.XPATH,f"//div[contains(@class,'dx-list-item-content') and normalize-space()=\"{username}\"]")))
        search_task.click()
    with allure.step("Click Company Project"):
        company_project_filter_btn = wait.until(EC.presence_of_element_located((By.XPATH, company_project_filter)))
        highlight_element(driver, company_project_filter_btn)
        company_project_filter_btn.click()
        time.sleep(2)

        search_input = wait.until(EC.presence_of_element_located((By.XPATH, column_filter_search_input)))
        search_input.clear()
        search_input.send_keys(task_name)
        time.sleep(3)

        search_task = wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class,'dx-list-item-content') and normalize-space()='Internal Task']")))
        search_task.click()
        print("✅ Clicked 'Internal Task'")

        ok_btn = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@aria-label='OK']")))
        highlight_element(driver, ok_btn)
        ok_btn.click()
        time.sleep(2)
        print("Clicked OK")
        wait_for_loader_to_disappear(driver, wait)
        
    with allure.step("Click Creator Filter"):
        creator_filter_btn = wait.until(EC.presence_of_element_located((By.XPATH, creator_filter)))
        highlight_element(driver, creator_filter_btn)
        creator_filter_btn.click()
        time.sleep(2)

        search_input = wait.until(EC.presence_of_element_located((By.XPATH, column_filter_search_input)))
        highlight_element(driver, search_input)
        search_input.clear()
        search_input.send_keys(username)
        time.sleep(3)

        search_task = wait.until(EC.element_to_be_clickable((By.XPATH,f"//div[contains(@class,'dx-list-item-content') and normalize-space()=\"{username}\"]")))
        search_task.click()

        ok_btn = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@aria-label='OK']")))
        highlight_element(driver, ok_btn)
        ok_btn.click()
        time.sleep(2)
        print("Clicked OK")
        wait_for_loader_to_disappear(driver, wait)

    with allure.step("Click 'Mark Complete'"): 
        # Try clicking Mark Complete if present
        mark_complete_btn = wait.until(EC.presence_of_element_located((By.XPATH, "//button[.//span[text()='Mark Complete']]")))
        highlight_element(driver, mark_complete_btn)
        mark_complete_btn.click()
        print("✅ Mark Complete clicked")
        yes_btn = wait.until(EC.presence_of_element_located((By.XPATH, "//button[contains(@class,'ant-btn') and .//span[normalize-space()='Yes']]")))
        highlight_element(driver, yes_btn)
        yes_btn.click()
    

    with allure.step("Validate first Normal Notification"):
        try:
            # Refresh page to load notifications
            pg.hotkey('ctrl', 'r')
            pg.hotkey('ctrl', 'r')
            time.sleep(2)  # small wait after refresh

            # Click the notification icon
            notification_btn = wait.until(EC.presence_of_element_located((By.XPATH, notification_icon)))
            highlight_element(driver, notification_btn)
            notification_btn.click()
            time.sleep(2)  # wait for notifications to load

            # Get all normal notifications
            all_items = driver.find_elements(By.XPATH, "//li[contains(@class,'styles_normalText__')]")

            if all_items:
                first_item = all_items[0]
                highlight_element(driver, first_item)
                print(f"🔔 Normal Notification: {first_item.text.strip()}")
                return True
            else:
                print("ℹ️ No notifications found.")
                allure.attach("No notifications found", name="Notification Missing", attachment_type=allure.attachment_type.TEXT)
                return False

        except Exception as e:
            msg = f"❌ Error while fetching notifications: {e}"
            print(msg)
            allure.attach(msg, name="Notification Fetch Error", attachment_type=allure.attachment_type.TEXT)
            return False

