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


def step_fail(driver, step_name, error):
    allure.attach(str(error), name=f"{step_name} Error", attachment_type=allure.attachment_type.TEXT)
    allure.attach(driver.get_screenshot_as_png(), name=f"{step_name} Screenshot", attachment_type=allure.attachment_type.PNG)
    pytest.fail(f"❌ {step_name} failed")
def validate_license_subscription(driver, user_validation=False):
    wait = WebDriverWait(driver, 3)
    # wait_less = WebDriverWait(driver, 3)
    license_expired_count = 0

    
    # --- Check License Expiry ---
    if user_validation:
        with allure.step(f"Validating License Subscription"):
            try:
                # pg.press('esc')
                expired_licenses = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//button//span[text()='Renew Now']")))
                license_expired_count = len(expired_licenses)
                print(f"✅ Expired Licenses Count: {license_expired_count}")
            # except TimeoutException:
            #     print("ℹ️ No expired licenses found")
            except Exception as e:
                step_fail(driver, "Validating License Subscription", e)

            try:
                close_btn = wait.until(EC.presence_of_element_located((By.XPATH, '//button[@aria-label="Close"]')))
                close_btn.click()
                time.sleep(3)
                pg.press('esc')
                print("✅ License modal closed")
                return True
            except Exception as e:
                # step_fail(driver, "Closing License Modal", e)
                print("❌ Failed to close license modal")
                return False

        # --- Read User Title ---
        with allure.step("👤 Reading User Title from Dashboard"):
            try:
                user_title_elem = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='user-title']")))
                highlight_element(driver, user_title_elem)
                username = user_title_elem.text.strip()
                username = username.lower().replace('hi', '').replace('hello', '').replace(',', '').replace(';', '')
                print(f"✅ Username detected: {username}")
            except Exception as e:
                step_fail(driver, "Reading User Title", e)

        # --- Open Settings ---
        with allure.step("⚙️ Clicking Settings Button"):
            try:
                settings_btn = wait.until(EC.presence_of_element_located((By.XPATH, "//img[@title='Settings']")))
                highlight_element(driver, settings_btn)
                settings_btn.click()
                print("✅ Settings button clicked")
            except Exception as e:
                step_fail(driver, "Clicking Settings Button", e)
                # pytest.fail("❌ Failed to click Settings button")

        # --- Click Account ---
        with allure.step("👤 Navigating to Account"):
            try:
                account_icon = wait.until(EC.presence_of_element_located((By.XPATH, "//span[contains(text(),'Account')]")))
                highlight_element(driver, account_icon)
                account_icon.click()
                print("✅ Account section opened")
            except Exception as e:
                # allure.attach(str(e), name="Account Navigation Error", attachment_type=allure.attachment_type.TEXT)
                # pytest.fail("❌ Failed to open Account section")
                step_fail(driver, "Navigating to Account", e)

        # --- Open Your Licenses ---
        with allure.step("📜 Clicking 'Your Licenses'"):
            try:
                licenses_icon = wait.until(EC.element_to_be_clickable((By.XPATH, "//p[text()='Your Licenses']")))
                highlight_element(driver, licenses_icon)
                licenses_icon.click()
                print("✅ 'Your Licenses' clicked")
            except Exception as e:
                # allure.attach(str(e), name="Your Licenses Error", attachment_type=allure.attachment_type.TEXT)
                # pytest.fail("❌ Failed to click 'Your Licenses'")
                step_fail(driver, "Clicking 'Your Licenses'", e)

        # --- Edit License ---
        with allure.step("✏️ Clicking Edit License Button"):
            try:
                edit_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@title='Edit License']")))
                highlight_element(driver, edit_btn)
                edit_btn.click()
                print("✅ Edit License button clicked")
            except Exception as e:
                # allure.attach(str(e), name="Edit License Error", attachment_type=allure.attachment_type.TEXT)
                # pytest.fail("❌ Failed to click Edit License button")
                step_fail(driver, "Clicking Edit License", e)

        # --- Show Subscription Status ---
        with allure.step("📊 Opening Subscription Status"):
            try:
                subscription_status = wait.until(EC.element_to_be_clickable((By.XPATH, "//h2[text()='Subscription Status']")))
                highlight_element(driver, subscription_status)
                subscription_status.click()
                print("✅ Subscription Status opened")
            except Exception as e:
                # allure.attach(str(e), name="Subscription Status Error", attachment_type=allure.attachment_type.TEXT)
                # pytest.fail("❌ Failed to open Subscription Status")
                step_fail(driver, "Opening Subscription Status", e)

        # --- Fetch Inactive Licenses ---
        with allure.step("📜 Validating Inactive Licenses"):
            try:
                inactive_list = wait.until(
                    EC.presence_of_all_elements_located((By.XPATH, "//td[normalize-space()='Inactive']"))
                )
                if license_expired_count == len(inactive_list):
                    print(f"✅ License status validated, expired count: {len(inactive_list)}")
                else:
                    print(f"⚠️ License mismatch (Expected: {license_expired_count}, Found: {len(inactive_list)})")

                if inactive_list:
                    highlight_element(driver, inactive_list[0])
                    inactive_list[0].click()
                    print("➡️ Clicked on first Inactive License")
            except Exception:
                print("ℹ️ No inactive licenses found")

        # --- Close License Modal ---
        with allure.step("❎ Closing License Modal"):
            try:
                close_btn = wait.until(EC.presence_of_element_located((By.XPATH, "//button[@data-slot='dialog-close']")))
                highlight_element(driver, close_btn)
                close_btn.click()
                print("✅ License modal closed")
            except Exception as e:
                # allure.attach(str(e), name="Close Modal Error", attachment_type=allure.attachment_type.TEXT)
                # pytest.fail("❌ Failed to close license modal")
                step_fail(driver, "Closing License Modal", e)

        # --- Open Team Members ---
        with allure.step("👥 Navigating to Team Members"):
            try:
                team_members = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='menu-items']//span[text()='Team Members']")))
                highlight_element(driver, team_members)
                team_members.click()
                print("✅ Team Members clicked")
            except Exception as e:
                # allure.attach(str(e), name="Team Members Error", attachment_type=allure.attachment_type.TEXT)
                # pytest.fail("❌ Failed to click Team Members")
                step_fail(driver, "Navigating to Team Members", e)
        # --- Search for Admin ---
        with allure.step("🔍 Searching 'Admin' in Team Members"):
            try:
                search_input = wait.until(
                    EC.presence_of_element_located((By.XPATH, "//div[contains(@class,'dx-texteditor-input-container')]//input[@aria-label='Search in the data grid']"))
                )
                highlight_element(driver, search_input)
                search_input.send_keys("Admin")
                print("✅ Entered 'Admin' in search")
                time.sleep(2)
            except Exception as e:
                # allure.attach(str(e), name="Search Input Error", attachment_type=allure.attachment_type.TEXT)
                # pytest.fail("❌ Failed to search 'Admin'")
                step_fail(driver, "Searching 'Admin' in Team Members", e)

        # --- Read Compliance Officer Role ---
        with allure.step("🕵️ Validating Compliance Officer Role"):
            try:
                role_elem = wait.until(EC.presence_of_element_located((By.XPATH, "//tr[.//div[normalize-space()='{username}']]//td[@aria-colindex='5']")))
                highlight_element(driver, role_elem)
                role_text = role_elem.text.strip()
                print(f"✅ Role detected: {role_text}")

                if "Compliance Officer" in role_text:
                    print("✅ User validated as Compliance Officer")
                else:
                    print("⚠️ Role validation mismatch")
            except Exception as e:
                # allure.attach(str(e), name="Role Validation Error", attachment_type=allure.attachment_type.TEXT)
                # pytest.fail("❌ Failed to validate role")
                step_fail(driver, "Validating Compliance Officer Role", e)

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

    else:
        try:
            close_btn = wait.until(EC.presence_of_element_located((By.XPATH, '//button[@aria-label="Close"]')))
            close_btn.click()
            time.sleep(3)
            pg.press('esc')
            # print("✅ License modal closed")
            return True
        except Exception as e:
            # step_fail(driver, "Closing License Modal", e)
            print("❌ Failed to close license modal")
            return False