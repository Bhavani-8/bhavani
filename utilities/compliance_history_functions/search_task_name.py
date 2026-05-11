import os
import time
import json
import allure
import pytest
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import pyautogui as pg
from utilities.other_utils_functions.highlight import highlight_element
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from utilities.add_task_functions.wait_for_loader_to_disappear import wait_for_loader_to_disappear

def search_task_name(driver, wait):
    try:
        with open(os.path.join("data", "locators.json"), "r") as f:
            locators = json.load(f)
            task_title_label = locators["task_title_label"]

    except Exception as e:
        print(f"❌ Failed to load locators.json: {e}")
        return False
    with allure.step("Fetch the task name from the task list"):
        try:
            task_elem = wait.until(EC.presence_of_element_located((By.XPATH,"(//button[@data-slot='tooltip-trigger'])[1]")))
            highlight_element(driver, task_elem)
            first_task_name = task_elem.text.strip()
            if not first_task_name:
                first_task_name = task_elem.get_attribute("title").strip()
            if not first_task_name:
                raise Exception("Task name text is empty")
            print(f"🔹Task Name: {first_task_name}")
        except Exception as e:
            print(f"❌ Could not retrieve first task name: {e}")
            return False
    with allure.step(f"Search using task name: {first_task_name}"):
        try:

            search_input = wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@placeholder='Search history...']")))
            highlight_element(driver, search_input)
            search_input.clear()
            search_input.send_keys(first_task_name)

            wait_for_loader_to_disappear(driver, wait)
            time.sleep(3)  # Extra wait to ensure results load
            print(f"✅ Searched using first task name: {first_task_name}")
        except Exception as e:
            print(f"❌ Failed to search using first task name: {e}")
            return False
    
    with allure.step("Verify task name"):
        try:
            task_elem_after_search = wait.until(EC.presence_of_element_located((By.XPATH,"(//button[@data-slot='tooltip-trigger'])[1]")))
            highlight_element(driver, task_elem_after_search)
            task_elem_after_search.click()
            time.sleep(2)

            task_name_label = wait.until(EC.presence_of_element_located((By.XPATH, task_title_label)))
            highlight_element(driver, task_name_label)
            displayed_task_name = task_name_label.text.strip()
            print(f"🔹Displayed Task Name: {displayed_task_name}")
            if displayed_task_name == first_task_name:
                allure.attach(f"Displayed task name matches searched task name: {displayed_task_name}", name="Task Name Validation", attachment_type=allure.attachment_type.TEXT) 
            else:
                allure.attach(f"Displayed task name does NOT match searched task name. Displayed: {displayed_task_name}, Expected: {first_task_name}", name="Task Name Validation", attachment_type=allure.attachment_type.TEXT) 
                raise Exception("Displayed task name does not match searched task name")   
        except Exception as e:
            print(f"❌ Failed to open Task Details: {e}")
            return False

    return True

    
    
