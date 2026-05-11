import allure
from utilities.other_utils_functions.highlight import highlight_element
from utilities.add_task_functions.add_task_common import task_value_store
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


def set_license(driver, license_input_path, license_name, wait):
    # Step 1: Validate input
    if not license_name or str(license_name).strip() == '':
        msg = "❌ License input is blank."
        print(msg)
        allure.attach(msg, name="Input Error", attachment_type=allure.attachment_type.TEXT)
        return 'blank'

    # Step 2: Interact with input field
    try:
        # with allure.step("Locating and interacting with license input field"):
        license_input_elem = wait.until(EC.presence_of_element_located((By.XPATH, license_input_path)))
        highlight_element(driver, license_input_elem)
        license_input_elem.click()
        license_input_elem.clear()
        license_input_elem.send_keys(license_name)
    except Exception as e:
        msg = f"❌ Failed to locate or input license: {e}"
        print(msg)
        allure.attach(msg, name="Input Interaction Error", attachment_type=allure.attachment_type.TEXT)
        return False

    # Step 3: Validate input value
    try:
        # with allure.step("Validating license value"):
        license_value_check = license_input_elem.get_attribute('value')
        if license_value_check == license_name:
            msg = f"✅ License value is set correctly: {license_name}"
            print(msg)
            allure.attach(msg, name="License Validation", attachment_type=allure.attachment_type.TEXT)
            task_value_store("license", license_name)
            return True
        else:
            msg = f"❌ License mismatch. Expected: {license_name}, Found: {license_value_check}"
            print(msg)
            allure.attach(msg, name="License Value Error", attachment_type=allure.attachment_type.TEXT)
            return False
    except Exception as e:
        msg = f"🔥 Unexpected error during license validation: {e}"
        print(msg)
        allure.attach(msg, name="Error", attachment_type=allure.attachment_type.TEXT)
        return False
