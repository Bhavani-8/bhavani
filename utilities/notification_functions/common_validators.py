import time
import allure
from selenium.webdriver.common.by import By
from utilities.other_utils_functions.highlight import highlight_element

def verify_user_in_roles(driver, logged_in_email, locators):
    # Give the pop-up time to load the API data
    time.sleep(2) 
    
    with allure.step(f"Verifying if user is '{logged_in_email}' present as Assign To, Approver, CC, or Creator"):
        
        role_keys = {
            "Assignee": "assigned_to_name",
            "Approver": "approver_name",
            "CC": "cc_name",
            "Creator": "creator_name"
        }
        
        found_match = False
        matched_roles = []
        scanned_data = {} # Stores X-Ray data for debugging

        for role_name, json_key in role_keys.items():
            try:
                xpath = locators.get(json_key)
                if not xpath:
                    continue 
                
                elements = driver.find_elements(By.XPATH, xpath)
                
                for elem in elements:
                    if elem.is_displayed():
                        actual_text = elem.text.strip()
                        
                        # 🚨 THE MAGIC: Grabbing the email directly from the title attribute!
                        actual_title = elem.get_attribute("title")
                        safe_title = str(actual_title).strip() if actual_title else ""
                        
                        # X-Ray Data Logging
                        scanned_data[role_name] = f"Title='{safe_title}', Text='{actual_text}'"
                        
                        # Check if the logged-in email exactly matches the title attribute
                        if logged_in_email.lower() == safe_title.lower() or logged_in_email.lower() in actual_text.lower():
                            highlight_element(driver, elem)
                            found_match = True
                            matched_roles.append(role_name)
            except Exception:
                continue 
                
        if not found_match:
            debug_msg = " \n ".join([f"{k} -> {v}" for k, v in scanned_data.items()])
            if not debug_msg:
                debug_msg = "All fields were blank (Pop-up didn't load in time)."
                
            with allure.step(f"❌ Email '{logged_in_email}' not found. UI showed:\n{debug_msg}"): pass
            raise Exception(f"Fail: Expected email '{logged_in_email}' but UI showed:\n{debug_msg}")
            
        with allure.step(f"✅ Found email '{logged_in_email}' in roles: {', '.join(matched_roles)}"): pass
        return True