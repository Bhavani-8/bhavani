import allure
import os
import json
import pytest
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from utilities.other_utils_functions.highlight import highlight_element
import time
import re
from utilities.add_task_functions.add_task_common import validate_email, task_value_store


def set_approver(driver, approver_dropdown, approver, wait):
    given_mail = approver

    # Step 1: Validate input
    if not approver or approver.strip() == '':
        msg = "❌ Approver input is blank."
        print(msg)
        allure.attach(msg, name="Input Error", attachment_type=allure.attachment_type.TEXT)
        return 'blank'

    try:
        # with allure.step("Validating email format..."):
        mail_validated = False
        if '@' in approver or '.' in approver:
            if not validate_email(approver):
                msg = "❌ Invalid email address."
                print(msg)
                mail_validated = True
                allure.attach(msg, name="Input Error", attachment_type=allure.attachment_type.TEXT)
        if mail_validated:
            print('Mail format validated')
    except Exception as e:
        msg = f"❌ Email validation failed: {e}"
        print(msg)
        allure.attach(msg, name="Email Validation Error", attachment_type=allure.attachment_type.TEXT)
        return False

    # Step 2: Load locators
    try:
        # with allure.step("Loading locators..."):
        with open(os.path.join("data", 'locators.json'), 'r') as f:
            elements_details = json.load(f)
            approver_value_check_xpath = elements_details['approver_value_check']
        print("✅ Locators loaded successfully.")
    except (FileNotFoundError, json.JSONDecodeError) as e:
        msg = f"❌ Failed to load locators: {e}"
        print(msg)
        pytest.fail(msg)

    # Step 3: Open dropdown and enter Approver
    try:
        # with allure.step("Opening Approver dropdown and entering value..."):
        approver_input_elem = wait.until(EC.presence_of_element_located((By.XPATH, approver_dropdown)))
        highlight_element(driver, approver_input_elem)
        approver_input_elem.click()
        time.sleep(1)
    

    except Exception:
        print("⚠️ Primary locator failed, trying fallback locator...")

        try:
            approver_input_elem = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@class,'control') and .//div[text()='Approver*']]")))
            highlight_element(driver, approver_input_elem)
            approver_input_elem.click()
            time.sleep(1)

            print("✅ Approver To dropdown opened (fallback locator).")

        except Exception as e:
            msg = f"❌ Failed to open Approver To dropdown: {e}"
            print(msg)
            allure.attach(msg,name="Approver Error",attachment_type=allure.attachment_type.TEXT)
            return False


        input_field = driver.switch_to.active_element
        input_field.send_keys(approver)
        time.sleep(1)

        # Locate all dropdown options
        options_locator = (By.XPATH, "//div[contains(@class, '-option')]")
        all_options = wait.until(EC.presence_of_all_elements_located(options_locator))
        option_texts = [opt.text.strip() for opt in all_options if opt.text.strip()]
        allure.attach('\n'.join(option_texts), name="All Dropdown Options", attachment_type=allure.attachment_type.TEXT)
    

    # Step 4: Handle dropdown selection
    try:
        # with allure.step("Selecting Approver from dropdown..."):
        found = False
        # Handle 'Create' option
        for option in option_texts:
            if option.lower().startswith('create') and approver.lower() in option.lower():
                print(f"🆕 Found 'Create' option: {option}")
                approver = option
                for opt in all_options:
                    if opt.text.strip().lower() == option.lower():
                        highlight_element(driver, opt)
                        opt.click()
                        found = True
                        break
                break

        # Standard option matching
        if not found:
            for option in option_texts:
                if str(approver).lower() == option.lower():
                    print(f"✅ Found matching option: {option}")
                    approver = option
                    option_locator = (By.XPATH, f"//div[contains(@class, '-option') and text()='{approver}']")
                    dropdown_option = wait.until(EC.visibility_of_element_located(option_locator))
                    highlight_element(driver, dropdown_option)
                    dropdown_option.click()
                    allure.attach(f"Successfully selected: {approver}", name="Selection", attachment_type=allure.attachment_type.TEXT)
                    found = True
                    break

        if not found:
            msg = f"❌ No matching option found for: {approver}"
            print(msg)
            allure.attach(msg, name="Error", attachment_type=allure.attachment_type.TEXT)
            return False
    except Exception as e:
        msg = f"❌ Error selecting Approver from dropdown: {e}"
        print(msg)
        allure.attach(msg, name="Dropdown Selection Error", attachment_type=allure.attachment_type.TEXT)
        return False

    # Step 5: Validate selection
    try:
        # with allure.step("Validating Approver selection..."):
        approver_value_input = wait.until(EC.presence_of_element_located((By.XPATH, approver_value_check_xpath)))
        highlight_element(driver, approver_value_input)
        approver_value_text = approver_value_input.text.strip().lower()
        given_mail_lower = given_mail.strip().lower()
        print(f"🧪 Validation Debug — Given: {given_mail_lower}, UI Value: {approver_value_text}, Approver: {approver}")

        # Case 1: Direct match
        if approver_value_text == given_mail_lower:
            print(f"✅ Approver match successful.")
            allure.attach(f"Approver value is set correctly.", name="Approver Validation", attachment_type=allure.attachment_type.TEXT)
            task_value_store("approver", approver_value_text)
            return True

        # Case 2: Extract email from 'Create "email@example.com"'
        match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', approver)
        if match:
            extracted_email = match.group().strip().lower()
            if approver_value_text == extracted_email == given_mail_lower:
                print(f"✅ Email extracted and matched: {extracted_email}")
                task_value_store("approver", approver_value_text)
                return True

        # Mismatch Case
        msg = f"❌ Approver mismatch. Expected: {given_mail_lower}, Found: {approver_value_text}"
        print(msg)
        allure.attach(msg, name="Approver Value Error", attachment_type=allure.attachment_type.TEXT)
        return False
    except Exception as e:
        msg = f"🔥 Unexpected error during Approver validation: {e}"
        print(msg)
        allure.attach(msg, name="Error", attachment_type=allure.attachment_type.TEXT)
        return False
