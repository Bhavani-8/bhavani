import allure
from utilities.other_utils_functions.highlight import highlight_element
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
from utilities.add_task_functions.daily_frequency import daily_frequency
from utilities.add_task_functions.weekly_frequency import weekly_frequency
from utilities.add_task_functions.mon_quar_hyear_fyear_frtnt_frequency import mon_quar_hyear_fyear_frtnt_frequency
from utilities.add_task_functions.add_task_common import task_value_store


def set_frequency(driver, frequency_option, frequency, repeat_if_due_date_is_on_holiday,end_frequency_date, weekday_name, repeat_day_and_month,frequency_value_check, wait):
    frequency = frequency.capitalize()

    try:
        # Step 1: Open frequency dropdown
        # with allure.step("Opening frequency dropdown..."):
        # with allure.step("Open Frequency Dropdown"):
        #     try:
        #         frequency_option_elem = wait.until(EC.element_to_be_clickable((By.XPATH, frequency_option)))
        #         highlight_element(driver, frequency_option_elem)
        #         frequency_option_elem.click()
        #         print("✅ Frequency dropdown opened (primary locator).")

        #     except Exception:
        #         print("⚠️ Primary locator failed, trying fallback locator...")
        #         update_frequency_option_elem = wait.until(EC.element_to_be_clickable((By.XPATH, "(//div[@class='css-10g6km5-control'])[1]")))
        #         highlight_element(driver, update_frequency_option_elem)
        #         update_frequency_option_elem.click()
        #         print("✅ Frequency dropdown opened (fallback locator).")
        #     time.sleep(0.5)
        with allure.step("Open Frequency Dropdown"):
            try:
                frequency_option_elem = wait.until(EC.element_to_be_clickable((By.XPATH, frequency_option)))
                highlight_element(driver, frequency_option_elem)
                frequency_option_elem.click()
                time.sleep(2)
                print("✅ Frequency dropdown opened (primary locator).")

            except Exception:
                print("⚠️ Primary locator failed, trying first fallback...")

                try:
                    update_frequency_option_elem = wait.until(
                        EC.element_to_be_clickable((By.XPATH, "//div[contains(@class,'control') and .//div[contains(text(),'Frequency')]]"))
                    )
                    highlight_element(driver, update_frequency_option_elem)
                    update_frequency_option_elem.click()
                    time.sleep(2)
                    print("✅ Frequency dropdown opened (fallback locator 1).")

                except Exception:
                    print("⚠️ First fallback failed, trying second fallback...")

                    try:
                        update_frequency_option_elem = wait.until(
                            EC.element_to_be_clickable((By.XPATH, "//div[contains(@class,'control') and .//div[text()='Only once']]"))
                        )
                        highlight_element(driver, update_frequency_option_elem)
                        update_frequency_option_elem.click()
                        time.sleep(2)
                        print("✅ Frequency dropdown opened (fallback locator 2).")

                    except Exception as e:
                        print("⚠️ Fallback 2 failed, trying fallback 3..")
                    

                        try:
                            update_frequency_option_elem = wait.until(
                                EC.element_to_be_clickable((By.XPATH, "(//div[@class='css-10g6km5-control'])[3]"))
                            )
                            highlight_element(driver, update_frequency_option_elem)
                            update_frequency_option_elem.click()
                            time.sleep(2)
                            print("✅ Frequency dropdown opened (fallback locator 2).")

                        except Exception as e:
                            print("❌ All locators failed to open Frequency dropdown.")
                            raise e

            time.sleep(2)


        # Step 2: Fetch available options
        # with allure.step("Fetching available options..."):
        option_elements = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//div[contains(@class,'-option')]")))
        option_texts = [option.text for option in option_elements if option.text.strip()]
        print(f"Available options: {option_texts}")

        if not option_texts:
            msg = "❌ No dropdown options found."
            print(msg)
            allure.attach(msg, name="Frequency Failure", attachment_type=allure.attachment_type.TEXT)
            return False

        # Step 3: Validate frequency
        # with allure.step(f"Validating frequency '{frequency}'..."):
        if frequency not in option_texts:
            msg = f"❌ Frequency '{frequency}' not found in dropdown options: {option_texts}"
            print(msg)
            allure.attach(msg, name="Frequency Failure", attachment_type=allure.attachment_type.TEXT)
            return False
        print(f"✅ Frequency '{frequency}' is available.")

        # Step 4: Select frequency
        # with allure.step(f"Selecting frequency '{frequency}'..."):
        try:
            match frequency:
                case 'Daily' | 'Only once':
                    print(f"➡️ Calling daily_frequency for '{frequency}'.")
                    return daily_frequency(driver, frequency,repeat_if_due_date_is_on_holiday,end_frequency_date, option_elements,frequency_value_check, wait)

                case 'Weekly':
                    print(f"➡️ Calling weekly_frequency for '{frequency}'.")
                    return weekly_frequency(driver, frequency, weekday_name,repeat_if_due_date_is_on_holiday,end_frequency_date, option_elements,frequency_value_check, wait)
                case 'Monthly' | 'Quarterly' | 'Half-yearly' | 'Yearly' | 'Fortnightly':
                    print(f"➡️ Calling mon_quar_hyear_frtnt_frequency for '{frequency}'.")
                    return mon_quar_hyear_fyear_frtnt_frequency(
                        driver, frequency, repeat_day_and_month,
                        repeat_if_due_date_is_on_holiday, end_frequency_date,
                        option_elements, frequency_value_check, wait
                    )
        except Exception as e:
            msg = f"❌ Error while setting frequency '{frequency}': {str(e)}"
            print(msg)
            allure.attach(msg, name="Frequency Failure", attachment_type=allure.attachment_type.TEXT)
            return False

       # ✅ Step 5: Validate selected frequency (🔥 ADDED)
        # -------------------------------
        # ✅ Step 4: Validation (LIKE RISK)
        # -------------------------------
        try:
            frequency_value_elem = wait.until(EC.presence_of_element_located((By.XPATH, frequency_value_check)))

            highlight_element(driver, frequency_value_elem)

            actual = frequency_value_elem.text.strip()
            expected = frequency

            print(f"Comparing {actual} with {expected}")

            allure.attach(f"Validating '{actual}' with '{expected}' for field 'frequency'",name="Frequency Validation",attachment_type=allure.attachment_type.TEXT)

            if actual.lower() == expected.lower():
                print(f"✅ Match: {actual} == {expected}")
                task_value_store("frequency", actual)
                return True
            else:
                msg = f"❌ Mismatch: {actual} != {expected}"
                print(msg)
                allure.attach(f"Validating '{actual}' with '{expected}' for field 'frequency'",name="Frequency Validation",attachment_type=allure.attachment_type.TEXT)
                return False
        except Exception as e:
            msg = f"❌ Frequency validation failed: {e}"
            print(msg)
            allure.attach(msg, name="Validation Error", attachment_type=allure.attachment_type.TEXT)
            return False

    except Exception as e:
        msg = f"🔥 Error in set_frequency: {e}"
        print(msg)
        allure.attach(msg, name="Frequency Error", attachment_type=allure.attachment_type.TEXT)
        return False