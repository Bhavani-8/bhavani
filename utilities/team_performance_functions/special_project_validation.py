from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import allure
import time
import pytest
import json
import os
from utilities.other_utils_functions.highlight import highlight_element
from utilities.add_task_utils import wait_for_loader_to_disappear
from selenium.webdriver.common.keys import Keys



try:
    with open(os.path.join("data", 'locators.json'), 'r') as f:
        elements_details = json.load(f)
        project_icon = elements_details['project_icon']
        dashboard_icon = elements_details['dashboard_icon']
        special_task_icon = elements_details['special_task_icon']
        team_performance_btn = elements_details['team_performance_btn']
except FileNotFoundError:
    pytest.fail("❌ locators.json file not found")
except json.JSONDecodeError:
    pytest.fail("❌ Invalid JSON in locators.json")


def special_project_check(driver, wait, dash_type='QCC'):

    with allure.step("Open project Icon"):
            try:
                project_icon_btn = wait.until(EC.presence_of_element_located((By.XPATH, project_icon)))
                highlight_element(driver, project_icon_btn)
                project_icon_btn.click()
                time.sleep(2)
                print("✅ Project icon clicked")
            except Exception as e:
                msg = f"Failed to Click Project Icon: {str(e)}"
                print(msg)
                allure.attach(msg, name="Project Icon Error", attachment_type=allure.attachment_type.TEXT)
                raise Exception(msg)
            
            
            with allure.step("Fetch the first task name from the task list"):
                try:
                    first_project_name_elem = wait.until(EC.presence_of_element_located((By.XPATH, "(//tr[contains(@class,'dx-data-row')])[2]//td[1]//div[@title]")))
                    highlight_element(driver, first_project_name_elem)
                    first_project_name= first_project_name_elem.get_attribute("title").strip()
                    # if not first_project_name:
                    #     first_project_name= first_project_name_elem.get_attribute("title").strip()
                    # if not first_project_name:
                    #     raise Exception("Task name text is empty")

                    print(f"📋 Copied First Project Name: {first_project_name}")
                except Exception as e:
                    msg = f"Failed to Fetch Project name: {str(e)}"
                    print(msg)
                    allure.attach(msg, name="Project Name Error", attachment_type=allure.attachment_type.TEXT)
                    raise Exception(msg)
            
            with allure.step("Open Special Task Dashboard → Special Team Performance"):
                try:
                    print("📍 Opening Special Task Dashboard...")
                    special_task_icon_elem = wait.until(EC.element_to_be_clickable((By.XPATH, special_task_icon)))
                    highlight_element(driver, special_task_icon_elem)
                    special_task_icon_elem.click()
                    print("✅ Special Task Dashboard icon clicked")

                    wait_for_loader_to_disappear(driver, wait)
                    special_team_perf_elem = wait.until(EC.element_to_be_clickable((By.XPATH, team_performance_btn)))
                    highlight_element(driver, special_team_perf_elem)
                    special_team_perf_elem.click()
                    print("✅ Special Team Performance clicked")
                    wait_for_loader_to_disappear(driver, wait)
                except Exception as e:
                    msg = f"Failed to Click Special Dashboard Icon: {str(e)}"
                    print(msg)
                    allure.attach(msg, name="Special Dashboard Icon Error", attachment_type=allure.attachment_type.TEXT)
                    raise Exception(msg)
            
            with allure.step("Open Project Filter"):
                try:
                    filter_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "(//div[contains(@class,'dx-toolbar-item-content')]//button[contains(@class,'ant-btn-icon-only')])[2]")))
                    highlight_element(driver, filter_btn)
                    filter_btn.click()
                    print("✅ Filter button clicked")
                except Exception as e:
                    msg = f"Failed to Click Project Filter: {str(e)}"
                    print(msg)
                    allure.attach(msg, name="Project Filter Error", attachment_type=allure.attachment_type.TEXT)
                    raise Exception(msg)
            with allure.step("Click select project and enter project name"):
                try:
                    # 1️⃣ Click the Select Project dropdown (the control box)
                    dropdown = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@class,'control')]")))
                    highlight_element(driver, dropdown)
                    dropdown.click()

                    # 2️⃣ Locate the REAL input field React Select creates
                    input_box = wait.until(EC.visibility_of_element_located((By.XPATH, "//input[contains(@id,'react-select') and @type='text']")))
                    highlight_element(driver, input_box)
                    input_box.send_keys(first_project_name)
                    input_box.send_keys(Keys.ENTER) 

                    print(f"✅ Selected project: {first_project_name}")

                except Exception as e:
                    msg = f"Failed to Click Project Dropdown: {str(e)}"
                    print(msg)
                    allure.attach(msg, name="Project Dropdown Error", attachment_type=allure.attachment_type.TEXT)
                    raise Exception(msg)
                filter_label_text = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='ant-popover-title']")))
                filter_label_text.click()

            # ---------------------------
            with allure.step("Apply Date Range"):
                try:
                    apply_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Apply']")))
                    highlight_element(driver, apply_btn)
                    apply_btn.click()
                    time.sleep(4)
                except Exception as e:
                    msg = f"Failed to Click Apply Date: {str(e)}"
                    print(msg)
                    allure.attach(msg, name="Apply Date Error", attachment_type=allure.attachment_type.TEXT)
                    raise Exception(msg)
                    
                    
            try:
                filter_btn_elem = wait.until(EC.element_to_be_clickable((By.XPATH,"(//div[contains(@class,'dx-toolbar-item-content')]//button[contains(@class,'ant-btn-icon-only')])[2]")))
                driver.execute_script("arguments[0].scrollIntoView({behavior:'auto', block:'center'});", filter_btn_elem)
                highlight_element(driver, filter_btn_elem)
                driver.execute_script("arguments[0].click();", filter_btn_elem)
                print("✅ Date filter toolbar reopened")
            except Exception as e:
                msg = f"Failed to Click Filter label: {str(e)}"
                print(msg)
                allure.attach(msg, name="Filter label Error", attachment_type=allure.attachment_type.TEXT)
                raise Exception(msg)

            # ---------------------------
            # Click Reset
            # ---------------------------
            try:
                reset_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Reset']")))
                driver.execute_script("arguments[0].scrollIntoView({behavior:'auto', block:'center'});", reset_btn)
                highlight_element(driver, reset_btn)
                reset_btn.click()
                print("✅ Date filter reset successfully")
                time.sleep(4)
            except Exception as e:
                msg = f"Failed to Click Reset Button: {str(e)}"
                print(msg)
                allure.attach(msg, name="Reset Button Error", attachment_type=allure.attachment_type.TEXT)
                raise Exception(msg)


    return True