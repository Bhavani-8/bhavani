import os
import time
import json
import allure
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from utilities.other_utils_functions.highlight import highlight_element
from utilities.add_task_functions.wait_for_loader_to_disappear import wait_for_loader_to_disappear

def not_applicable_search_task(driver, wait):
    try:
        with open(os.path.join("data", "locators.json"), "r") as f:
            locators = json.load(f)
            task_title_label = locators["task_title_label"]
            settings_icon = locators["settings_icon"]

    except Exception as e:
        print(f"❌ Failed to load locators.json: {e}")
        return False

    with allure.step("Click Settings"):
        try:
            settings_btn = wait.until(EC.presence_of_element_located((By.XPATH, settings_icon)))
            highlight_element(driver, settings_btn)
            settings_btn.click()
        except Exception as e:
            print("❌ Failed to click Settings")
            allure.attach(str(e), name="Settings Error", attachment_type=allure.attachment_type.TEXT)
            raise
    with allure.step("Click Not Applicable"):
        try:
            not_applicable = wait.until(EC.presence_of_element_located((By.XPATH, "//span[text()='Not Applicable tasks']")))
            highlight_element(driver, not_applicable)
            not_applicable.click()
            time.sleep(1)
        except Exception as e:
            print("❌ Failed to click not applicable")
            allure.attach(str(e), name="Not Applicable Error", attachment_type=allure.attachment_type.TEXT)
            raise
    with allure.step("Fetch the task name from the task list"):
        try:
            task_elem = wait.until(EC.presence_of_element_located((By.XPATH,"//div[@class='overflow-hidden whitespace-normal wrap-break-word']")))
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

            search_input = wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@placeholder='Search records...']")))
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
            task_elem = wait.until(EC.presence_of_element_located((By.XPATH,"//div[@class='overflow-hidden whitespace-normal wrap-break-word']")))
            highlight_element(driver, task_elem)
            first_task_name = task_elem.text.strip()
            if not first_task_name:
                first_task_name = task_elem.get_attribute("title").strip()
            if not first_task_name:
                raise Exception("Task name text is empty")
            print(f"🔹 Task Name: {first_task_name}")  
            allure.attach(first_task_name,  name="First Task Name", attachment_type=allure.attachment_type.TEXT)
        except Exception as e:
            print(f"❌ Failed to open Task Details: {e}")
            return False

    return True

    
    
