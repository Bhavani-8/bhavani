import allure
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from utilities.other_utils_functions.highlight import highlight_element
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from utilities.add_task_functions.wait_for_loader_to_disappear import wait_for_loader_to_disappear
import time
import json
import os
import pyautogui as pg
import pytest
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains

def license_subscription(driver, user_validation=False):
    wait = WebDriverWait(driver, 7)
    wait_less = WebDriverWait(driver, 3)
    license_expired_count = 0
    license_active_count = 0

    with allure.step("Load locators.json"):
        try:
            with open(os.path.join("data", "locators.json"), "r") as f:
                elements_details = json.load(f)
            settings_icon = elements_details["settings_icon"]
            toast_msg = elements_details["toast_msg"]
        except Exception as e:
            print("No Locators found")

    # --- Check License Expiry ---
    if user_validation:
        with allure.step(f"Validating License Subscription"):
            try:
                # pg.press('esc')
                expired_licenses = wait_less.until(
                    EC.presence_of_all_elements_located((By.XPATH, "//button//span[text()='Renew Now']"))
                )
                license_expired_count = len(expired_licenses)
                print(f"✅ Expired Licenses Count: {license_expired_count}")
            except TimeoutException:
                print("ℹ️ No expired licenses found")



        # --- Read User Title ---
        with allure.step("👤 Reading User Title from Dashboard"):
            try:
                user_title_elem = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='user-title']")))
                highlight_element(driver, user_title_elem)
                username = user_title_elem.text.strip()
                username = username.lower().replace('hi', '').replace('hello', '').replace(',', '').replace(';', '')
                print(f"✅ Username detected: {username}")
            except Exception as e:
                allure.attach(str(e), name="User Title Error", attachment_type=allure.attachment_type.TEXT)
                pytest.fail("❌ Failed to read user title")

        # --- Open Settings ---
        with allure.step("⚙️ Clicking Settings Button"):
            try:
                settings_btn = wait.until(EC.presence_of_element_located((By.XPATH, settings_icon)))
                highlight_element(driver, settings_btn)
                settings_btn.click()
                print("✅ Settings button clicked")
            except Exception as e:
                allure.attach(str(e), name="Settings Button Error", attachment_type=allure.attachment_type.TEXT)
                pytest.fail("❌ Failed to click Settings button")

        # --- Click Account ---
        with allure.step("👤 Navigating to Account"):
            try:
                account_icon = wait.until(EC.presence_of_element_located((By.XPATH, "//span[contains(text(),'Account')]")))
                highlight_element(driver, account_icon)
                account_icon.click()
                print("✅ Account section opened")
            except Exception as e:
                allure.attach(str(e), name="Account Navigation Error", attachment_type=allure.attachment_type.TEXT)
                pytest.fail("❌ Failed to open Account section")

        # --- Open Your Licenses ---
        with allure.step("📜 Clicking 'Your Licenses'"):
            try:
                licenses_icon = wait.until(EC.visibility_of_element_located((By.XPATH, "//p[text()='Your Licenses']")))
                highlight_element(driver, licenses_icon)
                print("✅ 'Your Licenses' clicked")
            except Exception as e:
                allure.attach(str(e), name="Your Licenses Error", attachment_type=allure.attachment_type.TEXT)
                pytest.fail("❌ Failed to click 'Your Licenses'")

        # --- Edit License ---
        with allure.step("✏️ Clicking Edit License Button"):
            try:
                edit_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@title='Edit License']")))
                highlight_element(driver, edit_btn)
                edit_btn.click()
                print("✅ Edit License button clicked")
            except Exception as e:
                allure.attach(str(e), name="Edit License Error", attachment_type=allure.attachment_type.TEXT)
                pytest.fail("❌ Failed to click Edit License button")

        # --- Show Subscription Status ---
        with allure.step("📊 Opening Subscription Status"):
            try:
                subscription_status = wait.until(EC.visibility_of_element_located((By.XPATH, "//h2[text()='Subscription Status']")))
                highlight_element(driver, subscription_status)
                print("✅ Subscription Status opened")
            except Exception as e:
                allure.attach(str(e), name="Subscription Status Error", attachment_type=allure.attachment_type.TEXT)
                pytest.fail("❌ Failed to open Subscription Status")

        # --- Fetch Inactive Licenses ---
        with allure.step("📜 Validating Active & Inactive Licenses"):
            try:
                inactive_list = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//td[normalize-space()='Inactive']")))
                
                active_list = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//td[normalize-space()='Active']")))

                actual_inactive = len(inactive_list)
                actual_active = len(active_list)

                # ---------------- INACTIVE VALIDATION ----------------
                if license_expired_count == actual_inactive:
                    msg_inactive = f"Inactive Licenses Matched | Actual: {actual_inactive} | Expected: {license_expired_count}"
                    print(f"✅ {msg_inactive}")
                else:
                    msg_inactive = f"Inactive Licenses Mismatch | Actual: {actual_inactive} | Expected: {license_expired_count}"
                    print(f"❌ {msg_inactive}")

                allure.attach(msg_inactive,name="Inactive License Validation",attachment_type=allure.attachment_type.TEXT)

                # ---------------- ACTIVE VALIDATION ----------------
                if license_active_count == actual_active:
                    msg_active = f"Active Licenses Matched | Actual: {actual_active} | Expected: {license_active_count}"
                    print(f"✅ {msg_active}")
                else:
                    msg_active = f"Active Licenses Mismatch | Actual: {actual_active} | Expected: {license_active_count}"
                    print(f"❌ {msg_active}")

                allure.attach(msg_active,name="Active License Validation",attachment_type=allure.attachment_type.TEX)

                # ---------------- OPTIONAL CLICK ----------------
                if inactive_list:
                    highlight_element(driver, inactive_list[0])
                    inactive_list[0].click()
                    print("➡️ Clicked on first Inactive License")

            except Exception as e:
                msg_error = f"No license data found or error occurred: {str(e)}"
                print(f"ℹ️ {msg_error}")

                allure.attach(msg_error,name="License Validation Error",attachment_type=allure.attachment_type.TEXT)

        # --- Close License Modal ---
        with allure.step("❎ Closing License Modal"):
            try:
                close_btn = wait.until(EC.presence_of_element_located((By.XPATH, "//button[@data-slot='dialog-close']")))
                highlight_element(driver, close_btn)
                close_btn.click()
                print("✅ License modal closed")
            except Exception as e:
                allure.attach(str(e), name="Close Modal Error", attachment_type=allure.attachment_type.TEXT)
                pytest.fail("❌ Failed to close license modal")

        # --- Open Team Members ---
        with allure.step("👥 Navigating to Team Members"):
            try:
                team_members = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='menu-items']//span[text()='Team Members']")))
                highlight_element(driver, team_members)
                team_members.click()
                print("✅ Team Members clicked")
            except Exception as e:
                allure.attach(str(e), name="Team Members Error", attachment_type=allure.attachment_type.TEXT)
                pytest.fail("❌ Failed to click Team Members")

        # --- Search for Admin ---
        with allure.step("🔍 Searching 'Admin' in Team Members"):
            try:
                search_input = wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class,'dx-texteditor-input-container')]//input[@aria-label='Search in the data grid']")))
                highlight_element(driver, search_input)
                search_input.send_keys(username)
                print("✅ Entered 'Admin' in search")
                time.sleep(2)
            except Exception as e:
                allure.attach(str(e), name="Search Input Error", attachment_type=allure.attachment_type.TEXT)
                pytest.fail("❌ Failed to search 'Admin'")

        # --- Read Compliance Officer Role ---
        with allure.step("🕵️ Validating Compliance Officer Role"):
            try:
                role_elem = wait.until(EC.presence_of_element_located((By.XPATH, f"//tr[.//div[normalize-space()='{username}']]//td[@aria-colindex='5']")))
                highlight_element(driver, role_elem)
                role_text = role_elem.text.strip()
                print(f"✅ Role detected: {role_text}")

                if "Compliance Officer" in role_text:
                    print("✅ User validated as Compliance Officer")
                else:
                    print("⚠️ Role validation mismatch")
            except Exception as e:
                allure.attach(str(e), name="Role Validation Error", attachment_type=allure.attachment_type.TEXT)
                pytest.fail("❌ Failed to validate role")

        # --- Return to Dashboard ---
        with allure.step("📊 Returning to Dashboard"):
            try:
                with open('data/locators.json') as f:
                    locators = json.load(f)
                dashboard_icon = locators['dashboard_icon']
                dashboard_icon_elem = wait.until(EC.presence_of_element_located((By.XPATH, dashboard_icon)))
                highlight_element(driver, dashboard_icon_elem)
                dashboard_icon_elem.click()
                print("✅ Dashboard icon clicked")
                wait_for_loader_to_disappear(driver, wait)
                return True
            except Exception as e:
                allure.attach(str(e), name="Dashboard Return Error", attachment_type=allure.attachment_type.TEXT)
                pytest.fail("❌ Failed to return to Dashboard")
                return False

    