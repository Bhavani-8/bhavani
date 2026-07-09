
import allure
import json
import os
import time
import pytest
import pandas as pd
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from utilities.other_utils_functions.highlight import highlight_element
from utilities.add_task_utils import wait_for_loader_to_disappear
from utilities.add_task_functions.format_time_if_valid import format_time_if_valid
from utilities.add_task_functions.format_date_if_valid import format_date_if_valid
from utilities.add_task_utils import add_task_check
from selenium.webdriver import ActionChains
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import TimeoutException


def step_fail(driver, step_name, error):
    allure.attach(str(error), name=f"{step_name} Error", attachment_type=allure.attachment_type.TEXT)
    allure.attach(driver.get_screenshot_as_png(), name=f"{step_name} Screenshot", attachment_type=allure.attachment_type.PNG)
    pytest.fail(f"❌ {step_name} failed")
   
def task_list_delete(driver, wait):

    with allure.step("Load locators.json"):
        try:
            with open(os.path.join("data", "locators.json"), "r") as f:
                elements_details = json.load(f)

            project_icon = elements_details["project_icon"]
            trash_icon = elements_details['trash_icon']
            milestone_confirm_btn = elements_details['milestone_confirm_btn']
            milestone_cancel_btn = elements_details['milestone_cancel_btn']
            task_list_submit_btn = elements_details['task_list_submit_btn']
            print("✅ locators.json loaded")
        except Exception as e:
            step_fail(driver, "Select HOD", e)
        
    with allure.step("Click project icon"):
        try:
            project_btn = wait.until(EC.presence_of_element_located((By.XPATH, project_icon)))
            highlight_element(driver, project_btn)
            project_btn.click()
            time.sleep(2)
        except Exception as e:
            step_fail(driver, "Click project icon", e)
    # ✅ FETCH TASK NAME BEFORE DELETE
    with allure.step("Click Project Task"):
        try:
            project_file = os.path.join("latest_data", "latest_project.txt")
            with open(project_file, "r") as f:
                created_project_name = f.read().strip()
            project_task = wait.until(EC.presence_of_element_located((By.XPATH, f"//div[@class='w-full truncate' and contains(@title,'{created_project_name}')]")))
            driver.execute_script("arguments[0].scrollIntoView({block:'center', inline:'center'});", project_task)
            highlight_element(driver, project_task)
            project_task.click()
            time.sleep(2)
        except Exception as e:
            step_fail(driver, "Click Project Task", e)
    with allure.step("Click 'Add New Milestone' button"):
        try:
            milestone_btn = wait.until(EC.presence_of_element_located((By.XPATH, "//button[@title='Add new milestone']")))
            highlight_element(driver, milestone_btn)
            milestone_btn.click()
        except Exception as e:
            step_fail(driver, "Click 'Add New Milestone' button", e)
    with allure.step("Enter Milestone Name"):
    
        try:
            milestone_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@id='milestone-title']")))
            highlight_element(driver, milestone_input)
            created_milestone = f"milestone_restore_check"
            milestone_input.send_keys(created_milestone)
            milestone_file = os.path.join("latest_data", "latest_milestone.txt")
            with open(milestone_file, "w") as f:
                f.write(created_milestone)

        except Exception as e:
           step_fail(driver, "Enter Milestone Name", e)
    with allure.step("Click Submit Milestone"):
        try:
            confirm_btn = wait.until(EC.presence_of_element_located((By.XPATH, milestone_confirm_btn)))
            highlight_element(driver, confirm_btn)
            confirm_btn.click()
            time.sleep(2)
            print("✅ Project Submit clicked")
        except Exception as e:
            step_fail(driver, "Submit Task List", e)

    with allure.step("Click three dots menu"):
        time.sleep(2)
        try:
            milestone_file = os.path.join("latest_data", "latest_milestone.txt")

            with open(milestone_file, "r") as f:
                created_milestone = f.read().strip()
            milestone_btn = wait.until(EC.presence_of_element_located((By.XPATH, f"//tr[contains(@class,'dx-data-row')][.//div[contains(@title,'{created_milestone}')]]//button[contains(@class,'ant-btn-icon-only')]")))
            driver.execute_script("arguments[0].scrollIntoView({block:'center', inline:'center'});", milestone_btn)
            highlight_element(driver, milestone_btn)
            milestone_btn.click()
        except Exception as e:
            step_fail(driver, "Click three dots menu", e)   
    with allure.step("Click 'Add Tasklist' button"):
        
        try:
            task_list_btn = wait.until(EC.presence_of_element_located((By.XPATH, "//button[@title='Add Tasklist']")))
            highlight_element(driver, task_list_btn)
            # task_list_btn.click
            driver.execute_script("arguments[0].click();", task_list_btn)
        except Exception as e:
            step_fail(driver, "Click 'Add Tasklist' button", e)
    with allure.step("Enter Task List Name"):
        
        
        try:
            task_list_input = wait.until(EC.presence_of_element_located((By.XPATH, "(//input[@class='modal-input'])[2]")))
            highlight_element(driver, task_list_input)
        
            created_task_list = f"task_list_delete_check"
            task_list_input.send_keys(created_task_list)
            task_list_file = os.path.join("latest_data", "latest_task_list.txt")
            with open(task_list_file, "w") as f:
                f.write(created_task_list)
           
        except Exception as e:
            step_fail(driver, "Enter Task List Name", e)
    with allure.step("Submit Task List"):
        try:
            submit_btn = wait.until(EC.presence_of_element_located((By.XPATH, task_list_submit_btn)))
            highlight_element(driver, submit_btn)
            submit_btn.click()
            time.sleep(2)
            print("✅ Project Submit clicked")
        except Exception as e:
            step_fail(driver, "Submit Task List", e)
    with allure.step("Click Dropdown Tasklist"):
        try:
            milestone_file = os.path.join("latest_data", "latest_milestone.txt")

            with open(milestone_file, "r") as f:
                created_milestone = f.read().strip()
            drop_down_task = wait.until(EC.presence_of_element_located((By.XPATH, f"//div[@title='{created_milestone}']/ancestor::tr//div[contains(@class,'dx-treelist-empty-space')]")))
            highlight_element(driver, drop_down_task)
            drop_down_task.click()
            time.sleep(3)
        except Exception as e:
            step_fail(driver, "Click Dropdown Tasklist", e)
    with allure.step("Verify Task List Creation"):
        try:
            task_list_file = os.path.join("latest_data", "latest_task_list.txt")

            with open(task_list_file, "r") as f:
                created_task_list = f.read().strip()
            task_list_elem = wait.until(EC.visibility_of_element_located((By.XPATH, f"//div[contains(text(),'{created_task_list}')]")))
            highlight_element(driver, task_list_elem)
            fetch_task_list = task_list_elem.text.strip()
            print(f"✅ Task List '{fetch_task_list}' created successfully")
        except Exception as e:
            step_fail(driver, "Verify Task List Creation", e)
    with allure.step("Click Task List three dots menu"):
        try:
            task_list_file = os.path.join("latest_data", "latest_task_list.txt")

            with open(task_list_file, "r") as f:
                created_task_list = f.read().strip()
            task_list_btn = wait.until(EC.presence_of_element_located((By.XPATH, f"//tr[contains(@class,'dx-data-row')][.//div[contains(@title,'{created_task_list}')]]//button[contains(@class,'ant-btn-icon-only')]")))
            driver.execute_script("arguments[0].scrollIntoView({block:'center', inline:'center'});", task_list_btn)
            highlight_element(driver, task_list_btn)
            task_list_btn.click()
        except Exception as e:
            step_fail(driver, "Click Task List three dots menu", e)
    
    with allure.step("Click Delete Task List Task"):
        try:
            delete_btn = wait.until(EC.presence_of_element_located((By.XPATH, "//button[@title='Delete']")))
            highlight_element(driver, delete_btn)
            delete_btn.click()
            print("🗑️ Delete button clicked")

            yes_btn = wait.until(EC.presence_of_element_located((By.XPATH,"//button//span[text()='Yes']")))
            highlight_element(driver, yes_btn)
            yes_btn.click()
            time.sleep(2)
        except Exception as e:
            step_fail(driver, "Click Delete Task List Task", e)
        
    with allure.step("Click Milestone close button on task details"):
        try:
            milestone_close_btn = wait.until(EC.presence_of_element_located((By.XPATH, milestone_cancel_btn)))
            highlight_element(driver, milestone_close_btn)
            milestone_close_btn.click()
            time.sleep(2)
        except Exception as e:
            step_fail(driver, "Click Milestone close button on task details", e)

    with allure.step("Click Trash Icon"):
        try:
            print()
            trash_btn = wait.until(EC.presence_of_element_located((By.XPATH, trash_icon)))
            highlight_element(driver, trash_btn)
            trash_btn.click()
        except Exception as e:
            step_fail(driver, "Click Trash Icon", e)
    
    with allure.step("Click Task List Tab"):
        try:
            time.sleep(3)
            task_list_tab = wait.until(EC.presence_of_element_located((By.XPATH, "//button[text()='Task Lists']")))
            highlight_element(driver, task_list_tab)
            task_list_tab.click()
        except Exception as e:
            step_fail(driver, "Click Task List Tab", e)
    with allure.step("Verify Deleted Task List in Trash"):
        try:
            task_list_file = os.path.join("latest_data", "latest_task_list.txt")

            with open(task_list_file, "r") as f:
                created_task_list = f.read().strip()
            
            task_list_in_trash = wait.until(EC.visibility_of_element_located((By.XPATH, f"//span[@title='{created_task_list}']")))
            highlight_element(driver, task_list_in_trash)
            fetch_task_list_in_trash = task_list_in_trash.text.strip()
            print(f"✅ Task List '{fetch_task_list_in_trash}' found in Trash")
        except Exception as e:
            step_fail(driver, "Verify Deleted Task List in Trash", e)

    with allure.step("Restore Deleted Task List"):
        try:
            time.sleep(3)
            task_list_file = os.path.join("latest_data", "latest_task_list.txt")

            with open(task_list_file, "r") as f:
                created_task_list = f.read().strip()
            restore_elem = wait.until(EC.presence_of_element_located((By.XPATH, f"//tr[@data-slot='table-row'][.//span[@title='{created_task_list}']]//button[@title='Restore Task List']")))
            actions = ActionChains(driver)
            actions.move_to_element(restore_elem).perform()
            highlight_element(driver, restore_elem)
            restore_elem.click()
            wait_for_loader_to_disappear(driver, wait)
            time.sleep(3)
        except Exception as e:
           step_fail(driver, "Restore Deleted Task", e)

    with allure.step("Click project icon again"):
        try:
            project_btn = wait.until(EC.presence_of_element_located((By.XPATH, project_icon)))
            highlight_element(driver, project_btn)
            project_btn.click()
            time.sleep(2)
        except Exception as e:
            step_fail(driver, "Click project icon again", e)
   
    with allure.step("Click Project Task"):
        try:
            time.sleep(1)
            project_file = os.path.join("latest_data", "latest_project.txt")
            with open(project_file, "r") as f:
                created_project_name = f.read().strip()
            project_task = wait.until(EC.presence_of_element_located((By.XPATH, f"//div[@class='w-full truncate' and contains(@title,'{created_project_name}')]")))
            driver.execute_script("arguments[0].scrollIntoView({block:'center', inline:'center'});", project_task)
            highlight_element(driver, project_task)
            project_task.click()
            time.sleep(2)
        except Exception as e:
            step_fail(driver, "Click Project Task", e)
    with allure.step("Click Dropdown Tasklist"):
        try:
            milestone_file = os.path.join("latest_data", "latest_milestone.txt")

            with open(milestone_file, "r") as f:
                created_milestone = f.read().strip()
            drop_down_task = wait.until(EC.presence_of_element_located((By.XPATH, f"//div[@title='{created_milestone}']/ancestor::tr//div[contains(@class,'dx-treelist-empty-space')]")))
            highlight_element(driver, drop_down_task)
            drop_down_task.click()
            time.sleep(3)
        except Exception as e:
            step_fail(driver, "Click Dropdown Tasklist", e)
    
    with allure.step("Click Task List three dots menu"):
        try:
            task_list_file = os.path.join("latest_data", "latest_task_list.txt")

            with open(task_list_file, "r") as f:
                created_task_list = f.read().strip()
            task_list_btn = wait.until(EC.presence_of_element_located((By.XPATH, f"//tr[contains(@class,'dx-data-row')][.//div[contains(@title,'{created_task_list}')]]//button[contains(@class,'ant-btn-icon-only')]")))
            driver.execute_script("arguments[0].scrollIntoView({block:'center', inline:'center'});", task_list_btn)
            highlight_element(driver, task_list_btn)
            task_list_btn.click()
            time.sleep(0.5)
        except Exception as e:
            step_fail(driver, "Click Task List three dots menu", e)
    with allure.step("Delete Task list task"):
        try:
            delete_btn = wait.until(EC.presence_of_element_located((By.XPATH, "//button[@title='Delete']")))
            highlight_element(driver, delete_btn)
            delete_btn.click()
            time.sleep(0.5)

            yes_btn = wait.until(EC.presence_of_element_located((By.XPATH, "//button//span[text()='Yes']")))
            highlight_element(driver, yes_btn)
            yes_btn.click()
            time.sleep(2)

        except Exception as e:
            step_fail(driver, "Click three dots menu", e)
    with allure.step("Click Milestone close button on task details"):
        try:
            milestone_close_btn = wait.until(EC.presence_of_element_located((By.XPATH, milestone_cancel_btn)))
            highlight_element(driver, milestone_close_btn)
            milestone_close_btn.click()
            time.sleep(1)
        except Exception as e:
            step_fail(driver, "Click Milestone close button on task details", e)
    
    return True