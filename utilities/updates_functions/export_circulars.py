import time
import pytest
import os
import json
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from utilities.other_utils_functions.highlight import highlight_element
import pyautogui as pg
from selenium.common.exceptions import TimeoutException
from utilities.add_task_functions.wait_for_loader_to_disappear import wait_for_loader_to_disappear
from datetime import datetime, timedelta
def export_circulars(driver, wait):
    wait_less = WebDriverWait(driver, 5)

    # ✅ Load locators
    with allure.step("Load locators.json for Export Data Validation"):
        try:
            with open(os.path.join("data", 'locators.json'), 'r') as f:
                elements_details = json.load(f)
                dash_total_btn = elements_details['dash_total_btn']
                dash_col_all_selection_btn = elements_details['dash_col_all_selection_btn']
                export_btn = elements_details['export_btn']
                export_all_data_btn = elements_details['export_all_data_btn']
                export_selected_rows_btn = elements_details['export_selected_rows_btn']
                toast_msg = elements_details['toast_msg']
            print("✅ locators.json loaded successfully")
        except FileNotFoundError as e:
            print("❌ locators.json file not found")
            allure.attach(str(e), name="Locators_FileNotFound", attachment_type=allure.attachment_type.TEXT)
            pytest.fail("locators.json file not found")
        except json.JSONDecodeError as e:
            print("❌ Invalid JSON in locators.json")
            allure.attach(str(e), name="Invalid_JSON", attachment_type=allure.attachment_type.TEXT)
            pytest.fail("Invalid JSON in locators.json")


    # ✅ Export → All Data
    with allure.step("Export All Data from Dashboard"):
        try:
            export_data_btn = wait_less.until(EC.presence_of_element_located((By.XPATH, "//button[text()='Export']")))
            export_data_btn.click()
        except Exception as e:
            print("❌ Failed to export Button")
            allure.attach(str(e), name="Export_All_Error", attachment_type=allure.attachment_type.TEXT)
            return False
    with allure.step("Click Last Month Option"):
        try:
            last_month_option = wait_less.until(EC.presence_of_element_located((By.XPATH, "//div[text()='Last month']")))
            last_month_option.click()
        except Exception as e:
            print("❌ Failed to select Last Month option")
            allure.attach(str(e), name="Last_Month_Option_Error", attachment_type=allure.attachment_type.TEXT)
            return False
    
        try:
            toast = wait.until(EC.presence_of_element_located((By.XPATH, toast_msg)))
            highlight_element(driver, toast)
            print(f"📢 Toast message - Last Month: {toast.text.strip()}")
        except Exception as e:
            print("❌ Failed to capture toast message after exporting all data")
            allure.attach(str(e), name="Export_All_Toast_Error", attachment_type=allure.attachment_type.TEXT)
            return False
    with allure.step("Export All Data from Dashboard"):
        try:
            export_data_btn = wait_less.until(EC.presence_of_element_located((By.XPATH, "//button[text()='Export']")))
            export_data_btn.click()
        except Exception as e:
            print("❌ Failed to export Button")
            allure.attach(str(e), name="Export_All_Error", attachment_type=allure.attachment_type.TEXT)
            return False

    with allure.step("Click Last 2 Months Option"):
        try:
            last_2_month_option = wait_less.until(EC.presence_of_element_located((By.XPATH, "//div[text()='Last 2 months']")))
            last_2_month_option.click()
        except Exception as e:
            print("❌ Failed to select Last 2 Months option")
            allure.attach(str(e), name="Last_2_Months_Option_Error", attachment_type=allure.attachment_type.TEXT)
            return False
        try:
            toast = wait.until(EC.presence_of_element_located((By.XPATH, toast_msg)))
            highlight_element(driver, toast)
            print(f"📢 Toast message - Last 2 Months: {toast.text.strip()}")
            time.sleep(6)
        except Exception as e:
            print("❌ Failed to capture toast message after exporting all data")
            allure.attach(str(e), name="Export_All_Toast_Error", attachment_type=allure.attachment_type.TEXT)
            return False
    with allure.step("Export All Data from Dashboard"):
        try:
            export_data_btn = wait_less.until(EC.presence_of_element_located((By.XPATH, "//button[text()='Export']")))
            export_data_btn.click()
        except Exception as e:
            print("❌ Failed to export Button")
            allure.attach(str(e), name="Export_All_Error", attachment_type=allure.attachment_type.TEXT)
            return False
    with allure.step("Click Last 3 Months Option"):
        try:
            last_3_month_option = wait_less.until(EC.presence_of_element_located((By.XPATH, "//div[text()='Last 3 months']")))
            last_3_month_option.click()
        except Exception as e:
            print("❌ Failed to select Last 3 Months option")
            allure.attach(str(e), name="Last_3_Months_Option_Error", attachment_type=allure.attachment_type.TEXT)
            return False
        try:
            toast = wait.until(EC.presence_of_element_located((By.XPATH, toast_msg)))
            highlight_element(driver, toast)
            print(f"📢 Toast message - Last 3 Months: {toast.text.strip()}")
        except Exception as e:
            print("❌ Failed to capture toast message after exporting all data")
            allure.attach(str(e), name="Export_All_Toast_Error", attachment_type=allure.attachment_type.TEXT)
            return False
    with allure.step("Export All Data from Dashboard"):
        try:
            export_data_btn = wait_less.until(EC.presence_of_element_located((By.XPATH, "//button[text()='Export']")))
            export_data_btn.click()
        except Exception as e:
            print("❌ Failed to export Button")
            allure.attach(str(e), name="Export_All_Error", attachment_type=allure.attachment_type.TEXT)
            return False
    with allure.step("Click Custom Option"):
        try:
            custom_option = wait_less.until(EC.presence_of_element_located((By.XPATH, "//div[text()='Custom']")))
            custom_option.click()
        except Exception as e:
            print("❌ Failed to select Custom option")
            allure.attach(str(e), name="Custom_Option_Error", attachment_type=allure.attachment_type.TEXT)
            return False
    
        try:
            calendar_option = wait.until(EC.presence_of_element_located((By.XPATH, "//button[@data-slot='popover-trigger']")))
            calendar_option.click()
            time.sleep(0.5)
        except Exception as e:
            print("❌ Failed to click calendar option")
            allure.attach(str(e), name="Calendar_Option_Error", attachment_type=allure.attachment_type.TEXT)
            return False
        try:
            
            # wait = WebDriverWait(driver, 10)

            today = datetime.today()
            start_date = today - timedelta(days=7)

            # Format → M/D/YYYY (IMPORTANT)
            start_day = f"{start_date.month}/{start_date.day}/{start_date.year}"
            end_day = f"{today.month}/{today.day}/{today.year}"

            print("Start:", start_day)
            print("End:", end_day)

            # Click start date
            
            star_date = wait.until(EC.element_to_be_clickable((By.XPATH, f"//button[@data-day='{start_day}']")))
            star_date.click()

            # Click end date (today)
            end_xpath = f"//button[@data-day='{end_day}']"
            end_date = wait.until(EC.element_to_be_clickable((By.XPATH, end_xpath)))
            end_date.click()
        except Exception as e:
            print("❌ Failed to select custom date range")
            allure.attach(str(e), name="Custom_Date_Selection_Error", attachment_type=allure.attachment_type.TEXT)
            return False
        try:
            export_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "(//button[text()='Export'])[2]")))
            export_btn.click()
        except Exception as e:
            print("❌ Failed to click Export button after selecting custom date range")
            allure.attach(str(e), name="Custom_Export_Button_Error", attachment_type=allure.attachment_type.TEXT)
            return False
        try:
            toast = wait.until(EC.presence_of_element_located((By.XPATH, toast_msg)))
            highlight_element(driver, toast)
            print(f"📢 Toast message - Custom Date Range: {toast.text.strip()}")
            time.sleep(5)
        except Exception as e:
            print("❌ Failed to capture toast message after exporting all data")
            allure.attach(str(e), name="Export_All_Toast_Error", attachment_type=allure.attachment_type.TEXT)
            return False
    with allure.step("Select Circular Checkbox"):
        try:
            checkbox_elem = wait.until(EC.presence_of_element_located((By.XPATH, "(//span[@role='checkbox' and @aria-checked='false'])[2]")))
            highlight_element(driver, checkbox_elem)
            checkbox_elem.click()
            print("✅ Circular checkbox selected")
            time.sleep(2)
        except Exception as e:
            print("❌ Failed to select Circular checkbox")
            allure.attach(str(e), name="Circular_Checkbox_Error", attachment_type=allure.attachment_type.TEXT)
            return False
    
    with allure.step("Export All Data from Dashboard"):
        try:
            export_data_btn = wait_less.until(EC.presence_of_element_located((By.XPATH, "//button[text()='Export']")))
            export_data_btn.click()
        except Exception as e:
            print("❌ Failed to export Button")
            allure.attach(str(e), name="Export_All_Error", attachment_type=allure.attachment_type.TEXT)
            return False
        
    with allure.step("Click Selected Circulars Option"):
        try:
            selected_circulars_option = wait.until(EC.presence_of_element_located((By.XPATH, "//div[text()='Selected circulars']")))
            selected_circulars_option.click()
            time.sleep(3)
        except Exception as e:
            print("❌ Failed to select Selected Circulars option")
            allure.attach(str(e), name="Selected_Circulars_Option_Error", attachment_type=allure.attachment_type.TEXT)
            return False
        
    return True