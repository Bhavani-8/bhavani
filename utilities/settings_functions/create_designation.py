

import allure
import os
import json
import time
import pytest

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from utilities.other_utils_functions.highlight import highlight_element
from utilities.add_task_utils import wait_for_loader_to_disappear
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import ActionChains


def step_fail(driver, step_name, error):
    allure.attach(str(error), name=f"{step_name} Error", attachment_type=allure.attachment_type.TEXT)
    allure.attach(driver.get_screenshot_as_png(), name=f"{step_name} Screenshot", attachment_type=allure.attachment_type.PNG)
    pytest.fail(f"❌ {step_name} failed")

def create_designation(driver, wait, designation_name, designation_alias, description, hod_name):

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
            settings_btn = wait.until(EC.presence_of_element_located((By.XPATH, settings_icon)))
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

    with allure.step("Click on Department"):
        try:
            designation_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[normalize-space(text())='designation']")))
            highlight_element(driver, designation_btn)
            designation_btn.click()
        except Exception as e:
            step_fail(driver, "Click Designation", e)

    with allure.step("Click on Create Designation"):
        try:
            create_designation_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Create Designation']")))
            highlight_element(driver, create_designation_btn)
            create_designation_btn.click()
        except Exception as e:
            step_fail(driver, "Click Create Designation", e)

    with allure.step("Enter Designation Name"):
        try:
            designation_input = wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@name='designation_name']")))
            highlight_element(driver, designation_input)
            designation_input.clear()
            designation_input.send_keys(designation_name)
        except Exception as e:
            step_fail(driver, "Enter Designation Name", e)

    with allure.step("Enter Designation Alias"):
        try:
            alias_input = wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@name='designation_alias']")))
            highlight_element(driver, alias_input)
            alias_input.clear()
            alias_input.send_keys(designation_alias)
        except Exception as e:
            step_fail(driver, "Enter Designation Alias", e)

    with allure.step("Enter Description"):
        try:
            description_input = wait.until(EC.visibility_of_element_located((By.XPATH, "//textarea[@name='reason']")))
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", description_input)
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

    print("🎉 Designation created successfully")
    with allure.step("Fetch Designation Name from Designation Tab"):
        designation_elem = wait.until(EC.visibility_of_element_located((By.XPATH, f"//div[contains(@class,'_wordWrap')]//p[@title='{designation_alias}']")))
        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", designation_elem)
        highlight_element(driver, designation_elem, 0.2)
        fetched_designation = designation_elem.text.strip()
        print(f"Designation Name from Designation: {fetched_designation}")
        allure.attach(fetched_designation,name="Designation Name",attachment_type=allure.attachment_type.TEXT)
    with allure.step("Click on Team Members"):
        try:
            team_members_btn = wait.until(EC.presence_of_element_located((By.XPATH, "//span[text()='Team Members']")))
            highlight_element(driver, team_members_btn)
            team_members_btn.click()
            time.sleep(3)
        except Exception as e:
            step_fail(driver, "Click Team Members", e)
   
    with allure.step("Click Three Dots of Team Member"):
        try:
            scroll_container = wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class,'dx-scrollable-container')]")))
            # Scroll completely to right
            driver.execute_script("arguments[0].scrollLeft = arguments[0].scrollWidth;",scroll_container)
            click_three_dots_btn = wait.until(EC.element_to_be_clickable((By.XPATH, f"//tr[.//div[@title='{hod_name}']]//button")))
            highlight_element(driver, click_three_dots_btn)
            click_three_dots_btn.click()

            edit_department_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[normalize-space()='Edit Department']")))
            highlight_element(driver, edit_department_btn)
            edit_department_btn.click()
        except Exception as e:
            step_fail(driver, "Add Department to Team Members", e)
    # with allure.step("Select Department"):
    #     try:
    #         department_dropdown = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@class,'control') and .//div[text()='Select department...']]")))
    #         highlight_element(driver, department_dropdown)
    #         department_dropdown.click()

    #         department_input = driver.switch_to.active_element
    #         department_input.send_keys(department_name)
    #         time.sleep(1)

    #         department_option = wait.until(EC.element_to_be_clickable((By.XPATH, f"//div[contains(@class, '-option') and text()='{department_name}']")))
    #         highlight_element(driver, department_option)
    #         department_option.click()

    #         # update_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@type='button' and normalize-space()='Update']")))
    #         # highlight_element(driver, update_btn)   
    #         # update_btn.click()
    #         # time.sleep(1)
    #     except Exception as e:
    #         step_fail(driver, "Select Designation", e)
    with allure.step("Select Department"):
        try:
            designation_dropdown = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@class,'control') and .//div[text()='Select designation...']]")))
            highlight_element(driver, designation_dropdown)
            designation_dropdown.click()

            designation_input = driver.switch_to.active_element
            designation_input.send_keys(designation_name)
            time.sleep(1)

            designation_option = wait.until(EC.element_to_be_clickable((By.XPATH, f"//div[contains(@class, '-option') and text()='{designation_name}']")))
            highlight_element(driver, designation_option)
            designation_option.click()

            update_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@type='button' and normalize-space()='Update']")))
            highlight_element(driver, update_btn)   
            update_btn.click()
            time.sleep(1)
        except Exception as e:
            step_fail(driver, "Select Designation", e)
    with allure.step("Click on Team Members"):
        try:
            team_members_btn = wait.until(EC.presence_of_element_located((By.XPATH, "//span[text()='Team Members']")))
            highlight_element(driver, team_members_btn)
            team_members_btn.click()
        except Exception as e:
            step_fail(driver, "Click Team Members", e)
    wait_for_loader_to_disappear(driver, wait)
    time.sleep(3)

    with allure.step("Fetch Designation Name from Team Members Tab"):
        team_member_designation_elem = wait.until(EC.visibility_of_element_located((By.XPATH, f"//tr[.//div[normalize-space()='{hod_name}']]/td[@aria-colindex='4']")))
        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", team_member_designation_elem)
        highlight_element(driver, team_member_designation_elem, 0.2)
        fetched_team_member_designation = team_member_designation_elem.text.strip()
        print(f"Designation Name from Team Members Tab: {fetched_team_member_designation}")
        allure.attach(fetched_team_member_designation,name="Designation Name",attachment_type=allure.attachment_type.TEXT)
    
    with allure.step("Verify Designation Name in Designation Tab and Team Members Tab"):
        if fetched_designation == fetched_team_member_designation:
            print("✅ Designation Name Verified successfully!")
            allure.attach(f"Verified Designation Name: {fetched_team_member_designation}",name="Designation Name Check",attachment_type=allure.attachment_type.TEXT)
            time.sleep(2)
            return True
        else:
            print(f"❌ Designation Name Mismatch! Grid: {fetched_designation}, Team Members Tab: {fetched_team_member_designation}")
            allure.attach(f"Grid: {fetched_designation}\nTeam Members Tab: {fetched_team_member_designation}",name="Designation Name Mismatch",attachment_type=allure.attachment_type.TEXT)
            step_fail(driver, "Verify Designation name in designation tab and Team Members Tab", e)
    
    return True



