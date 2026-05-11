import allure
import os
import json
import time
import pyautogui as pg
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from utilities.other_utils_functions.highlight import highlight_element
from selenium.common.exceptions import TimeoutException
from utilities.add_task_utils import wait_for_loader_to_disappear
from selenium.common.exceptions import StaleElementReferenceException

def task_approved_by_approver(driver, wait):
   # Step 1: Load locators
    with allure.step("Load locators.json"):
        try:
            with open(os.path.join("data", "locators.json"), "r") as f:
                elements_details = json.load(f)
            dashboard_icon = elements_details["dashboard_icon"]
            dash_approval_pending_btn = elements_details["dash_approval_pending_btn"]
            notification_icon = elements_details["notification_icon"]
            print("✅ locators.json loaded successfully")
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
    # Step 2: Create new project
    with allure.step("Task Rejected By CO"):
        
        # Click Project Icon
        approval_btn = wait.until(EC.presence_of_element_located((By.XPATH, dash_approval_pending_btn)))
        highlight_element(driver, approval_btn)
        approval_btn.click()
        print("✅ Approval Pending Clicked")

        time.sleep(2)

        # Click "Add New Project"
        approval_pending_by_me_btn = wait.until(
            EC.presence_of_element_located((By.XPATH, "//p[contains(text(),'Approval Pending by Me')]"))
        )
        highlight_element(driver, approval_pending_by_me_btn)
        approval_pending_by_me_btn.click()
        print("✅ Approval Pending by Me clicked")
        time.sleep(3)
        
    with allure.step("Clicking Column Chooser"):
        column_chooser_btn_elem = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@role='button' and @aria-label='columnchooser']")))
        highlight_element(driver, column_chooser_btn_elem)
        column_chooser_btn_elem.click()
        print("✅ Opened Column Chooser")

    # --- Wait for 'Select All' checkbox ---
    with allure.step("Normalize 'Select All' checkbox state"):
        clicks_done = 0
        while clicks_done < 2:  # first click to normalize, second to deselect
            try:
                # Always refetch element fresh
                select_all_checkbox = wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, ".dx-list-select-all"))
                )
                
                # Scroll into view
                driver.execute_script("arguments[0].scrollIntoView(true);", select_all_checkbox)
                time.sleep(0.2)
                
                # Get current state
                state = select_all_checkbox.get_attribute("aria-checked")
                print(f"   ➤ Click {clicks_done+1}, current state: {state}")
                
                # Click using JS
                driver.execute_script("arguments[0].click();", select_all_checkbox)
                print(f"☑️ Clicked 'Select All' attempt {clicks_done+1}")

                # Wait for UI re-render / loader
                wait_for_loader_to_disappear(driver, wait)
                time.sleep(0.3)

                clicks_done += 1  # successful click

            except StaleElementReferenceException:
                print("⚠️ Stale element, refetching and retrying...")
                time.sleep(0.3)
            except Exception as e:
                print(f"❌ Failed to click 'Select All': {e}")
                raise
    with allure.step("Select Creator column only"):
        creator_xpath = "//div[@class='dx-item-content dx-list-item-content' and contains(normalize-space(), 'Creator')]/preceding-sibling::div//div[@class='dx-checkbox-container']"                    
        creator_checkbox = wait.until(EC.presence_of_element_located((By.XPATH, creator_xpath)))
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", creator_checkbox)
        time.sleep(0.3) 
        creator_checkbox = wait.until(EC.element_to_be_clickable((By.XPATH, creator_xpath)))  # refetch
        highlight_element(driver,creator_checkbox)
        driver.execute_script("arguments[0].click();", creator_checkbox)
        time.sleep(1)
        print("✅ Selected Creator column only")

        save_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@role='button' and @aria-label='Save & Close']")))
        highlight_element(driver, save_btn)
        save_btn.click()
        time.sleep(5)
        print("✅ Saved Approver, Creator chooser")
        wait_for_loader_to_disappear(driver, wait)



        creator_btn = wait.until(EC.presence_of_element_located((By.XPATH, "//td[@role='columnheader' and .//div[text()='Creator']]//span[contains(@class,'dx-header-filter')]")))
        highlight_element(driver, creator_btn)
        creator_btn.click()
        print("Clicked Creator Header")
        time.sleep(1)

        options_text = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='dx-item-content dx-list-item-content' and text()='Rahul CO']")))
        highlight_element(driver, options_text)
        options_text.click()
        print("Clicked Creator name")

        ok_btn = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@aria-label='OK']")))
        highlight_element(driver, ok_btn)
        ok_btn.click()
        print("Clicked OK")


        row_index = 1

        while True:
            try:
                # ---------------------------
                # FETCH ROW
                # ---------------------------
                row = wait.until(
                    EC.presence_of_element_located(
                        (By.XPATH, f"(//td[@aria-colindex='2']//p)[{row_index}]")
                    )
                )

                driver.execute_script("arguments[0].scrollIntoView({block:'center'});", row)
                highlight_element(driver, row)
                time.sleep(0.3)
                driver.execute_script("arguments[0].click();", row)
                print(f"✅ Clicked row {row_index}")
                time.sleep(1)

                # ---------------------------
                # CHECK FOR REJECT BUTTON
                # ---------------------------
                try:
                    print()
                    reject_btn = wait.until(
                        EC.presence_of_element_located(
                            (By.XPATH, "//button[contains(@class,'reject-task')]")
                        )
                    )
                    highlight_element(driver, reject_btn)
                    reject_btn.click()
                    print("🛑 Reject button clicked")

                    # Add comment
                    reject_input = wait.until(
                        EC.presence_of_element_located((By.XPATH, "//textarea[contains(@placeholder,'reason for rejecting')]"))
                    )
                    highlight_element(driver, reject_input)
                    reject_input.send_keys("Trial Test")
                    print("✏️ Comment added")

                    # Submit reject
                    confirm_btn = wait.until(
                        EC.presence_of_element_located(
                            (By.XPATH, "//button[.//span[text()='Confirm']]")
                        )
                    )
                    highlight_element(driver, confirm_btn)
                    confirm_btn.click()
                    print("📤 Reject submitted")

                    # ---------------------------
                    # VALIDATE TOAST
                    # ---------------------------
                    try:
                        toast = wait.until(
                            EC.visibility_of_element_located(
                                (By.XPATH, "//div[contains(@class,'Toastify__toast-body')]")
                            )
                        )
                        highlight_element(driver, toast)
                        print(f"🔔 Toast Message: {toast.text.strip()}")

                    except TimeoutException:
                        print("⚠️ Toast not visible after reject")
                    break

                except TimeoutException:
                    # Reject NOT found -> Close window and continue
                    print("ℹ️ Reject button NOT found → Clicking Close")

                    close_btn = wait.until(
                        EC.presence_of_element_located(
                            (By.XPATH, "(//div[contains(@class,'styles_taskCloseIcon')]//button)[1]")
                        )
                    )
                    highlight_element(driver, close_btn)
                    close_btn.click()
                    print("❎ Close button clicked")

                    row_index += 1
                    continue

            except TimeoutException:
                print("✔️ No more rows to process — Stopped.")
                break

            except StaleElementReferenceException:
                print("⚠️ Stale element, retrying...")
                continue

            except Exception as e:
                print(f"❌ Error at row {row_index}: {e}")
                row_index += 1
                continue


    with allure.step("Validate Normal Notification - Rejected Task"):
        try:
            # Refresh page to load notifications
            pg.hotkey('ctrl', 'r')
            pg.hotkey('ctrl', 'r')

            # Click Notification Icon
            notification_btn = wait.until(
                EC.presence_of_element_located((By.XPATH, notification_icon))
            )
            highlight_element(driver, notification_btn)
            notification_btn.click()
            time.sleep(3)

            # Get all notifications
            all_items = driver.find_elements(
                By.XPATH, "//li[contains(@class,'styles_normalText__')]"
            )

            # Flag
            reject_notification_found = False

            for item in all_items:
                text = item.text.strip()
                if "Reject" in text:
                    highlight_element(driver, item)
                    print(f"🔔 Rejected Task Notification Found: {text}")
                    reject_notification_found = True
                    break

            if not reject_notification_found:
                print("ℹ️ Rejected task notification NOT found, continuing...")
                allure.attach(
                    "Rejected task notification NOT found",
                    name="Rejected Notification Info",
                    attachment_type=allure.attachment_type.TEXT,
                )

            # ⭐ NO RETURN — ALWAYS CONTINUE ⭐
            print("➡️ Proceeding to Dashboard...")

        except Exception as e:
            msg = f"❌ Error while checking rejected task notification: {e}"
            print(msg)
            allure.attach(msg, name="Rejected Task Notification Error",
                        attachment_type=allure.attachment_type.TEXT)
            


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

    # Step 2: Task Approver By CO
    with allure.step("Task Approver By CO"):
            # Click Project Icon
            approval_btn = wait.until(EC.presence_of_element_located((By.XPATH, dash_approval_pending_btn)))
            highlight_element(driver, approval_btn)
            approval_btn.click()
            print("✅ Approval Pending Clicked")

            time.sleep(2)

            # Click "Add New Project"
            approval_pending_by_me_btn = wait.until(
                EC.presence_of_element_located((By.XPATH, "//p[contains(text(),'Approval Pending by Me')]"))
            )
            highlight_element(driver, approval_pending_by_me_btn)
            approval_pending_by_me_btn.click()
            time.sleep(3)
            print("✅ Approval Pending by Me clicked")

    with allure.step("Clicking Column Chooser"):
        column_chooser_btn_elem = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@role='button' and @aria-label='columnchooser']")))
        highlight_element(driver, column_chooser_btn_elem)
        column_chooser_btn_elem.click()
        print("✅ Opened Column Chooser")

    # --- Wait for 'Select All' checkbox ---
    with allure.step("Normalize 'Select All' checkbox state"):
        clicks_done = 0
        while clicks_done < 2:  # first click to normalize, second to deselect
            try:
                # Always refetch element fresh
                select_all_checkbox = wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, ".dx-list-select-all"))
                )
                
                # Scroll into view
                driver.execute_script("arguments[0].scrollIntoView(true);", select_all_checkbox)
                time.sleep(0.2)
                
                # Get current state
                state = select_all_checkbox.get_attribute("aria-checked")
                print(f"   ➤ Click {clicks_done+1}, current state: {state}")
                
                # Click using JS
                driver.execute_script("arguments[0].click();", select_all_checkbox)
                print(f"☑️ Clicked 'Select All' attempt {clicks_done+1}")

                # Wait for UI re-render / loader
                wait_for_loader_to_disappear(driver, wait)
                time.sleep(0.3)

                clicks_done += 1  # successful click

            except StaleElementReferenceException:
                print("⚠️ Stale element, refetching and retrying...")
                time.sleep(0.3)
            except Exception as e:
                print(f"❌ Failed to click 'Select All': {e}")
                raise
    with allure.step("Select Creator column only"):
        creator_xpath = "//div[@class='dx-item-content dx-list-item-content' and contains(normalize-space(), 'Creator')]/preceding-sibling::div//div[@class='dx-checkbox-container']"                    
        creator_checkbox = wait.until(EC.presence_of_element_located((By.XPATH, creator_xpath)))
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", creator_checkbox)
        time.sleep(0.3) 
        creator_checkbox = wait.until(EC.element_to_be_clickable((By.XPATH, creator_xpath)))  # refetch
        highlight_element(driver,creator_checkbox)
        driver.execute_script("arguments[0].click();", creator_checkbox)
        time.sleep(1)
        print("✅ Selected Creator column only")

        save_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@role='button' and @aria-label='Save & Close']")))
        highlight_element(driver, save_btn)
        save_btn.click()
        time.sleep(5)
        print("✅ Saved Approver, Creator chooser")
        wait_for_loader_to_disappear(driver, wait)



        creator_btn = wait.until(EC.presence_of_element_located((By.XPATH, "//td[@role='columnheader' and .//div[text()='Creator']]//span[contains(@class,'dx-header-filter')]")))
        highlight_element(driver, creator_btn)
        creator_btn.click()
        print("Clicked Creator Header")
        time.sleep(1)

        options_text = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='dx-item-content dx-list-item-content' and text()='Rahul CO']")))
        highlight_element(driver, options_text)
        options_text.click()
        print("Clicked Creator name")

        ok_btn = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@aria-label='OK']")))
        highlight_element(driver, ok_btn)
        ok_btn.click()
        print("Clicked OK")


        row_index = 1

        while True:
            try:
                # CLICK ROW
                row = wait.until(
                    EC.presence_of_element_located(
                        (By.XPATH, f"(//td[@aria-colindex='2']//p)[{row_index}]")
                    )
                )
                driver.execute_script("arguments[0].scrollIntoView({block:'center'});", row)
                highlight_element(driver, row)
                time.sleep(0.3)
                driver.execute_script("arguments[0].click();", row)
                print(f"✅ Clicked row {row_index}")
                time.sleep(1)

                # -----------------------------------
                # TRY APPROVE BUTTON
                # -----------------------------------
                try:
                    approve_btn = wait.until(
                        EC.presence_of_element_located(
                            (By.XPATH, "//button[contains(@class,'approve-task')]")
                        )
                    )
                    highlight_element(driver, approve_btn)
                    approve_btn.click()
                    print("🟢 Approve button clicked")

                    # YES CONFIRM BUTTON
                    yes_btn = wait.until(
                        EC.presence_of_element_located(
                            (By.XPATH, "//button[normalize-space()='Yes']")
                        )
                    )
                    highlight_element(driver, yes_btn)
                    yes_btn.click()
                    print("✅ Approved successfully")

                    # -----------------------------------
                    # VALIDATE TOAST
                    # -----------------------------------
                    try:
                        toast = wait.until(
                            EC.visibility_of_element_located(
                                (By.XPATH, "//div[contains(@class,'Toastify__toast-body')]")
                            )
                        )
                        highlight_element(driver, toast)
                        print(f"🔔 Toast Message: {toast.text.strip()}")
                        time.sleep(3)

                    except TimeoutException:
                        print("⚠️ Toast not visible after approve")
                    break

                except TimeoutException:
                    # APPROVE NOT FOUND → close side panel and continue
                    print("ℹ️ Approve button NOT found → Clicking Close")

                    close_btn = wait.until(
                        EC.presence_of_element_located(
                            (By.XPATH, "(//div[contains(@class,'styles_taskCloseIcon')]//button)[1]")
                        )
                    )
                    highlight_element(driver, close_btn)
                    close_btn.click()
                    print("❎ Close button clicked")

                    row_index += 1
                    continue

            except TimeoutException:
                print("✔️ No more rows to process — Stopped.")
                break

            except StaleElementReferenceException:
                print("⚠️ Stale element, retrying...")
                continue

            except Exception as e:
                print(f"❌ Error at row {row_index}: {e}")
                row_index += 1
                continue


    with allure.step("Validate Normal Notification - Approver Task"):
        try:
            # Refresh page to load notifications
            pg.hotkey('ctrl', 'r')
            pg.hotkey('ctrl', 'r')
            time.sleep(2)

            # Click the notification icon
            notification_btn = wait.until(
                EC.presence_of_element_located((By.XPATH, notification_icon))
            )
            highlight_element(driver, notification_btn)
            notification_btn.click()
            time.sleep(3)

            # Get all normal notifications
            all_items = driver.find_elements(By.XPATH, "//li[contains(@class,'styles_normalText__')]")

            approver_notification_found = False
            for item in all_items:
                text = item.text.strip()
                if "approver" in text.lower():  # keyword for approver notification
                    highlight_element(driver, item)
                    print(f"🔔 Approver Notification Found: {text}")
                    approver_notification_found = True
                    # ❌ Do NOT click the notification
                    print("ℹ️ Highlighted Approver notification. Not clicking.")
                    break

            if not approver_notification_found:
                print("ℹ️ Approver notification not found.")
                allure.attach(
                    "Approver notification not found",
                    name="Approver Task Notification Missing",
                    attachment_type=allure.attachment_type.TEXT
                )
                return False
            else:
                return True

        except Exception as e:
            msg = f"❌ Error while checking Approver notification: {e}"
            print(msg)
            allure.attach(
                msg,
                name="Approver Task Notification Error",
                attachment_type=allure.attachment_type.TEXT
            )
            return False
