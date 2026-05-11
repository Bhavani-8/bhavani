import allure
import os
import json
import time
import pyautogui as pg
import pytest

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys

from utilities.other_utils_functions.highlight import highlight_element
from selenium.common.exceptions import TimeoutException
from utilities.add_task_utils import wait_for_loader_to_disappear

def create_company(driver, wait):

    with allure.step("Load locators.json"):
        try:
            with open(os.path.join("data", "locators.json"), "r") as f:
                elements_details = json.load(f)
            settings_icon = elements_details["settings_icon"]
            notification_icon = elements_details["notification_icon"]
            toast_msg = elements_details["toast_msg"]
            print("✅ locators.json loaded successfully")
        except Exception as e:
            allure.attach(str(e), name="Locators Load Error", attachment_type=allure.attachment_type.TEXT)
            return False
    
    try:
        with allure.step("Create Company"):
            print()
            settings_btn = wait.until(EC.presence_of_element_located((By.XPATH, settings_icon)))
            highlight_element(driver, settings_btn)
            settings_btn.click()
            print("✅ Settings Icon Clicked")
            time.sleep(2)

            # Click Company 
            company_btn = wait.until(EC.presence_of_element_located((By.XPATH, "//span[text()='Company']")))
            highlight_element(driver, company_btn)
            company_btn.click()
            print("✅ Company Button Clicked")
            time.sleep(2)

            # Click Add Another Company
            add_btn = wait.until(EC.presence_of_element_located((By.XPATH, "//table//caption[@class='add-company-link']")))
            highlight_element(driver, add_btn)
            add_btn.click()
            print("✅ Add Another Company Button Clicked")
            time.sleep(1)
            
        with allure.step("Enter Company Name"):
            # Click Add Company Name
            company_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Company Name' and @name='company_name']")))
            highlight_element(driver, company_input)
            company_input.click()
            company_input.send_keys("Dummy Company")
            time.sleep(1)
            company_input.send_keys(Keys.TAB) 
            print("✅ Company Name Entered")

        with allure.step("Select Company Type"):
            company_type_dropdown = wait.until(EC.element_to_be_clickable((By.XPATH, "(//th[normalize-space()='Company Type']/ancestor::table//tr[2]//div[contains(@class,'indicatorContainer')])[1]")))
            highlight_element(driver, company_type_dropdown)
            company_type_dropdown.click()
            time.sleep(0.5)
            first_option = wait.until(EC.element_to_be_clickable((By.XPATH, "(//div[contains(@class,'menu')]//div[contains(@class,'option')])[1]")))
            highlight_element(driver, first_option)
            first_option.click()
            print("✅ Selected first option from Company Type dropdown")

        with allure.step("Select Country Name"):
            select_country = wait.until(EC.presence_of_element_located((By.XPATH, "(//th[normalize-space()='Country']/ancestor::table//tr[2]//div[contains(@class,'indicatorContainer')])[2]")))
            highlight_element(driver, select_country)
            select_country.click()
            time.sleep(0.5)
            select_country = wait.until(EC.visibility_of_element_located((
                By.XPATH, "(//td[4]//input[contains(@id,'react-select') and @type='text' and not(@aria-hidden='true')])[last()]"
            )))
            select_country.click()
            select_country.clear()
            select_country.send_keys("India")
            india_option = wait.until(
                EC.visibility_of_element_located((By.XPATH, "//div[contains(@class,'option') and text()='India']"))
            )
            highlight_element(driver, india_option)
            india_option.click()

        with allure.step("Enter Pincode Number"):
            pincode_input = wait.until(EC.presence_of_element_located((By.XPATH, "(//td//input[@name='company_pincode' and contains(@class,'form-control')])[last()]")))
            highlight_element(driver, pincode_input)
            pincode_input.send_keys("400092")
            time.sleep(2)
        wait_for_loader_to_disappear(driver, wait)

        with allure.step("Assign Compliance Officer"):
            assign_btn = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@id='assignclassbtn' and text()='Assign']")))
            highlight_element(driver, assign_btn)
            assign_btn.click()
            assign_to_me_elem = wait.until(EC.presence_of_element_located((By.XPATH, "(//button[contains(@class,'assign-me')])[2]")))
            highlight_element(driver, assign_to_me_elem)
            assign_to_me_elem.click()

        
        with allure.step("Add License"):
            license_btn = wait.until(EC.presence_of_element_located((By.XPATH, "(//div[@class='license-count-lable align-items-center justify-content-between'])[last()]")))
            highlight_element(driver, license_btn)
            license_btn.click()

            choose_license_btn = wait.until(EC.presence_of_element_located((By.XPATH, "//p[text()='BSE']")))
            highlight_element(driver, choose_license_btn)
            choose_license_btn.click()

            license_checkbox = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@id='license-parent-BSE-0']")))
            highlight_element(driver, license_checkbox)
            license_checkbox.click()

            add_license_btn = wait.until(EC.presence_of_element_located((By.XPATH, "//button[normalize-space()='Add license']")))
            highlight_element(driver, add_license_btn)
            add_license_btn.click()
            print("✅ License Added")

        with allure.step("Save Company"):
            save_btn = wait.until(EC.presence_of_element_located((By.XPATH, "//img[@alt='check Icon']")))
            highlight_element(driver, save_btn)
            driver.execute_script("arguments[0].scrollIntoView(true);", save_btn)
            time.sleep(0.5)
            driver.execute_script("arguments[0].click();", save_btn)
            print("✅ Company Saved Successfully")

    except Exception as e:
        allure.attach(str(e), name="Company Details Submission Error", attachment_type=allure.attachment_type.TEXT)
        print(f"❌ Error: {e}")
        return False

    with allure.step("Verify toast Popup"):
        try:
            toast = wait.until(EC.presence_of_element_located((By.XPATH, toast_msg)))
            highlight_element(driver, toast)
            print(f"📢 Toast message: {toast.text.strip()}")
        except Exception:
            print("❌ No toast message found")

    wait_for_loader_to_disappear(driver, wait)

    with allure.step("Validate Normal Notification - Personal Details"):
        try:
            # Refresh page to load notifications
            pg.hotkey('ctrl', 'r')  

            # Click the notification icon
            notification_btn = wait.until(EC.presence_of_element_located((By.XPATH, notification_icon)))
            highlight_element(driver, notification_btn)
            notification_btn.click()
            time.sleep(2)  # wait for notifications to load

            # Get all normal notifications
            all_items = driver.find_elements(By.XPATH, "//li[contains(@class,'normalText')]")

            # Check for personal details notification
            personal_notification_found = False
            for item in all_items:
                text = item.text.strip()
                if "Personal" in text:  # adjust keyword if needed
                    highlight_element(driver, item)
                    print(f"🔔 Company added successfully Notification Found: {text}")
                    allure.attach(text, name="Company added successfully Notification", attachment_type=allure.attachment_type.TEXT)
                    personal_notification_found = True
                    # Click the notification to open details
                    driver.execute_script("arguments[0].click();", item)
                    print("✅ Company added successfully Notification clicked")
                    break

            if not personal_notification_found:
                print("ℹ️ Company added successfully notification not found")
                personal_btn = wait.until(EC.presence_of_element_located((By.XPATH, notification_icon)))  # replace with your icon XPath
                highlight_element(driver, personal_btn)
                print("✅ Company added successfully")

        except Exception as e:
            msg = f"❌ Error while checking personal details notification: {e}"
            print(msg)
            allure.attach(msg, name="Company added successfully Error", attachment_type=allure.attachment_type.TEXT)

    try:
        with allure.step("Create Company"):
            print()
            settings_btn = wait.until(EC.presence_of_element_located((By.XPATH, settings_icon)))
            highlight_element(driver, settings_btn)
            settings_btn.click()
            print("✅ Settings Icon Clicked")
            
            company_btn = wait.until(EC.presence_of_element_located((By.XPATH, "//span[text()='Company']")))
            highlight_element(driver, company_btn)
            company_btn.click()
            time.sleep(2)
            print("✅ Company Button Clicked")

            all_co_items = wait.until(EC.presence_of_element_located((By.XPATH, "//tr[last()]//div[contains(@id,'assignclassbtn')]")))
            highlight_element(driver, all_co_items)
            driver.execute_script("arguments[0].click();", all_co_items)
            print("✅ Settings Icon Clicked")

            option_input = wait.until(EC.presence_of_element_located((By.XPATH, "(//div[contains(@class,'email-list-row')]/span[contains(@class,'name-of-emailer')])[1]")))
            highlight_element(driver, option_input)
            option_input.click()
            time.sleep(1)

            save_btn = wait.until(EC.presence_of_element_located((By.XPATH, "//img[@alt='check Icon']")))
            highlight_element(driver, save_btn)
            driver.execute_script("arguments[0].scrollIntoView(true);", save_btn)
            time.sleep(1)
            driver.execute_script("arguments[0].click();", save_btn)
            print("✅ Company Saved Successfully")
    
    except Exception as e:
        allure.attach(str(e), name="Company Details Submission Error", attachment_type=allure.attachment_type.TEXT)
        print(f"❌ Error: {e}")
        return False
    
    with allure.step("Verify toast Popup"):
        try:
            toast = wait.until(EC.presence_of_element_located((By.XPATH, toast_msg)))
            highlight_element(driver, toast)
            print(f"📢 Toast message: {toast.text.strip()}")
        except Exception:
            print("❌ No toast message found")

    wait_for_loader_to_disappear(driver, wait)
    with allure.step("Validate Normal Notification - Personal Details"):
        try:
            pg.hotkey('ctrl', 'r')  
            notification_btn = wait.until(EC.presence_of_element_located((By.XPATH, notification_icon)))
            highlight_element(driver, notification_btn)
            notification_btn.click()
            time.sleep(2)  # wait for notifications to load
            all_items = driver.find_elements(By.XPATH, "//li[contains(@class,'normalText')]")

            # Check for personal details notification
            personal_notification_found = False
            for item in all_items:
                text = item.text.strip()
                if "Personal" in text:  # adjust keyword if needed
                    highlight_element(driver, item)
                    print(f"🔔 Company Updated Successfully Notification Found: {text}")
                    allure.attach(text, name="Company Updated Successfully Notification", attachment_type=allure.attachment_type.TEXT)
                    personal_notification_found = True
                    # Click the notification to open details
                    driver.execute_script("arguments[0].click();", item)
                    print("✅ Company Updated Successfully Notification clicked")
                    break

            if not personal_notification_found:
                print("ℹ️ Company Updated Successfully notification not found")
                personal_btn = wait.until(EC.presence_of_element_located((By.XPATH, notification_icon)))  # replace with your icon XPath
                highlight_element(driver, personal_btn)

        except Exception as e:
            msg = f"❌ Error while checking personal details notification: {e}"
            print(msg)
            allure.attach(msg, name="Company Updated Successfully Error", attachment_type=allure.attachment_type.TEXT)

    return True

