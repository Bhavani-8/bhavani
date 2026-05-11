import allure
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from utilities.other_utils_functions.highlight import highlight_element
import pyautogui as pg
from datetime import datetime, date


def set_due_date(driver, due_date_input, start_date_input, due_date, task_input_error_msg, wait):
    try:
        # with allure.step("Validating due date input..."):
        if not due_date or due_date.strip() == "":
            msg = "❌ Input validation failed: due_date parameter is empty or whitespace."
            print(msg)
            allure.attach(msg, name="Due Date Failure", attachment_type=allure.attachment_type.TEXT)
            return False

        # with allure.step("Locating and setting due date..."):
        start_date_input_elem = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, start_date_input))
        )
        due_date_input_elem = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, due_date_input))
        )
        highlight_element(driver, due_date_input_elem)
        due_date_input_elem.clear()
        due_date_input_elem.send_keys(due_date)
        pg.hotkey('tab')
        print(f"Entered due date: {due_date}")

        # with allure.step("Validating due date value..."):
        due_date_expected = datetime.strptime(due_date, "%d %B %Y").date()
        print(f"Due date expected: {due_date_expected}")

        start_date_value = datetime.strptime(
            start_date_input_elem.get_attribute("value"), "%d %B %Y"
        ).date()
        print(f"Start date fetched: {start_date_value}")

        todays_date = date.today()
        print(f"Today's date: {todays_date}")

        due_date_fetched = due_date_input_elem.get_attribute("value") or ""
        if due_date_fetched.strip():
            due_date_value = datetime.strptime(due_date_fetched, "%d %B %Y").date()
        else:
            if due_date_expected < todays_date:
                msg = (
                    f"❌ Due date {due_date_expected} is before today's date {todays_date}; "
                    "field was cleared by UI as expected."
                )
                print(msg)
                allure.attach(msg, name="Due Date Failure", attachment_type=allure.attachment_type.TEXT)
                return False
            else:
                msg = "❌ Due date input field is unexpectedly empty after entry."
                print(msg)
                allure.attach(msg, name="Due Date Failure", attachment_type=allure.attachment_type.TEXT)
                return False

        print(f"Due date fetched: {due_date_value}")

        if due_date_value < start_date_value:
            expected_msg = "Due date should not be prior to start date"
            task_input_error_msg_elem = wait.until(
                EC.presence_of_all_elements_located((By.XPATH, task_input_error_msg))
            )

            for msg_elem in task_input_error_msg_elem:
                if msg_elem.text.lower() == expected_msg.lower() or "end date" in msg_elem.text.lower():
                    print(f"✅ Expected error message displayed: {msg_elem.text}")
                else:
                    msg = f"❌ Unexpected error message displayed: {msg_elem.text}"
                    print(msg)
                    allure.attach(msg, name="Due Date Failure", attachment_type=allure.attachment_type.TEXT)
                    return False

            msg = f"❌ Due date {due_date_value} is before start date {start_date_value}."
            print(msg)
            allure.attach(msg, name="Due Date Failure", attachment_type=allure.attachment_type.TEXT)
            return False

        if due_date_value != due_date_expected:
            msg = f"❌ Due date mismatch. Expected: {due_date_expected}, Found: {due_date_value}"
            print(msg)
            allure.attach(msg, name="Due Date Failure", attachment_type=allure.attachment_type.TEXT)
            return False

        print(f"✅ Due date '{due_date_value}' matched with entered date '{due_date}'.")

        return True

    except Exception as e:
        msg = f"🔥 Error setting due date: {e}"
        print(msg)
        allure.attach(msg, name="Due Date Failure", attachment_type=allure.attachment_type.TEXT)
        return False
