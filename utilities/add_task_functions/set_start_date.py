import allure
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from datetime import datetime, date
import pyautogui as pg
from utilities.other_utils_functions.highlight import highlight_element


def set_start_date(driver, start_date_input, start_date, wait):
    print(f"Setting start date to: {start_date}")
    try:
        # with allure.step("Validating start date input..."):
        if not start_date or start_date.strip() == "":
            msg = "❌ Input validation failed: start_date parameter is empty or whitespace."
            print(msg)
            allure.attach(msg, name="Start Date Failure", attachment_type=allure.attachment_type.TEXT)
            return False

        # with allure.step("Locating and setting start date..."):
        start_date_input_elem = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, start_date_input))
        )
        highlight_element(driver, start_date_input_elem)
        start_date_input_elem.clear()
        start_date_input_elem.send_keys(start_date)
        pg.hotkey('tab')
        print(f"Entered start date: {start_date}")

        # with allure.step("Validating start date value..."):
        start_date_expected = datetime.strptime(start_date, "%d %B %Y").date()
        todays_date = date.today()
        print(f"Start date expected: {start_date_expected}")
        print(f"Today's date: {todays_date}")

        start_date_fetched = start_date_input_elem.get_attribute("value") or ""
        if start_date_fetched.strip():
            start_date_value = datetime.strptime(start_date_fetched, "%d %B %Y").date()
        else:
            if start_date_expected < todays_date:
                msg = (
                    f"❌ Start date: {start_date_expected} is before today's date: {todays_date}; "
                    "field was cleared by UI as expected."
                )
                print(msg)
                allure.attach(msg, name="Start Date Failure", attachment_type=allure.attachment_type.TEXT)
                return False
            else:
                msg = "❌ Start date input field is unexpectedly empty after entry."
                print(msg)
                allure.attach(msg, name="Start Date Failure", attachment_type=allure.attachment_type.TEXT)
                return False

        print(f"Value after setting start date: '{start_date_fetched}'")

        if start_date_value != start_date_expected:
            msg = f"❌ Start date mismatch. Expected: {start_date_expected}, Found: {start_date_value}"
            print(msg)
            allure.attach(msg, name="Start Date Failure", attachment_type=allure.attachment_type.TEXT)
            return False

        print(f"✅ Start date '{start_date_value}' matched with entered date '{start_date}'.")

        return True

    except Exception as e:
        msg = f"🔥 Error setting start date: {e}"
        print(msg)
        allure.attach(msg, name="Start Date Failure", attachment_type=allure.attachment_type.TEXT)
        return False
