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


def project_search_name(driver, wait):
    try:
        with open(os.path.join("data", "locators.json"), "r") as f:
            locators = json.load(f)
            project_icon = locators["project_icon"]
            first_task_name_text = locators['first_task_name_text']
            seacrh_input_elem = locators['seacrh_input_elem']
            verify_search_task = locators['verify_search_task']
            search_reset_btn = locators['search_reset_btn']

    except FileNotFoundError as e:
            msg = f"locators.json file not found: {str(e)}"
            print(msg)
            allure.attach(msg, name="Locators File Missing", attachment_type=allure.attachment_type.TEXT)
            return False
    except json.JSONDecodeError as e:
        msg = f"Invalid JSON in locators.json: {str(e)}"
        print(msg)
        allure.attach(msg, name="Locators JSON Error", attachment_type=allure.attachment_type.TEXT)
        return False

    
    with allure.step("Click project icon"):
        try:
            driver.refresh()
            wait_for_loader_to_disappear(driver, wait)
            project_btn = wait.until(EC.presence_of_element_located((By.XPATH, project_icon)))
            highlight_element(driver, project_btn)
            project_btn.click()
            time.sleep(2)
        except Exception as e:
            msg = f"Failed to Click Project Icon: {str(e)}"
            print(msg)
            allure.attach(msg, name="Project Icon Error", attachment_type=allure.attachment_type.TEXT)
            raise Exception(msg)
    
    
    with allure.step("Fetch first task name from Projects"):
        try:
            first_task_name_elem = wait.until(EC.presence_of_element_located((By.XPATH, first_task_name_text)))
            highlight_element(driver, first_task_name_elem)
            first_task_name = first_task_name_elem.get_attribute("title").strip()
            print(f"✅ First task name fetched: {first_task_name}")
        except Exception as e:
            msg = f"Failed to Fetch first task name from Projects: {str(e)}"
            print(msg)
            allure.attach(msg, name="Fetch first task name from Projects Error", attachment_type=allure.attachment_type.TEXT)
            raise Exception(msg)
    
    with allure.step(f"Search using task name: {first_task_name}"):
        try:

            search_input = wait.until(EC.visibility_of_element_located((By.XPATH, seacrh_input_elem)))
            highlight_element(driver, search_input)
            search_input.clear()
            search_input.send_keys(first_task_name)

            wait_for_loader_to_disappear(driver, wait)
            time.sleep(3)  # Extra wait to ensure results load
            print(f"✅ Searched using first task name: {first_task_name}")
        except Exception as e:
            msg = f"Failed to Click Search Input: {str(e)}"
            print(msg)
            allure.attach(msg, name="Search Input Error", attachment_type=allure.attachment_type.TEXT)
            raise Exception(msg)
    with allure.step("Verify search name after search"):
        try:
            search_task_name_elem = wait.until(EC.presence_of_element_located((By.XPATH, verify_search_task)))
            highlight_element(driver, search_task_name_elem)
            search_task_name_label = search_task_name_elem.get_attribute("title").strip()
            print(f"🔍 Task name label after search: {search_task_name_label}")
            if search_task_name_label == first_task_name:
                allure.attach(f"Expected: {first_task_name}, Found: {search_task_name_label}", name="Search Name Match", attachment_type=allure.attachment_type.TEXT)
                print("✅ Search name verification successful")
            else:
                print("❌ Search name verification failed")
                allure.attach(f"Expected: {first_task_name}, Found: {search_task_name_label}", name="Search Name Mismatch", attachment_type=allure.attachment_type.TEXT)
                return False
                
        except Exception as e:
            msg = f"Failed to Verify search name after search: {str(e)}"
            print(msg)
            allure.attach(msg, name="Verify search name after search Error", attachment_type=allure.attachment_type.TEXT)
            raise Exception(msg)
    with allure.step("Click Reset Button to clear search"):
        try:
            reset_btn = wait.until(EC.element_to_be_clickable((By.XPATH, search_reset_btn)))
            highlight_element(driver, reset_btn)
            reset_btn.click()
            wait_for_loader_to_disappear(driver, wait)
            time.sleep(2)  
            print("✅ Reset button clicked and search cleared")
        except Exception as e:
            msg = f"Failed to Click Reset Button to clear search: {str(e)}"
            print(msg)
            allure.attach(msg, name="Click Reset Button to clear search Error", attachment_type=allure.attachment_type.TEXT)
            raise Exception(msg)
    return True
    
    

    
    
