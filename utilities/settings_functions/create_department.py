import allure
import os
import json
import time
import pyautogui as pg
import pytest
import random

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains

from utilities.other_utils_functions.highlight import highlight_element
from selenium.common.exceptions import TimeoutException
from utilities.add_task_utils import wait_for_loader_to_disappear

def step_fail(driver, step_name, error):
    allure.attach(str(error), name=f"{step_name} Error", attachment_type=allure.attachment_type.TEXT)
    allure.attach(driver.get_screenshot_as_png(), name=f"{step_name} Screenshot", attachment_type=allure.attachment_type.PNG)
    pytest.fail(f"❌ {step_name} failed")

def create_department(driver, wait, company_name, department_name, hod_name, alias, description):

    with allure.step("Load locators.json"):
        try:
            with open(os.path.join("data", "locators.json"), "r") as f:
                elements_details = json.load(f)
            settings_icon = elements_details["settings_icon"]
            toast_msg = elements_details["toast_msg"]
        except Exception as e:
            step_fail(driver, "Load locators.json", e)

    with allure.step("Click Settings"):
        try:
            settings_btn = wait.until(EC.element_to_be_clickable((By.XPATH, settings_icon)))
            highlight_element(driver, settings_btn)
            settings_btn.click()
        except Exception as e:
            step_fail(driver, "Click Settings", e)

    with allure.step("Click on Department"):
        try:
            department_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[normalize-space()='Department']")))
            highlight_element(driver, department_btn)
            department_btn.click()
        except Exception as e:
            step_fail(driver, "Click Department", e)
    wait_for_loader_to_disappear(driver, wait)
    time.sleep(2)

    with allure.step("Click on Create Department"):
        try:
            create_department_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Create Department']")))
            highlight_element(driver, create_department_btn)
            create_department_btn.click()
            time.sleep(2)
        except Exception as e:
            step_fail(driver, "Click Create Department", e)

    with allure.step("Select Company"):
        try:
            company_file = os.path.join("data", "latest_company.txt")
            with open(company_file, "r") as f:
                created_company_name = f.read().strip()
            company_dropdown = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@role='combobox' and .//span[normalize-space()='Select Company']]")))
            highlight_element(driver, company_dropdown)
            company_dropdown.click()
            
            company_option = wait.until(EC.element_to_be_clickable((By.XPATH,f"//div[normalize-space()='{created_company_name}']")))
            driver.execute_script("arguments[0].scrollIntoView({block:'center'});",company_option)

            highlight_element(driver, company_option)
            company_option.click()

            print(f"✅ Selected Company: {created_company_name}")

        except Exception as e:
            step_fail(driver, "Select Company", e)

    with allure.step("Enter Department Name"):
        try:
            
           
            department_input = wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@name='department_name']")))
            highlight_element(driver, department_input)
            department_input.clear()
            department_input.send_keys(department_name)
            
        except Exception as e:
            step_fail(driver, "Enter Department Name", e)

    with allure.step("Select HOD"):
        try:
            hod_dropdown = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@role='combobox' and .//span[normalize-space()='Select HOD']]")))
            highlight_element(driver, hod_dropdown)
            hod_dropdown.click()

             
            hod_input = wait.until(EC.element_to_be_clickable((By.XPATH,f"//div[normalize-space()='{hod_name}']")))
            driver.execute_script("arguments[0].scrollIntoView({block:'center'});",hod_input)

            highlight_element(driver, hod_input)
            hod_input.click()
            
        except Exception as e:
            step_fail(driver, "Select HOD", e)

    with allure.step("Enter Department Alias"):
        try:
            alias_input = wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@name='department_alias']")))
            highlight_element(driver, alias_input)
            alias_input.clear()
            alias_input.send_keys(alias)
        except Exception as e:
            step_fail(driver, "Enter Department Alias", e)

    with allure.step("Enter Description"):
        try:
            description_input = wait.until(EC.visibility_of_element_located((By.XPATH, "//textarea[@name='description']")))
            ActionChains(driver).move_to_element(description_input).perform()
            highlight_element(driver, description_input)
            description_input.clear()
            description_input.send_keys(description)
        except Exception as e:
            step_fail(driver, "Enter Description", e)

    with allure.step("Click Save"):
        try:
            save_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Save']")))
            highlight_element(driver, save_btn)
            save_btn.click()
            time.sleep(3)
        except TimeoutException:
            print("⚠️ No options available — clicking Cancel")
            cancel_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Cancel']")))
            highlight_element(driver, cancel_btn)
            cancel_btn.click()
            time.sleep(1)
    with allure.step("Toast Msg"):
        try:
            toast = wait.until(EC.presence_of_element_located((By.XPATH, toast_msg)))
            highlight_element(driver, toast)
            print(f"📢 Toast message: {toast.text.strip()}")
            time.sleep(6)
        except Exception as e:
            step_fail(driver, "Toast Message Verification", e)

    with allure.step("Fetch Department Name from Department Tab"):
        department_elem = wait.until(EC.visibility_of_element_located((By.XPATH, f"//td[normalize-space()='{created_company_name}']/following-sibling::td[3]")))
        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", department_elem)
        highlight_element(driver, department_elem, 0.2)
        fetched_department = department_elem.text.strip()
        print(f"Department Name from Department: {fetched_department}")
        allure.attach(fetched_department,name="Department Name",attachment_type=allure.attachment_type.TEXT)

    with allure.step("Click on Team Members"):
        try:
            team_members_btn = wait.until(EC.presence_of_element_located((By.XPATH, "//span[text()='Team Members']")))
            highlight_element(driver, team_members_btn)
            team_members_btn.click()
        except Exception as e:
            step_fail(driver, "Click Team Members", e)
    wait_for_loader_to_disappear(driver, wait)
    time.sleep(3)

    with allure.step("Fetch Department Name from Team Members Tab"):
        team_member_department_elem = wait.until(EC.visibility_of_element_located((By.XPATH, f"//tr[.//div[normalize-space()='{hod_name}']]//td[@aria-colindex='3']")))
        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", team_member_department_elem)
        highlight_element(driver, team_member_department_elem, 0.2)
        fetched_team_member_department = team_member_department_elem.text.strip()
        print(f"Department Name from Team Members Tab: {fetched_team_member_department}")
        allure.attach(fetched_team_member_department,name="Department Name",attachment_type=allure.attachment_type.TEXT)
    
    with allure.step("Verify Department Name in Department Tab and Team Members Tab"):
        if fetched_department == fetched_team_member_department:
            print("✅ Department Name Verified successfully!")
            allure.attach(f"Verified Department Name: {fetched_team_member_department}",name="Department Name Check",attachment_type=allure.attachment_type.TEXT)
            time.sleep(2)
            return True
        else:
            print(f"❌ Department Name Mismatch! Department Alias: {fetched_department}, Team Members Department: {fetched_team_member_department}")
            allure.attach(f"Department Alias: {fetched_department}\nTeam Members Department: {fetched_team_member_department}",name="Department Name Mismatch",attachment_type=allure.attachment_type.TEXT)
            return False
    
    return True
