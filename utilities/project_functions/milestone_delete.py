
import allure
import json
import os
import time
import pytest
import pyautogui as pg
import random
import pandas as pd
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from utilities.other_utils_functions.highlight import highlight_element
from utilities.add_task_utils import wait_for_loader_to_disappear
from utilities.add_task_functions.format_time_if_valid import format_time_if_valid
from utilities.add_task_functions.format_date_if_valid import format_date_if_valid
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import StaleElementReferenceException


def step_fail(driver, step_name, error):
    allure.attach(str(error), name=f"{step_name} Error", attachment_type=allure.attachment_type.TEXT)
    allure.attach(driver.get_screenshot_as_png(), name=f"{step_name} Screenshot", attachment_type=allure.attachment_type.PNG)
    pytest.fail(f"❌ {step_name} failed")
   
def milestone_delete(driver, wait):

    with allure.step("Load locators.json"):
        try:
            with open(os.path.join("data", "locators.json"), "r") as f:
                elements_details = json.load(f)
            scroller_xpath = elements_details['scroller']
            project_icon = elements_details["project_icon"]
            trash_icon = elements_details['trash_icon']
            toast_msg = elements_details['toast_msg']
            column_chooser_btn = elements_details['column_chooser_btn']
            milestone_cancel_btn = elements_details['milestone_cancel_btn']
            print("✅ locators.json loaded")
        except Exception as e:
            step_fail(driver, "Load locators.json", e)
        
    with allure.step(" Click project icon"):
        try:
            project_btn = wait.until(EC.presence_of_element_located((By.XPATH, project_icon)))
            highlight_element(driver, project_btn)
            project_btn.click()
            time.sleep(3)
        except Exception as e:
            step_fail(driver, " Click project icon", e)
    
    with allure.step("Click Project Task"):
        try:
            time.sleep(1)
            project_file = os.path.join("data", "latest_project.txt")
            with open(project_file, "r") as f:
                created_project_name = f.read().strip()
            project_task = wait.until(EC.presence_of_element_located((By.XPATH, f"//div[@class='w-full truncate' and contains(@title,'{created_project_name}')]")))
            driver.execute_script("arguments[0].scrollIntoView({block:'center', inline:'center'});", project_task)
            highlight_element(driver, project_task)
            project_task.click()
            time.sleep(1)
        except Exception as e:
            step_fail(driver, "Click Project Task", e)
    
    with allure.step("Click 'Add New Milestone' button"):
        try:
            milestone_btn = wait.until(EC.presence_of_element_located((By.XPATH, "//button[@title='Add new milestone']")))
            highlight_element(driver, milestone_btn)
            milestone_btn.click()
            time.sleep(1)
        except Exception as e:
            step_fail(driver, "Click 'Add New Milestone' button", e)
    with allure.step("Enter Milestone Name"):
        # milestone = f"{milestone}_delete_check"
        try:
            milestone_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@id='milestone-title']")))
            highlight_element(driver, milestone_input)
            created_milestone = f"Milestone_delete_check"

            milestone_input.send_keys(created_milestone)
            milestone_file = os.path.join("data", "latest_milestone.txt")
            with open(milestone_file, "w") as f:
                f.write(created_milestone)

            print(f"Milestone Created: {created_milestone}")
        except Exception as e:
           step_fail(driver, "Enter Milestone Name", e)
    with allure.step("Click Submit Milestone"):
        try:
            submit_btn = wait.until(EC.presence_of_element_located((By.XPATH, "//button[normalize-space()='Confirm']")))
            highlight_element(driver, submit_btn)
            submit_btn.click()
            time.sleep(5)
        except TimeoutException:
            print("⚠️ Submit failed, trying Cancel...")     
            cancel_btn = wait.until(EC.presence_of_element_located((By.XPATH, "//button[normalize-space()='Cancel']")))
            highlight_element(driver, cancel_btn)
            cancel_btn.click()
    with allure.step("Verify Milestone Creation"):
        try:
            
            milestone_elem = wait.until(EC.visibility_of_element_located((By.XPATH, f"//div[contains(text(),'{created_milestone}')]")))
            highlight_element(driver, milestone_elem)
            fetch_milestone_elem = milestone_elem.text.strip()
            print(f"✅ Milestone '{fetch_milestone_elem}' created successfully")
            milestone_file = os.path.join("data", "latest_milestone.txt")

            with open(milestone_file, "w") as f:
                f.write(created_milestone)
        except Exception as e:
            step_fail(driver, "Verify Milestone Creation", e)  
    with allure.step("Click three dots menu"):
        time.sleep(7)
        try:
            milestone_file = os.path.join("data", "latest_milestone.txt")

            with open(milestone_file, "r") as f:
                created_milestone = f.read().strip()
            milestone_btn = wait.until(EC.presence_of_element_located((By.XPATH, f"//tr[contains(@class,'dx-data-row')][.//div[contains(@title,'{created_milestone}')]]//button[contains(@class,'ant-btn-icon-only')]")))
            driver.execute_script("arguments[0].scrollIntoView({block:'center', inline:'center'});", milestone_btn)
            highlight_element(driver, milestone_btn)
            milestone_btn.click()
        except Exception as e:
            step_fail(driver, "Click three dots menu", e)
    with allure.step("Click Delete Milestone"):
        try:
            delete_btn = wait.until(EC.presence_of_element_located((By.XPATH, "//button[@title='Delete']")))
            highlight_element(driver, delete_btn)
            delete_btn.click()
            print("🗑️ Delete button clicked")

            yes_btn = wait.until(EC.presence_of_element_located((By.XPATH,"//button//span[text()='Yes']")))
            highlight_element(driver, yes_btn)
            yes_btn.click()
            time.sleep(2)
            print("☑️ YES clicked — Milestone delete confirmed")

        except Exception as e:
            step_fail(driver, "Click Delete Milestone", e)
        
    with allure.step("Click Milestone close button on task details panel"):
        try:
            milestone_close_btn = wait.until(EC.presence_of_element_located((By.XPATH, milestone_cancel_btn)))
            highlight_element(driver, milestone_close_btn)
            milestone_close_btn.click()
            time.sleep(2)
            print("✅ Milestone Submit clicked")
        except Exception as e:
            step_fail(driver, "Click Milestone close button on task details panel", e)

    with allure.step("Click Trash Icon"):
        try:
            print()
            trash_btn = wait.until(EC.presence_of_element_located((By.XPATH, trash_icon)))
            highlight_element(driver, trash_btn)
            trash_btn.click()
        except Exception as e:
            step_fail(driver, "Click Trash Icon", e)
    
    with allure.step("Click Milestone Tab"):
        try:
            time.sleep(3)
            milestone_tab = wait.until(EC.presence_of_element_located((By.XPATH, "//button[text()='Milestones']")))
            highlight_element(driver, milestone_tab)
            milestone_tab.click()
            print("📌 Milestone tab clicked")
        except Exception as e:
            step_fail(driver, "Click Milestone Tab", e)
    with allure.step("Verify Deleted Milestone in Trash"):
        try:
            milestone_file = os.path.join("data", "latest_milestone.txt")

            with open(milestone_file, "r") as f:
                created_milestone = f.read().strip()
            milestone_in_trash = wait.until(EC.visibility_of_element_located((By.XPATH, f"//span[@title='{created_milestone}']")))
            highlight_element(driver, milestone_in_trash)
            fetch_milestone_in_trash = milestone_in_trash.text.strip()
            print(f"✅ Milestone '{fetch_milestone_in_trash}' found in Trash")
        except Exception as e:
            step_fail(driver, "Verify Deleted Milestone in Trash", e)

    with allure.step("Restore Deleted Milestone"):
        try:
            time.sleep(3)
            milestone_file = os.path.join("data", "latest_milestone.txt")

            with open(milestone_file, "r") as f:
                created_milestone = f.read().strip()
            restore_elem = wait.until(EC.presence_of_element_located((By.XPATH, f"//tr[@data-slot='table-row'][.//span[@title='{created_milestone}']]//button[@title='Restore Milestone']")))
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
            project_file = os.path.join("data", "latest_project.txt")
            with open(project_file, "r") as f:
                created_project_name = f.read().strip()
            project_task = wait.until(EC.presence_of_element_located((By.XPATH, f"//div[@class='w-full truncate' and contains(@title,'{created_project_name}')]")))
            driver.execute_script("arguments[0].scrollIntoView({block:'center', inline:'center'});", project_task)
            highlight_element(driver, project_task)
            project_task.click()
            time.sleep(2)
        except Exception as e:
            step_fail(driver, "Click Project Task", e)
    
    with allure.step("Click three dots menu"):
        try:
            time.sleep(5)
            milestone_file = os.path.join("data", "latest_milestone.txt")

            with open(milestone_file, "r") as f:
                created_milestone = f.read().strip()
            milestone_btn = wait.until(EC.presence_of_element_located((By.XPATH, f"//tr[contains(@class,'dx-data-row')][.//div[contains(@title,'{created_milestone}')]]//button[contains(@class,'ant-btn-icon-only')]")))
            driver.execute_script("arguments[0].scrollIntoView({block:'center', inline:'center'});", milestone_btn)
            highlight_element(driver, milestone_btn)
            milestone_btn.click()
        except Exception as e:
            step_fail(driver, "Click three dots menu", e)
    with allure.step("Click Delete Milestone"):
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
            step_fail(driver, "Click Delete Milestone", e)
    with allure.step("Click Milestone close button on task details"):
        try:
            milestone_close_btn = wait.until(EC.presence_of_element_located((By.XPATH, milestone_cancel_btn)))
            highlight_element(driver, milestone_close_btn)
            milestone_close_btn.click()
        except Exception as e:
            step_fail(driver, "Click Milestone close button on task details", e)
    
    return True