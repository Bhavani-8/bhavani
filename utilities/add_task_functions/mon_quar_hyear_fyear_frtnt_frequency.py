# from utilities.add_task_functions.normalize_day_and_month import normalize_day_and_month
# import allure
# from utilities.add_task_functions.normalize_date import normalize_date
# import os
# import json
# import pytest
# import pyautogui as pg
# from utilities.other_utils_functions.highlight import highlight_element
# import time
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.by import By
# from utilities.add_task_functions.add_task_common import task_value_store


# def mon_quar_hyear_fyear_frtnt_frequency(driver, frequency, repeat_day_and_month, repeat_if_due_date_is_on_holiday, end_frequency_date, option_elements, frequency_value_check, wait):
#     try:
            
#         print(f"Setting frequency: {frequency}")

#         # Step 1: Normalize day and month
#         with allure.step("Normalizing repeat day and month..."):
#             repeat_day, repeat_month = None, None
#             try:
#                 if repeat_day_and_month and repeat_day_and_month.strip() != '':
#                     repeat_day, repeat_month = normalize_day_and_month(repeat_day_and_month)
#                     if repeat_day is None or repeat_month is None:
#                         print("❌ Invalid repeat day/month format.")
#                     else:
#                         print(f"✅ Repeat day and month: {repeat_day} {repeat_month}")
#                 else:
#                     print("❌ No repeat day and month specified.")
#             except ValueError:
#                 print("❌ ValueError during day/month normalization")

#         # Step 2: Process repeat_if_due_date_is_on_holiday
#         with allure.step("Processing repeat_if_due_date_is_on_holiday..."):
#             repeat_if_due_date_is_on_holiday = str(repeat_if_due_date_is_on_holiday).strip()
#             mapping = {'before': 'Before', 'after': 'After', 'yes': 'Yes'}
#             repeat_if_due_date_is_on_holiday = mapping.get(repeat_if_due_date_is_on_holiday.lower(), None)
#             if repeat_if_due_date_is_on_holiday:
#                 print(f"✅ Repetition value: {repeat_if_due_date_is_on_holiday}")
#             else:
#                 msg = "Invalid repeat_if_due_date_is_on_holiday value or empty string"
#                 print(f"❌ {msg}")
#                 allure.attach(msg, name="Input Error", attachment_type=allure.attachment_type.TEXT)

#         # Step 3: Normalize end frequency date
#         with allure.step("Normalizing end frequency date..."):
#             end_frequency_date = str(end_frequency_date)
#             try:
#                 if end_frequency_date.strip():
#                     end_frequency_date = normalize_date(end_frequency_date)
#                     print(f"✅ Normalized end frequency date: {end_frequency_date}")
#                 else:
#                     end_frequency_date = None
#                     print("❌ End frequency date empty or invalid")
#             except ValueError:
#                 end_frequency_date = None
#                 print("❌ ValueError: end_frequency_date set to None")

#         # Step 4: Load locators
#         with allure.step("Loading locators..."):
#             try:
#                 with open(os.path.join("data", 'locators.json'), 'r') as f:
#                     elements_details = json.load(f)
#                     freq_repeat_day_input = elements_details['freq_repeat_day_input']
#                     freq_repeat_month_input = elements_details['freq_repeat_month_input']
#                     freq_repeat_month_selection = elements_details['freq_repeat_month_selection']
#                     freq_after_option = elements_details['freq_after_option']
#                     freq_before_option = elements_details['freq_before_option']
#                     freq_yes_option = elements_details['freq_yes_option']
#                     end_frequency_date_input = elements_details['end_frequency_date_input']
#                     freq_save_btn = elements_details['freq_save_btn']
#                     freq_cancel_btn = elements_details['freq_cancel_btn']
#                 print("✅ Locators loaded successfully.")
#             except (FileNotFoundError, json.JSONDecodeError) as e:
#                 print(f"❌ Error loading locators: {e}")
#                 pytest.fail(f"Locators loading failed: {e}")

#         # Step 5: Select frequency option
#         with allure.step(f"Selecting frequency '{frequency}' from dropdown..."):
#             matched_option = None
#             for option in option_elements:
#                 if option.text.strip() == frequency:
#                     matched_option = option
#                     break

#             if not matched_option:
#                 msg = f"No matching frequency option found: {frequency}"
#                 print(f"❌ {msg}")
#                 allure.attach(msg, name="Error", attachment_type=allure.attachment_type.TEXT)
#                 pytest.fail(msg)
#                 return False

#             highlight_element(driver, matched_option)
#             matched_option.click()
#             print(f"✅ Clicked frequency option: {frequency}")

#         # Step 6: Select day if applicable
#         with allure.step("Selecting repeat day..."):
#             day_selection = False
#             day_input = wait.until(EC.presence_of_element_located((By.XPATH, freq_repeat_day_input)))
#             highlight_element(driver, day_input)
#             if repeat_day:
#                 day_input.clear()
#                 day_input.send_keys(repeat_day)
#                 time.sleep(0.5)
#                 msg = f"Repeat day selected: {repeat_day}"
#                 print(f"✅ {msg}")
#                 allure.attach(msg, name="Repeat Day Selection", attachment_type=allure.attachment_type.TEXT)
#                 day_selection = True
#             else:
#                 msg = f"No repeat day selected"
#                 print(f"❌ {msg}")
#                 allure.attach(msg, name="Repeat Day Selection", attachment_type=allure.attachment_type.TEXT)

#         # Step 7: Select month if applicable
#         with allure.step("Selecting repeat month..."):
#             month_selection = False
#             month_input = wait.until(EC.presence_of_element_located((By.XPATH, freq_repeat_month_input)))
#             highlight_element(driver, month_input)
#             if repeat_month:
#                 month_input.click()
#                 month_xpath = freq_repeat_month_selection.replace('month', repeat_month)
#                 repeat_month_selection_elem = wait.until(EC.presence_of_element_located((By.XPATH, month_xpath)))
#                 repeat_month_selection_elem.click()
#                 time.sleep(0.5)
#                 msg = f"Repeat month selected: {repeat_month}"
#                 print(f"✅ {msg}")
#                 allure.attach(msg, name="Repeat Month Selection", attachment_type=allure.attachment_type.TEXT)
#                 month_selection = True
#             else:
#                 msg = "No repeat month selected"
#                 print(f"❌ {msg}")
#                 allure.attach(msg, name="Repeat Month Selection", attachment_type=allure.attachment_type.TEXT)

#         # Step 8: Select holiday repetition option if applicable
#         with allure.step("Selecting repeat if due date is on holiday..."):
#             holiday_selection = False
#             if repeat_if_due_date_is_on_holiday:
#                 repeat_mapping = {'Before': freq_before_option, 'After': freq_after_option, 'Yes': freq_yes_option}
#                 repeat_xpath = repeat_mapping.get(repeat_if_due_date_is_on_holiday)
#                 if repeat_xpath:
#                     repeat_elem = wait.until(EC.presence_of_element_located((By.XPATH, repeat_xpath)))
#                     highlight_element(driver, repeat_elem)
#                     repeat_elem.click()
#                     msg = f"Selected '{repeat_if_due_date_is_on_holiday}' option"
#                     print(f"✅ {msg}")
#                     allure.attach(msg, name="Repitition Value If Due Date Is On Holiday", attachment_type=allure.attachment_type.TEXT)
#                     holiday_selection = True

#         # Step 9: Set end frequency date
#         with allure.step("Setting end frequency date if applicable..."):
#             if end_frequency_date:
#                 select_date_elem = wait.until(EC.presence_of_element_located((By.XPATH, end_frequency_date_input)))
#                 select_date_elem.click()
#                 time.sleep(1)
#                 select_date_elem.send_keys(end_frequency_date)
#                 pg.press('tab')
#                 msg = f"End frequency date set: {end_frequency_date}"
#                 print(f"✅ {msg}")
#                 allure.attach(msg, name="End Frequency Date Selection", attachment_type=allure.attachment_type.TEXT)

#         # Step 10: Save or cancel based on selections
#         with allure.step("Saving or cancelling frequency selection..."):
#             if day_selection and month_selection and holiday_selection:
#                 save_button = wait.until(EC.presence_of_element_located((By.XPATH, freq_save_btn)))
#                 highlight_element(driver, save_button)
#                 save_button.click()
#                 msg = "Frequency set successfully"
#                 print(f"💾 ✅ {msg}")
#                 allure.attach(msg, name="Frequency Set & Saved Successfully", attachment_type=allure.attachment_type.TEXT)
#             else:
#                 cancel_button = wait.until(EC.presence_of_element_located((By.XPATH, freq_cancel_btn)))
#                 highlight_element(driver, cancel_button)
#                 cancel_button.click()
#                 msg = "Frequency selection cancelled"
#                 print(f"💾 ❌ {msg}")
#                 allure.attach(msg, name="Frequency Not Set: Cancelled Successfully", attachment_type=allure.attachment_type.TEXT)

#         # Step 11: Validate final frequency
#         with allure.step("Validating final frequency selection..."):
#             frequency_elem = wait.until(EC.presence_of_element_located((By.XPATH, frequency_value_check)))
#             selected_frequency = frequency_elem.text
#             if selected_frequency.lower() == frequency.lower():
#                 task_value_store("frequency", frequency)
#                 print(f"✅ Frequency validation successful: {selected_frequency}")
#                 return True
#             else:
#                 msg = f"Frequency validation failed: {selected_frequency} != {frequency}"
#                 print(f"❌ {msg}")
#                 allure.attach(msg, name="Frequency Validation Error", attachment_type=allure.attachment_type.TEXT)
#                 return False

#     except Exception as e:
#         msg = f"🔥 Error setting frequency '{frequency}': {e}"
#         print(msg)
#         allure.attach(str(e), name="Exception", attachment_type=allure.attachment_type.TEXT)
#         pytest.fail(msg)
#         return False


from utilities.add_task_functions.normalize_day_and_month import normalize_day_and_month
import allure
from utilities.add_task_functions.normalize_date import normalize_date
import os
import json
import pytest
import pyautogui as pg
from utilities.other_utils_functions.highlight import highlight_element
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from utilities.add_task_functions.add_task_common import task_value_store


def mon_quar_hyear_fyear_frtnt_frequency(
        driver, frequency, repeat_day_and_month,
        repeat_if_due_date_is_on_holiday,
        end_frequency_date,
        option_elements, frequency_value_check, wait):

    try:
        print(f"Setting frequency: {frequency}")

        # ✅ -------------------------------
        # 🔥 STEP 0: CLEAN ALL INPUTS
        # -------------------------------
        def clean(val):
            if val is None:
                return ""
            val = str(val).strip()
            if val.lower() in ["nan", "none", "0.0", ""]:
                return ""
            return val

        repeat_day_and_month = clean(repeat_day_and_month)
        repeat_if_due_date_is_on_holiday = clean(repeat_if_due_date_is_on_holiday)
        end_frequency_date = clean(end_frequency_date)

        print(f"DEBUG → repeat_day_and_month: {repeat_day_and_month}")
        print(f"DEBUG → repeat_if_due_date_is_on_holiday: {repeat_if_due_date_is_on_holiday}")
        print(f"DEBUG → end_frequency_date: {end_frequency_date}")

        # -------------------------------
        # STEP 1: Normalize day & month
        # -------------------------------
        with allure.step("Normalizing repeat day and month..."):
            repeat_day, repeat_month = None, None

            if repeat_day_and_month:
                # ✅ HANDLE numeric input like 1 / 1.0
                if repeat_day_and_month.replace(".", "", 1).isdigit():
                    repeat_day = str(int(float(repeat_day_and_month)))
                    repeat_month = None
                    print(f"✅ Numeric repeat day detected: {repeat_day}")

                else:
                    repeat_day, repeat_month = normalize_day_and_month(repeat_day_and_month)

                    if repeat_day is None or repeat_month is None:
                        print("❌ Invalid repeat day/month format.")
                    else:
                        print(f"✅ Repeat day and month: {repeat_day} {repeat_month}")
            else:
                print("⚠️ No repeat day and month specified.")

        # -------------------------------
        # STEP 2: Holiday logic
        # -------------------------------
        with allure.step("Processing repeat_if_due_date_is_on_holiday..."):
            mapping = {'before': 'Before', 'after': 'After', 'yes': 'Yes'}

            repeat_if_due_date_is_on_holiday = mapping.get(
                repeat_if_due_date_is_on_holiday.lower(), None
            )

            if repeat_if_due_date_is_on_holiday:
                print(f"✅ Repetition value: {repeat_if_due_date_is_on_holiday}")
            else:
                print("⚠️ No valid holiday repetition provided")

        # -------------------------------
        # STEP 3: Normalize end date
        # -------------------------------
        with allure.step("Normalizing end frequency date..."):
            if end_frequency_date:
                try:
                    end_frequency_date = normalize_date(end_frequency_date)
                    print(f"✅ Normalized end frequency date: {end_frequency_date}")
                except Exception:
                    end_frequency_date = None
                    print("❌ Invalid end frequency date")
            else:
                end_frequency_date = None

        # -------------------------------
        # STEP 4: Load locators
        # -------------------------------
        with allure.step("Loading locators..."):
            with open(os.path.join("data", 'locators.json'), 'r') as f:
                elements = json.load(f)

            freq_repeat_day_input = elements['freq_repeat_day_input']
            freq_repeat_month_input = elements['freq_repeat_month_input']
            freq_repeat_month_selection = elements['freq_repeat_month_selection']
            freq_after_option = elements['freq_after_option']
            freq_before_option = elements['freq_before_option']
            freq_yes_option = elements['freq_yes_option']
            end_frequency_date_input = elements['end_frequency_date_input']
            freq_save_btn = elements['freq_save_btn']
            freq_cancel_btn = elements['freq_cancel_btn']
            desc_save_btn = elements['desc_save_btn']

            print("✅ Locators loaded successfully.")

        # -------------------------------
        # STEP 5: Select frequency
        # -------------------------------
        with allure.step(f"Selecting frequency '{frequency}'"):
            matched_option = None
            for option in option_elements:
                if option.text.strip().lower() == frequency.lower():
                    matched_option = option
                    break

            if not matched_option:
                pytest.fail(f"❌ Frequency not found: {frequency}")

            highlight_element(driver, matched_option)
            matched_option.click()
            print(f"✅ Clicked frequency option: {frequency}")

        # -------------------------------
        # STEP 6: Select day
        # -------------------------------
        with allure.step("Selecting repeat day..."):
            day_selection = False
            day_input = wait.until(EC.presence_of_element_located((By.XPATH, freq_repeat_day_input)))

            if repeat_day:
                highlight_element(driver, day_input)
                day_input.clear()
                day_input.send_keys(repeat_day)
                day_selection = True
                print(f"✅ Repeat day selected: {repeat_day}")
            else:
                print("⚠️ No repeat day selected")

        # -------------------------------
        # STEP 7: Select month
        # -------------------------------
        with allure.step("Selecting repeat month..."):
            month_selection = False
            if repeat_month:
                month_input = wait.until(EC.presence_of_element_located((By.XPATH, freq_repeat_month_input)))
                highlight_element(driver, month_input)
                month_input.click()

                month_xpath = freq_repeat_month_selection.replace('month', repeat_month)
                month_elem = wait.until(EC.presence_of_element_located((By.XPATH, month_xpath)))
                month_elem.click()

                month_selection = True
                print(f"✅ Repeat month selected: {repeat_month}")
            else:
                print("⚠️ No repeat month selected")

        # -------------------------------
        # STEP 8: Holiday selection
        # -------------------------------
        with allure.step("Selecting holiday option..."):
            holiday_selection = False

            mapping = {
                'Before': freq_before_option,
                'After': freq_after_option,
                'Yes': freq_yes_option
            }

            if repeat_if_due_date_is_on_holiday:
                xpath = mapping.get(repeat_if_due_date_is_on_holiday)
                if xpath:
                    elem = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
                    highlight_element(driver, elem)
                    elem.click()
                    holiday_selection = True
                    print(f"✅ Selected holiday option: {repeat_if_due_date_is_on_holiday}")

        # -------------------------------
        # STEP 9: End date
        # -------------------------------
        with allure.step("Setting end frequency date..."):
            if end_frequency_date:
                date_elem = wait.until(EC.presence_of_element_located((By.XPATH, end_frequency_date_input)))
                date_elem.click()
                date_elem.send_keys(end_frequency_date)
                pg.press('tab')
                print(f"✅ End date set: {end_frequency_date}")

        # -------------------------------
        # STEP 10: SAVE (FIXED)
        # -------------------------------
        # with allure.step("Saving frequency"):
        #     if any([day_selection, month_selection, holiday_selection]):
        #         save_btn = wait.until(EC.presence_of_element_located((By.XPATH, freq_save_btn)))
        #         highlight_element(driver, save_btn)
        #         save_btn.click()
        #         print("💾 ✅ Frequency saved")
        #     else:
        #         cancel_btn = wait.until(EC.presence_of_element_located((By.XPATH, freq_cancel_btn)))
        #         cancel_btn.click()
        #         print("💾 ❌ Frequency cancelled")
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

        # -------------------------------
        # STEP 11: VALIDATION (FIXED)
        # -------------------------------
        with allure.step("Validating frequency"):
            freq_elem = wait.until(EC.presence_of_element_located((By.XPATH, frequency_value_check)))
            highlight_element(driver, freq_elem)

            actual = freq_elem.text.strip()

            def normalize(text):
                return text.lower().replace("-", "").replace(" ", "")

            print(f"Comparing actual='{actual}' with expected='{frequency}'")

            if normalize(actual) == normalize(frequency):
                task_value_store("frequency", actual)
                print("✅ Frequency validation successful")
                return True
            else:
                print(f"❌ Mismatch: {actual} != {frequency}")
                return False

    except Exception as e:
        print(f"🔥 Error setting frequency '{frequency}': {e}")
        allure.attach(str(e), name="Exception", attachment_type=allure.attachment_type.TEXT)
        return False