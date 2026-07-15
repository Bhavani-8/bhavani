import allure
import time
import random 
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from utilities.add_task_functions.show_toast import show_toast
from utilities.other_utils_functions.highlight import highlight_element
from utilities.add_task_functions.add_task_common import task_value_store


def set_task_name(driver, task_name_input, task_name, wait):
    try:
        # with allure.step("Validating task name input..."):
        if not task_name or task_name.strip() == "":
            msg = "❌ Input validation failed: task_name parameter is empty or whitespace."
            print(msg)
            allure.attach(msg, name="Task Name Failure", attachment_type=allure.attachment_type.TEXT)
            show_toast(driver, msg)
            time.sleep(2)
            return False

        if len(task_name) > 100:
            msg = "❌ Input validation failed: task_name parameter is too long. Must be < 100 characters."
            print(msg)
            allure.attach(msg, name="Task Name Failure", attachment_type=allure.attachment_type.TEXT)
            return False

        # with allure.step("Locating and setting task name..."):
        # unique_task_name = f"{task_name}_{random.randint(1000, 9999)}"
       
        with allure.step(f"Entering task name: {task_name}"):
            task_name_input_elem = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, task_name_input))
            )
            highlight_element(driver, task_name_input_elem)
            task_name_input_elem.send_keys(task_name)
            print(f"Task name '{task_name}' entered.")

            value_after_set = task_name_input_elem.get_attribute("value") or ""
            value_after_set = value_after_set.strip()
            print(f"Set task name to: '{task_name}', read back: '{value_after_set}'")

            task_value_store("task_name", task_name)
            print("✅ Task name stored successfully.")

            if value_after_set != task_name:
                msg = f"❌ Task name mismatch. Expected: '{task_name}', Found: '{value_after_set}'"
                print(msg)
                allure.attach(msg, name="Task Name Failure", attachment_type=allure.attachment_type.TEXT)
                return False
            return True

        # with allure.step("Storing task name..."):


    except Exception as e:
        msg = f"❌ Error setting task name: {e}"
        print(msg)
        allure.attach(msg, name="Task Name Failure", attachment_type=allure.attachment_type.TEXT)
        return False
