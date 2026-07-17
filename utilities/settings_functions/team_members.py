import allure
import os
import json
import time
import pytest

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from utilities.other_utils_functions.highlight import highlight_element
from utilities.add_task_utils import wait_for_loader_to_disappear


def step_fail(driver, step_name, error):
    allure.attach(str(error), name=f"{step_name} Error", attachment_type=allure.attachment_type.TEXT)
    allure.attach(driver.get_screenshot_as_png(), name=f"{step_name} Screenshot", attachment_type=allure.attachment_type.PNG)
    pytest.fail(f"❌ {step_name} failed")

def invite_team_member(driver, wait, full_name, email, role, department_name, designation_name, full_name_2, email_2):
    with allure.step("Load locators.json"):
        try:
            with open(os.path.join("data", "locators.json"), "r") as f:
                elements_details = json.load(f)
            settings_icon = elements_details["settings_icon"]
            toast_msg = elements_details["toast_msg"]
            print("✅ locators.json loaded successfully")
        except Exception as e:
            allure.attach(str(e), name="Locators Load Error", attachment_type=allure.attachment_type.TEXT)
            return False
    
    with allure.step("Click Settings"):
        try:
            settings_btn = wait.until(EC.element_to_be_clickable((By.XPATH, settings_icon)))
            highlight_element(driver, settings_btn)
            settings_btn.click()
        except Exception as e:
            step_fail(driver, "Click Settings", e)
    
    with allure.step("Click on Team Members"):
        try:
            team_members_btn = wait.until(EC.presence_of_element_located((By.XPATH, "//span[text()='Team Members']")))
            highlight_element(driver, team_members_btn)
            team_members_btn.click()
        except Exception as e:
            step_fail(driver, "Click Team Members", e)
    wait_for_loader_to_disappear(driver, wait)
    time.sleep(3)

    with allure.step("Click on Add New Button"):
        try:
            add_new_btn = wait.until(EC.presence_of_element_located((By.XPATH, "//button[normalize-space()='Add New']")))
            highlight_element(driver, add_new_btn)
            add_new_btn.click()
        except Exception as e:
           step_fail(driver, "Click Add New Button", e)
    
    with allure.step("Click on Create Department"):
        try:
            full_name_elem = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@name='full_name']")))
            highlight_element(driver, full_name_elem)
            full_name_elem.send_keys(full_name)
        except Exception as e:
            step_fail(driver, "Click Department", e)

    with allure.step("Enter Designation"):
        try:
            email_elem = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@name='email']")))
            highlight_element(driver,  email_elem)
            email_elem.send_keys(email)
            print("✅ Designation name entered")
        except Exception as e:
            step_fail(driver, "Enter Designation", e)
   

    with allure.step("Enter role(s)"):
        try:
            # Convert Excel value into list (handles single or multiple)
            if isinstance(role, str):
                cleaned_role = role.strip().strip("{}")  # remove { }
                role_list = [r.strip() for r in cleaned_role.split(",") if r.strip()]
            elif isinstance(role, list):
                role_list = role
            else:
                role_list = [str(role).strip()]

            print(f"➡️ Roles to select: {role_list}")

            for role_name in role_list:
                # Open dropdown each time (React dropdown closes after selection)
                role_dropdown = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@class,'control') and .//div[text()='Select role...']]")))
                highlight_element(driver, role_dropdown)
                role_dropdown.click()

                role_input = driver.switch_to.active_element
                role_input.clear()
                role_input.send_keys(role_name)
                time.sleep(1)

                role_option = wait.until(EC.element_to_be_clickable((By.XPATH, f"//div[contains(@class,'option') and normalize-space()='{role_name}']")))
                highlight_element(driver, role_option)
                role_option.click()

                print(f"✅ Role selected: {role_name}")
                time.sleep(0.5)

        except Exception as e:
            step_fail(driver, "Enter role(s)", e)


    with allure.step("Enter Department"):
        try:
            department_dropdown = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@class,'control') and .//div[text()='Select department...']]")))
            time.sleep(0.5)
            highlight_element(driver, department_dropdown)
            department_dropdown.click()

            department_input = driver.switch_to.active_element
            department_input.send_keys(department_name)
            time.sleep(1)

            department_option = wait.until(EC.element_to_be_clickable((By.XPATH, f"//div[contains(@class,'option') and normalize-space()='{department_name}']")))
            highlight_element(driver, department_option)
            department_option.click()
        except Exception as e:
            step_fail(driver, "Enter Department", e)
    with allure.step("Enter Description"):
        try:
            designation_dropdown = wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class,'control') and .//div[text()='Select designation...']]")))
            time.sleep(0.5)
            highlight_element(driver,designation_dropdown)
            designation_dropdown.click()

            designation_input = driver.switch_to.active_element
            designation_input.send_keys(designation_name)
            time.sleep(1)

            designation_option = wait.until(EC.element_to_be_clickable((By.XPATH, f"//div[contains(@class,'option') and normalize-space()='{designation_name}']")))
            highlight_element(driver, designation_option)
            designation_option.click()
        except Exception as e:
            step_fail(driver, "Enter Description", e)

    with allure.step("Click on Invite Button"):
        try:
            invite_btn = wait.until(EC.presence_of_element_located((By.XPATH, "//button[.//span[text()='Invite']]")))
            highlight_element(driver,  invite_btn)
            invite_btn.click()
            wait_for_loader_to_disappear(driver, wait)
            print("✅ Save button clicked")
            time.sleep(5)
        except Exception as e:
            step_fail(driver, "Click Invite Button", e)
    with allure.step("Toast Msg"):
        try:
            toast = wait.until(EC.presence_of_element_located((By.XPATH, toast_msg)))
            highlight_element(driver, toast)
            print(f"📢 Toast message: {toast.text.strip()}")
            time.sleep(6)
        except Exception as e:
            step_fail(driver, "Toast Message Verification", e)
    with allure.step("Click on Add New Button"):
        try:
            add_new_btn = wait.until(EC.presence_of_element_located((By.XPATH, "//button[normalize-space()='Add New']")))
            highlight_element(driver, add_new_btn)
            add_new_btn.click()
        except Exception as e:
           step_fail(driver, "Click Add New Button", e)
    
    with allure.step("Click on Create Department"):
        try:
            full_name_elem = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@name='full_name']")))
            highlight_element(driver, full_name_elem)
            full_name_elem.send_keys(full_name_2)
        except Exception as e:
            step_fail(driver, "Click Department", e)

    with allure.step("Enter Designation"):
        try:
            email_elem = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@name='email']")))
            highlight_element(driver,  email_elem)
            email_elem.send_keys(email_2)
            print("✅ Designation name entered")
        except Exception as e:
            step_fail(driver, "Enter Designation", e)
   
    with allure.step("Enter role(s)"):
        try:
            # Convert Excel value into list (handles single or multiple)
            if isinstance(role, str):
                cleaned_role = role.strip().strip("{}")  # remove { }
                role_list = [r.strip() for r in cleaned_role.split(",") if r.strip()]
            elif isinstance(role, list):
                role_list = role
            else:
                role_list = [str(role).strip()]

            print(f"➡️ Roles to select: {role_list}")

            for role_name in role_list:
                # Open dropdown each time (React dropdown closes after selection)
                role_dropdown = wait.until(
                    EC.element_to_be_clickable((By.XPATH, "//div[contains(@class,'control') and .//div[text()='Select role...']]"))
                )
                highlight_element(driver, role_dropdown)
                role_dropdown.click()

                role_input = driver.switch_to.active_element
                role_input.clear()
                role_input.send_keys(role_name)
                time.sleep(1)

                role_option = wait.until(
                    EC.element_to_be_clickable((By.XPATH, f"//div[contains(@class,'option') and normalize-space()='{role_name}']"))
                )
                highlight_element(driver, role_option)
                role_option.click()

                print(f"✅ Role selected: {role_name}")
                time.sleep(0.5)

        except Exception as e:
            step_fail(driver, "Enter role(s)", e)


    with allure.step("Enter Department"):
        try:
            department_dropdown = wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class,'control') and .//div[text()='Select department...']]")))
            time.sleep(0.5)
            highlight_element(driver, department_dropdown)
            department_dropdown.click()

            department_input = driver.switch_to.active_element
            department_input.send_keys(department_name)
            time.sleep(1)

            department_option = wait.until(EC.presence_of_element_located((By.XPATH, f"//div[contains(@class,'option') and normalize-space()='{department_name}']")))
            highlight_element(driver, department_option)
            department_option.click()
        except Exception as e:
            step_fail(driver, "Enter Department", e)
    with allure.step("Enter Description"):
        try:
            designation_dropdown = wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class,'control') and .//div[text()='Select designation...']]")))
            time.sleep(0.5)
            highlight_element(driver,designation_dropdown)
            designation_dropdown.click()

            designation_input = driver.switch_to.active_element
            designation_input.send_keys(designation_name)
            time.sleep(1)

            role_option = wait.until(EC.presence_of_element_located((By.XPATH, f"//div[contains(@class,'option') and normalize-space()='{designation_name}']")))
            highlight_element(driver, role_option)
            role_option.click()
        except Exception as e:
            step_fail(driver, "Enter Description", e)

    with allure.step("Click on Invite Button"):
        try:
            invite_btn = wait.until(EC.presence_of_element_located((By.XPATH, "//button[.//span[text()='Invite']]")))
            highlight_element(driver,  invite_btn)
            invite_btn.click()
            wait_for_loader_to_disappear(driver, wait)
            print("✅ Save button clicked")
            time.sleep(5)
        except Exception as e:
            step_fail(driver, "Click Invite Button", e)
    with allure.step("Toast Msg"):
        try:
            toast = wait.until(EC.presence_of_element_located((By.XPATH, toast_msg)))
            highlight_element(driver, toast)
            print(f"📢 Toast message: {toast.text.strip()}")
            time.sleep(6)
        except Exception as e:
            step_fail(driver, "Toast Message Verification", e)
    

    
    return True

