from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import allure
import json
import os
import time

from utilities.add_task_utils import wait_for_loader_to_disappear
from utilities.other_utils_functions.highlight import highlight_element
from utilities.search_utils import clear_search


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
def upper_dashboard_validation(driver, wait):

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
        "Next 6 Days": elements_details["dash_6_days_btn"],
        "8 To 30 Days": elements_details["dash_8_to_30_days_btn"],
        "Beyond 30 Days": elements_details["dash_beyond_30_days_btn"],
        "Total": elements_details["dash_total_btn"]
    }

    dash_value_selector_template = elements_details["dash_value_selector_template"]
    dash_value_validator_template = elements_details["dash_value_validator_template"]
    dash_sum_value_selector = elements_details["dash_sum_value_selector"]
    dash_select_all_checkbox = elements_details["dash_select_all_checkbox"]

    titles = ["Assigned To Me", "Assigned To Others", "Not Assigned", "CC"]


    for idx, (btn_name, btn_path) in enumerate(dash_buttons.items()):

        safe_click(driver, wait, btn_path, f"{btn_name} Button")
        wait_for_loader_to_disappear(driver, wait)

        for title in titles:
            with allure.step(f"Validating '{title}' in '{btn_name}'"):
                try:
                    # --- Get the value element
                    dash_value_selector = dash_value_selector_template.replace("{title}", title)
                    dash_value_elements = wait.until(EC.presence_of_all_elements_located((By.XPATH, dash_value_selector)))

                    if len(dash_value_elements) <= idx:
                        continue

                    value_elem = dash_value_elements[idx]
                    actual_value = int(value_elem.text.replace(",", "").strip() or 0)

                    # --- Get the validator element for expected value
                    dash_value_validator = dash_value_validator_template.replace("{title}", title)
                    validator_elem = wait.until(EC.presence_of_element_located((By.XPATH, dash_value_validator)))
                    expected_value = int(validator_elem.text.replace(",", "").strip() or 0)
                    highlight_element(driver, validator_elem, duration=0.2)  # Header
                    highlight_element(driver, value_elem, duration=0.3)      # Actual value

                    # --- Activate the grid
                    driver.execute_script("arguments[0].click();", validator_elem)
                    time.sleep(3)
                    # highlight_element(driver, validator_elem, duration=0.2)
                    wait_for_loader_to_disappear(driver, wait)

                    
                    # --- Click Select All
                    select_all_elem = wait.until(EC.presence_of_element_located((By.XPATH, dash_select_all_checkbox)))
                    driver.execute_script("arguments[0].click();", select_all_elem)
                    time.sleep(2)
                    wait_for_loader_to_disappear(driver, wait)

                    # --- OUTPUT FORMAT (UNIFORM)
                    if actual_value == expected_value:
                        print(f"✅ {btn_name} - {title} - Select all - matched ({actual_value})")
                    else:
                        print(f"❌ {btn_name} - {title} - Select all - mismatch "
                              f"(Actual: {actual_value}, Expected: {expected_value})")

                except Exception as e:
                    print(f"❌ {btn_name} - {title} validation failed: {e}")
                    allure.attach(str(e), f"{btn_name}-{title} Error", allure.attachment_type.TEXT)

        with allure.step(f"Validating Total in '{btn_name}'"):
            try:
                sum_elements = wait.until(EC.presence_of_all_elements_located((By.XPATH, dash_sum_value_selector)))

                if len(sum_elements) <= idx:
                    print(f"ℹ️ {btn_name} - Total value not available")
                    continue

                sum_elem = sum_elements[idx]
                actual_sum = int(sum_elem.text.replace(",", "").strip() or 0)

                sum_elem.click()
                wait_for_loader_to_disappear(driver, wait)

                dash_sum_validator = dash_value_validator_template.replace("{title}", "All")
                total_validator_elem = wait.until(EC.presence_of_element_located((By.XPATH, dash_sum_validator)))
                highlight_element(driver, total_validator_elem)
                expected_sum = int(total_validator_elem.text.replace(",", "").strip() or 0)

                # Click validator to activate grid
                driver.execute_script("arguments[0].click();", total_validator_elem)
                wait_for_loader_to_disappear(driver, wait)
                # Click Select All
                select_all_elem = wait.until(EC.presence_of_element_located((By.XPATH, dash_select_all_checkbox)))
                driver.execute_script("arguments[0].click();", select_all_elem)
                wait_for_loader_to_disappear(driver, wait)

                # Output Total
                if actual_sum == expected_sum:
                    print(f"✅ {btn_name} - Total - Select all - matched ({actual_sum})")
                else:
                    print(f"❌ {btn_name} - Total - Select all - mismatch "
                          f"(Actual: {actual_sum}, Expected: {expected_sum})")

            except Exception as e:
                print(f"❌ {btn_name} - Total validation failed: {e}")
                allure.attach(str(e), f"{btn_name}-Total Error", allure.attachment_type.TEXT)

    return True
