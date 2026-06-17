
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

def task_category(driver, wait, category_name, category_desc):
    with allure.step("Load locators.json"):
        try:
            with open(os.path.join("data", "locators.json"), "r") as f:
                elements_details = json.load(f)
            settings_icon = elements_details["settings_icon"]
            toast_msg = elements_details["toast_msg"]
            special_task_icon = elements_details['special_task_icon']
            print("✅ locators.json loaded successfully")
        except Exception as e:
            allure.attach(str(e), name="Locators Load Error", attachment_type=allure.attachment_type.TEXT)
            return False
    
    with allure.step("Click Settings"):
        try:
            settings_btn = wait.until(EC.presence_of_element_located((By.XPATH, settings_icon)))
            highlight_element(driver, settings_btn)
            settings_btn.click()
        except Exception as e:
            step_fail(driver, "Click Settings", e)
    
    with allure.step("Click on Task Category"):
        try:
            task_category_btn = wait.until(EC.presence_of_element_located((By.XPATH, "//span[text()='Task Category']")))
            highlight_element(driver, task_category_btn)
            task_category_btn.click()
        except Exception as e:
            step_fail(driver, "Click Task Category", e)
    wait_for_loader_to_disappear(driver, wait)
    time.sleep(3)

    with allure.step("Click on Add Category"):
        try:
            add_category_btn = wait.until(EC.presence_of_element_located((By.XPATH, "//button[contains(.,'Add Task Category')]")))
            highlight_element(driver, add_category_btn)
            add_category_btn.click()
        except Exception as e:
            step_fail(driver, "Click Add Category", e)
    
    with allure.step("Enter Task Category"):
        try:
            category_input_elem = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@name='category']")))
            highlight_element(driver, category_input_elem)
            category_input_elem.clear()
            # category_input_elem.send_keys(category_name)
            category_input_elem.send_keys(category_name.strip())
        except Exception as e:
            step_fail(driver, "Enter Task Category", e)
    with allure.step("Enter Task Category Description"):
        try:
            category_desc_text= wait.until(EC.presence_of_element_located((By.XPATH, "//textarea[@name='description']")))
            highlight_element(driver, category_desc_text)
            category_desc_text.clear()
            category_desc_text.send_keys(category_desc)
        except Exception as e:
            step_fail(driver, "Enter Task Category Description", e)
    with allure.step("Click Create Button"):
        try:
            create_btn= wait.until(EC.presence_of_element_located((By.XPATH, "//button[normalize-space()='Create']")))
            highlight_element(driver, create_btn)
            create_btn.click()
            time.sleep(2)
        except Exception as e:
            step_fail(driver, "Click Create Button", e)
    
    try:
        task_category_elem = wait.until(EC.visibility_of_element_located((By.XPATH, "//td[text()='IT']")))
        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", task_category_elem)
        time.sleep(0.3)
        highlight_element(driver, task_category_elem, 0.2)  # Assuming your highlight function exists

        fetched_category = task_category_elem.text.strip()
        print(f"Task Category from Settings: {fetched_category}")
        
        with allure.step("Open Dashboard"):
            try:
                time.sleep(2)
                special_task_icon_elem = wait.until(EC.element_to_be_clickable((By.XPATH, special_task_icon)))
                highlight_element(driver, special_task_icon_elem)
                special_task_icon_elem.click()
            except Exception as e:
                allure.attach(str(e), name="Dashboard Open Error", attachment_type=allure.attachment_type.TEXT)
                return False

        task_dashboard_label_elem = wait.until(EC.visibility_of_element_located((By.XPATH, "//button[normalize-space()='IT']")))
        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", task_dashboard_label_elem)
        highlight_element(driver, task_dashboard_label_elem, 0.2)
        fetched_dashboard_category = task_dashboard_label_elem.text.strip()
        print(f"Task Category from Dashboard: {fetched_dashboard_category}")
        
        with allure.step("Verify Task Category in Dashboard"):
            actual = fetched_dashboard_category
            expected = fetched_category
            if actual == expected:
                msg = f"Task Category Matched | Actual: '{actual}' | Expected: '{expected}'"
                print(f"✅ {msg}")
                allure.attach(msg,name="Task Category Validation",attachment_type=allure.attachment_type.TEXT)
        
                return True
            else:
                msg = f"Mismatch | Actual: '{actual}' | Expected: '{expected}'"
                print(f"❌ {msg}")

                allure.attach(msg,name="Task Category Mismatch",attachment_type=allure.attachment_type.TEXT)
                return False

    except Exception as e:
        print(f"❌ Error during task category verification: {e}")
        allure.attach(str(e), name="Verification Exception", attachment_type=allure.attachment_type.TEXT)
        return False


