import allure
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
import allure
import time
import json 
from datetime import datetime, timedelta

from utilities.add_task_utils import wait_for_loader_to_disappear
import os
import pyautogui as pg  
from utilities.other_utils_functions.highlight import highlight_element

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


def lower_dashboard_date_filter(driver, wait, dash_type='QCC'):
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
            time.sleep(4)
        except Exception:
            print("⚠️ Apply button not found — skipping")

    
    with open(os.path.join("data", 'locators.json'), 'r') as f:
        elements_details = json.load(f)
        special_task_icon = elements_details['special_task_icon']
        dash_approval_pending_btn = elements_details['dash_approval_pending_btn']
        dash_rejected_task_btn = elements_details['dash_rejected_task_btn']
        dash_completed_btn = elements_details['dash_completed_btn']
        dash_title_label = elements_details['dash_title_label']
        dash_others_value_selector_template = elements_details['dash_others_value_selector_template']
        dash_value_selector_template = elements_details['dash_value_selector_template']
        dash_value_validator_template = elements_details['dash_value_validator_template']
        dash_sum_value_selector = elements_details['dash_sum_value_selector']
        dash_select_all_checkbox = elements_details['dash_select_all_checkbox']
        dashboard_icon = elements_details["dashboard_icon"]
        special_task_icon = elements_details["special_task_icon"]

    dash_buttons_others = {
            'Approval Pending': dash_approval_pending_btn,
            'Rejected Tasks': dash_rejected_task_btn,
            'Completed': dash_completed_btn,
        }

    titles = [['Approval Pending by Me', 'Approval Pending by Others', 'CC', 'All'], ['Assigned To Me', 'Assigned To Others', 'CC', 'All'], ['Completed By Me', 'Completed By Others', 'CC', 'All']]
    if dash_type == "QCC":
        safe_click(driver, wait, dashboard_icon, "Dashboard Icon")
    else:
        safe_click(driver, wait, special_task_icon, "Special Task Dashboard Icon")

    wait_for_loader_to_disappear(driver, wait)
    for idx, (btn_name, btn_path) in enumerate(dash_buttons_others.items()):

        btn_elem = wait.until(EC.presence_of_element_located((By.XPATH, btn_path)))
        btn_elem.click()
        print()
        print(f"📊 {btn_name} button clicked.")
        wait_for_loader_to_disappear(driver, wait)

        # Fetch and print dashboard title
        dash_title_label_elem = wait.until(EC.presence_of_element_located((By.XPATH, dash_title_label)))
        title_text = dash_title_label_elem.text.strip()
        print(f"Button title fetched: {title_text}")

        dash_others_value_selector = dash_others_value_selector_template.replace('{title}', btn_name)
        dash_others_value_selector_elem = wait.until(EC.presence_of_all_elements_located((By.XPATH, dash_others_value_selector)))
        
        for i, (elem, title) in enumerate(zip(dash_others_value_selector_elem, titles[idx]), start=1):
            with allure.step(f"Validating '{title}' in '{btn_name}'"):
                try:

                    dash_value_validator = dash_value_validator_template.replace('{title}', title)
                    dash_value_validator_elem = wait.until(EC.presence_of_element_located((By.XPATH, dash_value_validator)))
                    
                    # value_elem = dash_value_validator_elem[idx]
                    actual_value = int(dash_value_validator_elem.text.replace(",", "").strip() or 0)
                    highlight_element(driver, dash_value_validator_elem, duration=0.2)

                    # --- Get the validator element for expected value
                    dash_value_validator = dash_value_validator_template.replace("{title}", title)
                    validator_elem = wait.until(EC.presence_of_element_located((By.XPATH, dash_value_validator)))
                    expected_value = int(validator_elem.text.replace(",", "").strip() or 0)
                    highlight_element(driver, elem, duration=0.2)
                    driver.execute_script("arguments[0].click();", validator_elem)
                    time.sleep(3)

                    wait_for_loader_to_disappear(driver, wait)

                    # ✅ FIX: Skip Select All if no data
                    if actual_value == 0:
                        print(f"✅ {btn_name} - {title} - No data found (0)")
                        continue

                    select_all_elem = wait.until(EC.presence_of_element_located((By.XPATH, dash_select_all_checkbox)))
                    driver.execute_script("arguments[0].click();", select_all_elem)
                    time.sleep(3)
                    wait_for_loader_to_disappear(driver, wait)

                    
                    # Output
                    if actual_value == expected_value:
                        print(f"✅ {btn_name} - {title} - Select all - matched ({actual_value})")
                    else:
                        print(f"❌ {btn_name} - {title} - Select all - mismatch (Actual: {actual_value}, Expected: {expected_value})")
                except Exception as e:
                    print(f"❌ {btn_name} - {title} validation failed: {e}")
                    allure.attach(str(e), f"{btn_name}-{title} Error", allure.attachment_type.TEXT)

        with allure.step(f"Validating Total in '{btn_name}'"):
            try:
                dash_sum_value_selector_elem = wait.until(EC.presence_of_all_elements_located((By.XPATH, dash_sum_value_selector)))

                lower_dashboard_sums = dash_sum_value_selector_elem[-3:]
                sum_value_test_elem = lower_dashboard_sums[idx]

                highlight_element(driver, sum_value_test_elem, duration=0.2)
                driver.execute_script("arguments[0].click();", sum_value_test_elem)

                time.sleep(3)
                wait_for_loader_to_disappear(driver, wait)

                actual_sum_value = int(sum_value_test_elem.text.strip())

                dash_sum_value_validator = dash_value_validator_template.replace('{title}', 'All')
                dash_value_validator_elem = wait.until(EC.presence_of_element_located((By.XPATH, dash_sum_value_validator)))
                highlight_element(driver, dash_value_validator_elem)
                
                expected_sum_value = int(dash_value_validator_elem.text.strip())
                
                if actual_value == 0:
                    print(f"✅ {btn_name} - Total - No data found (0)")
                    continue

                select_all_elem = wait.until(EC.presence_of_element_located((By.XPATH, dash_select_all_checkbox)))
                driver.execute_script("arguments[0].click();", select_all_elem)
                time.sleep(3)
                wait_for_loader_to_disappear(driver, wait)
                
                if actual_value == expected_value:
                    print(f"✅ {btn_name} - Total - Select all - matched ({actual_sum_value})")
                else:
                    print(f"❌ {btn_name} - Total - Select all - mismatch (Actual: {actual_value}, Expected: {expected_sum_value})")

            except Exception as e:
                    print(f"❌ {btn_name} - Total validation failed: {e}")
                    allure.attach(str(e), f"{btn_name}-Total Error", allure.attachment_type.TEXT)
    return True

       