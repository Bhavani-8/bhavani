import allure
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from utilities.other_utils_functions.highlight import highlight_element
from utilities.add_task_functions.add_task_common import task_value_store

def add_description(driver, description_btn, description_input, description, desc_save_btn, desc_view, wait):
    if not description or description.strip() == '':
        msg = "❌ Description input is blank."
        print(msg)
        allure.attach(msg, name="Input Error", attachment_type=allure.attachment_type.TEXT)
        return 'blank'

    try:
        # with allure.step("Click description button"):
        description_btn_elem = wait.until(EC.presence_of_element_located((By.XPATH, description_btn)))
        highlight_element(driver, description_btn_elem)
        description_btn_elem.click()
        time.sleep(2)
        print("Clicked description button")

        # with allure.step("Enter description text"):
        description_input_elem = wait.until(EC.presence_of_element_located((By.XPATH, description_input)))
        highlight_element(driver, description_input_elem)
        description_input_elem.click()
        time.sleep(0.5)  # Small delay to ensure the input is ready
        description_input_elem.send_keys(description)
        time.sleep(1)
        print(f"Description Input: {description}")

        # with allure.step("Save description"):
        try:
            desc_save_button = wait.until(
                EC.element_to_be_clickable((By.XPATH, desc_save_btn))
            )
            highlight_element(driver, desc_save_button)
            desc_save_button.click()
            print("✅ Description Saved (primary locator)")

        except Exception as e1:
            print(f"⚠️ Primary locator failed: {e1}")

            try:
                update_desc_save_button = wait.until(
                    EC.element_to_be_clickable((By.XPATH, "(//button//span[text()='Save'])[2]"))
                )
                highlight_element(driver, update_desc_save_button)
                update_desc_save_button.click()
                print("✅ Description Saved (fallback locator)")

            except Exception as e2:
                print(f"❌ Both locators failed: {e2}")
                raise



        # with allure.step("Validate saved description"):
        desc_view_area = wait.until(EC.presence_of_element_located((By.XPATH, desc_view)))
        highlight_element(driver, desc_view_area)
        desc_value = desc_view_area.text.strip()
        print(f"Description Value: {desc_value}")

        if desc_value == description:
            print("Description saved correctly")
            task_value_store("description", description)
            return True
        else:
            msg = f"❌ Description mismatch. Expected: {description}, Found: {desc_value}"
            print(msg)
            allure.attach(msg, name="Description Validation Error", attachment_type=allure.attachment_type.TEXT)
            return False

    except Exception as e:
        print(f"Error adding description: {e}")
        allure.attach(str(e), name="Add Description Error", attachment_type=allure.attachment_type.TEXT)
        return False
