
import allure
import json
import os
import time
import pytest
from datetime import datetime
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from utilities.other_utils_functions.highlight import highlight_element
from selenium.common.exceptions import TimeoutException
from utilities.add_task_utils import wait_for_loader_to_disappear
import random

def step_fail(driver, step_name, error):
    allure.attach(str(error), name=f"{step_name} Error", attachment_type=allure.attachment_type.TEXT)
    allure.attach(driver.get_screenshot_as_png(), name=f"{step_name} Screenshot", attachment_type=allure.attachment_type.PNG)
    pytest.fail(f"❌ {step_name} failed")
   
def create_milestone(driver, wait, milestone):

    with allure.step("Load locators.json"):
        try:
            with open(os.path.join("data", "locators.json"), "r") as f:
                elements_details = json.load(f)

            project_icon = elements_details["project_icon"]
            add_new_milestone = elements_details['add_new_milestone']
            milestone_input_elem = elements_details['milestone_input_elem']
            milestone_confirm_btn = elements_details['milestone_confirm_btn']
            milestone_cancel_btn = elements_details['milestone_cancel_btn']

            print("✅ locators.json loaded")
        except Exception as e:
            step_fail(driver, "Load locators.json", e)
        
    with allure.step("Click project icon"):
        try:
            project_btn = wait.until(EC.presence_of_element_located((By.XPATH, project_icon)))
            highlight_element(driver, project_btn)
            project_btn.click()
            time.sleep(2)
        except Exception as e:
           step_fail(driver, "Click project icon", e)

    with allure.step("Select the latest project task"):
        try:
             # Read the project name created in create_project.py
            project_file = os.path.join("latest_data", "latest_project.txt")
            with open(project_file, "r") as f:
                created_project_name = f.read().strip()
            project_task = wait.until(EC.presence_of_element_located((By.XPATH, f"//div[@class='w-full truncate' and @title='{created_project_name}']")))
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", project_task)
            time.sleep(0.5)                                                                   
            highlight_element(driver, project_task)
            driver.execute_script("arguments[0].click();", project_task)
            time.sleep(2)
        except Exception as e:
            step_fail(driver, "Select the latest project task", e)
    with allure.step("Click 'Add New Milestone' button"):
        try:
            milestone_btn = wait.until(EC.presence_of_element_located((By.XPATH, add_new_milestone)))
            highlight_element(driver, milestone_btn)
            milestone_btn.click()
        except Exception as e:
            step_fail(driver, "Click 'Add New Milestone' button", e)
    with allure.step("Enter Milestone Name"):
        try:
            milestone_input = wait.until(EC.presence_of_element_located((By.XPATH, milestone_input_elem)))
            highlight_element(driver, milestone_input)
            unique_milestone = f"{milestone}_{random.randint(1000, 9999)}"
            # unique_milestone = f"{milestone}_{datetime.now().strftime('%H%M')}"
            milestone_input.send_keys(unique_milestone)
            milestone_file = os.path.join("latest_data", "latest_milestone.txt")
            with open(milestone_file, "w") as f:
                f.write(unique_milestone)

        except Exception as e:
           step_fail(driver, "Enter Milestone Name", e)
    with allure.step("Click Submit Milestone"):
        try:
            confirm_btn = wait.until(EC.presence_of_element_located((By.XPATH, milestone_confirm_btn)))
            highlight_element(driver, confirm_btn)
            confirm_btn.click()
            time.sleep(1)
            print("✅ Project Submit clicked")
        except Exception as e:
           step_fail(driver, "Click Submit", e) 
           
    
    with allure.step("Verify Milestone Creation"):
        try:
            milestone_in_list = wait.until(EC.visibility_of_element_located((By.XPATH, f"//div[contains(text(),'{unique_milestone}')]")))
            highlight_element(driver, milestone_in_list)
            fetched_milestone_in_list = milestone_in_list.text.strip() 
            print(f"Milestone Name: {fetched_milestone_in_list}")
        except Exception as e:
           step_fail(driver, "Verify Milestone in List", e) 

    with allure.step("Click Milestone close button on task details panel"):
        try:
            milestone_close_btn = wait.until(EC.presence_of_element_located((By.XPATH, milestone_cancel_btn)))
            highlight_element(driver, milestone_close_btn)
            milestone_close_btn.click()
            time.sleep(2)
        except Exception as e:
            step_fail(driver, "Click Milestone close button on task details panel", e)
    return True