import os
import time
import json
import allure
import pytest
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from utilities.other_utils_functions.highlight import highlight_element
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import TimeoutException
from utilities.add_task_functions.wait_for_loader_to_disappear import wait_for_loader_to_disappear

def search_task_by_existing_task_name(driver, wait):
    try:
        with open(os.path.join("data", "locators.json"), "r") as f:
            locators = json.load(f)
            task_search_btn = locators["task_search_btn"]
            task_search_input = locators["task_search_input"]
            dash_total_btn = locators["dash_total_btn"]
            column_chooser_btn = locators["column_chooser_btn"]
            column_chooser_save_btn = locators["column_chooser_save_btn"]

    except Exception as e:
        print(f"❌ Failed to load locators.json: {e}")
        return False
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
        try:
            column_chooser_btn_elem = wait.until(EC.presence_of_element_located((By.XPATH, column_chooser_btn)))
            driver.execute_script("arguments[0].click();", column_chooser_btn_elem)
            wait_for_loader_to_disappear(driver, wait)
        except TimeoutException:
            pytest.fail("❌ Column Chooser button not found")

        def get_state(elem):
            """
            Returns: 'selected', 'deselected', 'mixed'
            """
            aria = elem.get_attribute("aria-checked")
            if aria == "true":
                return "selected"
            elif aria == "false":
                return "deselected"
            else:
                return "mixed"   

        try:
            select_all_checkbox = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".dx-list-select-all-checkbox")))
            driver.execute_script("arguments[0].scrollIntoView(true);", select_all_checkbox)
            time.sleep(0.2)

            state = get_state(select_all_checkbox)
            print(f"➤ Initial 'Select All' state: {state}")
            if state == "deselected":
                print("✅ Already deselected, no action needed")
            elif state == "selected":
                print("🔁 Deselecting 'Select All'")
                driver.execute_script("arguments[0].click();", select_all_checkbox)
                wait_for_loader_to_disappear(driver, wait)
                time.sleep(0.3)
            elif state == "mixed":
                print("🔁 Mixed state detected → select all → deselect")
                driver.execute_script("arguments[0].click();", select_all_checkbox)
                wait_for_loader_to_disappear(driver, wait)
                time.sleep(0.3)
                select_all_checkbox = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".dx-list-select-all-checkbox")))
                driver.execute_script("arguments[0].click();", select_all_checkbox)
                wait_for_loader_to_disappear(driver, wait)
                time.sleep(0.3)

            select_all_checkbox = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".dx-list-select-all-checkbox")))
            final_state = get_state(select_all_checkbox)
            print(f"➤ Final 'Select All' state: {final_state}")

            if final_state != "deselected":
                pytest.fail(f"❌ Select All normalization failed, state: {final_state}")

            print("✅ 'Select All' normalized successfully")

        except StaleElementReferenceException:
            pytest.fail("❌ Stale element while normalizing Select All")

        column_chooser_save_btn_elem= wait.until(EC.element_to_be_clickable((By.XPATH, column_chooser_save_btn)))
        highlight_element(driver, column_chooser_save_btn_elem)
        column_chooser_save_btn_elem.click()
        time.sleep(7)
        print("✅ Column Chooser saved")
    with allure.step("Fetch the task name from the task list"):
        try:
            task_elem = wait.until(EC.presence_of_element_located((By.XPATH,"(//div[contains(@class,'justify-between')]//p[@class='_tr_text_11lye_10'])[1]")))
            highlight_element(driver, task_elem)
            first_task_name = task_elem.text.strip()
            if not first_task_name:
                first_task_name = task_elem.get_attribute("title").strip()
            if not first_task_name:
                raise Exception("Task name text is empty")
            print(f"🔹 Task Name: {first_task_name}")
        except Exception as e:
            print(f"❌ Could not retrieve first task name: {e}")
            return False
    with allure.step(f"Search using task name: {first_task_name}"):
        try:
            search_icon_btn = wait.until(EC.element_to_be_clickable((By.XPATH, task_search_btn)))
            highlight_element(driver, search_icon_btn)
            search_icon_btn.click()

            search_input = wait.until(EC.visibility_of_element_located((By.XPATH, task_search_input)))
            highlight_element(driver, search_input)
            search_input.clear()
            search_input.send_keys(first_task_name)

            wait_for_loader_to_disappear(driver, wait)
            time.sleep(3)  # Extra wait to ensure results load
            print(f"✅ Searched using first task name: {first_task_name}")
        except Exception as e:
            print(f"❌ Failed to search using first task name: {e}")
            return False
    return True

    
    
