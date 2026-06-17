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

        # ---------------- STEP 1: Validate weekday ----------------
        with allure.step("Validating weekday name..."):
            weekday_name = str(weekday_name).strip()
            valid_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

            if weekday_name.capitalize() in valid_days:
                weekday_name = weekday_name.capitalize()
                print(f"✅ Valid weekday: {weekday_name}")
                weekday_selection = True
            else:
                weekday_name = None
                weekday_selection = False
                print(f"❌ Invalid weekday name")

        # ---------------- STEP 2: Repeat option ----------------
        with allure.step("Processing repeat_if_due_date_is_on_holiday..."):
            repeat_if_due_date_is_on_holiday = str(repeat_if_due_date_is_on_holiday).strip().lower()
            mapping = {'before': 'Before', 'after': 'After', 'yes': 'Yes'}
            repeat_if_due_date_is_on_holiday = mapping.get(repeat_if_due_date_is_on_holiday)
            if repeat_if_due_date_is_on_holiday:
                print(f"✅ Repeat option: {repeat_if_due_date_is_on_holiday}")
            else:
                print("⚠️ Invalid or empty repeat option")

        # ---------------- STEP 3: Normalize date ----------------
        with allure.step("Normalizing end frequency date..."):
            end_frequency_date = str(end_frequency_date)
            try:
                if end_frequency_date.strip():
                    end_frequency_date = normalize_date(end_frequency_date)
                    print(f"✅ Normalized date: {end_frequency_date}")
                else:
                    end_frequency_date = None
                    print("❌ End frequency date empty or invalid")
            except Exception:
                end_frequency_date = None
                print("❌ ValueError: end_frequency_date set to None")

        with allure.step("Loading locators..."):
            try:
                with open(os.path.join("data", "locators.json"), "r") as f:
                    elements = json.load(f)

                freq_weekday_option = elements['freq_weekday_option']
                freq_after_option = elements['freq_after_option']
                freq_before_option = elements['freq_before_option']
                freq_yes_option = elements['freq_yes_option']
                end_frequency_date_input = elements['end_frequency_date_input']
                freq_save_btn = elements['freq_save_btn']
                freq_cancel_btn = elements['freq_cancel_btn']
            except (FileNotFoundError, json.JSONDecodeError) as e:
                print(f"❌ Error loading locators: {e}")
                pytest.fail(f"Locators loading failed: {e}")

        with allure.step("Selecting frequency from dropdown..."):
            matched_option = None

            for option in option_elements:
                if option.text.strip().lower() == frequency.lower():
                    matched_option = option
                    break

            if not matched_option:
                msg = f"Frequency not found: {frequency}"
                allure.attach(msg, name="Error", attachment_type=allure.attachment_type.TEXT)
                pytest.fail(msg)

            highlight_element(driver, matched_option)
            matched_option.click()
            print(f"✅ Selected frequency: {frequency}")

       
        with allure.step("Selecting weekday if applicable..."):
            if weekday_selection:
                freq_weekday_xpath = freq_weekday_option.replace("day", weekday_name)
                week_elem = wait.until(EC.presence_of_element_located((By.XPATH, freq_weekday_xpath)))
                highlight_element(driver, week_elem)
                week_elem.click()
                print(f"✅ Weekday selected: {weekday_name}")

        with allure.step("Selecting repeat option..."):
            try:
                if repeat_if_due_date_is_on_holiday == "Before":
                    repeat_elem = wait.until(EC.presence_of_element_located((By.XPATH, freq_before_option)))
                    repeat_elem.click()
                    repeat_selection_done = True

                elif repeat_if_due_date_is_on_holiday == "After":
                    repeat_elem = wait.until(EC.presence_of_element_located((By.XPATH, freq_after_option)))
                    repeat_elem.click()
                    repeat_selection_done = True

                elif repeat_if_due_date_is_on_holiday == "Yes":
                    repeat_elem = wait.until(EC.presence_of_element_located((By.XPATH, freq_yes_option)))
                    repeat_elem.click()
                    repeat_selection_done = True

                print("✅ Repeat option handled")

            except Exception as e:
                print(f"❌ Repeat option error: {e}")

        # ---------------- STEP 8: End date ----------------
        with allure.step("Setting end date..."):
            if end_frequency_date:
                try:
                    end_date_elem = wait.until(EC.presence_of_element_located((By.XPATH, end_frequency_date_input)))
                    end_date_elem.click()
                    end_date_elem.clear()
                    end_date_elem.send_keys(end_frequency_date)
                    pg.press("tab")
                    print(f"✅ End date set: {end_frequency_date}")
                except Exception as e:
                    print(f"❌ End date error: {e}")

        with allure.step("Saving frequency selection..."):
            try:
                time.sleep(1)
                
                if weekday_selection:
                    save_btn = wait.until(EC.presence_of_element_located((By.XPATH, freq_save_btn)))
                    highlight_element(driver, save_btn)
                    save_btn.click()
                    print("💾 Save clicked successfully")
                else:
                    cancel_btn = wait.until(EC.presence_of_element_located((By.XPATH, freq_cancel_btn)))
                    highlight_element(driver, cancel_btn)
                    cancel_btn.click()
                    print("❌ Cancel clicked")

            except Exception as e:
                msg = f"Save/Cancel error: {e}"
                allure.attach(msg, name="SaveCancel Error", attachment_type=allure.attachment_type.TEXT)
                return False

        with allure.step("Validating frequency..."):
            frequency_elem = wait.until(EC.presence_of_element_located((By.XPATH, frequency_value_check)))
            selected_frequency =  frequency_elem.text.strip()

            if selected_frequency.lower() == frequency.lower():
                task_value_store("frequency", frequency)
                print(f"✅ Validation passed: {selected_frequency}")
                return True
            else:
                msg = f"Mismatch: {selected_frequency} != {frequency}"
                allure.attach(msg, name="Validation Failed", attachment_type=allure.attachment_type.TEXT)
                return False

    except Exception as e:
        msg = f"🔥 Weekly frequency error: {e}"
        allure.attach(msg, name="Exception", attachment_type=allure.attachment_type.TEXT)
        pytest.fail(msg)
        return False