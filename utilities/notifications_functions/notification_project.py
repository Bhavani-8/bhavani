import allure
import json
import os
import time
import pyautogui as pg
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from utilities.other_utils_functions.highlight import highlight_element
from selenium.common.exceptions import TimeoutException
from utilities.add_task_utils import wait_for_loader_to_disappear

   
def create_project(driver, wait):

    with allure.step("Load locators.json"):
        try:
            with open(os.path.join("data", "locators.json"), "r") as f:
                elements_details = json.load(f)

            project_icon = elements_details["project_icon"]
            notification_icon = elements_details["notification_icon"]
            toast_msg = elements_details['toast_msg']

            print("✅ locators.json loaded")
        except Exception as e:
            allure.attach(str(e), "Locators Load Error")
            return False
        
    with allure.step("Create New Project"):
        try:
            project_btn = wait.until(EC.presence_of_element_located((By.XPATH, project_icon)))
            highlight_element(driver, project_btn)
            project_btn.click()
            time.sleep(2)

            add_project_btn = wait.until(EC.presence_of_element_located((By.XPATH, "//button[@title='Add New Project']")))
            highlight_element(driver, add_project_btn)
            add_project_btn.click()

            project_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@name='project_name']")))
            highlight_element(driver, project_input)
            project_input.send_keys("Automation_project")

            project_description = wait.until(EC.presence_of_element_located((By.XPATH, "//textarea[@name='project_overview']")))
            highlight_element(driver, project_description)
            project_description.send_keys("Test Description")
            time.sleep(0.5)

            submit_btn = wait.until(EC.presence_of_element_located((By.XPATH, "//button[contains(@class,'project-management__button') and contains(@class,'primary')]")))
            highlight_element(driver, submit_btn)
            submit_btn.click()
            print("✅ Project Submit clicked")

        except Exception as e:
            allure.attach(str(e), "Project Create Error")
            return False

    # ====================================
    # STEP 3: TOAST VALIDATION
    # ====================================
    with allure.step("Verify toast Popup"):
        try:
            toast = wait.until(EC.presence_of_element_located((By.XPATH, toast_msg)))
            highlight_element(driver, toast)
            print(f"📢 Toast message: {toast.text.strip()}")
            time.sleep(3)
        except Exception:
            print("❌ No toast message found")

    # ====================================
    # STEP 4: NOTIFICATION VALIDATION
    # ====================================
    with allure.step("Validate Project Notification"):
        try:
            pg.hotkey('ctrl', 'r')
            notification_btn = wait.until(EC.presence_of_element_located((By.XPATH, notification_icon)))
            highlight_element(driver, notification_btn)
            notification_btn.click()
            time.sleep(3)

            notifications = driver.find_elements(By.XPATH, "//li[contains(@class,'normalText')]")
            for n in notifications:
                if "Project" in n.text:
                    highlight_element(driver, n)
                    print("🔔 Project Notification:", n.text.strip())
                    break
        except Exception as e:
            allure.attach(str(e), "Notification Error")
    with allure.step("Click Project Icon"):
        print()
        project_btn = wait.until(EC.presence_of_element_located((By.XPATH, project_icon)))
        highlight_element(driver, project_btn)
        project_btn.click()
        print("✅ Project Icon Clicked")
        time.sleep(2)
    # ====================================
    # STEP 5: ADD CO-OWNER (ONCE)
    # ====================================
    with allure.step("Add Co-owner"):
    
        three_dot_btn = wait.until(EC.presence_of_element_located((By.XPATH, "(//div[starts-with(@id,'context-menu-assignment')]//button)[1]")))
        highlight_element(driver, three_dot_btn)
        three_dot_btn.click()
        print("⋮ First three-dot clicked")

        add_coowner_btn = wait.until(EC.presence_of_element_located((By.XPATH, "//button[@title='Add Co-owner']")))
        highlight_element(driver, add_coowner_btn)
        add_coowner_btn.click()
        print("👥 Add Co-owner clicked")

            # Click add button (user-add icon)
            # Try to find the first "Add User" button
        add_btn = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, "//button[contains(@class,'project-management__small-icon-button')]")))
        highlight_element(driver, add_btn)
        add_btn.click()
        print("➕ Add User clicked (first option)")

            #  # Open dropdown & select first user
        dropdown_btn = wait.until(EC.presence_of_element_located((By.XPATH, "(//div[contains(@class,'indicatorContainer')])[1]")))
        highlight_element(driver, dropdown_btn)
        dropdown_btn.click()
        try:
            first_option = wait.until(EC.presence_of_element_located((By.XPATH, "(//div[contains(@class,'option')])[1]")))
            highlight_element(driver, first_option)
            first_option.click()
            print("✅ First user selected")

            submit_btn = wait.until(EC.presence_of_element_located((By.XPATH, "//button[contains(@class,'project-management__button') and text()='Submit']")))
            highlight_element(driver, submit_btn)
            submit_btn.click()
            print("✔️ Submit clicked")
            time.sleep(0.5)

            done_btn = wait.until(EC.presence_of_element_located((By.XPATH, "//button[contains(@class,'project-management__button') and contains(@class,'primary')]")))
            highlight_element(driver, done_btn)
            done_btn.click()
        except TimeoutException:
            print("⚠️ No options available — clicking Cancel")

            cancel_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Cancel']")))
            highlight_element(driver, cancel_btn)
            cancel_btn.click()
            print("❌ Selection cancelled because no options were found")

            done_btn = wait.until(EC.presence_of_element_located((By.XPATH, "//button[contains(@class,'project-management__button') and contains(@class,'primary')]")))
            highlight_element(driver, done_btn)
            done_btn.click()

        

    # Validate CO-Owner toast
    with allure.step("Verify toast Popup"):
        try:
            toast = wait.until(EC.presence_of_element_located((By.XPATH, toast_msg)))
            highlight_element(driver, toast)
            print(f"📢 Toast message: {toast.text.strip()}")
            time.sleep(3)
        except Exception:
            print("❌ No toast message found")

            # Validate notification
    with allure.step("Check Notification for CO Added"):
        pg.hotkey('ctrl', 'r'); pg.hotkey('ctrl', 'r')
        notification_btn = wait.until(EC.presence_of_element_located((By.XPATH, notification_icon)))
        highlight_element(driver, notification_btn)
        notification_btn.click()
        print("✅ Notification icon clicked")
        time.sleep(4)

        notifications = driver.find_elements(By.XPATH, "//li[contains(@class,'normalText')]")
        for notif in notifications:
            if "User added successfully" in notif.text:
                highlight_element(driver, notif)
                print("🔔 CO Notification Found:", notif.text.strip())
                allure.attach(notif.text.strip(), name="CO Notification", attachment_type=allure.attachment_type.TEXT)
                break
    with allure.step("Click Project Icon"):
        print()
        project_btn = wait.until(EC.presence_of_element_located((By.XPATH, project_icon)))
        highlight_element(driver, project_btn)
        project_btn.click()
        print("✅ Project Icon Clicked")
        time.sleep(2)


    with allure.step("Delete Project / CO"):
        three_dot = wait.until(EC.presence_of_element_located( (By.XPATH, "(//button[contains(@class,'MuiIconButton-root') and @type='button'])[last()]")))
        highlight_element(driver, three_dot)
        driver.execute_script("arguments[0].click();", three_dot)
        time.sleep(1)

        # 2️⃣ Click Delete button
        delete_btn = wait.until(EC.presence_of_element_located((By.XPATH, "//button[@title='Delete']")))
        highlight_element(driver, delete_btn)
        delete_btn.click()
        print("🗑️ Delete clicked")
        time.sleep(1)

        yes_btn = wait.until(EC.presence_of_element_located((By.XPATH, "//button[contains(@class,'project-management__button--primary')]")))
        highlight_element(driver, yes_btn)
        yes_btn.click()
        print("☑️ YES clicked — Task delete confirmed")
        time.sleep(1)


        # 3️⃣ Check for error toast
    with allure.step("Verify toast Popup"):
        try:
            toast = wait.until(EC.presence_of_element_located((By.XPATH, toast_msg)))
            highlight_element(driver, toast)
            print(f"📢 Toast message: {toast.text.strip()}")
            time.sleep(6)
        except Exception:
            print("❌ No toast message found")

    wait_for_loader_to_disappear(driver, wait)


    # -----------------------------
        # ✅ Step 3: Validate Normal Notification (Project Deleted)
        # -----------------------------
    with allure.step("Validate Normal Notification - Project Deleted"):
        try:
            time.sleep(2)
            notification_btn = wait.until(EC.presence_of_element_located((By.XPATH, notification_icon)))
            driver.execute_script("arguments[0].click();", notification_btn)
            print("✅ Notification icon clicked via JS.")
            time.sleep(2)

            all_items = driver.find_elements(By.XPATH, "//li[contains(@class,'normalText')]")

            if not all_items:
                print("❌ No normal notifications found.")
                allure.attach(
                    "No normal notifications found",
                    name="Normal Notification Missing",
                    attachment_type=allure.attachment_type.TEXT
                )
                return False

            project_deleted_found = False

            for item in all_items:
                text = item.text.strip().lower()

                # 🔥 Match project delete notification
                if "project deleted" in text:
                    try:
                        highlight_element(driver, item)
                    except:
                        pass

                    print(f"🔔 Project Deleted Notification Found: {text}")
                    project_deleted_found = True

                    # ❌ Do NOT click the notification
                    print("ℹ️ Only highlighted. Not clicking Project Deleted notification.")
                    break

            if not project_deleted_found:
                print("ℹ️ Project Deleted notification not found.")
                allure.attach(
                    "Project Deleted notification not found",
                    name="Project Deleted Missing",
                    attachment_type=allure.attachment_type.TEXT
                )
            return True

        except Exception as e:
            msg = f"❌ Error while processing Project Deleted notification: {e}"
            print(msg)
            allure.attach(
                msg,
                name="Project Deleted Notification Error",
                attachment_type=allure.attachment_type.TEXT
            )
            return False