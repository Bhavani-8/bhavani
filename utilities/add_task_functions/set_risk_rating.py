import allure
import os
import json
import pytest
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from utilities.other_utils_functions.highlight import highlight_element
import time
from utilities.add_task_functions.add_task_common import task_value_store


def set_risk_rating(driver, risk_rating_dropdown, risk, wait):
    if not risk or str(risk).strip() == '':
        msg = "❌ Risk input is blank."
        print(msg)
        allure.attach(msg, name="Input Error", attachment_type=allure.attachment_type.TEXT)
        return 'blank'

    # Step 1: Load locators
    try:
        # with allure.step("Loading locators for risk rating..."):
        with open(os.path.join("data", 'locators.json'), 'r') as f:
            elements_details = json.load(f)
            risk_value_check_xpath = elements_details['risk_value_check']
        print("✅ Locators loaded successfully.")
    except (FileNotFoundError, json.JSONDecodeError) as e:
        msg = f"❌ Failed to load locators: {e}"
        print(msg)
        pytest.fail(msg)

    # Step 2: Open dropdown and input risk
    try:
        # with allure.step("Opening risk dropdown and locating options..."):
        risk_input_elem = wait.until(EC.presence_of_element_located((By.XPATH, risk_rating_dropdown)))
        highlight_element(driver, risk_input_elem)
        risk_input_elem.click()
        time.sleep(1)

        # Locate all dropdown options
        options_locator = (By.XPATH, "//div[contains(@class, '-option')]")
        all_options = wait.until(EC.presence_of_all_elements_located(options_locator))
        option_texts = [opt.text.strip() for opt in all_options if opt.text.strip()]
        allure.attach('\n'.join(option_texts), name="All Dropdown Options", attachment_type=allure.attachment_type.TEXT)
    except Exception as e:
        msg = f"❌ Failed to open dropdown or fetch options: {e}"
        print(msg)
        allure.attach(msg, name="Dropdown Interaction Error", attachment_type=allure.attachment_type.TEXT)
        return False

    # Step 3: Select matching risk option
    try:
        # with allure.step("Selecting risk option from dropdown..."):
        found = False
        for option in option_texts:
            if str(risk).lower() in option.lower():
                print(f"✅ Found matching option: {option}")
                risk = option
                found = True
                break

        if not found:
            msg = f"❌ No matching option found for: {risk}"
            print(msg)
            allure.attach(msg, name="Error", attachment_type=allure.attachment_type.TEXT)
            return False

        option_locator = (By.XPATH, f"//div[contains(@class, '-option') and text()='{risk}']")
        dropdown_option = wait.until(EC.visibility_of_element_located(option_locator))
        highlight_element(driver, dropdown_option)
        dropdown_option.click()
        allure.attach(f"Successfully selected: {risk}", name="Selection", attachment_type=allure.attachment_type.TEXT)
    except Exception as e:
        msg = f"❌ Error selecting risk option: {e}"
        print(msg)
        allure.attach(msg, name="Dropdown Selection Error", attachment_type=allure.attachment_type.TEXT)
        return False

    # Step 4: Validate selection
    try:
        # with allure.step("Validating selected risk..."):
        risk_value_input = wait.until(EC.presence_of_element_located((By.XPATH, risk_value_check_xpath)))
        highlight_element(driver, risk_value_input)
        risk_value_text = risk_value_input.text.strip()
        allure.attach(f"Risk Value Check (after selection): {risk_value_text}", name="Risk Value Check", attachment_type=allure.attachment_type.TEXT)

        if risk_value_text == risk:
            print(f"✅ Risk value set correctly: {risk_value_text}")
            task_value_store("risk", risk)
            return True
        else:
            msg = f"❌ Risk mismatch. Expected: {risk}, Found: {risk_value_text}"
            print(msg)
            allure.attach(msg, name="Risk Value Error", attachment_type=allure.attachment_type.TEXT)
            return False
    except Exception as e:
        msg = f"🔥 Unexpected error during risk validation: {e}"
        print(msg)
        allure.attach(msg, name="Error", attachment_type=allure.attachment_type.TEXT)
        return False
