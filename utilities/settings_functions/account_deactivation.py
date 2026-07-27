import time
import allure
import os
import json
from datetime import datetime
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# Import your central utilities
from utilities.login_utils import login_check
from utilities.other_utils_functions.highlight import highlight_element

# 1. Load Locators Once
with open(os.path.join("data", 'locators.json'), 'r') as f:
    elements_details = json.load(f)
    stgs_icon = elements_details["settings_page"]["settings_icon"]
    toast_msg = elements_details["toast_msg"]
    full_name = elements_details["settings1_page"]["full_name_input"]
    deactivation_button = elements_details["settings1_page"]["deactivate_account_btn"]
    deactivation_reason = elements_details["settings1_page"]["deactivate_reason_input"]
    deactivation_submit_btn = elements_details["settings1_page"]["deactivate_submit_btn"]
    logout_btn = elements_details["logout_btn"]
    logout_cnfrm_btn = elements_details["logout_cnfrm"]
    reject_req_cfrm_btn = elements_details["FINAL_YES_BTN"]
    Settings_personal_tab = elements_details["settings1_page"]["personal_tab"]
    Settings_Security_tab = elements_details["settings1_page"]["security_tab"]
    
    # Dashboard Nav Locators
    aprvl_pending = elements_details["dash_approval_pending_btn"]
    completed_tab_btn = elements_details["dash_completed_btn"] 
    
    # Locators from officer_request_reject
    Deactivation_req_tab = elements_details["officer_request_reject"]["dynamic_request_row"]
    req_tab = elements_details["officer_request_reject"]["requests_tab"]
    deactivate_req_header = elements_details["officer_request_reject"]["deactivate_req_header"]
    drr_block = elements_details["officer_request_reject"]["drr_block"]


# --- TEAM MEMBER FUNCTIONS ---

def get_full_name(driver, wait):
    name_input = wait.until(EC.visibility_of_element_located((By.XPATH, full_name)))
    wait.until(lambda d: len(name_input.get_attribute("value").strip()) > 0)
    highlight_element(driver, name_input)
    return name_input.get_attribute("value") 

def submit_deactivation_request(driver, wait, reason_text):
    deactivate_btn = wait.until(EC.presence_of_element_located((By.XPATH, deactivation_button)))
    highlight_element(driver, deactivate_btn)
    driver.execute_script("arguments[0].click();", deactivate_btn)

    reason_input = wait.until(EC.visibility_of_element_located((By.XPATH, deactivation_reason)))
    highlight_element(driver, reason_input)
    reason_input.send_keys(reason_text)

    submit_btn = wait.until(EC.presence_of_element_located((By.XPATH, deactivation_submit_btn)))
    highlight_element(driver, submit_btn)
    driver.execute_script("arguments[0].click();", submit_btn)

    submission_time = datetime.now().strftime("%I:%M %p")
    if submission_time.startswith("0"):
        submission_time = submission_time[1:]
        
    return submission_time

def verify_success_popup(driver, wait):
    try:
        popup = wait.until(EC.visibility_of_element_located((By.XPATH, toast_msg)))
        highlight_element(driver, popup)
        time.sleep(2)
        return True
    except TimeoutException:
        return False

def logout(driver, wait):
    try:
        logout_button = wait.until(EC.element_to_be_clickable((By.XPATH, logout_btn)))
        highlight_element(driver, logout_button)
        driver.execute_script("arguments[0].click();", logout_button)
        time.sleep(1) 
        
        yes_buttons = driver.find_elements(By.XPATH, logout_cnfrm_btn)
        for btn in yes_buttons:
            if btn.is_displayed():
                highlight_element(driver, btn)
                driver.execute_script("arguments[0].click();", btn)
                break
                
        wait.until(EC.url_contains("login"))
        
    except TimeoutException:
        print("⚠️ UI Logout failed or stuck, falling back to invisible session wipe.")
        driver.delete_all_cookies()
        driver.execute_script("window.localStorage.clear();")
        driver.execute_script("window.sessionStorage.clear();")
        
    time.sleep(1) 


# --- COMPLIANCE OFFICER FUNCTIONS ---

def validate_and_reject_request(driver, wait, expected_name, expected_reason, expected_time):
    raw_xpath = Deactivation_req_tab
    strict_row_xpath = raw_xpath.format(name=expected_name, reason=expected_reason, time=expected_time)
    
    try:
        time.sleep(3) 
        request_row = wait.until(EC.visibility_of_element_located((By.XPATH, strict_row_xpath)))
        
        try:
            name_xpath = f".//*[contains(text(), '{expected_name}')]"
            name_elem = request_row.find_element(By.XPATH, name_xpath)
            highlight_element(driver, name_elem)
            
            reason_xpath = f".//*[contains(text(), '{expected_reason}')]"
            reason_elem = request_row.find_element(By.XPATH, reason_xpath)
            highlight_element(driver, reason_elem)
            
            time_xpath = f".//*[contains(text(), '{expected_time}')]"
            time_elem = request_row.find_element(By.XPATH, time_xpath)
            highlight_element(driver, time_elem)
            
            time.sleep(1.5) 
        except Exception as e:
            pass
                 
        initial_reject_btn = request_row.find_element(By.XPATH, "//button[@title='Reject']")
        highlight_element(driver, initial_reject_btn)
        driver.execute_script("arguments[0].click();", initial_reject_btn) 
        
        final_yes_btn = wait.until(EC.presence_of_element_located((By.XPATH, reject_req_cfrm_btn)))
        highlight_element(driver, final_yes_btn)
        driver.execute_script("arguments[0].click();", final_yes_btn) 
        
        # ⏱️ CAPTURE THE EXACT REJECTION TIME
        rejection_time = datetime.now().strftime("%I:%M %p")
        if rejection_time.startswith("0"):
            rejection_time = rejection_time[1:]
        
        try:
            success_msg = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, toast_msg))
            )
            highlight_element(driver, success_msg)
            time.sleep(2) 
        except TimeoutException:
            pass 
        
        time.sleep(1) 
        # 🔄 Return BOTH the success boolean AND the new rejection time
        return True, rejection_time
        
    except TimeoutException:
        print(f"❌ Could not find request for {expected_name} matching reason '{expected_reason}' at '{expected_time}'!")
        return False, ""

def verify_request_is_gone(driver, expected_name, expected_reason, expected_time):
    raw_xpath = Deactivation_req_tab
    strict_row_xpath = raw_xpath.format(name=expected_name, reason=expected_reason, time=expected_time)
    
    matches = driver.find_elements(By.XPATH, strict_row_xpath)
    if len(matches) > 0:
        highlight_element(driver, matches[0], border_color="red")
        return False 
    return True 

def verify_completed_deactivation_block(driver, wait, expected_name, expected_reason, expected_rejection_time):

    # 1. Header Validation
    with allure.step("Validate 'Deactivation User Requests' Header is present in Completed Requests section"):
        try:
            time.sleep(2) 
            header = wait.until(EC.visibility_of_element_located((By.XPATH, deactivate_req_header)))
            highlight_element(driver, header)
        except TimeoutException:
            assert False, "❌ UI ERROR: 'Deactivation User Requests' header did not load in Completed section!"

    # 2. Block & Content Validation (Name, Reason, and dynamically highlighting Time)
    with allure.step(f"Validate Name, Reason, and Rejection Time ({expected_rejection_time}) are present in Completed Deactivation Requests"):
        try:
            block = wait.until(EC.visibility_of_element_located((By.XPATH, drr_block)))
            
            # Find the EXACT ROW matching our user and unique reason
            row_xpath = f".//tr[td[contains(., '{expected_name}')] and td[contains(., '{expected_reason}')]]"
            specific_row = block.find_element(By.XPATH, row_xpath)
            
            name_elem = specific_row.find_element(By.XPATH, "./td[1]")
            highlight_element(driver, name_elem)
            actual_name_text = name_elem.text
            
            reason_elem = specific_row.find_element(By.XPATH, "./td[3]")
            highlight_element(driver, reason_elem)
            actual_reason_text = reason_elem.text
            
            # Highlight and verify column 4 contains our exact Rejection Time
            time_elem = specific_row.find_element(By.XPATH, "./td[4]")
            highlight_element(driver, time_elem)
            actual_time_text = time_elem.text
            
            # 🔥 NEW: Attach the EXACT data scraped from the UI to the Allure Report
            allure.attach(
                f"👤 Found Name: {actual_name_text}\n📝 Found Reason: {actual_reason_text}\n⏰ Found Action Time: {actual_time_text}", 
                name="📄 Actual Data Extracted from UI Table", 
                attachment_type=allure.attachment_type.TEXT
            )

            assert expected_rejection_time in actual_time_text, f"❌ TIME MISMATCH: Expected action time '{expected_rejection_time}', but UI showed '{actual_time_text}'"
            
            time.sleep(1.5)
            
        except TimeoutException:
            assert False, "❌ UI ERROR: The 'drr_block' container did not load!"
        except NoSuchElementException:
            assert False, f"❌ DATA MATCH ERROR: Could not find a row with Name '{expected_name}' and Reason '{expected_reason}'!"

    # 3. Rejected Label Validation
    with allure.step(f"Validate 'Rejected' label is present for {expected_name} in completed requests"):
        try:
            # We already found the specific row, just look for the label INSIDE that row
            label_elem = specific_row.find_element(By.XPATH, ".//span[text()='Rejected']") 
            highlight_element(driver, label_elem)
            
            # Attach proof that the label was found
            actual_label_text = label_elem.text
            allure.attach(
                f"🏷️ Found Status Label: {actual_label_text}", 
                name="📄 Status Label Extracted", 
                attachment_type=allure.attachment_type.TEXT
            )
            
            time.sleep(1)
        except NoSuchElementException:
            assert False, f"❌ STATUS ERROR: The 'Rejected' label did not appear for {expected_name}!"

    return True


# PART 2: THE EXECUTION FLOW 
def account_deactivation_module(driver, wait, tm_user, tm_pwd, co_user, co_pwd):
    """Executes the dual-role Account Deactivation flow for Compliance Sutra."""
    
    recorded_reason = f"Automation Deactivation Test - {datetime.now().strftime('%H:%M:%S')}"
    recorded_name = ""
    recorded_time = ""
    recorded_rejection_time = ""

    driver.delete_all_cookies()
    driver.execute_script("window.localStorage.clear();")
    driver.execute_script("window.sessionStorage.clear();")

    with allure.step("1. Login as Team Member"):
        driver.get("http://192.168.30.11:8081/login") 
        login_check(driver, waittime=30, trial=1, username=tm_user, password=tm_pwd) 
        time.sleep(1.5) 

    with allure.step("2. Navigate to Settings & Record Name"):
        settings_icon = wait.until(EC.presence_of_element_located((By.XPATH, stgs_icon)))
        highlight_element(driver, settings_icon)
        driver.execute_script("arguments[0].click();", settings_icon) 
        time.sleep(1) 
        
        personal_tab = wait.until(EC.presence_of_element_located((By.XPATH, Settings_personal_tab)))
        driver.execute_script("arguments[0].click();", personal_tab) 
        time.sleep(1)
        
        recorded_name = get_full_name(driver, wait)
        allure.attach(recorded_name, name="Recorded Full Name", attachment_type=allure.attachment_type.TEXT)

    with allure.step("3. Submit Deactivation Request"):
        security_tab = wait.until(EC.presence_of_element_located((By.XPATH, Settings_Security_tab)))
        driver.execute_script("arguments[0].click();", security_tab) 
        time.sleep(1.5)
        
        recorded_time = submit_deactivation_request(driver, wait, recorded_reason)
        
        allure.attach(
            f"👤 Name: {recorded_name}\n📝 Reason: {recorded_reason}\n⏰ Time: {recorded_time}", 
            name="📤 Data Submitted by Team Member", 
            attachment_type=allure.attachment_type.TEXT
        )
        
        toast_success = verify_success_popup(driver, wait)
        assert toast_success is True, "❌ 'Request Sent' popup did not appear!"
            
    with allure.step("4. Logout Team Member"):
        logout(driver, wait)

    with allure.step("5. Login as Compliance Officer"):
        driver.get("http://192.168.30.11:8081/login") 
        login_check(driver, waittime=30, trial=1, username=co_user, password=co_pwd)
        time.sleep(1.5) 

    with allure.step("6. Navigate to Approval Pending -> Requests"):
        approval_menu = wait.until(EC.presence_of_element_located((By.XPATH, aprvl_pending)))
        highlight_element(driver, approval_menu) 
        driver.execute_script("arguments[0].click();", approval_menu) 
        time.sleep(1.5) 
        
        requests_tab = wait.until(EC.presence_of_element_located((By.XPATH, req_tab)))
        highlight_element(driver, requests_tab) 
        driver.execute_script("arguments[0].click();", requests_tab) 
        time.sleep(2) 
        
    with allure.step("7. Validate and Reject Request"):
        allure.attach(
            f"👤 Expected Name: {recorded_name}\n📝 Expected Reason: {recorded_reason}\n⏰ Submission Time: {recorded_time}", 
            name="🔍 Compliance Officer is Searching For", 
            attachment_type=allure.attachment_type.TEXT
        )
        
        # 🔄 Unpack both the boolean and our new Rejection Time variable!
        found_and_rejected, recorded_rejection_time = validate_and_reject_request(driver, wait, recorded_name, recorded_reason, recorded_time)
        assert found_and_rejected is True, f"❌ Could not find or reject request for {recorded_name}!"

    with allure.step("8. Verify Specific Request is Removed"):
        refresh_tab = driver.find_element(By.XPATH, req_tab)
        highlight_element(driver, refresh_tab)
        refresh_tab.click()
        time.sleep(3) 

        is_gone = verify_request_is_gone(driver, recorded_name, recorded_reason, recorded_time)
        assert is_gone is True, "🚨 Bug! The specific rejected request is still visible in the table!"

    with allure.step("9. Navigate to Completed -> Completed Requests"):
        completed_menu = wait.until(EC.presence_of_element_located((By.XPATH, completed_tab_btn)))
        highlight_element(driver, completed_menu)
        driver.execute_script("arguments[0].click();", completed_menu)
        time.sleep(1.5)
        
        completed_requests_tab = wait.until(EC.presence_of_element_located((By.XPATH, req_tab)))
        highlight_element(driver, completed_requests_tab)
        driver.execute_script("arguments[0].click();", completed_requests_tab)
        time.sleep(3) 

    with allure.step("10. Verify Rejected Record in Completed Tab"):
        allure.attach(
            f"👤 Target Name: {recorded_name}\n📝 Target Reason: {recorded_reason}\n⏰ Expected Action Time: {recorded_rejection_time}", 
            name="✅ Verifying Record in Completed Tab", 
            attachment_type=allure.attachment_type.TEXT
        )
        
        # 🔄 Pass the new 'recorded_rejection_time' to the final verification function
        verify_completed_deactivation_block(driver, wait, recorded_name, recorded_reason, recorded_rejection_time)

    with allure.step("11. Final Logout"):
        logout(driver, wait)
        
    return True