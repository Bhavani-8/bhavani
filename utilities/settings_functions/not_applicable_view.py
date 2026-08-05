from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import allure 
import os
import json
import pytest
import time

from utilities.add_task_functions.wait_for_loader_to_disappear import wait_for_loader_to_disappear
from utilities.other_utils_functions.highlight import highlight_element


def not_applicable_view(driver, wait):
    # ------------------------------------------
    # STEP 1: LOAD LOCATORS
    # ------------------------------------------
    with allure.step("Load locators.json"):
        try:
            with open(os.path.join("data", 'locators.json'), 'r') as f:
                elements_details = json.load(f)
                settings_icon = elements_details["settings_icon"]
            print("✅ locators.json loaded successfully")
        except Exception as e:
            allure.attach(str(e), name="Locators Error", attachment_type=allure.attachment_type.TEXT)
            pytest.fail("Failed to load locators.json")
    
    with allure.step("Click Settings"):
        try:
            settings_btn = wait.until(EC.presence_of_element_located((By.XPATH, settings_icon)))
            highlight_element(driver, settings_btn)
            settings_btn.click()
        except Exception as e:
            print("❌ Failed to click Settings")
            allure.attach(str(e), name="Settings Error", attachment_type=allure.attachment_type.TEXT)
            raise
    
    with allure.step("Click Not Applicable"):
        try:
            not_applicable = wait.until(EC.presence_of_element_located((By.XPATH, "//span[text()='Not Applicable tasks']")))
            highlight_element(driver, not_applicable)
            not_applicable.click()
            time.sleep(1)
        except Exception as e:
            print("❌ Failed to click not applicable")
            allure.attach(str(e), name="Not Applicable Error", attachment_type=allure.attachment_type.TEXT)
            raise

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
            header_label = wait.until(EC.element_to_be_clickable((By.XPATH, "(//div[@class='-ml-1.5 flex items-center gap-1'])[1]")))
            header_label.click()
        except Exception as e:
            print(f"❌ Failed to click Header label: {e}")
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
            company_name = wait.until(EC.presence_of_element_located((By.XPATH, "//span[text()='Company Name']")))
            highlight_element(driver, company_name)
            company_name.click()
            time.sleep(2)
            print("🟦 'Company' deselected")
        except Exception as e:
            allure.attach(str(e), name="Deselect Company Error", attachment_type=allure.attachment_type.TEXT)
            return False

        try:
            header_label = wait.until(EC.element_to_be_clickable((By.XPATH, "(//div[@class='-ml-1.5 flex items-center gap-1'])[1]")))
            header_label.click()
        except Exception as e:
            print(f"❌ Failed to click Header label: {e}")
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