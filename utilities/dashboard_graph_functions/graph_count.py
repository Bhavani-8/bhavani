import os
import time
import json
import allure
import re
import pytest
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import pyautogui as pg
from utilities.other_utils_functions.highlight import highlight_element
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from utilities.add_task_functions.wait_for_loader_to_disappear import wait_for_loader_to_disappear

def dashboard_graph_count(driver, wait):
    try:
        with open(os.path.join("data", "locators.json"), "r") as f:
            locators = json.load(f)
            task_title_label = locators["task_title_label"]

    except Exception as e:
        print(f"❌ Failed to load locators.json: {e}")
        return False
   
    with allure.step("Click on graph button"):
        try:

            graph_btn = wait.until(EC.visibility_of_element_located((By.XPATH, "//div[contains(@class,'justify-end')]//button")))
            highlight_element(driver, graph_btn)
            graph_btn.click()

            wait_for_loader_to_disappear(driver, wait)
            time.sleep(3) 
        except Exception as e:
            print(f"❌ Failed to search using first task name: {e}")
            return False
    
        try:
            dashboard_status = wait.until(EC.presence_of_element_located((By.XPATH,"//*[name()='rect' and @fill='#9e63fd']")))
            highlight_element(driver, dashboard_status)
            dashboard_status.click()
            time.sleep(8)

            year_btn = wait.until(EC.presence_of_element_located((By.XPATH, "//button[.//*[name()='path' and contains(@d,'m12 4')]]")))
            highlight_element(driver, year_btn)
            year_btn.click()
            time.sleep(1)
            year_btn.click()
            time.sleep(1)

            month_fetch_view = wait.until(EC.presence_of_element_located((By.XPATH, "((//*[name()='rect' and @fill='#7a73ff'])[5]/following::*[name()='text' and number(.)=number(.)])[1]")))
            highlight_element(driver, month_fetch_view)
            time.sleep(1)
            month_fetch = month_fetch_view.text.strip()
            print(f"Fetched: {month_fetch}")

            all_month_view = wait.until(EC.presence_of_element_located((By.XPATH,"(//*[name()='rect' and @stroke-width='0'])[1]")))
            highlight_element(driver, all_month_view)
            # fetch_month_view = all_month_view.get_attribute("fill")
            all_month_view.click()
            # print(f"🔹 Month View: {fetch_month_view}")
            time.sleep(2)

        except Exception as e:
            print(f"❌ Failed to open Task Details: {e}")
            return False
      
    
    with allure.step("Validate Graph Count vs Selected Count"):
        try:
           
            select_all_checkbox = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='dx-checkbox-container']")))
            highlight_element(driver, select_all_checkbox)
            select_all_checkbox.click()

            wait_for_loader_to_disappear(driver, wait)
            time.sleep(2)

            selected_elem = wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class,'dx-item-content') and contains(.,'selected')]")))
            selected_text = selected_elem.text.strip()
            selected_count = int(re.search(r'\d+', selected_text).group())

            print(f"📋 Selected Count: {selected_count}")
            graph_count = int(month_fetch)

            validation_msg = f"Graph='{month_fetch}', Selected='{selected_count}'"

            print(validation_msg)

            allure.attach(validation_msg,name="Graph Validation",attachment_type=allure.attachment_type.TEXT)
            
            if graph_count != selected_count:
                print(f"❌ FAIL: {validation_msg}")

                allure.attach(driver.get_screenshot_as_png(),name="Graph Count Mismatch",attachment_type=allure.attachment_type.PNG)
                pytest.fail(validation_msg)

            else:
                print(f"✅ PASS: {validation_msg}")

        except Exception as e:
            error_msg = f"❌ Graph Validation Error: {str(e)}"
            print(error_msg)

            allure.attach(error_msg,name="Graph Validation Error",attachment_type=allure.attachment_type.TEXT)
            allure.attach(driver.get_screenshot_as_png(),name="Error Screenshot",attachment_type=allure.attachment_type.PNG)
            pytest.fail(error_msg)
        return True