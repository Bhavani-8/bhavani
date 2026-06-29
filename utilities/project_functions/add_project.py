import allure
import json
import os
import time
import pytest

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from utilities.other_utils_functions.highlight import highlight_element
from utilities.add_task_utils import wait_for_loader_to_disappear
from datetime import datetime
import random

def step_fail(driver, step_name, error):
    allure.attach(str(error), name=f"{step_name} Error", attachment_type=allure.attachment_type.TEXT)
    allure.attach(driver.get_screenshot_as_png(), name=f"{step_name} Screenshot", attachment_type=allure.attachment_type.PNG)
    pytest.fail(f"❌ {step_name} failed")
   
def create_project(driver, wait, project_name, project_description):

    with allure.step("Load locators.json"):
        try:
            with open(os.path.join("data", "locators.json"), "r") as f:
                elements_details = json.load(f)

            project_icon = elements_details["project_icon"]
            toast_msg = elements_details['toast_msg']
            add_new_project = elements_details['add_new_project']
            project_input_elem = elements_details['project_input_elem']
            project_submit_btn = elements_details['project_submit_btn']
            project_cancel_btn = elements_details['project_cancel_btn']
            project_description_text = elements_details['project_description_text']


            print("✅ locators.json loaded")
        except Exception as e:
            step_fail(driver, "Load locators.json", e)
        
    with allure.step("Click project icon"):
        try:
            project_btn = wait.until(EC.presence_of_element_located((By.XPATH, project_icon)))
            highlight_element(driver, project_btn)
            project_btn.click()
            time.sleep(3)
        except Exception as e:
           step_fail(driver, "Click project icon", e)
    with allure.step("Click 'Add New Project' button"):
        try:
            add_new_project_btn = wait.until(EC.element_to_be_clickable((By.XPATH, add_new_project)))
            highlight_element(driver, add_new_project_btn)
            driver.execute_script("arguments[0].click();", add_new_project_btn)
            time.sleep(1)
        except Exception as e:
           step_fail(driver, "Click 'Add New Project' button", e)
    #
    with allure.step("Enter Project Name"):
        try:
            project_input = wait.until(EC.presence_of_element_located((By.XPATH, project_input_elem)))
            highlight_element(driver, project_input)


            unique_project_name = f"{project_name}_{random.randint(1000, 9999)}"

            project_input.send_keys(unique_project_name)
            
            project_file = os.path.join("data", "latest_project.txt")
            with open(project_file, "w") as f:
                f.write(unique_project_name)

            print(f"Project Name Created: {unique_project_name}")

        except Exception as e:
            step_fail(driver, "Enter Project Name", e)

    with allure.step("Enter Project Description"):
        try:
            desc_input = wait.until(EC.presence_of_element_located((By.XPATH, project_description_text)))
            highlight_element(driver, desc_input)
            desc_input.send_keys(project_description)
            time.sleep(1)
        except Exception as e:
           step_fail(driver, "Enter Project Description", e)

    with allure.step("Click submit button"):
        try:
            submit_btn = wait.until(EC.presence_of_element_located((By.XPATH, project_submit_btn)))
            highlight_element(driver, submit_btn)
            submit_btn.click()
            wait_for_loader_to_disappear(driver, wait)
            time.sleep(2)
        except Exception as e:
              step_fail(driver, "Click submit button", e)
    
    with allure.step("Verify Toast Message"):
        try:
            toast_element = wait.until(EC.presence_of_element_located((By.XPATH, toast_msg)))
            highlight_element(driver, toast_element)
            toast_text = toast_element.text.strip()
            print(f"Toast Message: {toast_text}")
        except Exception as e:
            step_fail(driver, "Verify Toast Message", e)
        

    with allure.step("Verify project task"):
        try:
            project_task = wait.until(EC.presence_of_element_located((By.XPATH, f"//div[@class='w-full truncate' and contains(@title,'{unique_project_name}')]")))
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", project_task)
            time.sleep(0.5)                                                                   
            highlight_element(driver, project_task)
            fetched_project_in_list = project_task.text.strip() 
            print(f"Project Name: {fetched_project_in_list}")
        except Exception as e:
            step_fail(driver, "Select the latest project task", e)
    return True
   