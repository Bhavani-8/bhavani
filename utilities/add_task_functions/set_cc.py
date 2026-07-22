import allure
from utilities.add_task_functions.add_task_common import validate_email, task_value_store
import os
import json
import pytest
import pyautogui as pg
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from utilities.other_utils_functions.highlight import highlight_element
import time
import re


def set_cc(driver, cc_dropdown, cc, wait):
    given_mail = cc

    # Step 1: Validate input
    if not cc or cc.strip() == '':
        msg = "❌ CC input is blank."
        print(msg)
        allure.attach(msg, name="Input Error", attachment_type=allure.attachment_type.TEXT)
        return 'blank'

    try:
        # with allure.step("Validating email format..."):
        mail_validated = False
        if '@' in cc or '.' in cc:
            if not validate_email(cc):
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
            cc_value_check_xpath = elements_details['cc_value_check']
        print("✅ Locators loaded successfully.")
    except (FileNotFoundError, json.JSONDecodeError) as e:
        msg = f"❌ Failed to load locators: {e}"
        print(msg)
        pytest.fail(msg)

    # Step 3: Open dropdown and enter CC
    try:
        # with allure.step("Opening CC dropdown and entering value..."):
        cc_input_elem = wait.until(EC.presence_of_element_located((By.XPATH, cc_dropdown)))
        highlight_element(driver, cc_input_elem)
        cc_input_elem.click()
        time.sleep(1)

        # Fetch all dropdown options
        options_locator = (By.XPATH, "//div[contains(@class, '-option')]")
        all_options = wait.until(EC.presence_of_all_elements_located(options_locator))
        option_texts = [opt.text.strip() for opt in all_options if opt.text.strip()]
        print(f"Available options: {option_texts}")
        allure.attach('\n'.join(option_texts), name="All Dropdown Options", attachment_type=allure.attachment_type.TEXT)

        input_field = driver.switch_to.active_element
        input_field.send_keys(cc)
        time.sleep(1)
    except Exception as e:
        msg = f"❌ Failed to open dropdown or enter CC: {e}"
        print(msg)
        allure.attach(msg, name="Dropdown Interaction Error", attachment_type=allure.attachment_type.TEXT)
        return False

    # Step 4: Handle dropdown selection
    try:
        # with allure.step("Selecting CC from dropdown..."):
        user_title_elem = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='user-title']")))
        username = user_title_elem.text.strip().lower().replace('hi', '').replace('hello', '').replace(',', '').replace(';', '')
        print(f"Cleaned username: {username}")

        found = False
        for option in option_texts:
            # Prevent creator from being selected
            if username.strip().lower() == option.strip().lower():
                print(f'Creator should not be present in CC. Found matching option: {username}')
                return False

            # Handle 'Create' option
            if option.lower().startswith('create') and cc.lower() in option.lower():
                print(f"🆕 Found 'Create' option: {option}")
                cc = option
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
                if str(cc).lower() == option.lower() or option.lower() in str(cc).lower():
                    print(f"✅ Found matching option: {option}")
                    cc = option
                    option_locator = (By.XPATH, f"//div[contains(@class,'-option')][contains(.,'{cc}')]")
                    dropdown_option = wait.until(EC.element_to_be_clickable(option_locator))
                    highlight_element(driver, dropdown_option)
                    driver.execute_script("arguments[0].scrollIntoView({block:'center'});",dropdown_option)
                    driver.execute_script("arguments[0].click();",dropdown_option)
                    # dropdown_option.click()
                    allure.attach(f"Successfully selected: {cc}", name="Selection", attachment_type=allure.attachment_type.TEXT)
                    found = True
                    break

        if not found:
            msg = f"❌ No matching option found for: {cc}"
            print(msg)
            allure.attach(msg, name="Error", attachment_type=allure.attachment_type.TEXT)
            return False
    except Exception as e:
        msg = f"❌ Error selecting CC from dropdown: {e}"
        print(msg)
        allure.attach(msg, name="Dropdown Selection Error", attachment_type=allure.attachment_type.TEXT)
        return False

    # Step 5: Validate selection
    try:
        # with allure.step("Validating CC selection..."):
        cc_value_input = wait.until(EC.presence_of_element_located((By.XPATH, cc_value_check_xpath)))
        highlight_element(driver, cc_value_input)
        cc_value_text = cc_value_input.text.strip().lower()
        given_mail_lower = given_mail.strip().lower()
        print(f"🧪 Validation Debug — Given: {given_mail_lower}, UI Value: {cc_value_text}, CC: {cc}")

        if cc_value_text == given_mail_lower:
            allure.attach(f"CC value is set correctly.", name="CC Validation", attachment_type=allure.attachment_type.TEXT)
            task_value_store("cc", cc_value_text)
            return True

        # Try to extract email from 'Create "email"' format
        match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', cc)
        if match:
            extracted_email = match.group().strip().lower()
            if cc_value_text == extracted_email == given_mail_lower:
                print(f"✅ Email extracted and matched: {extracted_email}")
                task_value_store("cc", cc_value_text)
                return True

        msg = f"❌ CC mismatch for email. Expected: {given_mail_lower}, Found: {cc_value_text}"
        print(msg)
        allure.attach(msg, name="CC Value Error", attachment_type=allure.attachment_type.TEXT)
        return False

    except Exception as e:
        msg = f"🔥 Unexpected error during CC validation: {e}"
        print(msg)
        allure.attach(msg, name="Error", attachment_type=allure.attachment_type.TEXT)
        return False
