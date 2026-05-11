import allure
from utilities.add_task_functions.show_toast import show_toast
import os
import json
import pytest
import pyautogui as pg
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from utilities.other_utils_functions.highlight import highlight_element
from datetime import datetime
from utilities.add_task_functions.add_task_common import task_value_store


def set_deadline_input(driver, start_date_input, due_date_input, deadline_input, internal_deadline, wait):
    if internal_deadline is None or str(internal_deadline).strip() == '':
        msg = "❌ Internal deadline input is blank."
        print(msg)
        allure.attach(msg, name="Input Error", attachment_type=allure.attachment_type.TEXT)
        return 'blank'

    # Step 1: Convert input to int
    try:
        # with allure.step("Converting internal_deadline to integer..."):
        internal_deadline = int(float(internal_deadline))
        print(f"Internal deadline converted: {internal_deadline}")
    except ValueError:
        msg = f"❌ Invalid internal_deadline format: {internal_deadline}"
        print(msg)
        allure.attach(msg, name="Conversion Error", attachment_type=allure.attachment_type.TEXT)
        show_toast(driver, msg)
        return 'invalid'

    # Step 2: Load locators
    try:
        # with allure.step("Loading locators for internal deadline..."):
        with open(os.path.join("data", 'locators.json'), 'r') as f:
            elements_details = json.load(f)
            deadline_err_msg_xpath = elements_details['deadline_err_msg']
        print("✅ Locators loaded successfully.")
    except (FileNotFoundError, json.JSONDecodeError) as e:
        msg = f"❌ Error loading locators.json: {e}"
        print(msg)
        pytest.fail(msg)

    # Step 3: Locate input fields and set value
    try:
        # with allure.step("Locating input fields and setting internal deadline..."):
        start_date_elem = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, start_date_input)))
        due_date_elem = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, due_date_input)))
        deadline_elem = wait.until(EC.presence_of_element_located((By.XPATH, deadline_input)))

        highlight_element(driver, deadline_elem)
        deadline_elem.clear()
        deadline_elem.send_keys(internal_deadline)
        pg.press('Tab')

        value_after_set = deadline_elem.get_attribute("value")
        start_value = start_date_elem.get_attribute("value")
        due_value = due_date_elem.get_attribute("value")

        msg = f"Values fetched: start={start_value}, due={due_value}, deadline={value_after_set}"
        print(msg)
        allure.attach(msg, name="Fetched Values", attachment_type=allure.attachment_type.TEXT)

    except Exception as e:
        msg = f"❌ Error locating fields or setting value: {e}"
        print(msg)
        allure.attach(msg, name="Input Error", attachment_type=allure.attachment_type.TEXT)
        return False

    # Step 4: Validate internal deadline
    try:
        # with allure.step("Validating internal deadline against start and due dates..."):
        start_date = datetime.strptime(start_value, "%d %B %Y")
        due_date = datetime.strptime(due_value, "%d %B %Y")
        date_diff = (due_date - start_date).days

        if internal_deadline > date_diff:
            msg = f"❌ Internal deadline {internal_deadline} exceeds start-due difference {date_diff}"
            print(msg)
            allure.attach(msg, name="Deadline Validation", attachment_type=allure.attachment_type.TEXT)

            error_elem = wait.until(EC.presence_of_element_located((By.XPATH, deadline_err_msg_xpath)))
            highlight_element(driver, error_elem)
            error_text = error_elem.text.strip()

            if error_text == "Internal deadline date can't be less than start date.":
                print("✅ Error message matches expected value.")
                deadline_elem.clear()
                task_value_store("internal_deadline", internal_deadline)
                return False
            else:
                print("❌ Error message does not match expected value.")
                allure.attach(f"Error message does not match expected value.", name="Deadline Error", attachment_type=allure.attachment_type.TEXT)
                deadline_elem.clear()
                return False
        else:
            msg = f"✅ Internal deadline is valid: {internal_deadline} < {date_diff}"
            print(msg)
            allure.attach(msg, name="Deadline Check", attachment_type=allure.attachment_type.TEXT)

    except ValueError as e:
        msg = f"⚠️ Date parsing failed: {e}"
        print(msg)
        allure.attach(msg, name="Parsing Error", attachment_type=allure.attachment_type.TEXT)
        return False

# Step 5: Confirm final input
    try:
    # with allure.step("Validating input after setting..."):
        if int(value_after_set) == int(internal_deadline):
            msg = f"✅ Internal deadline {value_after_set} is set correctly."
            print(msg)
            allure.attach(f"Final Input after setting: {value_after_set}", name="Internal Deadline Field", attachment_type=allure.attachment_type.TEXT)
            task_value_store("internal_deadline", internal_deadline)
            return True
        else:
            msg = f"❌ Internal deadline mismatch: expected {internal_deadline}, got {value_after_set}"
            print(msg)
            allure.attach(msg, name="Validation Error", attachment_type=allure.attachment_type.TEXT)
            return False

    except Exception as e:
        msg = f"🔥 Unexpected error during final validation: {e}"
        print(msg)
        allure.attach(msg, name="Error", attachment_type=allure.attachment_type.TEXT)
        return False
