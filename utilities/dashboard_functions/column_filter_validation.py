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
import pytest
from selenium.common.exceptions import TimeoutException

import pyautogui as pg
from selenium.webdriver.common.keys import Keys
from utilities.add_task_functions.wait_for_loader_to_disappear import wait_for_loader_to_disappear

def step_fail(driver, step_name, error):
    allure.attach(str(error), name=f"{step_name} Error", attachment_type=allure.attachment_type.TEXT)
    allure.attach(driver.get_screenshot_as_png(), name=f"{step_name} Screenshot", attachment_type=allure.attachment_type.PNG)
    pytest.fail(f"❌ {step_name} failed")
def attach_failure_artifacts(driver, test_name, error):
    """Capture screenshot + attach error text to Allure"""
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        os.makedirs("screenshots", exist_ok=True)
        screenshot_path = f"screenshots/{test_name}_{timestamp}.png"
        driver.save_screenshot(screenshot_path)
        allure.attach.file(screenshot_path,name=f"Failure Screenshot - {test_name}",attachment_type=allure.attachment_type.PNG)
    except Exception as e:
        step_fail(driver, "Login failed", e)

def get_outer_element(current_elem, levels_up=1):
    outer_elem = current_elem
    for _ in range(levels_up):
        outer_elem = outer_elem.find_element(By.XPATH, "./..")  # go to parent
    return outer_elem

def column_filter_validation(driver, wait):
    wait_less = WebDriverWait(driver, 5)
    with allure.step("Load locators from JSON"):
        try:
            with open(os.path.join("data", 'locators.json'), 'r') as f:
                elements_details = json.load(f)
            print("✅ Locators loaded successfully")
        except Exception as e:
            step_fail(driver, "Loading locators failed", e)


    dash_col_filter_button_template = elements_details['dash_col_filter_button_template']
    dash_col_filter_search_btn = elements_details['dash_col_filter_search_btn']
    dash_col_filter_ok_btn = elements_details['dash_col_filter_ok_btn']
    dash_col_filter_cancel_btn = elements_details['dash_col_filter_cancel_btn']
    dash_filter_reset_btn = elements_details['dash_filter_reset_btn']
    dash_total_btn = elements_details['dash_total_btn']
    toast_msg = elements_details['toast_msg']
    column_chooser_btn = elements_details['column_chooser_btn']
    select_all_checkbox = elements_details['select_all_checkbox']
    column_chooser_save_btn = elements_details['column_chooser_save_btn']
    task_list_headers = elements_details['task_list_headers']
    not_found_label = elements_details['not_found_label']
    filter_dropdown_list = elements_details['filter_dropdown_list']

    with allure.step("Click Total button"):
        total_btn_elem = wait.until(EC.element_to_be_clickable((By.XPATH, dash_total_btn)))
        total_btn_elem.click()
        wait_for_loader_to_disappear(driver, wait)
        print("✅ Clicked Total button")

    with allure.step("Open Column Chooser"):
        chooser = wait.until(EC.element_to_be_clickable((By.XPATH, column_chooser_btn)))
        highlight_element(driver, chooser)
        chooser.click()
        print("✅ Opened Column Chooser")

    with allure.step("Select All columns"):
        select_all = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, select_all_checkbox)))
        if select_all.get_attribute("aria-checked") in ["false", "mixed"]:
            driver.execute_script("arguments[0].click();", select_all)
            print("☑️ Selected all columns")
        else:
            print("ℹ️ All columns already selected")

    with allure.step("Save Column Chooser"):
        save_btn = wait.until(EC.element_to_be_clickable((By.XPATH, column_chooser_save_btn)))
        highlight_element(driver, save_btn)
        save_btn.click()
        print("✅ Column chooser saved")

    toast = wait.until(EC.presence_of_element_located((By.XPATH, toast_msg)))
    print(f"📢 Toast message: {toast.text}")

    wait_for_loader_to_disappear(driver, wait)

    scroll_container = driver.find_element(By.XPATH, "//div[contains(@class,'dx-scrollable-container')]")
    processed_columns = set()
    no_new_columns_count = 0

    print("🚀 Starting column-wise filter validation")

    while True:

        headers = driver.find_elements(By.XPATH, task_list_headers)
        visible_cols = [h.text.strip() for h in headers if h.text.strip()]
        new_cols = [c for c in visible_cols if c not in processed_columns]

        if not new_cols:
            no_new_columns_count += 1
        else:
            no_new_columns_count = 0

        if no_new_columns_count >= 3:
            break

        for col_name in new_cols:
            processed_columns.add(col_name)

            with allure.step(f"➡️ Filtering column: {col_name}"):
                try:
                    if col_name in ["Internal Deadline", "Due Date", "Assign Date"]:
                        filter_xpath = dash_col_filter_button_template.replace("//span[contains(@class,'dx-header-filter')]","//button").replace("{col_name}", col_name)
                    else:
                        filter_xpath = dash_col_filter_button_template.replace("{col_name}", col_name)

                    filter_buttons = driver.find_elements(By.XPATH, filter_xpath)

                    if not filter_buttons:
                        print(f"⏭️ No filter available for column: {col_name}, skipping...")
                        continue

                    filter_btn = filter_buttons[0]

                    driver.execute_script("arguments[0].scrollIntoView({block:'center'});",filter_btn)
                    time.sleep(0.3)
                    highlight_element(driver, filter_btn)

                    driver.execute_script("arguments[0].click();", filter_btn)
                    print(f"⏳ Opening filter for {col_name}")
                    time.sleep(2)

                    wait_for_loader_to_disappear(driver, wait)

                    if col_name in ["Internal Deadline", "Due Date", "Assign Date"]:
                        with allure.step(f"Apply date filter for {col_name}"):
                            date_filters(driver, wait, col_name)
                    else:
                        with allure.step(f"Select first option in filter dropdown for {col_name}"):
                            options = wait.until(EC.presence_of_all_elements_located((By.XPATH, filter_dropdown_list)))

                            if options:
                                highlight_element(driver, options[0])
                                options[0].click()
                                print(f"☑️ Selected first filter option for {col_name}")
                                time.sleep(2)

                                ok_btn = wait.until(EC.element_to_be_clickable((By.XPATH, dash_col_filter_ok_btn)))
                                highlight_element(driver, ok_btn)
                                ok_btn.click()
                                print(f"✅ Applied filter for {col_name}")
                                time.sleep(4)

                    # wait_for_loader_to_disappear(driver, wait)
                    with allure.step(f"Check if results found for {col_name}"):
                        try:
                            wait_less.until(EC.presence_of_element_located((By.XPATH, not_found_label)))
                            print(f"⚠️ No Task Found for {col_name}")
                        except Exception as e:
                            print(f"✅ Tasks found for {col_name}")
                    with allure.step(f"Reset filter for {col_name}"):
                        try:
                            reset_btn = wait_less.until(EC.element_to_be_clickable((By.XPATH, dash_filter_reset_btn)))
                            reset_btn.click()
                            time.sleep(2)
                            wait_for_loader_to_disappear(driver, wait)
                            print(f"🔄 Reset filter for {col_name}")
                        except Exception as e:
                            print(f"⚠️ Reset filter not found for column: {col_name} — continuing...")
                            continue
                        print()
                except Exception as e:
                    step_fail(driver, "Filtering column failed", e)
                    continue

        driver.execute_script("arguments[0].scrollLeft += 400;", scroll_container)
        time.sleep(0.8)

    print("🎯 Column filtering completed for ALL headers")
    print(f"📊 Total columns validated: {len(processed_columns)}")
    print(f"📊 Columns: {processed_columns}")

    return True


# =====================================================
# DATE FILTER HANDLER
# =====================================================
def date_filters(driver, wait, col_name):
    today = datetime.today().date()
    past_date = (today - timedelta(days=3)).strftime("%Y-%m-%d")
    future_date = (today + timedelta(days=3)).strftime("%Y-%m-%d")

    print(f"📅 {col_name} → Applying range {past_date} → {future_date}")
    with allure.step(f"📅 Apply date filter for {col_name} from {past_date} to {future_date}"):
        base = ("//div[@class='flex flex-col gap-1 text-sm'='{col_name}']""/..//input[@placeholder='{range}']").replace("{col_name}", col_name)

        from_input = wait.until(EC.presence_of_element_located((By.XPATH, base.replace("{range}", "From"))))
        from_input.click()
        from_input.send_keys(past_date)
        time.sleep(0.3)

        to_input = wait.until(EC.presence_of_element_located((By.XPATH, base.replace("{range}", "To"))))
        to_input.click()
        to_input.send_keys(future_date)
        time.sleep(0.3)

        apply_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Apply']")))
        apply_btn.click()
        time.sleep(0.5)

        print(f"✅ Date filter applied for {col_name}")
