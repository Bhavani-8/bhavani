from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from datetime import datetime
import time
import allure
import os
import json
import pytest
from utilities.other_utils_functions.highlight import highlight_element
from utilities.highlight import highlight_element


def send_circular_to_user(driver, wait, user_name):

    # ------------------------------------------
    # STEP 1: LOAD LOCATORS
    # ------------------------------------------
    with allure.step("Load locators.json"):
        try:
            with open(os.path.join("data", 'locators.json'), 'r') as f:
                elements_details = json.load(f)
            circ_checkbox = elements_details['circ_checkbox']
            circ_checkbox_label = elements_details['circ_checkbox_label']
            send_email = elements_details['send_email']
            send_mail = elements_details['send_mail']
            email_log = elements_details['email_log']
            calender_btn = elements_details['calender_btn']
            email_log_header = elements_details['email_log_header']
            fetch_subject = elements_details['fetch_subject']
            email_log_close_btn = elements_details['email_log_close_btn']

            print("✅ locators.json loaded successfully")
        except Exception as e:
            allure.attach(str(e), name="Locators Error", attachment_type=allure.attachment_type.TEXT)
            pytest.fail("Failed to load locators.json")


    # ------------------------------------------
    # STEP 2: SELECT CIRCULAR CHECKBOX
    # ------------------------------------------
    with allure.step("Select Circular Checkbox"):
        checkbox_elem = wait.until(EC.presence_of_element_located((By.XPATH, circ_checkbox)))
        highlight_element(driver, checkbox_elem)
        checkbox_elem.click()
        print("✅ Circular checkbox selected")
        time.sleep(2)

        circular_label = wait.until(EC.visibility_of_element_located((By.XPATH, circ_checkbox_label)))
        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", circular_label)
        time.sleep(1)
        highlight_element(driver, circular_label, 0.2)  # Assuming your highlight function exists
        fetched_circular = circular_label.text.strip()
        print(f"Circular Found: {fetched_circular}")

    # ------------------------------------------
    # STEP 3: CLICK SEND EMAIL BUTTON
    # ------------------------------------------
    with allure.step("Click Send Email"):
        send_email_button = wait.until(EC.presence_of_element_located((By.XPATH, send_email)))
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
        send_mail_button = wait.until(EC.presence_of_element_located((By.XPATH, send_mail)))
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
        email_log_button = wait.until(EC.presence_of_element_located((By.XPATH, email_log)))
        highlight_element(driver, email_log_button)
        email_log_button.click()
        print("✅ Clicked Send Email")
        time.sleep(5)

        
   
    with allure.step("Select Start and End Dates"):
        try:
            # Open calendar
            date_button = wait.until(EC.element_to_be_clickable((By.XPATH, calender_btn)))
            highlight_element(driver, date_button)
            date_button.click()

            today = datetime.today()

            # Windows
            today_str = f"{today.day}/{today.month}/{today.year}"
            # Linux/Mac use:
            # today_str = today.strftime("%-m/%-d/%Y")

            today_xpath = f"//button[@data-day='{today_str}']"

            # First click → Start Date
            first_date = wait.until(
                EC.element_to_be_clickable((By.XPATH, today_xpath))
            )
            highlight_element(driver, first_date)
            first_date.click()
            print("✅ Start date selected")

            time.sleep(1)

            # Second click → End Date
            second_date = wait.until(
                EC.element_to_be_clickable((By.XPATH, today_xpath))
            )
            highlight_element(driver, second_date)
            second_date.click()
            print("✅ End date selected")

            time.sleep(1)

            # Close calendar if required
            email_log_label = wait.until(EC.element_to_be_clickable((By.XPATH, email_log_header)))
            email_log_label.click()

        except Exception as e:
            print(f"❌ Calendar interaction failed: {e}")

            allure.attach(
                str(e),
                name="Calendar Failure",
                attachment_type=allure.attachment_type.TEXT
            )


        user_elem = wait.until(EC.visibility_of_element_located((By.XPATH, f"//td[normalize-space()='{user_name}']")))
        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", user_elem)
        time.sleep(0.3)
        highlight_element(driver, user_elem, 0.2)  # Assuming your highlight function exists
        fetched_user_email_log = user_elem.text.strip()
        print(f"User Name Found: {fetched_user_email_log}")
        

        subject = wait.until(EC.visibility_of_element_located((By.XPATH, fetch_subject)))
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
        cross_btn = wait.until( EC.presence_of_element_located((By.XPATH, email_log_close_btn)))
        highlight_element(driver, cross_btn)
        cross_btn.click()
        time.sleep(1)

    return True