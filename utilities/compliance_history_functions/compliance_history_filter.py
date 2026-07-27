from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import allure 
import pandas as pd
import pyautogui as pg
import os
import json
import pytest
import time
from datetime import datetime, timedelta

from utilities.add_task_functions.wait_for_loader_to_disappear import wait_for_loader_to_disappear
from utilities.other_utils_functions.highlight import highlight_element


def compliance_history_filter(driver, wait):
    wait_less = WebDriverWait(driver, 5)
    # ------------------------------------------
    # STEP 1: LOAD LOCATORS
    # ------------------------------------------
    with allure.step("Load locators.json"):
        try:
            with open(os.path.join("data", 'locators.json'), 'r') as f:
                elements_details = json.load(f)
            print("✅ locators.json loaded successfully")
        except Exception as e:
            allure.attach(str(e), name="Locators Error", attachment_type=allure.attachment_type.TEXT)
            pytest.fail("Failed to load locators.json")

    with allure.step("Select Update Checkbox"):
        try:
            filters_btn = wait.until(EC.presence_of_element_located((By.XPATH, "//button[@data-slot='drawer-trigger']")))
            highlight_element(driver, filters_btn)
            filters_btn.click()
            print("🟦 First checkbox clicked")
            time.sleep(2)
        except Exception as e:
            allure.attach(str(e), name="Updates Section Error", attachment_type=allure.attachment_type.TEXT)
            return False
    
    with allure.step("Click on Select Company Dropdown"):
        try:
            select_company = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Select Company']")))
            highlight_element(driver, select_company)
            select_company.click()
            time.sleep(2)
            print("🟦 Select Company clicked")
        except Exception as e:
            allure.attach(str(e), name="Select Company Error", attachment_type=allure.attachment_type.TEXT)
            return False
        try :
            select_first_company = wait.until(EC.element_to_be_clickable((By.XPATH, "(//div[@class='flex flex-1 gap-2 shrink-0 whitespace-nowrap'])[1]")))
            highlight_element(driver, select_first_company)  
            fetch_company_name = select_first_company.text
            select_first_company.click()
            time.sleep(1)
            print(f"🟦 First company selected: {fetch_company_name}")
            allure.attach(f"Company: {fetch_company_name}",name="Selected Company",attachment_type=allure.attachment_type.TEXT)
            filters_label = wait.until(EC.element_to_be_clickable((By.XPATH, "//h2[text()='Filters']"))) 
            filters_label.click()
            time.sleep(2)     
        except Exception as e:
            allure.attach(str(e), name="Select First Company Error", attachment_type=allure.attachment_type.TEXT)
            return False     

    with allure.step("Click on Select License Dropdown"):
        try:
            select_license = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Select License']")))
            highlight_element(driver, select_license)
            select_license.click()
            time.sleep(2)
            print("🟦 Select License clicked")
        except Exception as e:
            allure.attach(str(e), name="Select License Error", attachment_type=allure.attachment_type.TEXT)
            return False
    
    
        try :
            select_first_license = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[text()='CDSL']")))
            highlight_element(driver, select_first_license)
            fetch_license_name = select_first_license.text  
            select_first_license.click()
            time.sleep(1)
            print(f"🟦 First industry selected: {fetch_license_name}")
            allure.attach(f"Industry: {fetch_license_name}",name="Selected Industry",attachment_type=allure.attachment_type.TEXT)
            filters_label = wait.until(EC.element_to_be_clickable((By.XPATH, "//h2[text()='Filters']"))) 
            filters_label.click()
            time.sleep(2)     
        except Exception as e:
            allure.attach(str(e), name="Select First Industry Error", attachment_type=allure.attachment_type.TEXT)
            return False 
    
    with allure.step("Click on Select Date calendar"):
        try:
            select_from_date = wait.until(EC.element_to_be_clickable((By.XPATH, "(//button[@aria-label='Select date'])[1]")))
            highlight_element(driver, select_from_date)
            select_from_date.click()
            time.sleep(2)

            # today = datetime.today()
            # today_str = today.strftime("%#m/%#d/%Y")  

            # date_btn = wait.until(EC.presence_of_element_located((By.XPATH, f"//button[@data-day='{today_str}']")))

            # driver.execute_script("arguments[0].scrollIntoView(true);", date_btn)
            # driver.execute_script("arguments[0].click();", date_btn)
            today_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Today')]")))
            highlight_element(driver, today_btn)
            driver.execute_script("arguments[0].click();", today_btn)
            time.sleep(2)
            time.sleep(2)
            print("🟦 Select Date clicked")
        except Exception as e:
            allure.attach(str(e), name="Select Date Error", attachment_type=allure.attachment_type.TEXT)
            return False
        try :
            select_to_date = wait.until(EC.element_to_be_clickable((By.XPATH, "(//button[@aria-label='Select date'])[2]")))
            highlight_element(driver, select_to_date)
            select_to_date.click()
            time.sleep(2)

            # today = datetime.today()
            # today_str = today.strftime("%#m/%#d/%Y")  
           
            # date_btn = wait.until(EC.element_to_be_clickable((By.XPATH, f"//button[@data-day='{today_str}']")))

            # driver.execute_script("arguments[0].scrollIntoView(true);", date_btn)
            # driver.execute_script("arguments[0].click();", date_btn)

            today_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Today')]")))
            highlight_element(driver, today_btn)
            driver.execute_script("arguments[0].click();", today_btn)
            time.sleep(2)
            print("🟦 Select Date clicked")
        except Exception as e:
            allure.attach(str(e), name="Select Date Error", attachment_type=allure.attachment_type.TEXT)
            return False
    with allure.step("Click on View Updates button"):
        try:
            history_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='View History']")))
            highlight_element(driver, history_btn)
            history_btn.click()
            time.sleep(3)
            print("🟦 View Updates button clicked")
        except Exception as e:
            allure.attach(str(e), name="Updates Button Error", attachment_type=allure.attachment_type.TEXT)
            return False
        
    with allure.step(f"Check if results found "):
        try:
            no_results_text =wait.until(EC.presence_of_element_located((By.XPATH, "//td[text()='No results.']")))
            highlight_element(driver, no_results_text)
            print(f"⚠️ No Task Found ")
            allure.attach("No results found in table",name="No Results",attachment_type=allure.attachment_type.TEXT)
        except Exception as e:
            print(f"✅ Tasks found ")
    
    with allure.step("Select Update Checkbox"):
        try:
            filters_btn = wait.until(EC.presence_of_element_located((By.XPATH, "//button[@data-slot='drawer-trigger']")))
            highlight_element(driver, filters_btn)
            filters_btn.click()
            print("🟦 First checkbox clicked")
            time.sleep(2)
        except Exception as e:
            allure.attach(str(e), name="Updates Section Error", attachment_type=allure.attachment_type.TEXT)
            return False
    
    with allure.step("Click on Reset Button"):
        try:
            reset_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Reset']")))
            highlight_element(driver, reset_btn)
            reset_btn.click()
            time.sleep(2)
            print("🟦 Reset button clicked")
        except Exception as e:
            allure.attach(str(e), name="Reset Button Error", attachment_type=allure.attachment_type.TEXT)
            return False
    
    return True