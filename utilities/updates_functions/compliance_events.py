from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import allure 
import pandas as pd
import pyautogui as pg
import os
import json
import pytest
import time


from utilities.other_utils_functions.highlight import highlight_element
from selenium.common.exceptions import TimeoutException
from utilities.add_task_utils import add_task_check
from utilities.add_task_utils import get_test_case_list
from utilities.add_task_utils import load_test_config_excel_data
from utilities.add_task_utils import wait_for_loader_to_disappear
def compliance_events(driver, wait):
    wait_less = WebDriverWait(driver, 5)
    # ------------------------------------------
    # STEP 1: LOAD LOCATORS
    # ------------------------------------------
    with allure.step("Load locators.json"):
        try:
            with open(os.path.join("data", 'locators.json'), 'r') as f:
                elements_details = json.load(f)
                task_update_tab = elements_details['task_update_tab']
                dash_col_filter_search_btn = elements_details['dash_col_filter_search_btn']
                dash_col_filter_ok_btn = elements_details['dash_col_filter_ok_btn']
            print("✅ locators.json loaded successfully")
        except Exception as e:
            allure.attach(str(e), name="Locators Error", attachment_type=allure.attachment_type.TEXT)
            pytest.fail("Failed to load locators.json")

    # Check Search Button
    with allure.step("Click Search Button"):
        search_button = wait.until(EC.presence_of_element_located((By.XPATH, "(//button[contains(@class,'group/button')])[1]")))
        highlight_element(driver, search_button)
        search_button.click()

        search_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Search...']")))
        search_input.send_keys("Mock Trading")
        print("✅ Clicked Search Button")
        time.sleep(2)
        print("✅ Clicked Close Button")
    # ------------------------------------------
    # STEP 2: OPEN UPDATES SECTION
    # ------------------------------------------
    with allure.step("Select Update Checkbox"):
        try:
            select_elem = wait.until(EC.presence_of_element_located((By.XPATH, "(//div[@class='flex flex-col min-w-0 flex-1 gap-1'])[1]")))
            highlight_element(driver, select_elem)
            select_elem.click()
            print("🟦 First checkbox clicked")
            time.sleep(2)
        except Exception as e:
            allure.attach(str(e), name="Updates Section Error", attachment_type=allure.attachment_type.TEXT)
            return False

    with allure.step("Open Compliance Events"):
        compliance_events = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Compliance Events']")))
        highlight_element(driver, compliance_events)
        compliance_events.click()
        print("🟦 Compliance Events clicked")
        time.sleep(3)

    # Column header names (order must match filters)
    column_headers = [
        'Name',
        'License',
        'Frequency',
        'Risk Rating'
    ]

    filter_icons = wait.until(
        EC.presence_of_all_elements_located((By.XPATH, "//button[@data-slot='popover-trigger']"))
    )

    total_filters = len(filter_icons)
    print(f"🔢 Total filters found: {total_filters}")

    failed_filters = []

    for index, column_name in enumerate(column_headers):

        with allure.step(f"Filter → {column_name}"):

            try:
                print()

                # ✅ Skip if filter not present
                if index >= total_filters:
                    print(f"⏭️ No filter available for column: {column_name}, skipping...")
                    continue

                # Re-fetch each time (avoid stale)
                filter_icons = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//button[.//*[contains(@class,'lucide-funnel')]]")))

                filter_icon = filter_icons[index]

                # ✅ Scroll properly (important for last column)
                driver.execute_script("arguments[0].scrollIntoView({block:'center', inline:'center'});", filter_icon)
                time.sleep(1)

                highlight_element(driver, filter_icon)
                filter_icon.click()
                print(f"🟦 Opened filter : {column_name}")
                time.sleep(2)
                
                # Select checkbox
                checkbox = wait.until(EC.element_to_be_clickable((By.XPATH, "(//span[@class='truncate grow'])[1]")))
                highlight_element(driver, checkbox)
                fetch_checkbox_name = checkbox.text.strip()
                print(f"🟦 First checkbox name: {fetch_checkbox_name}")
                checkbox.click()
                time.sleep(2)

                # Click outside to apply
                compliance_events_label = wait.until(EC.element_to_be_clickable((By.XPATH, "//h2[text()='Compliance Events']")))
                # highlight_element(driver, compliance_events_label)
                compliance_events_label.click()
                time.sleep(1)
                wait_for_loader_to_disappear(driver, wait)

                # Re-open filter
                filter_icons = wait.until(
                    EC.presence_of_all_elements_located((By.XPATH, "//button[.//*[contains(@class,'lucide-funnel')]]"))
                )
                filter_icon = filter_icons[index]

                driver.execute_script("arguments[0].scrollIntoView({block:'center'});", filter_icon)
                filter_icon.click()
                time.sleep(2)

                # Clear filter
                clear_filter_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Clear filters']")))
                highlight_element(driver, clear_filter_btn)
                clear_filter_btn.click()
                time.sleep(2)

                compliance_events_label = wait.until(EC.element_to_be_clickable((By.XPATH, "//h2[text()='Compliance Events']")))
                compliance_events_label.click()
                wait_for_loader_to_disappear(driver, wait)

            except Exception as e:
                print(f"❌ Filter failed for : {column_name} | {e}")
                allure.attach(str(e), name=f"{column_name} Filter Error",
                            attachment_type=allure.attachment_type.TEXT)
                failed_filters.append(column_name)
                continue
    with allure.step("Impact Button"):

        try:
            impact_btn_elem = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[.//*[contains(@class,'lucide-info')]]")))
            highlight_element(driver, impact_btn_elem)
            impact_btn_elem.click()
            time.sleep(0.5)

            compliance_events_label = wait.until(EC.element_to_be_clickable((By.XPATH, "//h2[text()='Compliance Events']")))
            compliance_events_label.click()
            wait_for_loader_to_disappear(driver, wait)
        except Exception as e:
            print(f"❌ Impact button failed: {e}")

            allure.attach(
                str(e),
                name="Impact Button Error",
                attachment_type=allure.attachment_type.TEXT
            )

            failed_filters.append("Impact")
    # ✅ Fail after loop
    if failed_filters:
        pytest.fail(f"Filters failed for: {failed_filters}")
    return True