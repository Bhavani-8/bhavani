import allure
import os
import json
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from utilities.other_utils_functions.highlight import highlight_element
from utilities.add_task_utils import wait_for_loader_to_disappear

def personal_details(driver, wait):

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
            time.sleep(2)  # Wait for page to load completely
            # Click Project Icon
            settings_btn = wait.until(EC.presence_of_element_located((By.XPATH, settings_icon)))
            highlight_element(driver, settings_btn)
            settings_btn.click()
            print("✅ Settings Icon Clicked")

            time.sleep(2)

            # Click "Personal Details tab"
            personal_btn = wait.until(EC.presence_of_element_located((By.XPATH, "//span[text()='Personal']")))
            highlight_element(driver, personal_btn)
            personal_btn.click()
            print("✅ Personal Details tab clicked")

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
            save_btn = wait.until(EC.presence_of_element_located((By.XPATH, "//button[text()='Save Changes']")))
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

    
    return True