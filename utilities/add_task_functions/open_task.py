import pytest
import os
import json
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import ActionChains
from utilities.other_utils_functions.highlight import highlight_element
import pyautogui as pg
import time
import allure
from selenium.common.exceptions import TimeoutException
from utilities.add_task_functions.wait_for_loader_to_disappear import wait_for_loader_to_disappear
from selenium.common.exceptions import StaleElementReferenceException


def open_task(driver, wait, task_name):
    try:
        with open(os.path.join("data", 'locators.json'), 'r') as f:
            elements_details = json.load(f)
            task_search_btn = elements_details['task_search_btn'] 
            task_search_input = elements_details['task_search_input']
            task_open_btn = elements_details['task_open_btn']
            
    except FileNotFoundError:
        pytest.fail("❌ locators.json file not found")
    except json.JSONDecodeError:
        pytest.fail("❌ Invalid JSON in locators.json")

    try:
        search_icon_btn = wait.until(EC.presence_of_element_located((By.XPATH, task_search_btn)))
        highlight_element(driver, search_icon_btn)
        search_icon_btn.click()

        # Enter task name
        search_input = wait.until(EC.visibility_of_element_located((By.XPATH, task_search_input)))
        highlight_element(driver, search_input)
        search_input.clear()
        search_input.send_keys(task_name)

        wait_for_loader_to_disappear(driver, wait)
        time.sleep(5)
    except Exception as e:
        msg = f"🔥 Error Searching Task: {e}"
        print(msg)
        allure.attach(msg, name="Search Task Failure", attachment_type=allure.attachment_type.TEXT)
        return False
       
    with allure.step("Opening task from table"):
        try:
            task_open_btn_elem = wait.until(EC.element_to_be_clickable((By.XPATH, task_open_btn)))
            highlight_element(driver, task_open_btn_elem)
            task_open_btn_elem.click()
            print("✅ Task opened from table")
            time.sleep(3)
            wait_for_loader_to_disappear(driver, wait)
            return True
        except Exception as err:
            allure.attach(str(err), name="Task Open Error", attachment_type=allure.attachment_type.TEXT)
            print(f"❌ Error opening task: {err}")
            return False
