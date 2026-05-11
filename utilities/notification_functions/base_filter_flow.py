import time
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from utilities.other_utils_functions.highlight import highlight_element
from utilities.notification_functions.common_validators import verify_user_in_roles

# ==============================================================================
# THE MASTER WORKER: Handles ALL standard dropdown filters (With Smart Scanning)
# ==============================================================================
def execute_filter_and_validate(driver, wait, locators, logged_in_email, filter_key, filter_name, expected_inner_status=None, outer_keyword=None):
    
    with allure.step(f"Running Master Flow for: {filter_name}"):
        
        # 1. OPEN DROPDOWN
        with allure.step("Opening Filter Dropdown"):
            dropdown_btn = wait.until(EC.element_to_be_clickable((By.XPATH, locators["drop_down_button"])))
            highlight_element(driver, dropdown_btn)
            ActionChains(driver).move_to_element(dropdown_btn).click().perform()
            time.sleep(1.5) 

        # 2. SELECT DYNAMIC FILTER
        with allure.step(f"Selecting '{filter_name}' Filter"):
            filter_xpath = locators.get(filter_key)
            if not filter_xpath:
                raise Exception(f"Fail: Missing '{filter_key}' in locators.json")
                
            filter_option = wait.until(EC.element_to_be_clickable((By.XPATH, filter_xpath)))
            ActionChains(driver).move_to_element(filter_option).perform()
            time.sleep(0.5)
            highlight_element(driver, filter_option)
            time.sleep(0.5)
            try:
                filter_option.click()
            except:
                ActionChains(driver).move_to_element(filter_option).click().perform()
            time.sleep(3) 

        # 3. GRAB FIRST ITEM OR SMART SCAN
        with allure.step(f"Fetching the correct '{filter_name}' notification"):
            items = wait.until(EC.presence_of_all_elements_located((By.XPATH, locators["notification_all_items"])))
            if not items:
                raise Exception(f"Fail: '{filter_name}' filter applied but the notification list is empty!")

            target_notification = None

            if outer_keyword:
                for item in items:
                    if outer_keyword.lower() in item.text.lower():
                        target_notification = item
                        break
                
                if not target_notification:
                    raise Exception(f"Fail: Scanned {len(items)} items, but none contained the text '{outer_keyword}'.")
            else:
                target_notification = items[0]

        # 4. OPEN THE TASK
        with allure.step("Deep Dive: Opening the task"):
            highlight_element(driver, target_notification)
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", target_notification)
            time.sleep(0.5)
            ActionChains(driver).move_to_element(target_notification).click().perform()
            time.sleep(3)

        # 5. OPTIONAL: SPECIFIC LABEL CHECK (For Approved Tasks)
        if expected_inner_status:
            with allure.step(f"Is the internal status label exactly '{expected_inner_status}'?"):
                try:
                    status_labels = wait.until(EC.presence_of_all_elements_located((By.XPATH, locators["task_approved_tag"])))
                    visible_label = next((label for label in status_labels if label.is_displayed()), None)
                    if visible_label is None:
                        raise Exception("Label found in code but hidden behind pop-up.")
                        
                    highlight_element(driver, visible_label)
                    inner_status = visible_label.text.strip()
                    
                    if expected_inner_status.lower() not in inner_status.lower():
                        raise Exception(f"Fail: Found '{inner_status}', expected '{expected_inner_status}'")
                except Exception as e:
                    raise Exception(f"Fail: Could not read internal pop-up status. Error: {e}")

        # 6. DYNAMIC 4-ROLE EMAIL CHECK
        verify_user_in_roles(driver, logged_in_email, locators)

        return True