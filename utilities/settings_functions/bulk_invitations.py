import allure
import json
import os
import time
import pyperclip
import pyautogui as pg
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from utilities.other_utils_functions.highlight import highlight_element

   
def bulk_invitations(driver, wait):

    with allure.step("Load locators.json"):
        try:
            with open(os.path.join("data", "locators.json"), "r") as f:
                elements_details = json.load(f)

            settings_icon = elements_details["settings_icon"]
            toast_msg = elements_details["toast_msg"]
            team_members_btn = elements_details["team_members_btn"]
            invitations_tab_btn = elements_details["invitations_tab_btn"]
            upload_users_btn = elements_details["upload_users_btn"]
            upload_yes_btn = elements_details["upload_yes_btn"]
            invitations_req_btn = elements_details["invitations_req_btn"]

            print("✅ locators.json loaded")
        except FileNotFoundError as e:
            msg = f"locators.json file not found: {str(e)}"
            print(msg)
            allure.attach(msg, name="Locators File Missing", attachment_type=allure.attachment_type.TEXT)
            return False
        except json.JSONDecodeError as e:
            msg = f"Invalid JSON in locators.json: {str(e)}"
            print(msg)
            allure.attach(msg, name="Locators JSON Error", attachment_type=allure.attachment_type.TEXT)
            return False

    with allure.step("Click Settings"):
        try:
            settings_btn = wait.until(EC.element_to_be_clickable((By.XPATH, settings_icon)))
            highlight_element(driver, settings_btn)
            settings_btn.click()
        except Exception as e:
            msg = f"Failed to Click Settings Icon: {str(e)}"
            print(msg)
            allure.attach(msg, name="Settings Icon Error", attachment_type=allure.attachment_type.TEXT)
            raise Exception(msg)
        

    with allure.step("Click on Team Members"):
        try:
            team_members = wait.until(EC.presence_of_element_located((By.XPATH, team_members_btn)))
            highlight_element(driver, team_members)
            team_members.click()
            time.sleep(2)
        except Exception as e:
            msg = f"Failed to Click Team Member Tab: {str(e)}"
            print(msg)
            allure.attach(msg, name="Team Member tab Error", attachment_type=allure.attachment_type.TEXT)
            raise Exception(msg)

    with allure.step("Click on Team Members"):
        try:
            invitations_tab = wait.until(EC.presence_of_element_located((By.XPATH, invitations_tab_btn)))
            highlight_element(driver, invitations_tab)
            invitations_tab.click()
            time.sleep(2)
        except Exception as e:
            msg = f"Failed to Click Invitations Tab: {str(e)}"
            print(msg)
            allure.attach(msg, name="Invitations tab Error", attachment_type=allure.attachment_type.TEXT)
            raise Exception(msg)

    with allure.step("Click on Team Members"):
        try:
            upload_users = wait.until(EC.presence_of_element_located((By.XPATH, upload_users_btn)))
            highlight_element(driver, upload_users)
            upload_users.click()
            time.sleep(1)
            file_path = os.path.abspath(os.path.join('data', "bulk_email_template.xlsx"))
            upload_users.send_keys(file_path)
            print(f"Uploading file: {file_path}")

            # Copy file path
            pyperclip.copy(file_path)

            # Paste into File name box
            pg.hotkey("ctrl", "v")
            time.sleep(1)

            # Click Open
            pg.press("enter")

            print("✅ File uploaded successfully")
            time.sleep(2)
        except Exception as e:
            msg = f"Failed to Click Upload Users: {str(e)}"
            print(msg)
            allure.attach(msg, name="Upload Users Error", attachment_type=allure.attachment_type.TEXT)
            raise Exception(msg)
    try:
        yes_btn = wait.until(EC.presence_of_element_located((By.XPATH, upload_yes_btn)))
        highlight_element(driver, yes_btn)
        yes_btn.click()
        time.sleep(1)
    except Exception as e:
        msg = f"Failed to Click Yes Button: {str(e)}"
        print(msg)
        allure.attach(msg, name="Yes Button Error", attachment_type=allure.attachment_type.TEXT)
        raise Exception(msg)

    try:
        toast = wait.until(EC.presence_of_element_located((By.XPATH, toast_msg)))
        highlight_element(driver, toast)
        print(f"📢 Toast message: {toast.text.strip()}")
        time.sleep(1)
    except Exception as e:
        msg = f"Toast message not found: {str(e)}"
        print(msg)
        allure.attach(str(e), name="Toast message Error", attachment_type=allure.attachment_type.TEXT)
        raise Exception(msg)

    with allure.step("Click on Team Members"):
        try:
            invitation_req_tab = wait.until(EC.presence_of_element_located((By.XPATH, invitations_req_btn)))
            highlight_element(driver, invitation_req_tab)
            invitation_req_tab.click()
            time.sleep(2)
        except Exception as e:
            msg = f"Failed to Click Invitation Requests Tab: {str(e)}"
            print(msg)
            allure.attach(msg, name="Invitation Requests  tab Error", attachment_type=allure.attachment_type.TEXT)
            raise Exception(msg)

    return True
        

        