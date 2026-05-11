import allure
from utilities.other_utils_functions.highlight import highlight_element
import time
import os
import json
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from utilities.add_task_functions.add_task_common import task_value_store


def set_task_category(driver, task_category_dropdown, task_category, wait):
    if not task_category or task_category == '':
        msg = "❌ Category input is blank."
        print(msg)
        allure.attach(msg, name="Input Error", attachment_type=allure.attachment_type.TEXT)
        return 'blank'
     
    try:
        task_category_input_elem = wait.until(EC.presence_of_element_located((By.XPATH, task_category_dropdown)))
        highlight_element(driver, task_category_input_elem)
        task_category_input_elem.click()
        time.sleep(1)

        # Locate all dropdown options
        options_locator = (By.XPATH, "//div[contains(@class, '-option')]")
        all_options = wait.until(EC.presence_of_all_elements_located(options_locator))
        option_texts = [opt.text.strip() for opt in all_options if opt.text.strip()]
        print(f'Option text: {option_texts}')
        allure.attach('\n'.join(option_texts), name="All Dropdown Options", attachment_type=allure.attachment_type.TEXT)

        found = False
        for option in option_texts:
            if str(task_category).lower() in option.lower():
                print(f"✅ Found matching option: {option}")
                task_category = option
                found = True
                break
        
        if not found:
            print(f"❌ No matching option found for: {task_category}")
            allure.attach(f"No matching option found for: {task_category}", name="Error", attachment_type=allure.attachment_type.TEXT)
            return False

        option_locator = (By.XPATH, f"//div[contains(@class, '-option') and text()='{task_category}']")
        dropdown_option = wait.until(EC.visibility_of_element_located(option_locator))
        print(f"Dropdown option found: {dropdown_option.text.strip()}")
        highlight_element(driver, dropdown_option)
        dropdown_option.click()
        print(f"Successfully selected: {task_category}")

        # task_category_text = wait.utnil(EC.presence_of_element_located((By.XPATH, "(//div[@class='css-19bb58m'])[6]")))
        # highlight_element(driver, wait)

         # -------------------------------
        # ✅ Step 5: Validation (ACTUAL vs EXPECTED)
        # -------------------------------
        try:
            selected_elem = wait.until(EC.presence_of_element_located((
                By.XPATH, "(//div[contains(@class,'singleValue')])[4]"
            )))
            highlight_element(driver, selected_elem)

            actual = selected_elem.text.strip()
            expected = task_category

            print(f"Comparing {actual} with {expected}")

            allure.attach(
                f"Validating '{actual}' with '{expected}' for field 'task_category'",
                name="Task Category Validation",
                attachment_type=allure.attachment_type.TEXT
            )

            if actual.lower() == expected.lower():
                print(f"✅ Match: {actual} == {expected}")

                # ✅ Store like other modules
                task_value_store("task_category", actual)

                return True
            else:
                print(f"❌ Mismatch: {actual} != {expected}")
                return False

        except Exception as e:
            msg = f"❌ Validation failed: {e}"
            print(msg)
            allure.attach(msg, name="Validation Error", attachment_type=allure.attachment_type.TEXT)
            return False

    except Exception as e:
        msg = f"❌ Error setting Task Category: {e}"
        print(msg)
        allure.attach(msg, name="Error", attachment_type=allure.attachment_type.TEXT)
        return False


