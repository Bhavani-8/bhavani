from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from datetime import datetime, timedelta

import time
import allure
import os
import json
import pytest
import pyautogui as pg  
from utilities.add_task_utils import wait_for_loader_to_disappear
from utilities.login_utils import login_check
from utilities.other_utils_functions.highlight import highlight_element
from utilities.add_task_utils import wait_for_loader_to_disappear
from utilities.other_utils_functions.license_utils import validate_license_subscription
from utilities.highlight import highlight_element


def send_circular_to_user(driver, wait, user_name):

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


    # ------------------------------------------
    # STEP 2: SELECT CIRCULAR CHECKBOX
    # ------------------------------------------
    with allure.step("Select Circular Checkbox"):
        checkbox_elem = wait.until(EC.presence_of_element_located((By.XPATH, "(//span[@role='checkbox'])[2]")))
        highlight_element(driver, checkbox_elem)
        checkbox_elem.click()
        print("✅ Circular checkbox selected")
        time.sleep(2)

        circular_label = wait.until(EC.visibility_of_element_located((By.XPATH, "(//p[@class='text-xs leading-snug font-semibold text-left'])[1]")))
        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", circular_label)
        time.sleep(1)
        highlight_element(driver, circular_label, 0.2)  # Assuming your highlight function exists
        fetched_circular = circular_label.text.strip()
        print(f"Circular Found: {fetched_circular}")

    # ------------------------------------------
    # STEP 3: CLICK SEND EMAIL BUTTON
    # ------------------------------------------
    with allure.step("Click Send Email"):
        send_email_button = wait.until(EC.presence_of_element_located((By.XPATH, "//button[text()='Send Email']")))
        highlight_element(driver, send_email_button)
        send_email_button.click()
        print("✅ Clicked Send Email")
        time.sleep(2)

    # ------------------------------------------
    # STEP 4: TYPE USER NAME IN INPUT
    # ------------------------------------------
    with allure.step("Enter User Name"):
        user_name = user_name.strip()
        user_check_box = wait.until(EC.presence_of_element_located((By.XPATH, f"//span[contains(text(),'{user_name}')]")))
        highlight_element(driver, user_check_box)
        fetched_user = user_check_box.text.strip()
        user_check_box.click()
        time.sleep(2)
        print(f"✅ User selected: {user_name}")

        
    # STEP 5: CLICK SEND MAIL BUTTON
    # ------------------------------------------
    with allure.step("Click Send Mail"):
        send_mail_button = wait.until(EC.presence_of_element_located((By.XPATH, "//button[text()='Send Mail']")))
        highlight_element(driver, send_mail_button)
        send_mail_button.click()
        print("📨 Email sent successfully!")
        time.sleep(3)

    # Validate toast message
    with allure.step("Validate toast notification for creation of a task without an assignee"):
        toast = wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class,'Toastify__toast--success')]")))
        highlight_element(driver, toast)
        print(f"📢 Toast message: {toast.text.strip()}")
    
    with allure.step("Click Send Email"):
        email_log_button = wait.until(EC.presence_of_element_located((By.XPATH, "//button[text()='Email Log']")))
        highlight_element(driver, email_log_button)
        email_log_button.click()
        print("✅ Clicked Send Email")
        time.sleep(5)

        
        
    with allure.step("Select Start and End Dates"):
        try:
           
            date_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@data-slot='popover-trigger']")))
            date_button.click()

            today = datetime.today()
            today_str = today.strftime("%#m/%#d/%Y")  # use %-m on Mac/Linux

            date_btn = wait.until(
                EC.element_to_be_clickable((By.XPATH, f"//button[@data-day='{today_str}']"))
            )

            highlight_element(driver, date_btn)

            # Click twice
            date_btn.click()
            time.sleep(2)

            email_log_label = wait.until(EC.element_to_be_clickable((By.XPATH, "//h1[text()='Email Log']")))
            email_log_label.click()

        except Exception as e:
            print(f"❌ Calendar interaction failed: {e}")
            allure.attach(str(e), name="Calendar Failure", attachment_type=allure.attachment_type.TEXT)   
            pytest.fail("Date selection failed")

        user_elem = wait.until(EC.visibility_of_element_located((By.XPATH, f"//td[normalize-space()='{user_name}']")))
        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", user_elem)
        time.sleep(0.3)
        highlight_element(driver, user_elem, 0.2)  # Assuming your highlight function exists
        fetched_user_email_log = user_elem.text.strip()
        print(f"User Name Found: {fetched_user_email_log}")
        

        subject = wait.until(EC.visibility_of_element_located((By.XPATH, "(//span[@class='line-clamp-2'])[last()]")))
        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", subject)
        time.sleep(0.3)
        highlight_element(driver, subject, 0.2)  # Assuming your highlight function exists
        fetched_subject = subject.text.strip()
        print(f"Circular found: {fetched_subject}")


         # Step 4: Validate  Circular 
    with allure.step("Verify User Name"):
        if fetched_user == fetched_user_email_log:
            print("✅ User Name Verified successfully!")
            allure.attach(f"User Name: {fetched_user}",name="User Name Check",attachment_type=allure.attachment_type.TEXT)
            return True
        else:
            print(f"❌ User Name Mismatch! Grid: {fetched_user}: {fetched_user_email_log}")
            allure.attach(f"Grid: {fetched_user}: {fetched_user_email_log}",name="User Name Mismatch",attachment_type=allure.attachment_type.TEXT)
            return False
        # =========================
        # Step 4: Validate  User Name
    with allure.step("Verify Circular"):
        if fetched_circular == fetched_subject:
            print("✅ Circular Verified successfully!")
            allure.attach(f"Circular: {fetched_circular}",name="Circular Check",attachment_type=allure.attachment_type.TEXT)
            return True
        else:
            print(f"❌ Circular Mismatch! Grid: {fetched_circular}: {fetched_subject}")
            allure.attach(f"Grid: {fetched_circular}: {fetched_subject}",name="Circular Mismatch",attachment_type=allure.attachment_type.TEXT)
            return False
            
    with allure.step("Clicked Close Button"):
        cross_btn = wait.until( EC.presence_of_element_located((By.XPATH, "//div[@class='flex flex-row items-center gap-2']//button")))
        highlight_element(driver, cross_btn)
        cross_btn.click()
        time.sleep(1)

    return True