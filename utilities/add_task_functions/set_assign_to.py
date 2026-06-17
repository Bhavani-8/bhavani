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


def set_assign_to(driver, assign_to_dropdown, assign_to, wait):
    given_mail = assign_to

    # Step 1: Validate input
    if not assign_to or assign_to.strip() == '':
        msg = "❌ Assign to input is blank."
        print(msg)
        allure.attach(msg, name="Input Error", attachment_type=allure.attachment_type.TEXT)
        return 'blank'

    try:
        # with allure.step("Validating email format..."):
        mail_validated = False
        if '@' in assign_to or '.' in assign_to:
            if not validate_email(assign_to):
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
            assign_value_check_xpath = elements_details['assign_value_check']
        print("✅ Locators loaded successfully.")
    except (FileNotFoundError, json.JSONDecodeError) as e:
        msg = f"❌ Failed to load locators: {e}"
        print(msg)
        pytest.fail(msg)

    # Step 3: Open dropdown and enter Assign To
    try:
        assign_input_elem = wait.until(
            EC.element_to_be_clickable((By.XPATH, assign_to_dropdown))
        )
        highlight_element(driver, assign_input_elem)
        assign_input_elem.click()
        time.sleep(1)

        print("✅ Assign To dropdown opened (primary locator).")

    except Exception:
        print("⚠️ Primary locator failed, trying fallback locator...")

        try:
            assign_input_elem = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@class,'control') and .//div[text()='Assign To*']]")))
            highlight_element(driver, assign_input_elem)
            assign_input_elem.click()
            time.sleep(1)

            print("✅ Assign To dropdown opened (fallback locator).")

        except Exception as e:
            msg = f"❌ Failed to open Assign To dropdown: {e}"
            print(msg)
            allure.attach(msg,name="Assign_To_Error",attachment_type=allure.attachment_type.TEXT)
            return False


    input_field = driver.switch_to.active_element
    input_field.send_keys(assign_to)
    time.sleep(1)

    # Locate all dropdown options
    options_locator = (By.XPATH, "//div[contains(@class, '-option')]")
    all_options = wait.until(EC.presence_of_all_elements_located(options_locator))
    option_texts = [opt.text.strip() for opt in all_options if opt.text.strip()]
    allure.attach('\n'.join(option_texts), name="All Dropdown Options", attachment_type=allure.attachment_type.TEXT)
    

    # Step 4: Handle dropdown selection
    try:
        # with allure.step("Selecting Assign To from dropdown..."):
        found = False
        # Handle 'Create' option
        for option in option_texts:
            if option.lower().startswith('create') and assign_to.lower() in option.lower():
                print(f"🆕 Found 'Create' option: {option}")
                assign_to = option
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
                if str(assign_to).lower() == option.lower():
                    print(f"✅ Found matching option: {option}")
                    assign_to = option
                    option_locator = (By.XPATH, f"//div[contains(@class, '-option') and text()='{assign_to}']")
                    dropdown_option = wait.until(EC.visibility_of_element_located(option_locator))
                    highlight_element(driver, dropdown_option)
                    dropdown_option.click()
                    allure.attach(f"Successfully selected: {assign_to}", name="Selection", attachment_type=allure.attachment_type.TEXT)
                    found = True
                    break

        if not found:
            msg = f"❌ No matching option found for: {assign_to}"
            print(msg)
            allure.attach(msg, name="Error", attachment_type=allure.attachment_type.TEXT)
            return False
    except Exception as e:
        msg = f"❌ Error selecting Assign To from dropdown: {e}"
        print(msg)
        allure.attach(msg, name="Dropdown Selection Error", attachment_type=allure.attachment_type.TEXT)
        return False

    # Step 5: Validate selection
    try:
        # with allure.step("Validating Assign To selection..."):
        assign_value_input = wait.until(EC.presence_of_element_located((By.XPATH, assign_value_check_xpath)))
        highlight_element(driver, assign_value_input)
        assign_value_text = assign_value_input.text.strip().lower()
        given_mail_lower = given_mail.strip().lower()
        print(f"🧪 Validation Debug — Given: {given_mail_lower}, UI Value: {assign_value_text}, Assign To: {assign_to}")

        # Case 1: Direct match
        if assign_value_text == given_mail_lower:
            print(f"✅ Assign To match successful.")
            allure.attach(f"Assign value is set correctly.", name="Assign To Validation", attachment_type=allure.attachment_type.TEXT)
            task_value_store("assign_to", assign_value_text)
            return True

        # Case 2: Extract email from 'Create "email@example.com"'
        match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', assign_to)
        if match:
            extracted_email = match.group().strip().lower()
            if assign_value_text == extracted_email == given_mail_lower:
                print(f"✅ Email extracted and matched: {extracted_email}")
                task_value_store("assign_to", assign_value_text)
                return True

        # Mismatch Case
        msg = f"❌ Assign To mismatch. Expected: {given_mail_lower}, Found: {assign_value_text}"
        print(msg)
        allure.attach(msg, name="Assign To Value Error", attachment_type=allure.attachment_type.TEXT)
        return False
    except Exception as e:
        msg = f"🔥 Unexpected error during Assign To validation: {e}"
        print(msg)
        allure.attach(msg, name="Error", attachment_type=allure.attachment_type.TEXT)
        return False
