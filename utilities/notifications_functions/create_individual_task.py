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




def create_individual_task(driver, wait):

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


    # ✅ Step 5: Comment added by User (Team Member)
    with allure.step("Added a comment as a user in the CO login"):
        print()

        # Click comment tab
        comment_user = wait.until(EC.presence_of_element_located((By.XPATH, task_comment_tab)))
        highlight_element(driver, comment_user)
        comment_user.click()
        print("✅ Comment tab clicked successfully.")
        # Locate comment input box
        comment_box = wait.until(EC.presence_of_element_located((By.XPATH, "//textarea[contains(@placeholder, 'Add a comment')]")))
        highlight_element(driver, comment_box)

        # Enter comment text
        comment_text = "This is a test comment"
        comment_box.send_keys(comment_text)
        print(f"✅ Comment entered: {comment_text}")
        allure.attach(comment_text, name="Entered Comment", attachment_type=allure.attachment_type.TEXT)

        # Highlight entered comment text
        highlight_element(driver, comment_box)

        # Locate and click the arrow (send) icon
        arrow_icon = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='inputIcon']//img[@alt='arrow-right']")))
        driver.execute_script("arguments[0].click();", arrow_icon)
        time.sleep(3)

        print("✅ Comment send arrow clicked successfully.")

    # -----------------------
    # 1️⃣ Validate Comment Popup (IF Present)
    # -----------------------
    # with allure.step("Validate 'Comments Added' popup"):
    #     comment_popup = None
    #     try:
    #         comment_popup = wait.until(
    #             EC.presence_of_element_located(
    #                 (By.XPATH, "//div[p[text()='Comments Added']]")
    #             )
    #         )
    #         highlight_element(driver, comment_popup)
    #         print("✅ Comment popup displayed: 'Comments Added'")
    #         allure.attach("Comment popup displayed", "Comments Added Popup",
    #                     allure.attachment_type.TEXT)

    #     except TimeoutException:
    #         print("ℹ️ 'Comments Added' popup NOT displayed — checking toast instead.")


# -----------------------
# 2️⃣ Validate Toast Notification (ONLY if popup not displayed)
# -----------------------
    with allure.step("Validate toast notification for creation of task without assignee"):
        try:
            toast = wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, toast_msg)
                )
            )
            highlight_element(driver, toast)
            print(f"📢 Toast message: {toast.text.strip()}")
        except Exception:
            print("❌ No toast message found")


# -----------------------
# 3️⃣ Validate Normal Notification - Created Task
# -----------------------
    with allure.step("Validate Normal Notification - Mark Complete"):
        try:
            time.sleep(5)

            notification_btn = wait.until(EC.presence_of_element_located((By.XPATH, notification_icon)))
            driver.execute_script("arguments[0].click();", notification_btn)
            print("✅ Notification icon clicked")
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
            time.sleep(2)
        except Exception as e:
            msg = f"❌ Normal Notification Error (Created Task): {e}"
            print(msg)
            allure.attach(msg, "Normal Notification Error", allure.attachment_type.TEXT)
            return False
    return True
        
        