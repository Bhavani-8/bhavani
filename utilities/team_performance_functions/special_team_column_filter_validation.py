import os
import json
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utilities.other_utils_functions.highlight import highlight_element
from datetime import datetime, timedelta
import time
from selenium.common.exceptions import TimeoutException
import pyautogui as pg
from selenium.webdriver.common.keys import Keys
from utilities.add_task_functions.wait_for_loader_to_disappear import wait_for_loader_to_disappear


def attach_failure_artifacts(driver, test_name, error=None):
    """Capture screenshot + attach error text to Allure"""
    try:
        os.makedirs("screenshots", exist_ok=True)
        screenshot_path = f"screenshots/{test_name}.png"
        driver.save_screenshot(screenshot_path)

        allure.attach.file(
            screenshot_path,
            name=f"Failure Screenshot - {test_name}",
            attachment_type=allure.attachment_type.PNG
        )

        if error:
            allure.attach(str(error), name=f"Error - {test_name}", attachment_type=allure.attachment_type.TEXT)

    except Exception as ss_err:
        print(f"❌ Failed to capture screenshot: {ss_err}")


def special_column_filter_validation(driver, wait):
    wait_less = WebDriverWait(driver, 5)

    with open(os.path.join("data", "locators.json"), "r") as f:
        elements_details = json.load(f)

    dash_col_filter_ok_btn = elements_details['dash_col_filter_ok_btn']
    column_chooser_btn = elements_details['column_chooser_btn']
    select_all_checkbox = elements_details['select_all_checkbox']
    column_chooser_save_btn = elements_details['column_chooser_save_btn']
    scroller_xpath = elements_details['scroller']
    not_found_label = elements_details['not_found_label']
    filter_dropdown_list = elements_details['filter_dropdown_list']

    # ---------------- Column Chooser ----------------
    column_chooser_btn_elem = wait.until(EC.element_to_be_clickable((By.XPATH, column_chooser_btn)))
    driver.execute_script("arguments[0].click();", column_chooser_btn_elem)
    wait_for_loader_to_disappear(driver, wait)

    select_all_checkbox_elem = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, select_all_checkbox)))
    if select_all_checkbox_elem.get_attribute("aria-checked") in ["false", "mixed"]:
        driver.execute_script("arguments[0].click();", select_all_checkbox_elem)

    column_chooser_save_btn_elem = wait.until(EC.element_to_be_clickable((By.XPATH, column_chooser_save_btn)))
    driver.execute_script("arguments[0].click();", column_chooser_save_btn_elem)
    wait_for_loader_to_disappear(driver, wait)
    time.sleep(3)

    scroller_elem = wait.until(EC.presence_of_element_located((By.XPATH, scroller_xpath)))

    headers = driver.find_elements(By.XPATH, "//td[@role='columnheader' and @aria-label]")
    print(f"🧩 Total columns found: {len(headers)}")

    special_filter_columns = {
        "Approval Pending": ["Complied", "Not Complied"],
        "Rejected": ["Complied", "Not Complied"],
        "Completed": ["Complied", "Not Complied"]
    }

    def open_filter_and_apply(header_elem, option_text=None):
        col_name = header_elem.get_attribute("aria-label").strip()
        with allure.step(f"🔎 Filter Validation → {col_name}"):
            driver.execute_script("""
                arguments[1].scrollLeft = arguments[0].offsetLeft - 150;
                arguments[0].scrollIntoView({block:'center', inline:'center'});
            """, header_elem, scroller_elem)
            time.sleep(0.7)

            filter_button = header_elem.find_element(By.XPATH, ".//span[contains(@class,'dx-header-filter')]")
            driver.execute_script("arguments[0].click();", filter_button)
            print(f"✅ Filter opened for {col_name}")

            options = wait.until(EC.presence_of_all_elements_located((By.XPATH, filter_dropdown_list)))

            selected_option = None
            if option_text:
                for opt in options:
                    if opt.text.strip().lower() == option_text.lower():
                        selected_option = opt
                        break
            else:
                selected_option = options[0]

            if not selected_option:
                print(f"⚠️ Option '{option_text}' not found in {col_name}")
                return

            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", selected_option)
            selected_option.click()
            print(f"➡️ Selected: {selected_option.text}")

            ok_btn = wait.until(EC.element_to_be_clickable((By.XPATH, dash_col_filter_ok_btn)))
            ok_btn.click()
            time.sleep(1)

        try:
            not_found = wait.until(EC.presence_of_element_located((By.XPATH, not_found_label)))
            highlight_element(driver, not_found)
            print("⚠️ No records found")
        except TimeoutException:
            print("✅ Records displayed")


        reset_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@role='button' and @title='Reset Filters']")))
        reset_btn.click()
        print("🔄 Filters reset")
        time.sleep(1)

    with allure.step("Apply filter on all columns"):
        for header in headers:
            col_name = header.get_attribute("aria-label").strip()
            print(f"\n🟦 Processing column → {col_name}")

            try:
                if col_name in special_filter_columns:
                    for sub_option in special_filter_columns[col_name]:
                        print(f"Sub-filter → {sub_option}")
                        open_filter_and_apply(header, sub_option)
                else:
                    open_filter_and_apply(header)

            except Exception as e:
                print(f"❌ Failed on column {col_name}: {e}")

        print("\n🎯 Column filter validation completed for all columns")
    return True
