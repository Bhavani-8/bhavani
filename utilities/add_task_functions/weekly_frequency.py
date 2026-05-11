import allure
from utilities.add_task_functions.normalize_date import normalize_date
import os
import json
import pytest
import pyautogui as pg
from utilities.other_utils_functions.highlight import highlight_element
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
from utilities.add_task_functions.add_task_common import task_value_store


def weekly_frequency(driver, frequency, weekday_name, repeat_if_due_date_is_on_holiday, end_frequency_date, option_elements, frequency_value_check, wait):
    try:
        print(f"Setting weekly frequency: {frequency}")

        # Step 1: Validate weekday name
        with allure.step("Validating weekday name..."):
            weekday_name = str(weekday_name).strip()
            valid_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            if weekday_name.capitalize() in valid_days:
                weekday_name = weekday_name.capitalize()
                print(f"✅ Valid weekday: {weekday_name}")
            else:
                weekday_name = None
                print(f"❌ Invalid weekday name: {weekday_name}")

        # Step 2: Process repeat_if_due_date_is_on_holiday
        with allure.step("Processing repeat_if_due_date_is_on_holiday..."):
            repeat_if_due_date_is_on_holiday = str(repeat_if_due_date_is_on_holiday).strip()
            mapping = {'before': 'Before', 'after': 'After', 'yes': 'Yes'}
            repeat_if_due_date_is_on_holiday = mapping.get(repeat_if_due_date_is_on_holiday.lower(), None)
            if repeat_if_due_date_is_on_holiday:
                print(f"✅ Repetition value: {repeat_if_due_date_is_on_holiday}")
            else:
                msg = "Invalid repeat_if_due_date_is_on_holiday value or empty"
                print(f"❌ {msg}")
                allure.attach(msg, name="Input Error", attachment_type=allure.attachment_type.TEXT)

        # Step 3: Normalize end frequency date
        with allure.step("Normalizing end frequency date..."):
            end_frequency_date = str(end_frequency_date)
            try:
                if end_frequency_date.strip():
                    end_frequency_date = normalize_date(end_frequency_date)
                    print(f"✅ Normalized end frequency date: {end_frequency_date}")
                else:
                    end_frequency_date = None
                    print("❌ End frequency date empty or invalid")
            except ValueError:
                end_frequency_date = None
                print("❌ ValueError: end_frequency_date set to None")

        # Step 4: Load locators
        with allure.step("Loading locators for weekly frequency..."):
            try:
                with open(os.path.join("data", 'locators.json'), 'r') as f:
                    elements_details = json.load(f)
                    freq_weekday_option = elements_details['freq_weekday_option']
                    weekly_freq_due_date = elements_details['weekly_freq_due_date']
                    freq_after_option = elements_details['freq_after_option']
                    freq_before_option = elements_details['freq_before_option']
                    freq_yes_option = elements_details['freq_yes_option']
                    end_frequency_date_input = elements_details['end_frequency_date_input']
                    freq_save_btn = elements_details['freq_save_btn']
                    freq_cancel_btn = elements_details['freq_cancel_btn']
                print("✅ Locators loaded successfully.")
            except (FileNotFoundError, json.JSONDecodeError) as e:
                print(f"❌ Error loading locators: {e}")
                pytest.fail(f"Locators loading failed: {e}")

        # Step 5: Select frequency from dropdown
        with allure.step(f"Selecting frequency '{frequency}' from dropdown..."):
            try:
                matched_option = None
                for option in option_elements:
                    if option.text.strip() == frequency:
                        matched_option = option
                        break
                if not matched_option:
                    msg = f"No matching frequency option found: {frequency}"
                    print(f"❌ {msg}")
                    allure.attach(msg, name="Error", attachment_type=allure.attachment_type.TEXT)
                    pytest.fail(msg)
                    return False

                highlight_element(driver, matched_option)
                matched_option.click()
                print(f"✅ Clicked frequency option: {frequency}")

            except Exception as e:
                msg = f"Error selecting frequency option: {e}"
                print(f"❌ {msg}")
                allure.attach(msg, name="Exception", attachment_type=allure.attachment_type.TEXT)
                return False

        # Step 6: Select weekday if applicable
        with allure.step("Selecting weekday if applicable..."):
            weekday_selection = False
            if weekday_name:
                freq_weekday_xpath = freq_weekday_option.replace('day', weekday_name)
                week_elem = wait.until(EC.presence_of_element_located((By.XPATH, freq_weekday_xpath)))
                highlight_element(driver, week_elem)
                week_elem.click()
                print(f"✅ Selected weekday: {weekday_name}")
                weekday_selection = True

        # Step 7: Handle repeat_if_due_date_is_on_holiday options
        with allure.step("Handling repeat_if_due_date_is_on_holiday options..."):
            repeat_selection_done = False
            if repeat_if_due_date_is_on_holiday:
                repeat_mapping = {'Before': freq_before_option, 'After': freq_after_option, 'Yes': freq_yes_option}
                repeat_xpath = repeat_mapping.get(repeat_if_due_date_is_on_holiday)
                if repeat_xpath:
                    repeat_elem = wait.until(EC.presence_of_element_located((By.XPATH, repeat_xpath)))
                    highlight_element(driver, repeat_elem)
                    repeat_elem.click()
                    print(f"✅ Selected repeat option: {repeat_if_due_date_is_on_holiday}")
                    repeat_selection_done = True

        # Step 8: Set end frequency date if applicable
        with allure.step("Setting end frequency date if applicable..."):
            if end_frequency_date:
                end_date_elem = wait.until(EC.presence_of_element_located((By.XPATH, end_frequency_date_input)))
                end_date_elem.click()
                time.sleep(1)
                end_date_elem.send_keys(end_frequency_date)
                pg.press('tab')
                print(f"✅ End frequency date set: {end_frequency_date}")

        # Step 9: Click Save or Cancel
        with allure.step("Saving or cancelling frequency selection..."):
            if weekday_selection and repeat_selection_done:
                save_btn = wait.until(EC.presence_of_element_located((By.XPATH, freq_save_btn)))
                highlight_element(driver, save_btn)
                save_btn.click()
                print("💾 Clicked Save. Frequency set successfully.")
            else:
                cancel_btn = wait.until(EC.presence_of_element_located((By.XPATH, freq_cancel_btn)))
                highlight_element(driver, cancel_btn)
                cancel_btn.click()
                print("💾 Clicked Cancel. Frequency not set.")

        # Step 10: Validate final frequency selection
        with allure.step("Validating final frequency selection..."):
            frequency_elem = wait.until(EC.presence_of_element_located((By.XPATH, frequency_value_check)))
            selected_frequency = frequency_elem.text
            if selected_frequency.lower() == frequency.lower():
                task_value_store("frequency", frequency)
                print(f"✅ Frequency validation successful: {selected_frequency}")
                return True
            else:
                msg = f"❌ Frequency validation failed: {selected_frequency} != {frequency}"
                print(msg)
                allure.attach(msg, name="Frequency Validation Error", attachment_type=allure.attachment_type.TEXT)
                return False

    except Exception as e:
        msg = f"🔥 Error setting weekly frequency: {e}"
        print(msg)
        allure.attach(str(e), name="Exception - Weekly Frequency", attachment_type=allure.attachment_type.TEXT)
        pytest.fail(msg)
        return False
