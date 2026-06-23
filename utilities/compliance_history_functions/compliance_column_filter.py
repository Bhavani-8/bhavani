
import os
import json
import pytest
import allure
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from utilities.other_utils_functions.highlight import highlight_element
from selenium.common.exceptions import TimeoutException

from utilities.add_task_utils import wait_for_loader_to_disappear

def compliance_column_filter(driver, wait):

    with allure.step("Load locators.json"):
        try:
            with open(os.path.join("data", "locators.json"), "r") as f:
                json.load(f)
            print("✅ locators.json loaded successfully")
        except Exception as e:
            allure.attach(str(e), name="Locators Error",
                          attachment_type=allure.attachment_type.TEXT)
            pytest.fail("Failed to load locators.json")

    column_headers = [
        "Complete On",
        "Task Name",
        "Company",
        "Assign To",
        "Approver",
        "Due Date",
        "Status",
    ]


    failed_filters = []

    for column_name in column_headers:

        with allure.step(f"Filter → {column_name}"):

            try:
                print()

                filter_xpath = f"//th[.//*[normalize-space()='{column_name}']]//button[@data-slot='popover-trigger']"
                try:
                    filter_icons = wait.until(EC.presence_of_all_elements_located((By.XPATH, filter_xpath)))
                except TimeoutException:
                    print(f"⏭️ No filter available for column: {column_name}, skipping...")
                    continue

                filter_icon = filter_icons[0]

                driver.execute_script("arguments[0].scrollIntoView({block:'center', inline:'center'});",filter_icon)
               
                highlight_element(driver, filter_icon)
                filter_icon.click()
                time.sleep(1)

                print(f"🟦 Opened filter : {column_name}")

                checkbox = wait.until(EC.element_to_be_clickable((By.XPATH, "(//span[@class='truncate grow'])[1]")))
                option_text = checkbox.text.strip()
                print(f"🟦 First checkbox name: {option_text}")

                checkbox.click()
                time.sleep(2)

                compliance_history_text = wait.until(EC.presence_of_element_located((By.XPATH, "//h2[@class='text-2xl font-bold']")))
                compliance_history_text.click()
                time.sleep(0.5)

                filter_icon = wait.until(EC.element_to_be_clickable((By.XPATH, filter_xpath)))
                highlight_element(driver, filter_icon)
                driver.execute_script("arguments[0].click();", filter_icon)
                time.sleep(1)

                clear_filter_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Clear filters']")))
                highlight_element(driver, clear_filter_btn)
                clear_filter_btn.click()
                time.sleep(2)

                compliance_history_text = wait.until(EC.presence_of_element_located((By.XPATH, "//h2[@class='text-2xl font-bold']")))
                compliance_history_text.click()
                time.sleep(0.5)

            except Exception as e:
                print(f"❌ Filter failed for : {column_name} | {e}")
                failed_filters.append(column_name)
                continue
    # # ✅ Fail after loop
    if failed_filters:
        raise Exception(f"Filters failed for: {failed_filters}")
    return True