import allure
import time
import os
import json
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from utilities.add_task_functions.wait_for_loader_to_disappear import wait_for_loader_to_disappear
from utilities.other_utils_functions.highlight import highlight_element


def check_day_week_month_buttons(driver, wait):
    
    with allure.step("Load locators.json"):
        try:
            with open(os.path.join("data", "locators.json"), "r") as f:
                elements_details = json.load(f)
            calendar_icon = elements_details["calendar_icon"]
            calendar_day_btn = elements_details["calendar_day_btn"]
            calendar_week_btn = elements_details["calendar_week_btn"]
            calendar_month_btn = elements_details["calendar_month_btn"]

            print("✅ locators.json loaded successfully")
        except Exception as e:
            allure.attach(str(e), name="Locators Load Error", attachment_type=allure.attachment_type.TEXT)
            return False
    
    with allure.step("Click Calendar Button"):
        try:
            calendar_btn = wait.until(EC.presence_of_element_located((By.XPATH, calendar_icon)))
            highlight_element(driver, calendar_btn)
            calendar_btn.click()
            time.sleep(3)
        except Exception as e:
            msg = f"failed to click Calender button: {str(e)}"
            print(msg)
            allure.attach(msg, name="Calendar Button Error", attachment_type=allure.attachment_type.TEXT)
            return False
    
    with allure.step("Click Day Button in Calendar"):
        try:
            day_btn = wait.until(EC.presence_of_element_located((By.XPATH, calendar_day_btn)))
            highlight_element(driver, day_btn)
            day_btn.click()
            wait_for_loader_to_disappear(driver, wait)
            time.sleep(3)
        except Exception as e:
            msg = f"failed to click Day button: {str(e)}"
            print(msg)
            allure.attach(msg, name="Day Button Error", attachment_type=allure.attachment_type.TEXT)
            return False
    
    with allure.step("Click Week Button in Calendar"):
        try:
            week_btn = wait.until(EC.presence_of_element_located((By.XPATH, calendar_week_btn)))
            highlight_element(driver, week_btn)
            week_btn.click()
            wait_for_loader_to_disappear(driver, wait)
            time.sleep(3)
        except Exception as e:
            msg = f"failed to click Week button: {str(e)}"
            print(msg)
            allure.attach(msg, name="Week Button Error", attachment_type=allure.attachment_type.TEXT)
            return False

    with allure.step("Click Month Button in Calendar"):
        try:
            month_btn = wait.until(EC.presence_of_element_located((By.XPATH, calendar_month_btn)))
            highlight_element(driver, month_btn)
            month_btn.click()
            wait_for_loader_to_disappear(driver, wait)
            time.sleep(3)
        except Exception as e:
            msg = f"failed to click Month button: {str(e)}"
            print(msg)
            allure.attach(msg, name="Month Button Error", attachment_type=allure.attachment_type.TEXT)
            return False

    
    return True