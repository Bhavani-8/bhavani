import allure
import os
import json
import time
import pyautogui as pg

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys

from utilities.other_utils_functions.highlight import highlight_element
from selenium.common.exceptions import TimeoutException
from utilities.add_task_utils import wait_for_loader_to_disappear

def edit_personal_details(driver, wait):


    # Step 1: Load locators
    with allure.step("Load locators.json"):
        try:
            with open(os.path.join("data", "locators.json"), "r") as f:
                elements_details = json.load(f)
            settings_icon = elements_details["settings_icon"]
            notification_icon = elements_details["notification_icon"]
            toast_msg = elements_details["toast_msg"]
            print("✅ locators.json loaded successfully")
        except Exception as e:
            allure.attach(str(e), name="Locators Load Error", attachment_type=allure.attachment_type.TEXT)
            return False

    # Step 2: Editing Personal Details   
    with allure.step("Editing Personal Details"):
        try:
            print()
            # Click Project Icon
            settings_btn = wait.until(EC.presence_of_element_located((By.XPATH, settings_icon)))
            highlight_element(driver, settings_btn)
            settings_btn.click()
            print("✅ Settings Icon Clicked")

            time.sleep(2)

            # Click "Add New Project"
            personal_btn = wait.until(EC.presence_of_element_located((By.XPATH, "//li[@class='active-class un-active-class']")))
            highlight_element(driver, personal_btn)
            personal_btn.click()
            print("✅ Add New Project button clicked")

            # Wait for designation input
            designation_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@id='designation']")))
            highlight_element(driver, designation_input)

            # Get current value
            current_value = designation_input.get_attribute("value").strip()
            print(f"🔎 Current Designation: {current_value}")

            # Decide new value based on current text
            if current_value.lower() == "team member":
                new_value = "Approver"
            elif current_value.lower() == "approver":
                new_value = "Team Member"
            else:
                new_value = "Team Member"  # default if empty/other value

            # Clear and set the new designation
            designation_input.clear()
            designation_input.send_keys(new_value)

            print(f"✅ Designation updated to: {new_value}")

            # Click Submit Button
            save_btn = wait.until(EC.presence_of_element_located((By.XPATH, "//button[contains(@class,'save-changes-blue-btn')]")))
            highlight_element(driver, save_btn)
            if save_btn.is_enabled():
                save_btn.click()
                print("✅ Save button clicked")
            else:
                print("⚠️ Save button is disabled")

        except Exception as e:
            allure.attach(str(e), name="Personal Details Submission Error", attachment_type=allure.attachment_type.TEXT)
            return False
        

    with allure.step("Verify toast Popup"):
        try:
            toast = wait.until(EC.presence_of_element_located((By.XPATH, toast_msg)))
            highlight_element(driver, toast)
            print(f"📢 Toast message: {toast.text.strip()}")
        except Exception:
            print("❌ No toast message found")

    wait_for_loader_to_disappear(driver, wait)

    with allure.step("Validate Normal Notification - Personal Details"):
        try:
            # Refresh page to load notifications
            pg.hotkey('ctrl', 'r')  

            # Click the notification icon
            notification_btn = wait.until(EC.presence_of_element_located((By.XPATH, notification_icon)))
            highlight_element(driver, notification_btn)
            notification_btn.click()
            time.sleep(2)  # wait for notifications to load

            # Get all normal notifications
            all_items = driver.find_elements(By.XPATH, "//li[contains(@class,'normalText')]")

            # Check for personal details notification
            personal_notification_found = False
            for item in all_items:
                text = item.text.strip()
                if "Personal" in text:  # adjust keyword if needed
                    highlight_element(driver, item)
                    print(f"🔔 Personal Details Notification Found: {text}")
                    allure.attach(text, name="Personal Details Notification", attachment_type=allure.attachment_type.TEXT)
                    personal_notification_found = True
                    # Click the notification to open details
                    driver.execute_script("arguments[0].click();", item)
                    print("✅ Personal Details Notification clicked")
                    break

            if not personal_notification_found:
                print("ℹ️ Personal Details notification not found. Opening Personal Details page...")
                personal_btn = wait.until(EC.presence_of_element_located((By.XPATH, notification_icon)))  # replace with your icon XPath
                highlight_element(driver, personal_btn)

        except Exception as e:
            msg = f"❌ Error while checking personal details notification: {e}"
            print(msg)
            allure.attach(msg, name="Personal Notification Error", attachment_type=allure.attachment_type.TEXT)

    return True