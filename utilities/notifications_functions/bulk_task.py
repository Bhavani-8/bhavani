import allure
import os
import json
import time
import pyautogui as pg
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from utilities.other_utils_functions.highlight import highlight_element
from utilities.add_task_utils import wait_for_loader_to_disappear


def bulk_task_not_assigned(driver, wait, filename='bulk_task_not_assigned_team_member.xlsx'):
    wait_less = WebDriverWait(driver, 5)
    # Step 1: Load locators
    with allure.step("Load locators.json"):
        try:
            with open(os.path.join("data", "locators.json"), "r") as f:
                elements_details = json.load(f)
            toast_msg = elements_details['toast_msg']
            notification_icon = elements_details["notification_icon"]
            add_task_float = elements_details['add_task_float'] 
            add_task_btn = elements_details['add_task_btn']
            create_bulk_task_btn = elements_details['create_bulk_task_btn']
            create_bulk_task_label = elements_details['create_bulk_task_label']
            dash_bulk_task_dropdown_file_input = elements_details['dash_bulk_task_dropdown_file_input']
            bulk_task_error_file_btn = elements_details['bulk_task_error_file_btn']
            form_cancel_btn = elements_details['form_cancel_btn']
            create_tasks_btn = elements_details['create_tasks_btn']
            print("✅ locators.json loaded successfully")
        except Exception as e:
            allure.attach(str(e), name="Locators Load Error", attachment_type=allure.attachment_type.TEXT)
            return False
        
    # Add Task Float
    # -------------------------
    try:
        with allure.step("➡️ Opening Add Task Float"):
            print()
            add_task_float_btn = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, add_task_float)))
            highlight_element(driver, add_task_float_btn)
            add_task_float_btn.click()
            wait_for_loader_to_disappear(driver, wait)
            print("✅ Opened Add Task Float")
    except Exception as err:
        allure.attach(str(err), name="Add Task Float Error", attachment_type=allure.attachment_type.TEXT)
        print(f"❌ Error opening Add Task Float: {err}")

    # -------------------------
    # Add Task Button
    # -------------------------
    try:
        with allure.step("➡️ Clicking Add Task Button"):
            print()
            add_task_button = wait.until(EC.presence_of_element_located((By.XPATH, add_task_btn)))
            highlight_element(driver, add_task_button)
            add_task_button.click()
            wait_for_loader_to_disappear(driver, wait)
            print("✅ Clicked Add Task Button")
    except Exception as err:
        allure.attach(str(err), name="Add Task Button Error", attachment_type=allure.attachment_type.TEXT)
        print(f"❌ Error clicking Add Task Button: {err}")

    # # Step 2: Bulk Task Creationr
    with allure.step(" Opening Bulk Task Creation form"):
        try:
            print()
            create_bulk_task_btn_elem = wait.until(EC.presence_of_element_located((By.XPATH, create_bulk_task_btn)))
            highlight_element(driver, create_bulk_task_btn_elem)
            create_bulk_task_btn_elem.click()
            wait_for_loader_to_disappear(driver, wait)
            print("✅ Create Bulk Task Clicked")

            time.sleep(2)
        except Exception as err:
            allure.attach(str(err), name="Bulk Task Form Error", attachment_type=allure.attachment_type.TEXT)
            print(f"❌ Error opening Bulk Task Creation form: {err}")
    try:
        with allure.step("➡️ Verifying Bulk Task Creation form title"):
            create_bulk_task_label_elem = wait.until(EC.presence_of_element_located((By.XPATH, create_bulk_task_label)))
            highlight_element(driver, create_bulk_task_label_elem)
            if create_bulk_task_label_elem.text == 'Bulk Task Creation':
                print("✅ Bulk Task Creation form title verified")
            else:
                print("❌ Bulk Task Creation form title mismatch")
                allure.attach("Form title mismatch", name="Form Title Error", attachment_type=allure.attachment_type.TEXT)
    except Exception as err:
        allure.attach(str(err), name="Form Title Error", attachment_type=allure.attachment_type.TEXT)
        print(f"❌ Error verifying Bulk Task Creation form: {err}")

    try:
        with allure.step("➡️ Uploading bulk task file"):
            file_input_elem = wait.until(EC.presence_of_element_located((By.XPATH, dash_bulk_task_dropdown_file_input)))
            highlight_element(driver, file_input_elem)
            file_path = os.path.abspath(os.path.join('data', filename))
            file_input_elem.send_keys(file_path)
            wait_for_loader_to_disappear(driver, wait)
            print(f"✅ Uploaded file: {file_path}")
    except Exception as err:
        allure.attach(str(err), name="File Upload Error", attachment_type=allure.attachment_type.TEXT)
        print(f"❌ Error uploading file: {err}")

    try:
        with allure.step("➡️ Handling validation results"):
            try:
                bulk_task_error_file_btn_elem = wait_less.until(EC.presence_of_element_located((By.XPATH, bulk_task_error_file_btn)))
                highlight_element(driver, bulk_task_error_file_btn_elem)
                bulk_task_error_file_btn_elem.click()

                form_cancel_btn_elem = wait_less.until(EC.presence_of_element_located((By.XPATH, form_cancel_btn)))
                highlight_element(driver, form_cancel_btn_elem)
                form_cancel_btn_elem.click()
                wait_for_loader_to_disappear(driver, wait)
                print("ℹ️ Error file found and form closed")
            except TimeoutException:
                print("ℹ️ No error file found, proceeding with task creation")
                create_tasks_btn_elem = wait_less.until(EC.presence_of_element_located((By.XPATH, create_tasks_btn)))
                highlight_element(driver, create_tasks_btn_elem)
                if create_tasks_btn_elem.is_enabled():
                    create_tasks_btn_elem.click()
                    print("✅ Clicked Create Tasks button")
                else:
                    form_cancel_btn_elem = wait_less.until(EC.presence_of_element_located((By.XPATH, form_cancel_btn)))
                    highlight_element(driver, form_cancel_btn_elem)
                    form_cancel_btn_elem.click()
                    print("❌ Create button disabled. Form closed")
                    allure.attach("Create button disabled. Form closed", name="Create Tasks Error", attachment_type=allure.attachment_type.TEXT)
                wait_for_loader_to_disappear(driver, wait)
    except Exception as err:
        allure.attach(str(err), name="Validation Handling Error", attachment_type=allure.attachment_type.TEXT)
        print(f"❌ Error handling validation: {err}")

    try:
        with allure.step("➡️ Checking for toast message"):
            try:
                toast_msg_elem = wait.until(EC.presence_of_element_located((By.XPATH, toast_msg)))
                highlight_element(driver, toast_msg_elem)
                msg = toast_msg_elem.text
                print(f"✅ Toast message displayed: {msg}")
                wait.until(EC.invisibility_of_element_located((By.XPATH, toast_msg)))
                wait_for_loader_to_disappear(driver, wait)
                time.sleep(3)
            except TimeoutException:
                print("ℹ️ No toast message found")
            except Exception as e:
                allure.attach(str(e), name="Toast Error", attachment_type=allure.attachment_type.TEXT)
                print(f"❌ Error fetching toast: {e}")
    except Exception as err:
        allure.attach(str(err), name="Toast Handling Error", attachment_type=allure.attachment_type.TEXT)
        print(f"❌ Unexpected error while handling toast: {err}")

    with allure.step("Step 3: Check Notification for Bulk Task"):
        try:
            # Refresh once to load new notifications
            pg.hotkey('ctrl', 'r')
            pg.hotkey('ctrl', 'r')

            notification_btn = wait.until(
                EC.presence_of_element_located((By.XPATH, notification_icon))
            )
            highlight_element(driver, notification_btn)
            notification_btn.click()
            print("🔔 Notification icon clicked")
            time.sleep(2)

            # Get all notifications
            all_notifications = driver.find_elements(
                By.XPATH, "//li[contains(@class,'styles_normalText__')]"
            )

            found = False
            for notif in all_notifications:
                if "bulk task" in notif.text.lower():     # 🔥 CHANGED HERE
                    highlight_element(driver, notif)
                    print(f"🔔 Bulk Task Notification Found: {notif.text.strip()}")
                    found = True
                    break

            if not found:
                print("ℹ️ Bulk Task notification not present")

        except Exception as e:
            print(f"❌ Error reading notifications: {e}")
            allure.attach(str(e), name="Notification Error", attachment_type=allure.attachment_type.TEXT)

        

    #     with allure.step("Open Dashboard"):
    #         try:
    #             print()
    #             dashboard_icon_elem = wait.until(EC.presence_of_element_located((By.XPATH, dashboard_icon)))
    #             highlight_element(driver, dashboard_icon_elem)
    #             dashboard_icon_elem.click()
    #             print("✅ Dashboard icon clicked")
    #         except Exception as e:
    #             allure.attach(str(e), name="Dashboard Open Error", attachment_type=allure.attachment_type.TEXT)
    #             return False
    #     # Add Task Float
    #     # -------------------------
    #     try:
    #         with allure.step("➡️ Opening Add Task Float"):
    #             add_task_float_btn = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, add_task_float)))
    #             highlight_element(driver, add_task_float_btn)
    #             add_task_float_btn.click()
    #             wait_for_loader_to_disappear(driver, wait)
    #             print("✅ Opened Add Task Float")
    #     except Exception as err:
    #         allure.attach(str(err), name="Add Task Float Error", attachment_type=allure.attachment_type.TEXT)
    #         print(f"❌ Error opening Add Task Float: {err}")

    # # -------------------------
    # # Add Task Button
    # # -------------------------
    # try:
    #     with allure.step("➡️ Clicking Add Task Button"):
    #         add_task_button = wait.until(EC.presence_of_element_located((By.XPATH, add_task_btn)))
    #         highlight_element(driver, add_task_button)
    #         add_task_button.click()
    #         wait_for_loader_to_disappear(driver, wait)
    #         print("✅ Clicked Add Task Button")
    # except Exception as err:
    #     allure.attach(str(err), name="Add Task Button Error", attachment_type=allure.attachment_type.TEXT)
    #     print(f"❌ Error clicking Add Task Button: {err}")

    # # # Step 2: Bulk Task Creationr
    # with allure.step(" Opening Bulk Task Creation form"):
    #     try:
    #         create_bulk_task_btn_elem = wait.until(EC.presence_of_element_located((By.XPATH, create_bulk_task_btn)))
    #         highlight_element(driver, create_bulk_task_btn_elem)
    #         create_bulk_task_btn_elem.click()
    #         wait_for_loader_to_disappear(driver, wait)
    #         print("✅ Create Bulk Task Clicked")

    #         time.sleep(2)
    #     except Exception as err:
    #         allure.attach(str(err), name="Bulk Task Form Error", attachment_type=allure.attachment_type.TEXT)
    #         print(f"❌ Error opening Bulk Task Creation form: {err}")
    # try:
    #     with allure.step("➡️ Verifying Bulk Task Creation form title"):
    #         create_bulk_task_label_elem = wait.until(EC.presence_of_element_located((By.XPATH, create_bulk_task_label)))
    #         highlight_element(driver, create_bulk_task_label_elem)
    #         if create_bulk_task_label_elem.text == 'Bulk Task Creation':
    #             print("✅ Bulk Task Creation form title verified")
    #         else:
    #             print("❌ Bulk Task Creation form title mismatch")
    #             allure.attach("Form title mismatch", name="Form Title Error", attachment_type=allure.attachment_type.TEXT)
    # except Exception as err:
    #     allure.attach(str(err), name="Form Title Error", attachment_type=allure.attachment_type.TEXT)
    #     print(f"❌ Error verifying Bulk Task Creation form: {err}")

    # try:
    #     with allure.step("➡️ Uploading bulk task file"):
    #         file_input_elem = wait.until(EC.presence_of_element_located((By.XPATH, dash_bulk_task_dropdown_file_input)))
    #         highlight_element(driver, file_input_elem)
    #         file_path = os.path.abspath(os.path.join('data', filename))
    #         file_input_elem.send_keys(file_path)
    #         wait_for_loader_to_disappear(driver, wait)
    #         print(f"✅ Uploaded file: {file_path}")
    # except Exception as err:
    #     allure.attach(str(err), name="File Upload Error", attachment_type=allure.attachment_type.TEXT)
    #     print(f"❌ Error uploading file: {err}")

    # try:
    #     with allure.step("➡️ Handling validation results"):
    #         try:
    #             bulk_task_error_file_btn_elem = wait_less.until(EC.presence_of_element_located((By.XPATH, bulk_task_error_file_btn)))
    #             highlight_element(driver, bulk_task_error_file_btn_elem)
    #             bulk_task_error_file_btn_elem.click()

    #             form_cancel_btn_elem = wait_less.until(EC.presence_of_element_located((By.XPATH, form_cancel_btn)))
    #             highlight_element(driver, form_cancel_btn_elem)
    #             form_cancel_btn_elem.click()
    #             wait_for_loader_to_disappear(driver, wait)
    #             print("ℹ️ Error file found and form closed")
    #         except TimeoutException:
    #             print("ℹ️ No error file found, proceeding with task creation")
    #             create_tasks_btn_elem = wait_less.until(EC.presence_of_element_located((By.XPATH, create_tasks_btn)))
    #             highlight_element(driver, create_tasks_btn_elem)
    #             if create_tasks_btn_elem.is_enabled():
    #                 create_tasks_btn_elem.click()
    #                 print("✅ Clicked Create Tasks button")
    #             else:
    #                 form_cancel_btn_elem = wait_less.until(EC.presence_of_element_located((By.XPATH, form_cancel_btn)))
    #                 highlight_element(driver, form_cancel_btn_elem)
    #                 form_cancel_btn_elem.click()
    #                 print("❌ Create button disabled. Form closed")
    #                 allure.attach("Create button disabled. Form closed", name="Create Tasks Error", attachment_type=allure.attachment_type.TEXT)
    #             wait_for_loader_to_disappear(driver, wait)
    # except Exception as err:
    #     allure.attach(str(err), name="Validation Handling Error", attachment_type=allure.attachment_type.TEXT)
    #     print(f"❌ Error handling validation: {err}")

    # try:
    #     with allure.step("➡️ Checking for toast message"):
    #         try:
    #             toast_msg_elem = wait.until(EC.presence_of_element_located((By.XPATH, toast_msg)))
    #             highlight_element(driver, toast_msg_elem)
    #             msg = toast_msg_elem.text
    #             print(f"✅ Toast message displayed: {msg}")
    #             wait.until(EC.invisibility_of_element_located((By.XPATH, toast_msg)))
    #             wait_for_loader_to_disappear(driver, wait)
    #             time.sleep(3)
    #         except TimeoutException:
    #             print("ℹ️ No toast message found")
    #         except Exception as e:
    #             allure.attach(str(e), name="Toast Error", attachment_type=allure.attachment_type.TEXT)
    #             print(f"❌ Error fetching toast: {e}")
    # except Exception as err:
    #     allure.attach(str(err), name="Toast Handling Error", attachment_type=allure.attachment_type.TEXT)
    #     print(f"❌ Unexpected error while handling toast: {err}")

    # with allure.step("Step 3: Check Notification for Bulk Task"):
    #     try:
    #         # Refresh once to load new notifications
    #         pg.hotkey('ctrl', 'r')
    #         pg.hotkey('ctrl', 'r')

    #         notification_btn = wait.until(
    #             EC.presence_of_element_located((By.XPATH, notification_icon))
    #         )
    #         highlight_element(driver, notification_btn)
    #         notification_btn.click()
    #         print("🔔 Notification icon clicked")
    #         time.sleep(2)

    #         # Get all notifications
    #         all_notifications = driver.find_elements(
    #             By.XPATH, "//li[contains(@class,'styles_normalText__')]"
    #         )

    #         found = False
    #         for notif in all_notifications:
    #             if "bulk task" in notif.text.lower():     # 🔥 CHANGED HERE
    #                 highlight_element(driver, notif)
    #                 print(f"🔔 Bulk Task Notification Found: {notif.text.strip()}")
    #                 found = True
    #                 break

    #         if not found:
    #             print("ℹ️ Bulk Task notification not present")

    #     except Exception as e:
    #         print(f"❌ Error reading notifications: {e}")
    #         allure.attach(str(e), name="Notification Error", attachment_type=allure.attachment_type.TEXT)
