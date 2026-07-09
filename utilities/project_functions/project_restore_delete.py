

import allure
import json
import os
import time
import pytest
import pyautogui as pg
import pandas as pd
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from utilities.other_utils_functions.highlight import highlight_element
from selenium.common.exceptions import TimeoutException
from utilities.add_task_utils import wait_for_loader_to_disappear
from selenium.webdriver import ActionChains
from utilities.add_task_functions.format_time_if_valid import format_time_if_valid
from utilities.add_task_functions.format_date_if_valid import format_date_if_valid
from utilities.add_task_utils import add_task_check

def step_fail(driver, step_name, error):
    allure.attach(str(error), name=f"{step_name} Error", attachment_type=allure.attachment_type.TEXT)
    allure.attach(driver.get_screenshot_as_png(), name=f"{step_name} Screenshot", attachment_type=allure.attachment_type.PNG)
    pytest.fail(f"❌ {step_name} failed")
   
def project_restore_delete(driver, wait):

    with allure.step("Load locators.json"):
        try:
            with open(os.path.join("data", "locators.json"), "r") as f:
                elements_details = json.load(f)

            project_icon = elements_details["project_icon"]
            toast_msg = elements_details['toast_msg']
            trash_icon = elements_details['trash_icon']

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
   
    with allure.step("Verify Project Task"):
        try:
            project_file = os.path.join("latest_data", "latest_project.txt")
            with open(project_file, "r") as f:
                created_project_name = f.read().strip()
            project_task = wait.until(EC.presence_of_element_located((By.XPATH, f"//div[contains(text(),'{created_project_name}')]")))
            highlight_element(driver, project_task)
            fetch_project_task = project_task.text.strip()
            print(f"✅ Project '{fetch_project_task}' verified")
        except Exception as e:
            step_fail(driver, "Verify Project Task", e) 

    with allure.step("Click Project three dots menu"):
        try:
            three_dots_btn = wait.until(EC.presence_of_element_located((By.XPATH, f"//tr[contains(@class,'dx-data-row')][.//div[@class='w-full truncate' and contains(@title,'{created_project_name}')]]//div[starts-with(@id,'context-menu-assignment-')]//button")))
            driver.execute_script("arguments[0].scrollIntoView({block:'center', inline:'center'});", three_dots_btn)
            highlight_element(driver, three_dots_btn)
            three_dots_btn.click()
            time.sleep(0.5)
        except Exception as e:
            step_fail(driver, "Click Project three dots menu", e)
    
    with allure.step("Click Delete Project"):
        try:
            delete_btn = wait.until(EC.presence_of_element_located((By.XPATH, "//button[@title='Delete']")))
            highlight_element(driver, delete_btn)
            delete_btn.click()
            print("🗑️ Delete button clicked")

            yes_btn = wait.until(EC.presence_of_element_located((By.XPATH,"//button//span[text()='Yes']")))
            highlight_element(driver, yes_btn)
            yes_btn.click()
            time.sleep(2)
            print("☑️ YES clicked — Task delete confirmed")

        except Exception as e:
            step_fail(driver, "Click Delete Project", e)
    
    with allure.step("Click Trash Icon"):
        try:
            print()
            trash_btn = wait.until(EC.presence_of_element_located((By.XPATH, trash_icon)))
            highlight_element(driver, trash_btn)
            trash_btn.click()
            print("🗑️ Trash icon clicked")

        except Exception as e:
            step_fail(driver, "Click Trash Icon", e)

    with allure.step("Click Projects Tab"):
        try:
            time.sleep(3)
            projects_tab = wait.until(EC.presence_of_element_located((By.XPATH, "//button[text()='Projects']")))
            highlight_element(driver, projects_tab)
            projects_tab.click()
            print("📌 Tasks tab clicked")
        except Exception as e:
            step_fail(driver, "Click Projects Tab", e)
    with allure.step("Verify Project Task"):
        try:
            project_file = os.path.join("latest_data", "latest_project.txt")
            with open(project_file, "r") as f:
                created_project_name = f.read().strip()
            project_elem = wait.until(EC.visibility_of_element_located((By.XPATH, f"//span[@title='{created_project_name}']")))
            highlight_element(driver, project_elem)
            fetch_project_elem = project_elem.text.strip()
            print(f"✅ Project '{fetch_project_elem}' created successfully")
        except Exception as e:
            step_fail(driver, "Verify Project Task", e) 
    
    with allure.step("Restore Deleted Task"):
        try:
            time.sleep(3)
            restore_elem = wait.until(EC.presence_of_element_located((By.XPATH, f"//tr[@data-slot='table-row'][.//span[@title='{created_project_name}']]//button[@title='Restore Project']")))
            actions = ActionChains(driver)
            actions.move_to_element(restore_elem).perform()
            highlight_element(driver, restore_elem)
            restore_elem.click()
            time.sleep(3)
            print("📌 Restore button clicked")

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
   
    with allure.step("Click Project three dots menu"):
        try:
            three_dots_btn = wait.until(EC.presence_of_element_located((By.XPATH, f"//tr[contains(@class,'dx-data-row')][.//div[@class='w-full truncate' and contains(@title,'{created_project_name}')]]//div[starts-with(@id,'context-menu-assignment-')]//button")))
            driver.execute_script("arguments[0].scrollIntoView({block:'center', inline:'center'});", three_dots_btn)
            highlight_element(driver, three_dots_btn)
            three_dots_btn.click()
            time.sleep(0.5)
        except Exception as e:
            step_fail(driver, "Click Project three dots menu", e)

    with allure.step("Click Delete Project"):
        try:
            delete_btn = wait.until(EC.presence_of_element_located((By.XPATH, "//button[@title='Delete']")))
            highlight_element(driver, delete_btn)
            delete_btn.click()
            time.sleep(0.5)
            print("🗑️ Delete button clicked")

            yes_btn = wait.until(EC.presence_of_element_located((By.XPATH,"//button//span[text()='Yes']")))
            highlight_element(driver, yes_btn)
            yes_btn.click()
            time.sleep(2)
            print("☑️ YES clicked — Task delete confirmed")

        except Exception as e:
            step_fail(driver, "Click Delete Project", e)

    
    return True