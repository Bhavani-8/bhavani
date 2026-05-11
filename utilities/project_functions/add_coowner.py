import allure
import json
import os
import time
import pytest
import pyautogui as pg
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from utilities.other_utils_functions.highlight import highlight_element
from selenium.common.exceptions import TimeoutException
from utilities.add_task_utils import wait_for_loader_to_disappear

   
def step_fail(driver, step_name, error):
    allure.attach(str(error), name=f"{step_name} Error", attachment_type=allure.attachment_type.TEXT)
    allure.attach(driver.get_screenshot_as_png(), name=f"{step_name} Screenshot", attachment_type=allure.attachment_type.PNG)
    pytest.fail(f"❌ {step_name} failed")
   
def add_coowner(driver, wait, project_name, coowner_name):

    with allure.step("Load locators.json"):
        try:
            with open(os.path.join("data", "locators.json"), "r") as f:
                elements_details = json.load(f)

            project_icon = elements_details["project_icon"]
            toast_msg = elements_details['toast_msg']

            print("✅ locators.json loaded")
        except Exception as e:
            step_fail(driver, "Load locators.json", e)
        
    with allure.step("Create New Project"):
        try:
            project_btn = wait.until(EC.presence_of_element_located((By.XPATH, project_icon)))
            highlight_element(driver, project_btn)
            project_btn.click()
            time.sleep(2)
        except Exception as e:
            allure.attach(str(e), "Project Create Error")
            return False

    with allure.step("Click the three dots menu for the task"):
        try:
            three_dots_btn = wait.until(EC.presence_of_element_located((By.XPATH, f"//tr[contains(@class,'dx-data-row')][.//div[@title='{project_name}']]//button")))
            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", three_dots_btn)
            highlight_element(driver, three_dots_btn)
            three_dots_btn.click()
        except Exception as e:
            step_fail(driver, "Click the three dots menu for the task", e)
    with allure.step("Click Add Co-owner or Add Button"):
        try:
            add_coowner_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@title='Add Co-owner']")))
            highlight_element(driver, add_coowner_btn)
            add_coowner_btn.click()
            print("👥 Add Co-owner clicked")

        except Exception as e:
            print("Add Co-owner not found, trying Add button...")

            try:
                add_btn = wait.until(EC.element_to_be_clickable((By.XPATH,"(//button[contains(@class,'project-management__small-icon-button')])[1]" )))
                highlight_element(driver, add_btn)
                add_btn.click()
                print("➕ Add User clicked (fallback option)")

            except Exception as e2:
                step_fail(driver, "Click Add Co-owner or Add Button", e2)
    with allure.step("Click Dropdown and Select Co-owner"):
        try:
            dropdown_btn = wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class,'css-1xc3v61-indicatorContainer')]")))
            highlight_element(driver, dropdown_btn)
            dropdown_btn.click()
            
            # select_input = wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(@id, 'react-select') and contains(text(),'Select user')]")))
            select_input = driver.switch_to.active_element
            highlight_element(driver, select_input)
            select_input.send_keys(coowner_name)
            time.sleep(1)
            
            coowner_option = wait.until(EC.element_to_be_clickable((By.XPATH, f"//div[contains(@class,'-option') and contains(.,'{coowner_name}')]")))
            highlight_element(driver, coowner_option)
            coowner_option.click()
        except Exception as e:
            step_fail(driver, "Click Dropdown and Select Co-owner", e)
    with allure.step("Click Add, Edit, Delete Checkbox"):
        try:
            add_checkbox = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@id='project-user-checkbox-add']")))
            highlight_element(driver, add_checkbox)
            add_checkbox.click()
            time.sleep(1)
            
            edit_checkbox = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@id='project-user-checkbox-edit']")))
            highlight_element(driver, edit_checkbox)
            edit_checkbox.click()
            time.sleep(1)

            delete_checkbox = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@id='project-user-checkbox-delete']")))
            highlight_element(driver, delete_checkbox)
            delete_checkbox.click()
            time.sleep(1)

            submit_btn = wait.until(EC.presence_of_element_located((By.XPATH, "//button//span[text()='Submit']")))
            highlight_element(driver, submit_btn)
            submit_btn.click()
            print("✔️ Submit clicked")
            time.sleep(3)

            # done_btn = wait.until(EC.presence_of_element_located((By.XPATH, "//button[contains(@class,'project-management__button') and contains(@class,'primary')]")))
            # highlight_element(driver, done_btn)
            # done_btn.click()
        except TimeoutException:
            print("⚠️ No options available — clicking Cancel")

            cancel_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Cancel']")))
            highlight_element(driver, cancel_btn)
            cancel_btn.click()
            print("❌ Selection cancelled because no options were found")

            done_btn = wait.until(EC.presence_of_element_located((By.XPATH, "//button//span[text()='Done']")))
            highlight_element(driver, done_btn)
            done_btn.click()
    with allure.step("Click the three dots menu from the project"):
        try:
            three_dots_btn = wait.until(EC.presence_of_element_located((By.XPATH, f"//tr[contains(@class,'dx-data-row')][.//div[@title='{project_name}']]//button")))
            driver.execute_script("arguments[0].scrollIntoView({block:'center', inline:'center'});", three_dots_btn)
            highlight_element(driver, three_dots_btn)
            three_dots_btn.click()
        except Exception as e:
            step_fail(driver, "Click the three dots menu from the project", e)
    with allure.step("Validate Co-owner Name and Permissions"):
        try:
            add_coowner_btn = wait.until(EC.presence_of_element_located((By.XPATH, "//button[@title='Add Co-owner']")))
            highlight_element(driver, add_coowner_btn)
            add_coowner_btn.click()
            print("👥 Add Co-owner clicked")

            coowner_name = wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@class='col-span-5 truncate']")))
            highlight_element(driver, coowner_name, 0.2)
            fetched_coowner_name = coowner_name.text.strip() 
            print(f"Co-owner Name: {fetched_coowner_name}")

            coowner_permissions =  wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@class='col-span-4 capitalize']")))
            highlight_element(driver, coowner_permissions, 0.2)
            fetched_coowner_permissions = coowner_permissions.text.strip()
            print(f"Permissions: {fetched_coowner_permissions}")
            time.sleep(1)

            # ✅ Allure Attach (TEXT)
            coowner_details = (f"Co-owner Name: {fetched_coowner_name}\n"f"Permissions: {fetched_coowner_permissions}")

            allure.attach(coowner_details,name="Co-owner Details",attachment_type=allure.attachment_type.TEXT)
    
        except Exception as e:
            step_fail(driver, "Validate Co-owner Name and Permissions", e)
            
    with allure.step("Click Done Button"):
        try:
            done_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button//span[text()='Done']")))
            highlight_element(driver, done_btn)
            done_btn.click()
            time.sleep(2)
        except Exception as e:
            step_fail(driver, "Click Done Button", e)
    

    return True
    