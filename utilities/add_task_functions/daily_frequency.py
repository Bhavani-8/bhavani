from utilities.add_task_functions.normalize_date import normalize_date
import allure
import os
import json
import pytest
from utilities.other_utils_functions.highlight import highlight_element
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from utilities.add_task_functions.add_task_common import task_value_store
import time
import pyautogui as pg
from pandas import Timestamp


# def daily_frequency(driver, frequency, repeat_if_due_date_is_on_holiday, end_frequency_date, option_elements, frequency_value_check, wait):
#     if frequency.lower() == "only once":
#         # Nothing to do for 'None'
#         print("ℹ️ Frequency set to 'Only Once' — no further configuration needed.")
#         return True
#         # pg.press("esc")
#         # return True
#     try:
#         # Step 1: Normalize end_frequency_date
#         with allure.step("Normalize end frequency date"):
#             try:
#                 if end_frequency_date and str(end_frequency_date).strip():
#                     end_frequency_date = normalize_date(str(end_frequency_date))
#                     print(f"📅 Normalized end frequency date: {end_frequency_date}")
#                 else:
#                     end_frequency_date = None
#                     print("⚠️ End frequency date is empty or invalid; using None.")
#             except ValueError:
#                 end_frequency_date = None
#                 print("⚠️ ValueError while normalizing end frequency date; using None.")

#         # Step 2: Process repeat_if_due_date_is_on_holiday input
#         with allure.step("Process repeat_if_due_date_is_on_holiday"):
#             raw_repeat = str(repeat_if_due_date_is_on_holiday).strip().lower()
#             if raw_repeat == "yes":
#                 repeat_flag = True
#                 print("🔄 Repeat if due date is on holiday: Yes")
#             elif raw_repeat == "no":
#                 repeat_flag = False
#                 print("🔄 Repeat if due date is on holiday: No")
#             elif raw_repeat == "":
#                 repeat_flag = None
#                 print("⚠️ repeat_if_due_date_is_on_holiday is empty; treated as None")
#             else:
#                 repeat_flag = None
#                 msg = f"❌ Invalid repeat_if_due_date_is_on_holiday value: '{repeat_if_due_date_is_on_holiday}'"
#                 print(msg)
#                 # This is a failure in input — attach evidence
#                 allure.attach(msg, name="Repeat Input Error", attachment_type=allure.attachment_type.TEXT)

#         # Step 3: Load locators
#         with allure.step("Load locators for daily frequency"):
#             try:
#                 print("📁 Loading locators for daily frequency...")
#                 with open(os.path.join("data", "locators.json"), "r") as f:
#                     elements_details = json.load(f)
#                 daily_freq_yes_option = elements_details["daily_freq_yes_option"]
#                 daily_freq_no_option = elements_details["daily_freq_no_option"]
#                 end_frequency_date_input = elements_details["end_frequency_date_input"]
#                 freq_save_btn = elements_details["freq_save_btn"]
#                 freq_cancel_btn = elements_details["freq_cancel_btn"]
#                 print("✅ Locators loaded successfully.")
#             except FileNotFoundError:
#                 msg = "❌ locators.json file not found."
#                 print(msg)
#                 allure.attach(msg, name="Locators Error", attachment_type=allure.attachment_type.TEXT)
#                 pytest.fail(msg)
#             except json.JSONDecodeError:
#                 msg = "❌ Invalid JSON in locators.json."
#                 print(msg)
#                 allure.attach(msg, name="Locators Error", attachment_type=allure.attachment_type.TEXT)
#                 pytest.fail(msg)

#         # Step 4: Find and click the matching frequency option
#         with allure.step("Select frequency option from dropdown"):
#             print(f"🔎 Looking for the frequency option: {frequency}")
#             found_option = None
#             for option in option_elements:
#                 opt_text = option.text.strip()
#                 print(f"   ➡️ Checking option: {opt_text}")
#                 if opt_text == frequency:
#                     found_option = option
#                     break

#             if not found_option:
#                 msg = f"❌ Frequency option '{frequency}' not found in dropdown list."
#                 print(msg)
#                 allure.attach(msg, name="Frequency Option Not Found", attachment_type=allure.attachment_type.TEXT)
#                 return False

#             # Click the found option
#             print(f"✅ Found matching option: {frequency}. Clicking...")
#             highlight_element(driver, found_option)
#             found_option.click()

#             if frequency == "Only once":
#                 # Nothing else to do for 'Only once'
#                 print("ℹ️ Frequency set to 'Only once' — no further configuration needed.")
#                 return True

#         # Step 5: Choose Yes/No radio for repeat-on-holiday
#         with allure.step("Choose repeat-on-holiday option"):
#             selected = False
#             if repeat_flag is True:
#                 try:
#                     elem = wait.until(EC.presence_of_element_located((By.XPATH, daily_freq_yes_option)))
#                     print("✅ 'Yes' option found.")
#                     highlight_element(driver, elem)
#                     elem.click()
#                     print("✅ Selected 'Yes' for repeat on holiday.")
#                     selected = True
#                 except Exception as e:
#                     msg = f"❌ Failed to select 'Yes' option: {e}"
#                     print(msg)
#                     allure.attach(msg, name="Select Yes Error", attachment_type=allure.attachment_type.TEXT)
#                     return False

#             elif repeat_flag is False:
#                 try:
#                     elem = wait.until(EC.presence_of_element_located((By.XPATH, daily_freq_no_option)))
#                     print("✅ 'No' option found.")
#                     highlight_element(driver, elem)
#                     elem.click()
#                     print("✅ Selected 'No' for repeat on holiday.")
#                     selected = True
#                 except Exception as e:
#                     msg = f"❌ Failed to select 'No' option: {e}"
#                     print(msg)
#                     allure.attach(msg, name="Select No Error", attachment_type=allure.attachment_type.TEXT)
#                     return False

#             else:
#                 # repeat_flag is None — treat as user-intent not provided; proceed to Cancel flow
#                 print("⚠️ No valid repeat-on-holiday option selected (value is None or invalid).")

#         # Step 6: If 'Yes' and end date provided, set end frequency date
#         with allure.step("Set end frequency date (if provided)"):
#             if selected and repeat_flag is True and end_frequency_date:
#                 try:
#                     date_elem = wait.until(EC.presence_of_element_located((By.XPATH, end_frequency_date_input)))
#                     highlight_element(driver, date_elem)
#                     date_elem.click()
#                     time.sleep(0.5)
#                     date_elem.clear()
#                     date_elem.send_keys(end_frequency_date)
#                     pg.press("tab")
#                     print(f"📅 End frequency date set: {end_frequency_date}")
#                 except Exception as e:
#                     msg = f"❌ Failed to set end frequency date '{end_frequency_date}': {e}"
#                     print(msg)
#                     allure.attach(msg, name="End Date Set Error", attachment_type=allure.attachment_type.TEXT)
#                     return False
#             else:
#                 if repeat_flag is True:
#                     print("ℹ️ No end frequency date provided; skipping end-date entry.")
#                 else:
#                     print("ℹ️ End frequency date not applicable for current selection.")

#         # Step 7: Click Save or Cancel depending on selection
#         with allure.step("Save or Cancel frequency selection"):
#             try:
#                 if selected:
#                     save_btn = wait.until(EC.presence_of_element_located((By.XPATH, freq_save_btn)))
#                     highlight_element(driver, save_btn)
#                     save_btn.click()
#                     print("💾 Clicked Save. Frequency set successfully.")
#                 else:
#                     cancel_btn = wait.until(EC.presence_of_element_located((By.XPATH, freq_cancel_btn)))
#                     highlight_element(driver, cancel_btn)
#                     cancel_btn.click()
#                     print("💾 Clicked Cancel. Frequency cancelled.")
#             except Exception as e:
#                 msg = f"❌ Error clicking Save/Cancel button: {e}"
#                 print(msg)
#                 allure.attach(msg, name="SaveCancel Error", attachment_type=allure.attachment_type.TEXT)
#                 return False

#         # Step 8: Validate the final selected frequency displayed in the UI
#         with allure.step("Validate selected frequency in UI"):
#             try:
#                 freq_elem = wait.until(EC.presence_of_element_located((By.XPATH, frequency_value_check)))
#                 selected_frequency = (freq_elem.text or "").strip()
#                 print(f"📌 Selected frequency read from UI: '{selected_frequency}'")
#                 if selected_frequency.lower() == (frequency or "").lower():
#                     # success — store value and return True
#                     task_value_store("frequency", frequency)
#                     print(f"✅ Frequency validation successful: '{selected_frequency}' == '{frequency}'")
#                     return True
#                 else:
#                     msg = f"❌ Frequency validation failed: UI shows '{selected_frequency}', expected '{frequency}'"
#                     print(msg)
#                     allure.attach(msg, name="Frequency Validation Error", attachment_type=allure.attachment_type.TEXT)
#                     return False
#             except Exception as e:
#                 msg = f"❌ Error validating selected frequency: {e}"
#                 print(msg)
#                 allure.attach(msg, name="Validation Error", attachment_type=allure.attachment_type.TEXT)
#                 return False

#     except Exception as e:
#         # Final catch-all
#         err_msg = f"🔥 Unexpected error in daily_frequency: {e}"
#         print(err_msg)
#         allure.attach(err_msg, name="Unexpected Error", attachment_type=allure.attachment_type.TEXT)
#         pytest.fail(err_msg)
#         return False

def daily_frequency(driver, frequency, repeat_if_due_date_is_on_holiday, end_frequency_date, option_elements, frequency_value_check, wait):
    try:
        # Step 1: Normalize end_frequency_date
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

        # Step 2: Process repeat_if_due_date_is_on_holiday input
        with allure.step("Process repeat_if_due_date_is_on_holiday"):
            raw_repeat = str(repeat_if_due_date_is_on_holiday).strip().lower()
            if raw_repeat == "yes":
                repeat_flag = True
                print("🔄 Repeat if due date is on holiday: Yes")
            elif raw_repeat == "no":
                repeat_flag = False
                print("🔄 Repeat if due date is on holiday: No")
            else:
                repeat_flag = None
                print(f"⚠️ repeat_if_due_date_is_on_holiday is invalid or empty; treated as None")

        # Step 3: Load locators
        with allure.step("Load locators for daily frequency"):
            try:
                print("📁 Loading locators for daily frequency...")
                with open(os.path.join("data", "locators.json"), "r") as f:
                    elements_details = json.load(f)
                daily_freq_yes_option = elements_details["daily_freq_yes_option"]
                daily_freq_no_option = elements_details["daily_freq_no_option"]
                end_frequency_date_input = elements_details["end_frequency_date_input"]
                freq_save_btn = elements_details["freq_save_btn"]
                freq_cancel_btn = elements_details["freq_cancel_btn"]
                print("✅ Locators loaded successfully.")
            except Exception as e:
                msg = f"❌ Error loading locators: {e}"
                print(msg)
                allure.attach(msg, name="Locators Error", attachment_type=allure.attachment_type.TEXT)
                pytest.fail(msg)

        # Step 4: Find and click the matching frequency option
        with allure.step("Select frequency option from dropdown"):
            print(f"🔎 Looking for the frequency option: {frequency}")
            found_option = None
            for option in option_elements:
                opt_text = option.text.strip()
                print(f"   ➡️ Checking option: {opt_text}")
                if opt_text.lower() == frequency.lower():   # case-insensitive match
                    found_option = option
                    break

            if not found_option:
                msg = f"❌ Frequency option '{frequency}' not found in dropdown list."
                print(msg)
                allure.attach(msg, name="Frequency Option Not Found", attachment_type=allure.attachment_type.TEXT)
                return False

            # Click the found option
            print(f"✅ Found matching option: {frequency}. Clicking...")
            highlight_element(driver, found_option)
            found_option.click()
            time.sleep(0.5)

            # If 'Only Once', skip further configuration
            if frequency.lower() == "only once":
                print("ℹ️ Frequency set to 'Only Once' — no further configuration needed.")
                return True

        # Step 5: Choose Yes/No radio for repeat-on-holiday
        with allure.step("Choose repeat-on-holiday option"):
            selected = False
            if repeat_flag is True:
                try:
                    elem = wait.until(EC.presence_of_element_located((By.XPATH, daily_freq_yes_option)))
                    highlight_element(driver, elem)
                    elem.click()
                    print("✅ Selected 'Yes' for repeat on holiday.")
                    selected = True
                except Exception as e:
                    msg = f"❌ Failed to select 'Yes' option: {e}"
                    print(msg)
                    allure.attach(msg, name="Select Yes Error", attachment_type=allure.attachment_type.TEXT)
                    return False

            elif repeat_flag is False:
                try:
                    elem = wait.until(EC.presence_of_element_located((By.XPATH, daily_freq_no_option)))
                    highlight_element(driver, elem)
                    elem.click()
                    print("✅ Selected 'No' for repeat on holiday.")
                    selected = True
                except Exception as e:
                    msg = f"❌ Failed to select 'No' option: {e}"
                    print(msg)
                    allure.attach(msg, name="Select No Error", attachment_type=allure.attachment_type.TEXT)
                    return False
            else:
                print("⚠️ No valid repeat-on-holiday option selected (value is None or invalid).")

        # Step 6: Set end frequency date if applicable
        with allure.step("Set end frequency date (if provided)"):
            if selected and repeat_flag is True and end_frequency_date:
                try:
                    date_elem = wait.until(EC.presence_of_element_located((By.XPATH, end_frequency_date_input)))
                    highlight_element(driver, date_elem)
                    date_elem.click()
                    time.sleep(0.5)
                    date_elem.clear()
                    date_elem.send_keys(end_frequency_date)
                    pg.press("tab")
                    print(f"📅 End frequency date set: {end_frequency_date}")
                except Exception as e:
                    msg = f"❌ Failed to set end frequency date '{end_frequency_date}': {e}"
                    print(msg)
                    allure.attach(msg, name="End Date Set Error", attachment_type=allure.attachment_type.TEXT)
                    return False
            else:
                print("ℹ️ End frequency date not applicable or not provided.")

        # Step 7: Click Save or Cancel
        with allure.step("Save or Cancel frequency selection"):
            try:
                if selected:
                    save_btn = wait.until(EC.presence_of_element_located((By.XPATH, freq_save_btn)))
                    highlight_element(driver, save_btn)
                    save_btn.click()
                    print("💾 Clicked Save. Frequency set successfully.")
                else:
                    cancel_btn = wait.until(EC.presence_of_element_located((By.XPATH, freq_cancel_btn)))
                    highlight_element(driver, cancel_btn)
                    cancel_btn.click()
                    print("💾 Clicked Cancel. Frequency cancelled.")
            except Exception as e:
                msg = f"❌ Error clicking Save/Cancel button: {e}"
                print(msg)
                allure.attach(msg, name="SaveCancel Error", attachment_type=allure.attachment_type.TEXT)
                return False

        # Step 8: Validate the final selected frequency
        with allure.step("Validate selected frequency in UI"):
            try:
                freq_elem = wait.until(EC.presence_of_element_located((By.XPATH, frequency_value_check)))
                selected_frequency = (freq_elem.text or "").strip()
                print(f"📌 Selected frequency read from UI: '{selected_frequency}'")
                if selected_frequency.lower() == frequency.lower():
                    task_value_store("frequency", frequency)
                    print(f"✅ Frequency validation successful: '{selected_frequency}' == '{frequency}'")
                    return True
                else:
                    msg = f"❌ Frequency validation failed: UI shows '{selected_frequency}', expected '{frequency}'"
                    print(msg)
                    allure.attach(msg, name="Frequency Validation Error", attachment_type=allure.attachment_type.TEXT)
                    return False
            except Exception as e:
                msg = f"❌ Error validating selected frequency: {e}"
                print(msg)
                allure.attach(msg, name="Validation Error", attachment_type=allure.attachment_type.TEXT)
                return False

    except Exception as e:
        err_msg = f"🔥 Unexpected error in daily_frequency: {e}"
        print(err_msg)
        allure.attach(err_msg, name="Unexpected Error", attachment_type=allure.attachment_type.TEXT)
        pytest.fail(err_msg)
        return False
