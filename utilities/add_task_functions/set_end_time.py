import allure
import os
import json
import pytest
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from utilities.other_utils_functions.highlight import highlight_element
import pyautogui as pg
from datetime import datetime, date
from selenium.webdriver import ActionChains
from utilities.add_task_functions.add_task_common import task_value_store


# def set_end_time(driver, end_time_input_path, end_time, wait):

#     if not end_time or end_time.strip() == '':
#         msg = "❌ End time input is blank."
#         print(msg)
#         allure.attach(msg, name="Input Error", attachment_type=allure.attachment_type.TEXT)
#         return 'blank'

#     try:
#     # with allure.step("Loading locators..."):
#         try:
#             with open(os.path.join("data", 'locators.json'), 'r') as f:
#                 locators = json.load(f)
#                 end_time_clear_btn = locators['end_time_clear_btn']
#                 error_msg_xpath = locators['task_input_error_msg']
#                 start_date_selector = locators['start_date_input']
#                 due_date_selector = locators['due_date_input']
#             print("✅ Locators loaded successfully.")
#         except (FileNotFoundError, json.JSONDecodeError) as e:
#             msg = f"❌ Error loading locators.json: {e}"
#             print(msg)
#             pytest.fail(msg)

#         # with allure.step("Locating input fields..."):
#         start_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, start_date_selector)))
#         due_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, due_date_selector)))
#         end_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, end_time_input_path)))
#         highlight_element(driver, end_input)

#         # with allure.step(f"Setting end time to {end_time}..."):
#         end_input.clear()
#         end_input.send_keys(end_time)
#         pg.press('Tab')

#         value_after_set = end_input.get_attribute("value")
#         end_time_fetched = datetime.strptime(value_after_set, '%I:%M %p')
#         end_time_obj = end_time_fetched.time()
#         print(f"End time fetched: {end_time_obj}")

#         # with allure.step("Logging current and input values..."):
#         todays_date = date.today()
#         current_time = datetime.now().strftime("%I:%M %p")
#         start_value = start_input.get_attribute("value")
#         due_value = due_input.get_attribute("value")
#         print(f"Today's date: {todays_date}, Current time: {current_time}")
#         print(f"Start value: {start_value}, Due value: {due_value}")

#         # with allure.step("Validating end time..."):
#         if start_value == due_value and value_after_set < current_time:
#             msg = f"❌ End time {value_after_set} is before current time {current_time}."
#             print(msg)
#             allure.attach(msg, name="End Time Validation", attachment_type=allure.attachment_type.TEXT)

#             error_elem = wait.until(EC.presence_of_element_located((By.XPATH, error_msg_xpath)))
#             highlight_element(driver, error_elem)
#             error_text = error_elem.text.strip()

#             if error_text == "End Time must be after or equal to current time.":
#                 print("✅ Error message validated.")
#                 clear_btn = wait.until(EC.presence_of_element_located((By.XPATH, end_time_clear_btn)))
#                 highlight_element(driver, clear_btn)
#                 ActionChains(driver).move_to_element(clear_btn).pause(1).click().perform()
#                 allure.attach("End time cleared due to invalid input", name="End Time Field", attachment_type=allure.attachment_type.TEXT)
#                 task_value_store("end_time", end_time)
#                 return False
#             else:
#                 print("❌ Unexpected error message.")
#                 return False

#         if value_after_set == end_time:
#             msg = f"✅ End time {value_after_set} is set correctly."
#             print(msg)
#             allure.attach(f"Final Input: {value_after_set}", name="End Time Field", attachment_type=allure.attachment_type.TEXT)
#             task_value_store("end_time", end_time)
#             return True

#         print("❌ End time value mismatch.")
#         return False

#     except Exception as e:
#         msg = f"🔥 Exception occurred while setting end time: {e}"
#         print(msg)
#         allure.attach(msg, name="Error", attachment_type=allure.attachment_type.TEXT)
#         return False



def set_end_time(driver, end_time_input_path, end_time, wait):
    if not end_time or end_time.strip() == '':
        msg = "❌ End time input is blank."
        print(msg)
        allure.attach(msg, name="Input Error", attachment_type=allure.attachment_type.TEXT)
        return 'blank'

    try:
        # Load locators
        with open(os.path.join("data", 'locators.json'), 'r') as f:
            locators = json.load(f)
        end_time_clear_btn = locators['end_time_clear_btn']
        error_msg_xpath = locators['task_input_error_msg']
        start_date_selector = locators['start_date_input']
        due_date_selector = locators['due_date_input']
        print("✅ Locators loaded successfully.")

        # Locate inputs
        start_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, start_date_selector)))
        due_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, due_date_selector)))
        end_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, end_time_input_path)))
        highlight_element(driver, end_input)

        # Set end time
        end_input.clear()
        end_input.send_keys(end_time)
        pg.press('Tab')

        # Fetch and convert to datetime.time
        value_after_set = end_input.get_attribute("value")
        end_time_obj = datetime.strptime(value_after_set, '%I:%M %p').time()
        print(f"End time fetched: {end_time_obj}")

        # Validate against current time
        now_time = datetime.now().time()
        if end_time_obj < now_time:
            msg = f"❌ End time {value_after_set} is before current time {now_time.strftime('%I:%M %p')}."
            print(msg)
            allure.attach(msg, name="End Time Validation", attachment_type=allure.attachment_type.TEXT)

            # Highlight error message if present
            error_elem = wait.until(EC.presence_of_element_located((By.XPATH, error_msg_xpath)))
            highlight_element(driver, error_elem)
            error_text = error_elem.text.strip()

            if error_text == "End Time must be after or equal to current time.":
                print("✅ Error message validated.")
                clear_btn = wait.until(EC.presence_of_element_located((By.XPATH, end_time_clear_btn)))
                highlight_element(driver, clear_btn)
                ActionChains(driver).move_to_element(clear_btn).pause(1).click().perform()
                allure.attach("End time cleared due to invalid input", name="End Time Field", attachment_type=allure.attachment_type.TEXT)
                task_value_store("end_time", end_time)
                return False
            return False

        # Success
        if value_after_set == end_time:
            msg = f"✅ End time {value_after_set} is set correctly."
            print(msg)
            allure.attach(f"Final Input: {value_after_set}", name="End Time Field", attachment_type=allure.attachment_type.TEXT)
            task_value_store("end_time", end_time)
            return True

        print("❌ End time value mismatch.")
        return False

    except Exception as e:
        msg = f"🔥 Exception occurred while setting end time: {e}"
        print(msg)
        allure.attach(msg, name="Error", attachment_type=allure.attachment_type.TEXT)
        return False
