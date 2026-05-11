
import allure
import json
import os
import time
import pytest
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from utilities.other_utils_functions.highlight import highlight_element
from selenium.common.exceptions import TimeoutException
from utilities.add_task_utils import wait_for_loader_to_disappear

def step_fail(driver, step_name, error):
    allure.attach(str(error), name=f"{step_name} Error", attachment_type=allure.attachment_type.TEXT)
    allure.attach(driver.get_screenshot_as_png(), name=f"{step_name} Screenshot", attachment_type=allure.attachment_type.PNG)
    pytest.fail(f"❌ {step_name} failed")
   
def create_task_list(driver, wait, project_name, milestone, task_list):

    with allure.step("Load locators.json"):
        try:
            with open(os.path.join("data", "locators.json"), "r") as f:
                elements_details = json.load(f)

            project_icon = elements_details["project_icon"]
            toast_msg = elements_details['toast_msg']
            add_task_list = elements_details['add_task_list']
            task_list_input_elem = elements_details['task_list_input_elem']
            task_list_submit_btn = elements_details['task_list_submit_btn']
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
    with allure.step("Click Project Task"):
        try:
            time.sleep(1)
            project_task = wait.until(EC.presence_of_element_located((By.XPATH, f"//div[@class='w-full truncate' and contains(@title,'{project_name}')]")))
            driver.execute_script("arguments[0].scrollIntoView({block:'center', inline:'center'});", project_task)
            highlight_element(driver, project_task)
            project_task.click()
            time.sleep(2)
        except Exception as e:
            step_fail(driver, "Click Project Task", e)

    with allure.step("Click three dots menu"):
        try:
            milestone_btn = wait.until(EC.presence_of_element_located((By.XPATH, f"//tr[contains(@class,'dx-data-row')][.//div[@title='{milestone}']]//button[contains(@class,'ant-btn-icon-only')]")))
            driver.execute_script("arguments[0].scrollIntoView({block:'center', inline:'center'});", milestone_btn)
            highlight_element(driver, milestone_btn)
            # driver.execute_script("arguments[0].click();", three_dots_btn)
            milestone_btn.click()
            time.sleep(2)
        except Exception as e:
            step_fail(driver, "Click three dots menu", e)
            
    with allure.step("Click 'Add Tasklist' button"):
        try:
            task_list_btn = wait.until(EC.presence_of_element_located((By.XPATH, add_task_list)))
            highlight_element(driver, task_list_btn)
            # task_list_btn.click
            driver.execute_script("arguments[0].click();", task_list_btn)
            time.sleep(3)
        except Exception as e:
            step_fail(driver, "Click 'Add Tasklist' button", e)

    with allure.step("Enter Task List Name"):
        try:
            task_list_input = wait.until(EC.presence_of_element_located((By.XPATH, task_list_input_elem)))
            highlight_element(driver, task_list_input)
            task_list_input.send_keys(task_list)
            time.sleep(3)
        except Exception as e:
            step_fail(driver, "Enter Task List Name", e)

    with allure.step("Submit Task List"):
        try:
            submit_btn = wait.until(EC.presence_of_element_located((By.XPATH, task_list_submit_btn)))
            highlight_element(driver, submit_btn)
            submit_btn.click()
            time.sleep(3)
            print("✅ Project Submit clicked")
        except Exception as e:
            step_fail(driver, "Submit Task List", e)
    
        try:
            toast = wait.until(EC.presence_of_element_located((By.XPATH, toast_msg)))
            highlight_element(driver, toast)
            print(f"📢 Toast message: {toast.text.strip()}")
            time.sleep(2)
        except Exception:
            print("❌ No toast message found")
    with allure.step("Click Dropdown Tasklist"):
        try:
            drop_down_task = wait.until(EC.presence_of_element_located((By.XPATH, f"//div[@title='{milestone}']/ancestor::tr//div[contains(@class,'dx-treelist-empty-space')]")))
            highlight_element(driver, drop_down_task)
            drop_down_task.click()
            time.sleep(3)
        except Exception as e:
            step_fail(driver, "Click Dropdown Tasklist", e)
        
    with allure.step("Verify Task List Creation"):
        try:
            task_list_in_list = wait.until(EC.visibility_of_element_located((By.XPATH, f"//div[contains(text(),'{task_list}')]")))
            highlight_element(driver, task_list_in_list)
            fetched_task_list_in_list = task_list_in_list.text.strip() 
            print(f"Task List Name: {fetched_task_list_in_list}")
        except Exception as e:
           step_fail(driver, "Verify Task List in List", e)

    with allure.step("Click Milestone Close Button"):
        try:
            close_btn = wait.until(EC.presence_of_element_located((By.XPATH, milestone_cancel_btn)))
            highlight_element(driver, close_btn)
            close_btn.click()
            time.sleep(2)
        except Exception as e:
            step_fail(driver, "Click Milestone Close Button", e)


   
    return True