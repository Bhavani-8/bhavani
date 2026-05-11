import time
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from utilities.other_utils_functions.highlight import highlight_element

# ==============================================================================
# HELPER WORKER 1: SEARCH TASK (COLLAPSIBLE DROPDOWN REPORTING)
# ==============================================================================
def _search_task_flow(driver, wait, locators):
    
    # 1. FETCHING TEXT
    with allure.step("Fetching the notification to search"):
        items = wait.until(EC.presence_of_all_elements_located((By.XPATH, locators["notification_all_items"])))
        if not items:
            raise Exception("The notification list is completely empty!")
            
        first_item = items[0]
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", first_item)
        time.sleep(0.5)
        
        bold_text_xpath = "(//strong[text()])[1]"
        bold_element = wait.until(EC.visibility_of_element_located((By.XPATH, bold_text_xpath)))
        highlight_element(driver, bold_element)
        time.sleep(1.5) 
        
        fetched_search_term = bold_element.text.strip() 

    # 2. SHOWING FETCHED TEXT
    with allure.step("Data Fetched"):
        with allure.step(f"The exact text we are searching for is '{fetched_search_term}'"):
            pass 

    # 3. PERFORMING POSITIVE SEARCH
    with allure.step(f"Searching the text term '{fetched_search_term}' in search box"):
        search_box = wait.until(EC.element_to_be_clickable((By.XPATH, locators["Notification_search_btn"])))
        highlight_element(driver, search_box)
        search_box.clear()
        search_box.send_keys(fetched_search_term + Keys.RETURN)
        time.sleep(3) 

    # 4. DYNAMIC VALIDATION
    result_items = driver.find_elements(By.XPATH, locators["notification_all_items"])
    
    with allure.step("Did all notifications with search term appear?"):
        if len(result_items) == 0:
            with allure.step("No - 0 results found."):
                pass
            raise Exception("Fail: List was empty after positive search.")
        else:
            mismatched_text = ""
            all_match = True
            for item in result_items:
                if fetched_search_term.lower() not in item.text.lower():
                    all_match = False
                    mismatched_text = item.text
                    break 
                    
            if all_match:
                with allure.step(f"Yes - Verified {len(result_items)} notifications on screen."):
                    pass 
            else:
                with allure.step(f"No - Mismatch found: '{mismatched_text}'"):
                    pass
                raise Exception("Fail: Found a notification in the search results that did not contain the search term.")

    # 5. NEGATIVE SEARCH & VALIDATION COMBINED
    with allure.step("Searching search term by adding space"):
        highlight_element(driver, search_box)
        search_box.send_keys(" " + Keys.RETURN)
        time.sleep(3) 
        
        try:
            empty_msg = wait.until(EC.visibility_of_element_located((By.XPATH, locators["no_data_msg"])))
            highlight_element(driver, empty_msg)
            with allure.step("✅ No notifications found"):
                pass 
        except Exception:
            with allure.step("❌ Notifications found"):
                pass
            raise Exception("Fail: System still showed notification results instead of 'no data' message.")

    return True