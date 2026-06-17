import allure
import json
import os
import time
import pytest
from datetime import datetime, timedelta
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from utilities.other_utils_functions.highlight import highlight_element
from selenium.common.exceptions import TimeoutException
from utilities.add_task_utils import wait_for_loader_to_disappear

   
def project_filter(driver, wait):

    with allure.step("Load locators.json"):
        try:
            with open(os.path.join("data", "locators.json"), "r") as f:
                elements_details = json.load(f)

            project_icon = elements_details["project_icon"]


            print("✅ locators.json loaded")
        except Exception as e:
            print(f"❌ Invalid JSON in locators.json")
            allure.attach(str(e), "Invalid JSON in locators.json", allure.attachment_type.TEXT)
            return False
        
    with allure.step("Click project icon"):
        try:
            project_btn = wait.until(EC.presence_of_element_located((By.XPATH, project_icon)))
            highlight_element(driver, project_btn)
            project_btn.click()
            time.sleep(2)
        except Exception as e:
           print(f"❌ Error Clicking Project Icon")
           allure.attach(str(e), "Errot clicking project icon", allure.attachment_type.TEXT)
           return False
    with allure.step("Click Project filter button"):
        try:
            project_filter = wait.until(EC.element_to_be_clickable((By.XPATH, "//i[@class='dx-icon dx-icon-filter']")))
            highlight_element(driver, project_filter)
            driver.execute_script("arguments[0].click();", project_filter)
            time.sleep(1)
        except Exception as e:
           print(f"❌ Error Clicking Project filter button")
           allure.attach(str(e), "Error clicking project filter button", allure.attachment_type.TEXT)
           return False
    
    with allure.step("Select Dates from Calendar"):
        try:

            today = datetime.today().date()
            past_date = (today - timedelta(days=3)).strftime("%Y-%m-%d")
            future_date = (today + timedelta(days=3)).strftime("%Y-%m-%d")
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
            print(f"❌ Error Selecting Dates from Calendar")
            allure.attach(str(e), "Error Selecting Dates form Calendar", allure.attachment_type.TEXT)
            return False
    
    with allure.step("Click Project filter button"):
        try:
            project_filter = wait.until(EC.element_to_be_clickable((By.XPATH, "//i[@class='dx-icon dx-icon-filter']")))
            highlight_element(driver, project_filter)
            driver.execute_script("arguments[0].click();", project_filter)
            time.sleep(1)
        except Exception as e:
           print(f"❌ Error Click Project filter button")
           allure.attach(str(e), "Error Click Project filter button", allure.attachment_type.TEXT)
           return False

        try:
            reset_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "(//span[text()='Reset'])[2]")))
            reset_btn.click()
            time.sleep(0.5)
        except Exception as e:
            print(f"❌ Error Clicking reset button")
            allure.attach(str(e), "Error clicking reset button", allure.attachment_type.TEXT)
           
    return True

    