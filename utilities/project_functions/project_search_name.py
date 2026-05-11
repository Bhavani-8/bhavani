import os
import time
import json
import allure
import pytest
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import pyautogui as pg
from utilities.other_utils_functions.highlight import highlight_element
from utilities.add_task_functions.wait_for_loader_to_disappear import wait_for_loader_to_disappear

def step_fail(driver, step_name, error):
    allure.attach(str(error), name=f"{step_name} Error", attachment_type=allure.attachment_type.TEXT)
    allure.attach(driver.get_screenshot_as_png(), name=f"{step_name} Screenshot", attachment_type=allure.attachment_type.PNG)
    pytest.fail(f"❌ {step_name} failed")

def project_search_name(driver, wait):
    try:
        with open(os.path.join("data", "locators.json"), "r") as f:
            locators = json.load(f)
            task_search_btn = locators["task_search_btn"]
            task_search_input = locators["task_search_input"]
            dash_total_btn = locators["dash_total_btn"]
            column_chooser_btn = locators["column_chooser_btn"]
            column_chooser_save_btn = locators["column_chooser_save_btn"]
            project_icon = locators["project_icon"]

    except Exception as e:
        print(f"❌ Failed to load locators.json: {e}")
        return False

    
    with allure.step("Click project icon"):
        try:
            project_btn = wait.until(EC.presence_of_element_located((By.XPATH, project_icon)))
            highlight_element(driver, project_btn)
            project_btn.click()
            time.sleep(2)
        except Exception as e:
            step_fail(driver, "Click project icon", e)
    
    with allure.step("Fetch first task name from Projects"):
        try:
            first_task_name_elem = wait.until(EC.presence_of_element_located((By.XPATH, "(//tr[contains(@class,'dx-data-row')])[2]//td[1]//div[@title]")))
            highlight_element(driver, first_task_name_elem)
            first_task_name = first_task_name_elem.text.strip()
            print(f"✅ First task name fetched: {first_task_name}")
        except Exception as e:
            step_fail(driver, "Fetch first task name from Projects", e)
    
    with allure.step(f"Search using task name: {first_task_name}"):
        try:

            search_input = wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@aria-label='Search in the data grid']")))
            highlight_element(driver, search_input)
            search_input.clear()
            search_input.send_keys(first_task_name)

            wait_for_loader_to_disappear(driver, wait)
            time.sleep(3)  # Extra wait to ensure results load
            print(f"✅ Searched using first task name: {first_task_name}")
        except Exception as e:
             step_fail(driver, f"Search using task name: {first_task_name}", e)
    with allure.step("Verify search name after search"):
        try:
            search_task_name_label = wait.until(EC.presence_of_element_located((By.XPATH, "(//div[@class='w-full truncate'])[1]")))
            highlight_element(driver, search_task_name_label)
            search_task_name_label = search_task_name_label.text.strip()
            print(f"🔍 Task name label after search: {search_task_name_label}")
            if search_task_name_label == first_task_name:
                allure.attach(f"Expected: {first_task_name}, Found: {search_task_name_label}", name="Search Name Match", attachment_type=allure.attachment_type.TEXT)
                print("✅ Search name verification successful")
            else:
                print("❌ Search name verification failed")
                allure.attach(f"Expected: {first_task_name}, Found: {search_task_name_label}", name="Search Name Mismatch", attachment_type=allure.attachment_type.TEXT)
                return False
                
        except Exception as e:
            step_fail(driver, "verify search name after search", e)     

    with allure.step("Click Reset Button to clear search"):
        try:
            reset_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@aria-label='Reset']")))
            highlight_element(driver, reset_btn)
            reset_btn.click()
            wait_for_loader_to_disappear(driver, wait)
            time.sleep(2)  
            print("✅ Reset button clicked and search cleared")
        except Exception as e:
            step_fail(driver, "Click Reset Button to clear search", e)
    return True
    
    

    
    
