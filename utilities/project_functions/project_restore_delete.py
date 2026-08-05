import allure
import json
import os
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from utilities.other_utils_functions.highlight import highlight_element
from utilities.add_task_utils import wait_for_loader_to_disappear
from selenium.webdriver import ActionChains


def project_restore_delete(driver, wait):

    with allure.step("Load locators.json"):
        try:
            with open(os.path.join("data", "locators.json"), "r") as f:
                elements_details = json.load(f)

            project_icon = elements_details["project_icon"]
            toast_msg = elements_details['toast_msg']
            trash_icon = elements_details['trash_icon']

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
        
    with allure.step("Click project icon"):
        try:
            driver.refresh()
            wait_for_loader_to_disappear(driver, wait)
            project_btn = wait.until(EC.presence_of_element_located((By.XPATH, project_icon)))
            highlight_element(driver, project_btn)
            project_btn.click()
            time.sleep(2)
        except Exception as e:
            msg = f"Failed to Click Project Icon: {str(e)}"
            print(msg)
            allure.attach(msg, name="Project Icon Error", attachment_type=allure.attachment_type.TEXT)
            raise Exception(msg)
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
            msg = f"Failed to Click Project Task: {str(e)}"
            print(msg)
            allure.attach(msg, name="Project Task Error", attachment_type=allure.attachment_type.TEXT)
            raise Exception(msg)
    
    with allure.step("Click Project three dots menu"):
        try:
            three_dots_btn = wait.until(EC.presence_of_element_located((By.XPATH, f"//tr[contains(@class,'dx-data-row')][.//div[@class='w-full truncate' and contains(@title,'{created_project_name}')]]//div[starts-with(@id,'context-menu-assignment-')]//button")))
            driver.execute_script("arguments[0].scrollIntoView({block:'center', inline:'center'});", three_dots_btn)
            highlight_element(driver, three_dots_btn)
            three_dots_btn.click()
            time.sleep(0.5)
        except Exception as e:
            msg = f"Failed to Click Three dots button: {str(e)}"
            print(msg)
            allure.attach(msg, name="Three dots button Error", attachment_type=allure.attachment_type.TEXT)
            raise Exception(msg)
    
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
            msg = f"Failed to Click Delete button: {str(e)}"
            print(msg)
            allure.attach(msg, name="Delete button Error", attachment_type=allure.attachment_type.TEXT)
            raise Exception(msg)
    
    with allure.step("Click Trash Icon"):
        try:
            print()
            trash_btn = wait.until(EC.presence_of_element_located((By.XPATH, trash_icon)))
            highlight_element(driver, trash_btn)
            trash_btn.click()
            print("🗑️ Trash icon clicked")

        except Exception as e:
            msg = f"Failed to Click Thrash Icon: {str(e)}"
            print(msg)
            allure.attach(msg, name="Thrash Icon Error", attachment_type=allure.attachment_type.TEXT)
            raise Exception(msg)

    with allure.step("Click Projects Tab"):
        try:
            time.sleep(3)
            projects_tab = wait.until(EC.presence_of_element_located((By.XPATH, "//button[text()='Projects']")))
            highlight_element(driver, projects_tab)
            projects_tab.click()
            print("📌 Tasks tab clicked")
        except Exception as e:
            msg = f"Failed to Click Projects Tab: {str(e)}"
            print(msg)
            allure.attach(msg, name="Projects Tab Error", attachment_type=allure.attachment_type.TEXT)
            raise Exception(msg)

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
            msg = f"Failed to Verify Project: {str(e)}"
            print(msg)
            allure.attach(msg, name="Projects Task Error", attachment_type=allure.attachment_type.TEXT)
            raise Exception(msg)
    
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
            msg = f"Failed to Click Restore Button: {str(e)}"
            print(msg)
            allure.attach(msg, name="Restore Button Error", attachment_type=allure.attachment_type.TEXT)
            raise Exception(msg)

    with allure.step("Click project icon again"):
        try:
            project_btn = wait.until(EC.presence_of_element_located((By.XPATH, project_icon)))
            highlight_element(driver, project_btn)
            project_btn.click()
            time.sleep(2)
        except Exception as e:
            msg = f"Failed to Click Project Icon: {str(e)}"
            print(msg)
            allure.attach(msg, name="Project Icon Error", attachment_type=allure.attachment_type.TEXT)
            raise Exception(msg)
    with allure.step("Click Project three dots menu"):
        try:
            three_dots_btn = wait.until(EC.presence_of_element_located((By.XPATH, f"//tr[contains(@class,'dx-data-row')][.//div[@class='w-full truncate' and contains(@title,'{created_project_name}')]]//div[starts-with(@id,'context-menu-assignment-')]//button")))
            driver.execute_script("arguments[0].scrollIntoView({block:'center', inline:'center'});", three_dots_btn)
            highlight_element(driver, three_dots_btn)
            three_dots_btn.click()
            time.sleep(0.5)
        except Exception as e:
            msg = f"Failed to Click Three dots button: {str(e)}"
            print(msg)
            allure.attach(msg, name="Three dots button Error", attachment_type=allure.attachment_type.TEXT)
            raise Exception(msg)
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
            msg = f"Failed to Click Delete button: {str(e)}"
            print(msg)
            allure.attach(msg, name="Delete button Error", attachment_type=allure.attachment_type.TEXT)
            raise Exception(msg)

    
    return True