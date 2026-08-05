import allure
import json
import os
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from utilities.other_utils_functions.highlight import highlight_element
from selenium.common.exceptions import TimeoutException
from utilities.add_task_utils import wait_for_loader_to_disappear

   
def add_coowner(driver, wait, coowner_name):

    with allure.step("Load locators.json"):
        try:
            with open(os.path.join("data", "locators.json"), "r") as f:
                elements_details = json.load(f)

            project_icon = elements_details["project_icon"]
            toast_msg = elements_details['toast_msg']
            add_coowner_elem = elements_details['add_coowner_elem']
            add_btn_elem = elements_details['add_btn_elem']
            coowner_drop_down_btn = elements_details['coowner_drop_down_btn']
            add_checkbox_btn = elements_details['add_checkbox_btn']
            edit_checkbox_btn = elements_details['edit_checkbox_btn']
            delete_checkbox_btn = elements_details['delete_checkbox_btn']
            coowner_submit_btn = elements_details['coowner_submit_btn']
            fetch_coowner_name = elements_details['fetch_coowner_name']
            fetch_coowner_permissions = elements_details['fetch_coowner_permissions']
            coowner_done_btn = elements_details['coowner_done_btn']


            print("✅ locators.json loaded")
        except FileNotFoundError as e:
            msg = f"locators.json file not found: {str(e)}"
            print(msg)
            allure.attach(msg, name="Locators File Missing", attachment_type=allure.attachment_type.TEXT)
            return False
        except json.JSONDecodeError as e:
            msg = f"Invalid JSON in locators.json: {str(e)}"
            print(msg)
            allure.attach(msg, name="Locators JSON Error", attachment_type=allure.attachment_type.TEXT)
            return False
        
    with allure.step("Create New Project"):
        try:
            driver.refresh()
            wait_for_loader_to_disappear(driver, wait)
            project_btn = wait.until(EC.presence_of_element_located((By.XPATH, project_icon)))
            highlight_element(driver, project_btn)
            project_btn.click()
            time.sleep(2)
        except Exception as e:
            allure.attach(str(e), "Project Create Error")
            return False

    with allure.step("Click the three dots menu for the task"):
        try:
              # Read the project name created in create_project.py
            project_file = os.path.join("latest_data", "latest_project.txt")
            with open(project_file, "r") as f:
                created_project_name = f.read().strip()
            three_dots_btn = wait.until(EC.presence_of_element_located((By.XPATH, f"//tr[contains(@class,'dx-data-row')][.//div[@title='{created_project_name}']]//button")))
            driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'start'});", three_dots_btn)
            highlight_element(driver, three_dots_btn)
            three_dots_btn.click()
        except Exception as e:
            msg = f"Failed to Click Project Task: {str(e)}"
            print(msg)
            allure.attach(msg, name="Project Task Error", attachment_type=allure.attachment_type.TEXT)
            raise Exception(msg)
    with allure.step("Click Add Co-owner or Add Button"):
        try:
            add_coowner_btn = wait.until(EC.element_to_be_clickable((By.XPATH, add_coowner_elem)))
            highlight_element(driver, add_coowner_btn)
            add_coowner_btn.click()
            print("👥 Add Co-owner clicked")

        except Exception as e:
            msg = f"Failed to Click Add Co-owner button: {str(e)}"
            print(msg)
            allure.attach(msg, name="Add Co-owner button Error", attachment_type=allure.attachment_type.TEXT)
            raise Exception(msg)
        # try:
        #     add_btn = wait.until(EC.element_to_be_clickable((By.XPATH, add_btn_elem)))
        #     highlight_element(driver, add_btn)
        #     add_btn.click()
        #     print("➕ Add User clicked (fallback option)")

        # except Exception as e:
        #     msg = f"Failed to Click Add button: {str(e)}"
        #     print(msg)
        #     allure.attach(msg, name="Add button Error", attachment_type=allure.attachment_type.TEXT)
        #     raise Exception(msg)
    with allure.step("Click Dropdown and Select Co-owner"):
        try:
            dropdown_btn = wait.until(EC.presence_of_element_located((By.XPATH, coowner_drop_down_btn)))
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
            msg = f"Failed to Click Dropdown and Select Co-owner: {str(e)}"
            print(msg)
            allure.attach(msg, name="Click Dropdown and Select Co-owner Error", attachment_type=allure.attachment_type.TEXT)
            raise Exception(msg)
    with allure.step("Click Add, Edit, Delete Checkbox"):
        try:
            add_checkbox = wait.until(EC.presence_of_element_located((By.XPATH, add_checkbox_btn)))
            highlight_element(driver, add_checkbox)
            add_checkbox.click()
            time.sleep(1)
            
            edit_checkbox = wait.until(EC.presence_of_element_located((By.XPATH, edit_checkbox_btn)))
            highlight_element(driver, edit_checkbox)
            edit_checkbox.click()
            time.sleep(1)

            delete_checkbox = wait.until(EC.presence_of_element_located((By.XPATH, delete_checkbox_btn)))
            highlight_element(driver, delete_checkbox)
            delete_checkbox.click()
            time.sleep(1)

            submit_btn = wait.until(EC.presence_of_element_located((By.XPATH, coowner_submit_btn)))
            highlight_element(driver, submit_btn)
            submit_btn.click()
            print("✔️ Submit clicked")
            time.sleep(3)

            
        except TimeoutException:
            print("⚠️ No options available — clicking Cancel")

            cancel_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Cancel']")))
            highlight_element(driver, cancel_btn)
            cancel_btn.click()
            print("❌ Selection cancelled because no options were found")

            done_btn = wait.until(EC.presence_of_element_located((By.XPATH, coowner_done_btn)))
            highlight_element(driver, done_btn)
            done_btn.click()
    with allure.step("Click the three dots menu from the project"):
        try:
              # Read the project name created in create_project.py
            project_file = os.path.join("latest_data", "latest_project.txt")
            with open(project_file, "r") as f:
                created_project_name = f.read().strip()
            three_dots_btn = wait.until(EC.presence_of_element_located((By.XPATH, f"//tr[contains(@class,'dx-data-row')][.//div[@title='{created_project_name}']]//button")))
            driver.execute_script("arguments[0].scrollIntoView({block:'center', inline:'center'});", three_dots_btn)
            highlight_element(driver, three_dots_btn)
            three_dots_btn.click()
        except Exception as e:
            msg = f"Failed to Click the three dots menu from the project: {str(e)}"
            print(msg)
            allure.attach(msg, name="Click the three dots menu from the project Error", attachment_type=allure.attachment_type.TEXT)
            raise Exception(msg)
    with allure.step("Validate Co-owner Name and Permissions"):
        try:
            add_coowner_btn = wait.until(EC.presence_of_element_located((By.XPATH, add_coowner_elem)))
            highlight_element(driver, add_coowner_btn)
            add_coowner_btn.click()
            print("👥 Add Co-owner clicked")

            coowner_name = wait.until(EC.visibility_of_element_located((By.XPATH, fetch_coowner_name)))
            highlight_element(driver, coowner_name, 0.2)
            fetched_coowner_name = coowner_name.text.strip() 
            print(f"Co-owner Name: {fetched_coowner_name}")

            coowner_permissions =  wait.until(EC.visibility_of_element_located((By.XPATH, fetch_coowner_permissions)))
            highlight_element(driver, coowner_permissions, 0.2)
            fetched_coowner_permissions = coowner_permissions.text.strip()
            print(f"Permissions: {fetched_coowner_permissions}")
            time.sleep(1)

            # ✅ Allure Attach (TEXT)
            coowner_details = (f"Co-owner Name: {fetched_coowner_name}\n"f"Permissions: {fetched_coowner_permissions}")

            allure.attach(coowner_details,name="Co-owner Details",attachment_type=allure.attachment_type.TEXT)
    
        except Exception as e:
            msg = f"Failed to Validate Co-owner Name and Permissions: {str(e)}"
            print(msg)
            allure.attach(msg, name="Validate Co-owner Name and Permissions Error", attachment_type=allure.attachment_type.TEXT)
            raise Exception(msg)
    with allure.step("Click Done Button"):
        try:
            done_btn = wait.until(EC.element_to_be_clickable((By.XPATH, coowner_done_btn)))
            highlight_element(driver, done_btn)
            done_btn.click()
            time.sleep(2)
        except Exception as e:
            msg = f"Failed to Click Done button: {str(e)}"
            print(msg)
            allure.attach(msg, name="Done button Error", attachment_type=allure.attachment_type.TEXT)
            raise Exception(msg)
    

    return True
    