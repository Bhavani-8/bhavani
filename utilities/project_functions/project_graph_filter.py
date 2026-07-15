import allure
import json
import os
import time
import pytest
from datetime import datetime, timedelta
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from utilities.other_utils_functions.highlight import highlight_element
from selenium.webdriver.common.keys import Keys

def graph_filter(driver, wait):

    with allure.step("Load locators.json"):
        try:
            with open(os.path.join("data", "locators.json"), "r") as f:
                elements_details = json.load(f)

            project_icon = elements_details["project_icon"]

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
            project_btn = wait.until(EC.presence_of_element_located((By.XPATH, project_icon)))
            highlight_element(driver, project_btn)
            project_btn.click()
            time.sleep(3)
        except Exception as e:
            msg = f"Failed to Click Project Icon: {str(e)}"
            print(msg)
            allure.attach(msg, name="Project Icon Error", attachment_type=allure.attachment_type.TEXT)
            raise Exception(msg)
   
        try:
            first_project_name_elem = wait.until(EC.presence_of_element_located((By.XPATH, "(//tr[contains(@class,'dx-data-row')])[2]//td[1]//div[@title]")))
            highlight_element(driver, first_project_name_elem)
            first_project_name = first_project_name_elem.get_attribute("title").strip()
            if not first_project_name:
                first_project_name= first_project_name_elem.get_attribute("title").strip()
            if not first_project_name:
                raise Exception("Task name text is empty")

            print(f"📋 Copied First Project Name: {first_project_name}")
        except Exception as e:
            msg = f"Failed to Fetch First Project Name: {str(e)}"
            print(msg)
            allure.attach(msg, name="Fetch First Project Name Error", attachment_type=allure.attachment_type.TEXT)
            raise Exception(msg)
    
        try:
            graph_btn = wait.until(EC.presence_of_element_located((By.XPATH, "//button[@title='Graph']")))
            highlight_element(driver, graph_btn)
            graph_btn.click()
            time.sleep(1)
        except Exception as e:
            msg = f"Failed to Click Graph button: {str(e)}"
            print(msg)
            allure.attach(msg, name=" Graph Button Error", attachment_type=allure.attachment_type.TEXT)
            raise Exception(msg)
        
        try:
            filter_btn = wait.until(EC.presence_of_element_located((By.XPATH, "(//div[contains(@class,'dx-toolbar-button')]//button[contains(@class,'ant-btn-icon-only')])[1]")))
            # dept_rect = wait.until(EC.presence_of_element_located((By.XPATH, "//*[name()='rect' and @height='113']")))
            highlight_element(driver, filter_btn)
            filter_btn.click()
            time.sleep(1)
        except Exception as e:
            msg = f"Failed to Click Filter button: {str(e)}"
            print(msg)
            allure.attach(msg, name=" Filter Button Error", attachment_type=allure.attachment_type.TEXT)
            raise Exception(msg)
    
       
        
        with allure.step("Select Dates from Calendar"):
            try:

                today = datetime.today().date()
                past_date = (today - timedelta(days=3)).strftime("%Y-%m-%d")
                future_date = (today + timedelta(days=3)).strftime("%Y-%m-%d")

                # -----------------------------
                # FROM DATE
                # -----------------------------
                from_input = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='From']")))
                from_input.click()

                from_date = wait.until(EC.element_to_be_clickable((By.XPATH, f"//td[@title='{past_date}']")))
                from_date.click()

                print(f"✅ Selected From Date: {past_date}")

                to_input = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='To']")))
                to_input.click()

                to_date = wait.until(EC.element_to_be_clickable((By.XPATH, f"//td[@title='{future_date}']")))
                to_date.click()
                print(f"✅ Selected To Date: {future_date}")

                apply_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[.//span[text()='Apply']]")))
                apply_btn.click()
                time.sleep(1)
            except Exception as e:
                msg = f"Failed to Click From Date button: {str(e)}"
                print(msg)
                allure.attach(msg, name="From Date Error", attachment_type=allure.attachment_type.TEXT)
                raise Exception(msg)
            
        try:
            select_project = wait.until(EC.presence_of_element_located((By.XPATH, "//button[@title='Open']")))
            highlight_element(driver, select_project)
            select_project.click()

            input_box = driver.switch_to.active_element
            highlight_element(driver, input_box)
            input_box.send_keys(first_project_name)
            time.sleep(1)

            project_option = wait.until(EC.presence_of_element_located((By.XPATH, f"//div[contains(@class, 'MuiAutocomplete-popper')]//li[contains(., '{first_project_name}')]")))
            highlight_element(driver, project_option)
            time.sleep(1)
            driver.execute_script("arguments[0].scrollIntoView(true);", project_option)
            driver.execute_script("arguments[0].click();", project_option)
            
            print(f"✅ Successfully selected: {first_project_name}")
        except Exception as e:
            msg = f"Failed to Click Select Project: {str(e)}"
            print(msg)
            allure.attach(msg, name="Select project Error", attachment_type=allure.attachment_type.TEXT)
            raise Exception(msg)
        

        filter_label_text = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='ant-drawer-title']")))
        filter_label_text.click()
    

       
        try:
            apply_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Apply']")))
            highlight_element(driver, apply_btn)
            apply_btn.click()
            time.sleep(4)
        except Exception as e:
            msg = f"Failed to Click Apply button: {str(e)}"
            print(msg)
            allure.attach(msg, name="Apply  Button Error", attachment_type=allure.attachment_type.TEXT)
            raise Exception(msg)
        
        
        try:
            close_filter_btn = wait.until(EC.presence_of_element_located((By.XPATH, "//button[@class='ant-drawer-close']")))
            highlight_element(driver, close_filter_btn)
            time.sleep(1)
            close_filter_btn.click()
        except Exception as e:
            msg = f"Failed to Click Close filter button: {str(e)}"
            print(msg)
            allure.attach(msg, name="filter Button Error", attachment_type=allure.attachment_type.TEXT)
            raise Exception(msg)
        

        try:
            filter_btn_elem = wait.until(EC.element_to_be_clickable((By.XPATH,"(//div[contains(@class,'dx-toolbar-item-content')]//button[contains(@class,'ant-btn-icon-only')])[1]")))
            driver.execute_script("arguments[0].scrollIntoView({behavior:'auto', block:'center'});", filter_btn_elem)
            highlight_element(driver, filter_btn_elem)
            driver.execute_script("arguments[0].click();", filter_btn_elem)
            print("✅ Date filter toolbar reopened")
        except Exception as e:
            msg = f"Failed to Click Filter button: {str(e)}"
            print(msg)
            allure.attach(msg, name="filter Button Error", attachment_type=allure.attachment_type.TEXT)
            raise Exception(msg)
        

        try:
            reset_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Reset']")))
            driver.execute_script("arguments[0].scrollIntoView({behavior:'auto', block:'center'});", reset_btn)
            highlight_element(driver, reset_btn)
            reset_btn.click()
            print("✅ Date filter reset successfully")
            time.sleep(4)
        except Exception as e:
            msg = f"Failed to Click Reset button: {str(e)}"
            print(msg)
            allure.attach(msg, name="Reset Button Error", attachment_type=allure.attachment_type.TEXT)
            raise Exception(msg)
        

    return True

        

            