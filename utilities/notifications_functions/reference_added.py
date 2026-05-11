import allure
import os
import json
import time
import pyautogui as pg
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from utilities.add_task_utils import wait_for_loader_to_disappear
from utilities.highlight import highlight_element
from selenium.common.exceptions import StaleElementReferenceException

from selenium.common.exceptions import TimeoutException
from selenium.webdriver import ActionChains


def reference_added_by_co(driver, wait):
    # Step 1: Load locators
    with allure.step("Load locators.json"):
        try:
            with open(os.path.join("data", "locators.json"), "r") as f:
                elements_details = json.load(f)
            dashboard_icon = elements_details["dashboard_icon"]
            dash_total_btn = elements_details["dash_total_btn"]
            notification_icon = elements_details["notification_icon"]
            err_msg_toast = elements_details["err_msg_toast"]
            print("✅ locators.json loaded successfully")
        except Exception as e:
            allure.attach(str(e), name="Locators Load Error", attachment_type=allure.attachment_type.TEXT)
            return False
  
    # Dashboard total button
    # -------------------------
    
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


        with allure.step("Select 'Company / Project' column only"):
            checkbox_elem = driver.find_element(
                By.XPATH,
                "//div[@class='dx-item-content dx-list-item-content' and contains(normalize-space(), 'Company / Project')]/preceding-sibling::div//div[@class='dx-checkbox-container']"
            )
            driver.execute_script("arguments[0].click();", checkbox_elem)
            print("✅ Selected 'Company / Project' column only")

        with allure.step("Save Column Chooser with partial selection"):
            save_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@role='button' and @aria-label='Save & Close']")))
            highlight_element(driver, save_btn)
            save_btn.click()
            time.sleep(5)
            print("✅ Saved column chooser")
            wait_for_loader_to_disappear(driver, wait)


            company_btn = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='dx-column-indicators']//span[contains(@aria-label, 'Company / Project')]")))
            highlight_element(driver, company_btn)
            company_btn.click()
            print("Compnay button Clicked")

            options_text = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='dx-item-content dx-list-item-content' and text()='ICICI 1']")))
            highlight_element(driver, options_text)
            options_text.click()
            
            print("Options text clicked")

            ok_btn = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@aria-label='OK']")))
            highlight_element(driver, ok_btn)
            ok_btn.click()
            time.sleep(2)
            print("Clicked OK")
            wait_for_loader_to_disappear(driver, wait)

            # Fetch all row elements from column 2 (excluding header)
            row = wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, "(//tr[contains(@class,'dx-row') and not(contains(@class,'dx-header-row'))]//td[@aria-colindex='2']//p)[1]")
                )
            )
            highlight_element(driver, row)

            # Scroll to make sure it is visible
            driver.execute_script("arguments[0].click();", row)
            time.sleep(2)

            # # Use JS click (DevExpress recommended)
            # driver.execute_script("arguments[0].click();", row)

            print("✅ Row clicked successfully using JS")

            ref_btn_xpath = "//h1[normalize-space()='Ref']"

            # Re-locate every time
            ref_btn = wait.until(EC.presence_of_element_located((By.XPATH, ref_btn_xpath)))
            highlight_element(driver, ref_btn)
            # driver.execute_script("arguments[0].click();", ref_btn)
            ref_btn.click()

            print("Ref Button Clicked")


            add_ref_btn = wait.until(EC.presence_of_element_located((By.XPATH, "//button[contains(text(),'Add Reference')]")))
            highlight_element(driver, add_ref_btn)
            add_ref_btn.click()
            print("✅ Trial reference added")

            ref_input = wait.until(EC.presence_of_element_located(
                (By.XPATH, "//div[@role='textbox' and @contenteditable='true']")
            ))
            highlight_element(driver, ref_input)
            ref_input.click()
            ref_input.send_keys("Trial Reference")

            save_btn = wait.until(EC.presence_of_element_located((By.XPATH, "//button[contains(@class,'project-management__button--primary') and contains(text(),'Save')]")))
            highlight_element(driver, save_btn)
            save_btn.click()
            print("Save Button clicked")

            # STEP 2: VALIDATE TOAST MESSAGE
    with allure.step("Step 2: Validate Toast Popup After Delete"):
        try:
            toast_msgs = wait.until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, err_msg_toast))
            )

            for toast in toast_msgs:
                highlight_element(driver, toast)
                msg = toast.text.strip()
                print(f"📢 Toast Message: {msg}")

                if msg == "Reference updated successfully!":
                    print("✅ SUCCESS: Reference Updated Successfully toast displayed")
                    break
                else:
                    print(f"❌ ERROR TOAST: {msg}")

        except TimeoutException:
            print("⚠️ No toast popup appeared")
            allure.attach("No toast popup", name="Toast Missing", attachment_type=allure.attachment_type.TEXT)


    with allure.step("Validate Normal Notification - Reference Updated"):
        try:
            # Refresh page to load notifications
            pg.hotkey('ctrl', 'r')
            pg.hotkey('ctrl', 'r')

            # Click the notification icon
            notification_btn = wait.until(
                EC.presence_of_element_located((By.XPATH, notification_icon))
            )
            highlight_element(driver, notification_btn)
            notification_btn.click()
            time.sleep(3)

            # Get all normal notifications
            all_items = driver.find_elements(
                By.XPATH, "//li[contains(@class,'styles_normalText__')]"
            )

            reference_found = False
            for item in all_items:
                text = item.text.strip()
                if "reference" in text.lower():   # 🔥 Check for Reference Updated notification
                    highlight_element(driver, item)
                    print(f"🔔 Reference Updated Successfully Found: {text}")
                    reference_found = True
                    break

            if not reference_found:
                print("ℹ️ Reference Updated Successfully notification not found.")
                allure.attach(
                    "Reference Updated Successfully notification not found",
                    name="Reference Update Notification Missing",
                    attachment_type=allure.attachment_type.TEXT
                )

        except Exception as e:
            msg = f"❌ Error while checking Reference Updated Successfully notification: {e}"
            print(msg)
            allure.attach(
                msg,
                name="Reference Updated Notification Error",
                attachment_type=allure.attachment_type.TEXT
            )
