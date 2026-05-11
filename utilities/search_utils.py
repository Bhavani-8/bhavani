from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
import pandas as pd
import pyautogui as pg
import allure
import os
import json
import pytest
import time

from utilities.add_task_utils import wait_for_loader_to_disappear
from utilities.highlight import highlight_element


# -------------------------
# Load locators (fail if missing/invalid)
# -------------------------
try:
    with allure.step("➡️ Loading locators from data/locators.json"):
        with open(os.path.join("data", "locators.json"), "r") as f:
            elements_details = json.load(f)
            task_search_btn = elements_details["task_search_btn"]
            task_search_input = elements_details["task_search_input"]
            toast_msg = elements_details["toast_msg"]
        print("✅ Loaded locators from locators.json")
except FileNotFoundError as err:
    allure.attach(str(err), name="locators.json not found", attachment_type=allure.attachment_type.TEXT)
    pytest.fail("locators.json file not found")
except json.JSONDecodeError as err:
    allure.attach(str(err), name="Invalid JSON in locators.json", attachment_type=allure.attachment_type.TEXT)
    pytest.fail("Invalid JSON in locators.json")
except Exception as err:
    allure.attach(str(err), name="Unexpected error loading locators", attachment_type=allure.attachment_type.TEXT)
    pytest.fail(f"Unexpected error loading locators: {err}")


def perform_search(driver, wait, search_value):
    try:
        with allure.step("➡️ Wait for toast/loader to disappear"):
            wait.until(EC.invisibility_of_element_located((By.XPATH, toast_msg)))
            wait_for_loader_to_disappear(driver, wait)
            print("✅ Loader/toast not visible")

        with allure.step("➡️ Click Task Search button"):
            task_search_btn_elem = wait.until(EC.element_to_be_clickable((By.XPATH, task_search_btn)))
            task_search_btn_elem.click()
            highlight_element(driver, task_search_btn_elem)
            print("✅ Clicked Task Search button")

        with allure.step("➡️ Enter search value into input"):
            task_search_input_elem = wait.until(EC.presence_of_element_located((By.XPATH, task_search_input)))
            task_search_input_elem.click()
            task_search_input_elem.clear()
            task_search_input_elem.send_keys(search_value)
            print(f"✅ Entered task name: {search_value}")

        with allure.step("➡️ Wait for search processing to finish"):
            wait_for_loader_to_disappear(driver, wait)
            time.sleep(3)
            print("✅ Search action completed")

    except Exception as err:
        allure.attach(str(err), name="Search Error", attachment_type=allure.attachment_type.TEXT)
        print(f"❌ Error occurred while searching: {err}")


def clear_search(driver, wait):
    try:
        with allure.step("➡️ Wait for toast to disappear"):
            wait.until(EC.invisibility_of_element_located((By.XPATH, toast_msg)))
            # print("✅ Toast not visible")

        with allure.step("➡️ Attempt to click clear button if present"):
            wait_less = WebDriverWait(driver, 5)
            try:
                search_input_clear_btn_elem = wait_less.until(
                    EC.element_to_be_clickable(
                        (By.XPATH, "//button[@class='MuiButtonBase-root MuiIconButton-root "
                                   "MuiIconButton-sizeMedium style_closeSearchIcon__29F5W css-1yxmbwk']")
                    )
                )
                search_input_clear_btn_elem.click()
                # print("✅ Search input cleared")
            except TimeoutException:
                pass
                # Expected case: clear button not present => input already empty
                # print("ℹ️ Search input already empty (clear button not present)")
            except Exception as err:
                allure.attach(str(err), name="Clear Search Error", attachment_type=allure.attachment_type.TEXT)
                print(f"❌ Error while clearing search input: {err}")

    except Exception as err:
        allure.attach(str(err), name="Clear Search Unexpected Error", attachment_type=allure.attachment_type.TEXT)
        print(f"❌ Unexpected error in clear_search: {err}")
