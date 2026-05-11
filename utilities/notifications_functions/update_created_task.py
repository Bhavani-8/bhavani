import allure
import os
import json
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from utilities.other_utils_functions.highlight import highlight_element
from selenium.common.exceptions import TimeoutException
import time
import pyautogui as pg
from utilities.add_task_functions.set_task_name import set_task_name
from utilities.add_task_utils import wait_for_loader_to_disappear




def update_created_task(driver, wait):

    # ✅ Step 3: Load locators
    with allure.step("Load locators.json"):
        try:
            with open(os.path.join("data", 'locators.json'), 'r') as f:
                elements_details = json.load(f)
            task_comment_tab = elements_details["task_comment_tab"]
            notification_icon = elements_details['notification_icon']
            toast_msg = elements_details['toast_msg']
            print("✅ locators.json loaded successfully")
        except Exception as e:
            allure.attach(str(e), name="Locators Load Error", attachment_type=allure.attachment_type.TEXT)
            return False
    
   
    with allure.step("Validate Normal Notification - Created Task"):
        try:
            time.sleep(5)

            notification_btn = wait.until(EC.presence_of_element_located((By.XPATH, notification_icon)))
            driver.execute_script("arguments[0].click();", notification_btn)
            print("✅ Notification icon clicked via JS.")
            time.sleep(7)
            all_items = driver.find_elements(By.XPATH, "//li[contains(@class,'normalText')]")
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


        edit_btn = wait.until(EC.presence_of_element_located((By.XPATH, "//button[@title='Edit']")))
        highlight_element(driver, edit_btn)
        edit_btn.click()
        print("✅ Edit clicked successfully.")



    with allure.step("Update Task Name"):
        try:
            # Wait for the task name input field to appear after clicking Edit
            task_name_input = wait.until(
                EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Task Name*']"))
            )
            highlight_element(driver, task_name_input)

            # Get current task name
            old_name = task_name_input.get_attribute("value")

            # Define new task name
            new_name = "Automation Task Updated"

            # Clear and update name
            task_name_input.clear()
            task_name_input.send_keys(new_name)
            print(f"✅ Task name updated successfully from '{old_name}' to '{new_name}'")

            # Attach before-after names to Allure
            allure.attach(
                f"Old Name: {old_name}\nNew Name: {new_name}",
                name="Updated Task Name Details",
                attachment_type=allure.attachment_type.TEXT
            )

            # Click Save or Update button
            save_btn = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Save') or contains(., 'Update')]"))
            )
            highlight_element(driver, save_btn)
            save_btn.click()
            print("✅ Save/Update button clicked successfully.")

        except Exception as e:
            msg = f"❌ Error while updating task name: {e}"
            print(msg)
            allure.attach(msg, name="Set Task Name Error", attachment_type=allure.attachment_type.TEXT)
            return False
    with allure.step("Popup Message"):
        update_popup = wait.until(EC.presence_of_element_located((By.XPATH, toast_msg)))
        highlight_element(driver, update_popup)
        print("✅ Task updated successfully")
        allure.attach("Task updated successfully", name="Task Updated Popup", attachment_type=allure.attachment_type.TEXT)

    # Validate toast message
    with allure.step("Validate toast notification for creation of a task without an assignee"):
        toast = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, toast_msg)
            )
        )
        highlight_element(driver, toast)
        print(f"📢 Toast message: {toast.text.strip()}")
    
    with allure.step("Validate Normal Notification - Created Task"):
        try:
            # Refresh page to load notifications
            pg.hotkey('ctrl', 'r')
            pg.hotkey('ctrl', 'r')
            time.sleep(2)

            # Click the notification icon
            notification_btn = wait.until(EC.presence_of_element_located((By.XPATH, notification_icon)))
            driver.execute_script("arguments[0].click();", notification_btn)
            print("✅ Notification icon clicked via JS.")
            time.sleep(2)

            # Fetch all normal notifications
            all_items = driver.find_elements(By.XPATH, "//li[contains(@class,'normalText')]")

            if not all_items:  
                # ❗ No notifications found
                print("ℹ️ No normal notifications found.")
                allure.attach("No normal notifications found", 
                            name="Normal Notification Missing", 
                            attachment_type=allure.attachment_type.TEXT)
                return False
            else:
                # ✔️ Notification found
                first_notification = all_items[0]
                driver.execute_script("arguments[0].scrollIntoView(true);", first_notification)

                try:
                    highlight_element(driver, first_notification)
                except Exception:
                    pass

                message_text = first_notification.text.strip()
                print(f"🔔 Normal Notification Found: {message_text}")

                allure.attach(message_text, 
                            name="Normal Notification (Created Task)", 
                            attachment_type=allure.attachment_type.TEXT)

                return True

        except Exception as e:
            msg = f"❌ Normal Notification Error (Created Task): {e}"
            print(msg)
            allure.attach(msg, 
                        name="Normal Notification Error (Created Task)", 
                        attachment_type=allure.attachment_type.TEXT)
            return False
