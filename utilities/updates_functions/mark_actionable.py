from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import allure 
import os
import json
import pytest
import time
from utilities.other_utils_functions.highlight import highlight_element
from utilities.add_task_utils import wait_for_loader_to_disappear

def step_fail(driver, step_name, error):
    allure.attach(str(error), name=f"{step_name} Error", attachment_type=allure.attachment_type.TEXT)
    allure.attach(driver.get_screenshot_as_png(), name=f"{step_name} Screenshot", attachment_type=allure.attachment_type.PNG)
    pytest.fail(f"❌ {step_name} failed")

def mark_actionable(driver, wait):

    with allure.step("Load locators.json"):
        try:
            with open(os.path.join("data", 'locators.json'), 'r') as f:
                elements_details = json.load(f)
                updates_icon = elements_details['updates_icon']
                update_circ_checkbox_label = elements_details['update_circ_checkbox_label']
                select_circular = elements_details['select_circular']
                toast_msg = elements_details['toast_msg']
                task_circ_close_btn = elements_details['task_circ_close_btn']
                mark_non_actionable = elements_details['mark_non_actionable']
                not_actionable_label = elements_details['not_actionable_label']
                mark_actionable_elem = elements_details['mark_actionable_elem']

            print("✅ locators.json loaded successfully")
        except Exception as e:
            step_fail(driver, "Load locators.json", e)
    with allure.step("Open Updates Section"):
        try:
            time.sleep(2)
            updates_btn = wait.until(EC.element_to_be_clickable((By.XPATH, updates_icon)))
            highlight_element(driver, updates_btn)
            updates_btn.click()
            wait_for_loader_to_disappear(driver, wait)
            time.sleep(1)
            print("✅ Updates icon clicked")
        except Exception as e:
            allure.attach(str(e), name="Updates Section Error", attachment_type=allure.attachment_type.TEXT)
            return False

    with allure.step("Select Update Checkbox"):
        try:
            circular_label = wait.until(EC.visibility_of_element_located((By.XPATH, update_circ_checkbox_label)))
            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", circular_label)
            time.sleep(0.3)
            highlight_element(driver, circular_label, 0.2)  # Assuming your highlight function exists
            fetched_circular = circular_label.text.strip()
            print(f"Circular: {fetched_circular}")

            select_elem = wait.until(EC.presence_of_element_located((By.XPATH, select_circular)))
            highlight_element(driver, select_elem)
            select_elem.click()
            print("🟦 First checkbox clicked")
            time.sleep(2)
        except Exception as e:
            step_fail(driver, "Load locators.json", e)

    with allure.step("Click Mark Non Actionable"):
        try:
            mark_non_actionable_btn = wait.until(EC.element_to_be_clickable((By.XPATH, mark_non_actionable)))
            highlight_element(driver, mark_non_actionable_btn)
            mark_non_actionable_btn.click()
            print("✅ 'click Mark Non Actionable")
        except Exception as e:
            step_fail(driver, "Load locators.json", e)
        
        try:
            toast = wait.until(EC.presence_of_element_located((By.XPATH, toast_msg)))
            highlight_element(driver, toast)
            print(f"📢 Toast message: {toast.text.strip()}")
        except Exception:
            print("❌ No toast message found")
        
        try:
            close_circular = wait.until(EC.presence_of_element_located((By.XPATH, task_circ_close_btn)))
            highlight_element(driver, close_circular)
            close_circular.click()
            print("✅ Circular closed successfully.")
            time.sleep(3)

            driver.refresh()
            wait_for_loader_to_disappear(driver, wait)
            time.sleep(3)

            print("✅ Page refreshed successfully.")

        except Exception:
            print("❌ Closed circular not found")
        try:
            na_label = wait.until(EC.visibility_of_element_located((By.XPATH, not_actionable_label)))
            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", na_label)
            time.sleep(0.3)
            highlight_element(driver, na_label)  

            na_label_text = na_label.text.strip()
            if na_label_text == "NA":
                print("✅ NA Label text value is 'NA'")
               
            else:
                print(f"❌ Expected 'NA' but found '{na_label_text}'")
                
        except Exception:
            print("❌ NA Label not found")
            
        
    with allure.step("Select Update Checkbox"):
        try:
            circular_label = wait.until(EC.visibility_of_element_located((By.XPATH, update_circ_checkbox_label)))
            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", circular_label)
            time.sleep(0.3)
            highlight_element(driver, circular_label, 0.2)  # Assuming your highlight function exists
            fetched_circular = circular_label.text.strip()
            print(f"Circular: {fetched_circular}")

            select_elem = wait.until(EC.presence_of_element_located((By.XPATH, select_circular)))
            highlight_element(driver, select_elem)
            select_elem.click()
            print("🟦 First checkbox clicked")
            time.sleep(2)
        except Exception as e:
            step_fail(driver, "Load locators.json", e)

    with allure.step("Click Mark Actionable"):
        try:
            mark_actionable_btn = wait.until(EC.element_to_be_clickable((By.XPATH, mark_actionable_elem)))
            highlight_element(driver, mark_actionable_btn)
            mark_actionable_btn.click()
            print("✅ 'click Mark Actionable")
        except Exception as e:
            step_fail(driver, "Load locators.json", e)
        
        try:
            toast = wait.until(EC.presence_of_element_located((By.XPATH, toast_msg)))
            highlight_element(driver, toast)
            print(f"📢 Toast message: {toast.text.strip()}")
        except Exception:
            print("❌ No toast message found")
        
        try:
            close_circular = wait.until(EC.presence_of_element_located((By.XPATH, task_circ_close_btn)))
            highlight_element(driver, close_circular)
            close_circular.click()
            print("✅ Circular closed successfully.")
            time.sleep(3)

            driver.refresh()
            wait_for_loader_to_disappear(driver, wait)
            time.sleep(3)

            print("✅ Page refreshed successfully.")

        except Exception:
            print("❌ Closed circular not found")
        

        
   
    return True

