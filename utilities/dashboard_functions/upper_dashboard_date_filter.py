import allure
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import allure
import time
import json 
from datetime import datetime, timedelta

from utilities.add_task_utils import wait_for_loader_to_disappear
import os
import pyautogui as pg  
from utilities.other_utils_functions.highlight import highlight_element


def get_outer_element(current_elem, levels_up=1):
    outer_elem = current_elem
    for _ in range(levels_up):
        outer_elem = outer_elem.find_element(By.XPATH, "./..")  # go to parent
    return outer_elem


def safe_click(driver, wait, xpath, description):
    """Wait for element, scroll, and click safely with loader handling."""
    with allure.step(f"Clicking on {description}"):
        try:
            elem = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
            driver.execute_script("arguments[0].scrollIntoView(true);", elem)
            try:
                elem.click()
            except Exception:
                driver.execute_script("arguments[0].click();", elem)  # fallback
            wait_for_loader_to_disappear(driver, wait)
            print(f"✅ {description} clicked successfully")
            return elem
        except Exception as e:
            allure.attach(str(e), name=f"{description} - Click Error",
                          attachment_type=allure.attachment_type.TEXT)
            print(f"❌ Failed to click {description}: {str(e)}")
            raise

def wait_for_loader_to_disappear(driver, wait):
    try:
        wait.until(
            EC.invisibility_of_element_located(
                (By.XPATH, "//div[contains(@class,'dx-loadpanel-wrapper')]")
            )
        )
    except:
        pass

def upper_dashboard_date_filter(driver, wait):
    """Validate dashboard tiles and check sub-title counts using the same Select All logic."""

    # -------------------------------
    # Open dashboard date filter & calendar
    # -------------------------------
    with allure.step("Open Dashboard Date Filter"):
        try:
            filter_btn = wait.until(EC.presence_of_element_located((By.XPATH, "//span[contains(@class,'ant-badge')]//button[@type='button']")))
            highlight_element(driver, filter_btn)
            filter_btn.click()
            print("✅ Filter button clicked")
        except Exception as e:
            print(f"❌ Filter button not clickable: {e}")
            return False

    with allure.step("Open Calendar Popup"):
        try:
            calendar_btn_elem = wait.until(EC.presence_of_element_located((By.XPATH, "//span[@role='img' and @aria-label='calendar']")))
            highlight_element(driver, calendar_btn_elem)
            driver.execute_script("arguments[0].click();", calendar_btn_elem)
            print("✅ Calendar icon clicked")
        except Exception as e:
            print(f"❌ Failed to open calendar: {e}")
            return False

    with allure.step("Select Start and End Dates"):
        try:
            today = datetime.today()
            start_date = today - timedelta(days=7)
            end_date = today + timedelta(days=7)

            start_date_str = start_date.strftime("%d %b %Y")
            end_date_str = end_date.strftime("%d %b %Y")

            pg.typewrite(start_date_str)
            pg.press('tab')
            time.sleep(1)
            pg.typewrite(end_date_str)
            pg.press('enter')
            time.sleep(1)

            print(f"📅 Selected Start: {start_date_str}")
            print(f"📅 Selected End  : {end_date_str}")

        except Exception as e:
            print(f"❌ Calendar interaction failed: {e}")

    with allure.step("Apply Date Range"):
        try:
            apply_btn = wait.until(EC.presence_of_element_located((By.XPATH, "//button[normalize-space()='Apply']")))
            driver.execute_script("arguments[0].scrollIntoView();", apply_btn)
            highlight_element(driver, apply_btn)
            apply_btn.click()
            print("✅ Date range applied")
            time.sleep(3)
        except Exception:
            print("⚠️ Apply button not found — skipping")



    # =====================================================
    # 🔹 LOAD LOCATORS
    # =====================================================
    with allure.step("Loading locators from JSON"):
        with open(os.path.join("data", "locators.json"), "r") as f:
            elements_details = json.load(f)
        print("✅ Locators loaded successfully")

    # =====================================================
    # 🔹 LOCATORS
    # =====================================================
    dashboard_icon = elements_details["dashboard_icon"]
    special_task_icon = elements_details["special_task_icon"]

    dash_buttons = {
        "Overdue": elements_details["dash_overdue_btn"],
        "Today": elements_details["dash_today_btn"],
        "Next 6 Day": elements_details["dash_6_days_btn"],
        "Next 8-30 Day": elements_details["dash_8_to_30_days_btn"],
        "Beyond 30 Day": elements_details["dash_beyond_30_days_btn"],
        "Total": elements_details["dash_total_btn"]
    }

    dash_value_selector_template = elements_details["dash_value_selector_template"]
    dash_value_validator_template = elements_details["dash_value_validator_template"]
    dash_sum_value_selector = elements_details["dash_sum_value_selector"]
    dash_select_all_checkbox = elements_details["dash_select_all_checkbox"]

    titles = ["Assigned To Me", "Assigned To Others", "Not Assigned", "CC"]

    for idx, (btn_name, btn_path) in enumerate(dash_buttons.items()):
        actual_value = 0
        expected_value = 0
        selected_count = None


        safe_click(driver, wait, btn_path, f"{btn_name} Button")
        wait_for_loader_to_disappear(driver, wait)

        for title in titles:
            
            try:
                # --- Get the value element
                dash_value_selector = dash_value_selector_template.replace("{title}", title)
                dash_value_elements = wait.until(EC.presence_of_all_elements_located((By.XPATH, dash_value_selector)))

                if len(dash_value_elements) <= idx:
                    continue

                value_elem = dash_value_elements[idx]
                actual_value = int(value_elem.text.replace(",", "").strip() or 0)
                highlight_element(driver, value_elem, duration=0.3) 
                with allure.step(f"Validating '{title}' in '{btn_name}' "f"(Dashboard Count: {actual_value})"):
                    # --- Get the validator element for expected value
                    dash_value_validator = dash_value_validator_template.replace("{title}", title)
                    validator_elem = wait.until(EC.presence_of_element_located((By.XPATH, dash_value_validator)))
                    expected_value = int(validator_elem.text.replace(",", "").strip() or 0)
                    highlight_element(driver, validator_elem, duration=0.2)  # Header
                         # Actual value

                    # --- Activate the grid
                    driver.execute_script("arguments[0].click();", validator_elem)
                    time.sleep(3)
                    # highlight_element(driver, validator_elem, duration=0.2)
                    wait_for_loader_to_disappear(driver, wait)

                    if actual_value == 0 and expected_value == 0:
                        success_msg = (
                            f"✅ {btn_name} - {title} - "
                            f"Dashboard Count : {actual_value}, "
                            f"Header Count : {expected_value}, "
                            f"Select All Count : No Tasks"
                        )
                        print(success_msg)
                        allure.attach(
                            success_msg,
                            name=f"{btn_name}-{title}-Matched",
                            attachment_type=allure.attachment_type.TEXT
                        )
                        continue

                    # If dashboard and header counts differ, fail immediately
                    if actual_value != expected_value:
                        error_msg = (
                            f"❌ {btn_name} - {title} Count Mismatch\n"
                            f"Dashboard Count : {actual_value}\n"
                            f"Header Count    : {expected_value}"
                        )
                        print(error_msg)
                        allure.attach(
                        error_msg,
                        name=f"{btn_name}-{title}-Mismatch",
                        attachment_type=allure.attachment_type.TEXT
                    )
                        raise AssertionError(error_msg)
                    # --- Click Select All
                    select_all_elem = wait.until(EC.presence_of_element_located((By.XPATH, dash_select_all_checkbox)))
                    driver.execute_script("arguments[0].click();", select_all_elem)
                    time.sleep(2)
                    wait_for_loader_to_disappear(driver, wait)

                    selected_count_elem = wait.until(EC.presence_of_element_located((By.XPATH, '//div[contains(text(),"selected")]')))
                    highlight_element(driver, selected_count_elem, duration=0.2)

                    selected_text = selected_count_elem.text.strip()
                    selected_count = int(selected_text.replace(",", "").split()[0])

                    # Validate Dashboard, Header and Select All counts
                    if actual_value == expected_value == selected_count:

                        success_msg = (
                            f"✅ {btn_name} - {title} - MATCHED\n\n"
                            f"Dashboard Count : {actual_value}\n"
                            f"Header Count    : {expected_value}\n"
                            f"Select All Count: {selected_count}"
                        )

                        print(success_msg)

                        allure.attach(
                            success_msg,
                            name=f"{btn_name}-{title}-Matched",
                            attachment_type=allure.attachment_type.TEXT
                        )

                    else:
                        error_msg = (
                            f"❌ {btn_name} - {title} Count Mismatch\n"
                            f"Dashboard Count : {actual_value}\n"
                            f"Header Count    : {expected_value}\n"
                            f"Select All Count: {selected_count}"
                        )
                        print(error_msg)
                        allure.attach(
                            error_msg,
                            name=f"{btn_name}-{title}-Mismatch",
                            attachment_type=allure.attachment_type.TEXT
                        )
                        raise AssertionError(error_msg)
            except Exception as e:
                print(f"❌ {btn_name} - {title} validation failed: {e}")
                allure.attach(str(e), f"{btn_name}-{title} Error", allure.attachment_type.TEXT)
                raise

       
        try:
            sum_elements = wait.until(EC.presence_of_all_elements_located((By.XPATH, dash_sum_value_selector)))

            if len(sum_elements) <= idx:
                print(f"ℹ️ {btn_name} - Total value not available")
                continue

            sum_elem = sum_elements[idx]
            actual_sum = int(sum_elem.text.replace(",", "").strip() or 0)
            with allure.step(f"Validating Total in '{btn_name}'"):
                sum_elem.click()
                wait_for_loader_to_disappear(driver, wait)
                highlight_element(driver, sum_elem, duration=0.3)
                dash_sum_validator = dash_value_validator_template.replace("{title}", "All")
                total_validator_elem = wait.until(EC.presence_of_element_located((By.XPATH, dash_sum_validator)))
                highlight_element(driver, total_validator_elem)
                expected_sum = int(total_validator_elem.text.replace(",", "").strip() or 0)

                # Click validator to activate grid
                driver.execute_script("arguments[0].click();", total_validator_elem)
                wait_for_loader_to_disappear(driver, wait)
                # Click Select All

                if actual_sum == 0 and expected_sum == 0:
                    print(
                        f"✅ {btn_name} - Total - "
                        f"Dashboard count : {actual_sum}, "
                        f"Header Count : {expected_sum}, "
                        f"Select All Count : No Tasks"

                    )
                    allure.attach(
                        success_msg,
                        name=f"{btn_name}-Total-Matched",
                        attachment_type=allure.attachment_type.TEXT
                    )
                    continue

                # Dashboard and Header mismatch
                if actual_sum != expected_sum:
                    error_msg = (
                        f"❌ {btn_name} - Total Count Mismatch\n"
                        f"Dashboard Count : {actual_sum}\n"
                        f"Header Count : {expected_sum}"
                    )
                    print(error_msg)
                    allure.attach(
                        error_msg,
                        name=f"{btn_name}- Total -Mismatch",
                        attachment_type=allure.attachment_type.TEXT
                    )
                    raise AssertionError(error_msg)

                select_all_elem = wait.until(EC.presence_of_element_located((By.XPATH, dash_select_all_checkbox)))
                driver.execute_script("arguments[0].click();", select_all_elem)
                wait_for_loader_to_disappear(driver, wait)

                selected_count_elem = wait.until(
                        EC.presence_of_element_located(
                            (By.XPATH, '//div[contains(text(),"selected")]')
                        )
                    )
                highlight_element(driver, selected_count_elem, duration=0.2)

                selected_text = selected_count_elem.text.strip()
                selected_count = int(selected_text.replace(",", "").split()[0])

                    # Validate Dashboard, Header and Select All counts
                if actual_sum == expected_sum == selected_count:
                    success_msg = (
                        f"✅ {btn_name} - Total - MATCHED\n\n"
                         f"Dashboard Count : {actual_sum}, "
                        f"Header Count : {expected_sum}, "
                        f"Select All Count : {selected_count}"
                    )

                    print(success_msg)

                    allure.attach(
                        success_msg,
                        name=f"{btn_name}-Total-Matched",
                        attachment_type=allure.attachment_type.TEXT
                    )
                   
                else:
                    error_msg = (
                        f"❌ {btn_name} - Total Count Mismatch\n"
                        f"Dashboard Total : {actual_sum}\n"
                        f"Header Total    : {expected_sum}\n"
                        f"Select All Count: {selected_count}"
                    )
                    print(error_msg)
                    allure.attach(
                        error_msg,
                        name=f"{btn_name}-{title}-Mismatch",
                        attachment_type=allure.attachment_type.TEXT
                    )
                    raise AssertionError(error_msg)

        except Exception as e:
            print(f"❌ {btn_name} - Total validation failed: {e}")
            # allure.attach(str(e), f"{btn_name}-Total Error", allure.attachment_type.TEXT)
            raise

    return True
