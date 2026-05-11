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


def compliance_view(driver, wait):
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

    with allure.step("Click View Button"):
        try:
            view_btn = wait.until(EC.presence_of_element_located((By.XPATH, "//button[normalize-space()='View' and @data-slot='popover-trigger']")))
            highlight_element(driver, view_btn)
            view_btn.click()
            print("🟦 View Button Clicked")
            time.sleep(2)
        except Exception as e:
            allure.attach(str(e), name="View Button Error", attachment_type=allure.attachment_type.TEXT)
            return False
    
    with allure.step("Select all options in view dropdown"):
        items = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//div[@data-slot='command-item']")))
        for i in range(len(items)):

            # 🔁 re-fetch (important for dynamic UI)
            items = driver.find_elements(By.XPATH, "//div[@data-slot='command-item']")
            item = items[i]

            name = item.text.strip()

            aria = item.get_attribute("aria-selected")
            selected = item.get_attribute("data-selected")
            checked = item.get_attribute("data-checked")

            # -----------------------------
            # NORMALIZE STATE
            # -----------------------------
            if aria == "true" or selected == "true" or checked == "true":
                status = "selected"
            else:
                status = "deselected"

            print(f"{name} → {status}")

            # -----------------------------
            # ONLY CLICK IF DESELECTED
            # -----------------------------
            if status == "deselected":

                driver.execute_script("arguments[0].scrollIntoView({block:'center'});",item)
                time.sleep(0.5)

                item.click()
                time.sleep(1)

                print(f"✅ Selected: {name}")

            else:
                print(f"✔ Already selected: {name}")

        try:
            compliance_label = wait.until(EC.element_to_be_clickable((By.XPATH, "//h2[text()='Compliance History']")))
            compliance_label.click()
        except Exception as e:
            print(f"❌ Failed to click Compliance History label: {e}")
            return False
    
    with allure.step("Verify all column headers"):
        try:
            print()
            headers = driver.find_elements(By.XPATH, "//th[@data-slot='table-head']")
            text = [h.text.strip() for h in headers if h.text.strip()]
            print(f"Column headers: {text}")

            headers_text = "\n".join(text)
            allure.attach(headers_text,name="Column Headers",attachment_type=allure.attachment_type.TEXT)

        except Exception as e:
            print(f"❌ Failed to fetch column headers: {e}")
            return False
    
    with allure.step("Click View Button"):
        try:
            print()
            view_btn = wait.until(EC.presence_of_element_located((By.XPATH, "//button[normalize-space()='View' and @data-slot='popover-trigger']")))
            highlight_element(driver, view_btn)
            view_btn.click()
            print("🟦 View Button Clicked")
            time.sleep(2)
        except Exception as e:
            allure.attach(str(e), name="View Button Error", attachment_type=allure.attachment_type.TEXT)
            return False
    with allure.step("Deselect Company"):
        try:
            company_item = wait.until(EC.presence_of_element_located((By.XPATH, "//span[text()='Company']")))
            highlight_element(driver, company_item)
            company_item.click()
            time.sleep(2)
            print("🟦 'Company' deselected")
        except Exception as e:
            allure.attach(str(e), name="Deselect Company Error", attachment_type=allure.attachment_type.TEXT)
            return False

        try:
            compliance_label = wait.until(EC.element_to_be_clickable((By.XPATH, "//h2[text()='Compliance History']")))
            compliance_label.click()
        except Exception as e:
            print(f"❌ Failed to click Compliance History label: {e}")
            return False
    
    with allure.step("Verify column headers after deselecting Company"):
        try:
            # STEP 8: Get headers again
            headers = driver.find_elements(By.XPATH, "//th[@data-slot='table-head']")
            after = [h.text.strip() for h in headers if h.text.strip()]
            print("AFTER:", after)

            after_text = "\n".join(after)
            allure.attach(after_text,name="Column Headers After Deselect",attachment_type=allure.attachment_type.TEXT)
        except Exception as e:
            print(f"❌ Failed to fetch column headers: {e}")
            return False
    
            
    return True