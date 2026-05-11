
import os
import json
import time
import pytest
import allure
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from utilities.dashboard_utils import highlight_element
from selenium.webdriver import ActionChains
from selenium.common.exceptions import StaleElementReferenceException
from utilities.dashboard_utils import wait_for_loader_to_disappear
from selenium.webdriver.common.keys import Keys


def column_filter_negative(driver, wait):
    wait_less = WebDriverWait(driver, 5)
    with allure.step("Load locators from JSON"):
        try:
            with open(os.path.join("data", 'locators.json'), 'r') as f:
                elements_details = json.load(f)
            print("✅ Locators loaded successfully")
        except Exception as e:
            allure.attach(str(e), "❌ Failed to load locators", allure.attachment_type.TEXT)
            print(f"❌ Failed to load locators: {e}")
            return False

    # Load all locators
    dash_col_filter_button_template = elements_details["dash_col_filter_button_template"]
    dash_col_filter_ok_btn = elements_details["dash_col_filter_ok_btn"]
    dash_filter_reset_btn = elements_details["dash_filter_reset_btn"]
    dash_total_btn = elements_details["dash_total_btn"]
    scroller = elements_details['scroller']
    column_chooser_btn = elements_details["column_chooser_btn"]
    select_all_checkbox = elements_details["select_all_checkbox"]
    column_chooser_save_btn = elements_details["column_chooser_save_btn"]
    task_list_headers = elements_details["task_list_headers"]
    date_filter_apply_btn = elements_details["date_filter_apply_btn"]
    toast_msg = elements_details["toast_msg"]
    dash_col_filter_search_btn = elements_details["dash_col_filter_search_btn"]

    with allure.step("Click Total button"):
        try:
            total_btn = wait.until(EC.element_to_be_clickable((By.XPATH, dash_total_btn)))
            highlight_element(driver, total_btn)
            total_btn.click()
            wait_for_loader_to_disappear(driver, wait)
            print("✅ Clicked Dashboard Total tab")
        except Exception as e:
            print(f"❌ Failed to click Total tab: {e}")
            return False
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

        save_btn = wait.until(EC.element_to_be_clickable((By.XPATH, column_chooser_save_btn)))
        highlight_element(driver, save_btn)
        save_btn.click()
        print("✅ Column chooser saved")
        wait_for_loader_to_disappear(driver, wait)
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
                        filter_xpath = filter_xpath = dash_col_filter_button_template.replace("//span[contains(@class,'dx-header-filter')]","//button").replace("{col_name}", col_name)
                    else:
                        filter_xpath = dash_col_filter_button_template.replace("{col_name}", col_name)
                    filter_buttons = driver.find_elements(By.XPATH, filter_xpath)

                    if not filter_buttons:
                        print(f"⏭️ No filter available for column: {col_name}, skipping...")
                        continue

                    filter_btn = filter_buttons[0]

                    driver.execute_script("arguments[0].scrollIntoView({block:'center'});",filter_btn)
                    time.sleep(2)
                    highlight_element(driver, filter_btn)

                    driver.execute_script("arguments[0].click();", filter_btn)
                    print(f"⏳Opening filter for {col_name}")
                    time.sleep(0.6)

                    wait_for_loader_to_disappear(driver, wait)

                    if col_name in ["Internal Deadline", "Due Date", "Assign Date"]:
                        with allure.step(f"Apply date filter for {col_name}"):
                            apply_date_filter(driver, wait, col_name, date_filter_apply_btn)
                            print(f"{col_name} : No task found for the applied date filter")
                    else:
                        with allure.step(f"No tasks found for the selected Task Name filter ({col_name})"):
                            result = apply_search_filter(driver, wait, dash_col_filter_search_btn, dash_col_filter_ok_btn, col_name)
                            # if result is True:
                            #     return True  # ❌ Bug found
                            if not result:
                                pytest.fail(f"❌ Unexpected data found in negative filter for column: {col_name}")
                    with allure.step(f"Check if results found for {col_name}"):
                        try:
                            reset_btn = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, dash_filter_reset_btn)))
                            reset_btn.click()
                            wait_for_loader_to_disappear(driver, wait)
                        except TimeoutException:
                            print(f"✅ Reset button not found after filtering {col_name}")
                        print()


                except Exception as e:
                    allure.attach(str(e), f"Filter failed - {col_name}", allure.attachment_type.TEXT)
                    pytest.fail(f"❌ Column filter failed: {col_name}")
                    # return True
                
        driver.execute_script("arguments[0].scrollLeft += 400;", scroll_container)
        time.sleep(0.8)

    print("🎯 Column filtering completed")
    print(f"📊 Total columns validated: {len(processed_columns)}")
    print(f"📊 Columns: {processed_columns}")
    return True  # ✅ No bug

def apply_date_filter(driver, wait, col_name, date_filter_apply_btn):
    from_date = "2000-01-01"
    to_date = "2012-12-01"

    base = ("//div[@class='flex flex-col gap-1 text-sm'='{col_name}']""/..//input[@placeholder='{range}']").replace("{col_name}", col_name)

    from_input = wait.until(EC.presence_of_element_located((By.XPATH, base.replace("{range}", "From"))))
    from_input.click()
    from_input.send_keys(from_date)
    time.sleep(0.3)

    to_input = wait.until(EC.presence_of_element_located((By.XPATH, base.replace("{range}", "To"))))
    to_input.click()
    to_input.send_keys(to_date)
    time.sleep(0.3)

    apply_button = wait.until(EC.element_to_be_clickable((By.XPATH, date_filter_apply_btn)))
    apply_button.click()
    time.sleep(5)
    print(f"📅 {col_name}: Applied date range {from_date} → {to_date}")
    time.sleep(1)


def apply_search_filter(driver, wait, dash_col_filter_search_btn, dash_col_filter_ok_btn, col_name):
    search_input = wait.until(EC.element_to_be_clickable((By.XPATH, dash_col_filter_search_btn)))
    search_input.clear()
    search_input.send_keys("QA developers")
    time.sleep(10)
    # result_summary = ""

    try:
        no_data_text =  wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(text(),'No data to display')]")))
        highlight_element(driver, no_data_text)
        print(f"{col_name} : No task found")
        result = True

    except TimeoutException:
        options = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//div[contains(@class,'dx-list-item') and @role='option']")))

        found_values = []

        for opt in options:
            try:
                value_text = opt.find_element(
                    By.XPATH, ".//div[contains(@class,'dx-list-item-content')]"
                ).text.strip()
                if value_text:
                    found_values.append(value_text)
            except:
                pass
        result_summary = found_values if found_values else ["Blank"]
        print(f"{col_name} : {result_summary}")
        result = False
            
    try:
        ok_button = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@aria-label='OK']")))
        highlight_element(driver, ok_button)
        ok_button.click()
        print("✅ Clicked OK button to apply filter")
        time.sleep(1)
    except TimeoutException:
        pytest.fail("❌ OK button not found to apply filter")
        return False

    return result

