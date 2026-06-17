# login_utils.py
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import pandas as pd
import pytest
import logging
import allure
import time
import json
import os

from utilities.other_utils_functions.highlight import highlight_element
from utilities.other_utils_functions.license_utils import validate_license_subscription
from load_test_config_excel_data import load_test_config_excel_data
from utilities.add_task_functions.wait_for_loader_to_disappear import wait_for_loader_to_disappear

def login_check(driver, waittime, trial, username, password, user_validation=False, dash_icon_validation=False):
    wait_less = WebDriverWait(driver, 10)
    wait = WebDriverWait(driver, 30)

    if pd.isna(password):
        password = ""

    # 🔍 Step 0: Load locators
    # with allure.step("📂 Loading locators.json file"):
    try:
        with open(os.path.join("data", 'locators.json'), 'r') as f:
            elements_details = json.load(f)
        mail_input_path = elements_details['mail_input']
        pass_input_path = elements_details['pass_input']
        show_pass_btn_path = elements_details['show_pass_btn']
        login_btn_path = elements_details['login_btn']
        err_msg_toast_path = elements_details['err_msg_toast']
        input_err_msg = elements_details['input_err_msg']
        toast_msg = elements_details['toast_msg']
        print("✅ Locators loaded successfully")
    except FileNotFoundError as e:
        allure.attach(str(e), name="Locators File Missing", attachment_type=allure.attachment_type.TEXT)
        pytest.fail("❌ locators.json file not found")
        return False
    except json.JSONDecodeError as e:
        allure.attach(str(e), name="Locators JSON Error", attachment_type=allure.attachment_type.TEXT)
        pytest.fail("❌ Invalid JSON in locators.json")
        return False

    time_taken = 0

    # 🔑 Enter Username
    with allure.step(f"Entering Company Email: '{username}'"):
        try:
            mail_input = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, mail_input_path)))
            highlight_element(driver, mail_input)
            mail_input.send_keys(username)
            print("✅ Email entered")
        except Exception as e:
            allure.attach(str(e), name="Email Input Error", attachment_type=allure.attachment_type.TEXT)
            pytest.fail("❌ Failed to enter email")
            return False

    # 🔑 Enter Password
    with allure.step(f"Entering Password: '{password}'"):
        try:
            password_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, pass_input_path)))
            highlight_element(driver, password_input)
            password_input.send_keys(password)
            print("✅ Password entered")
        except Exception as e:
            allure.attach(str(e), name="Password Input Error", attachment_type=allure.attachment_type.TEXT)
            pytest.fail("❌ Failed to enter password")
            return False

    # 👁️ Make Password Visible
    with allure.step("Making Password Visible"):
        try:
            show_pass_button = wait.until(EC.element_to_be_clickable((By.XPATH, show_pass_btn_path)))
            highlight_element(driver, show_pass_button)
            show_pass_button.click()
            if password_input.get_attribute('type') == 'text':
                print("✅ Password is visible")
        except Exception as e:
            allure.attach(str(e), name="Show Password Error", attachment_type=allure.attachment_type.TEXT)
            pytest.fail("❌ Failed to make password visible")
            return False

    # ➡️ Click Login Button
    with allure.step("Clicking Login Button"):
        try:
            login_button = wait.until(EC.presence_of_element_located((By.XPATH, login_btn_path)))
            highlight_element(driver, login_button)

            # Blank Input Check
            if username.strip() == "" or password.strip() == "":
                is_enabled = login_button.is_enabled()
                assert not is_enabled, "❌ Login button should be disabled for blank inputs"
                print("✅ Login button disabled for blank inputs")
                return False

            # Whitespace in Username
            if " " in username:
                is_enabled = login_button.is_enabled()
                assert not is_enabled, "❌ Login button should be disabled for extra spaces in username input"
                try:
                    input_err_msg_label = wait.until(EC.presence_of_element_located((By.CLASS_NAME, input_err_msg)))
                    highlight_element(driver, input_err_msg_label)
                    err_text = input_err_msg_label.text.strip()
                    if err_text:
                        print(f"❌ Error Message for Input: {err_text}")
                except Exception as e:
                    allure.attach(str(e), name="Whitespace Error Check", attachment_type=allure.attachment_type.TEXT)
                    pytest.fail("❌ No error label found for whitespace in username")
                return False
            
            # 🚫 Newly Invited User (Not Signed Up)
            if "invited" in username.lower():  

                try:
                    toast_msg_elem = wait.until(EC.presence_of_element_located((By.XPATH, toast_msg)))
                    highlight_element(driver, toast_msg_elem)

                    toast_text = toast_msg_elem.text.strip()
                    print(f"Toast Message: {toast_text}")

                    assert "User disabled or missing" in toast_text, \
                        f"❌ Expected 'User disabled or missing' but got '{toast_text}'"

                    print("✅ Proper error shown for invited user")
                    return False

                except Exception as e:
                    allure.attach(str(e), name="Invited User Error", attachment_type=allure.attachment_type.TEXT)
                    pytest.fail("❌ Toast message not found for invited user")

            login_button.click()
            time.sleep(0.5)
            wait_for_loader_to_disappear(driver, wait)
            print("✅ Login button clicked")

        except Exception as e:
            allure.attach(str(e), name="Login Button Error", attachment_type=allure.attachment_type.TEXT)
            pytest.fail("❌ Failed to click Login button")

    # 🔍 Toast Check
    try:
        for i in range(3):
            time.sleep(0.3)
            toast_msg_elems = wait_less.until(EC.presence_of_all_elements_located((By.XPATH, toast_msg)))
            # highlight_element(driver, toast_msg_elem)
            for toast_msg_elem in toast_msg_elems:
                msg = toast_msg_elem.text.strip()
                if msg and 'invalid' in msg.lower():
                    print(f"❌ Invalid login: {msg}")
                    return False
                elif msg:
                    # print(f"ℹ️ Toast Message: {msg}")
                    continue


    except Exception as err:
        pass
    for i in range(5):
        if not "dashboard-view" in driver.current_url:
        
            time.sleep(1)
        else:
            break
    
    if "dashboard-view" in driver.current_url:

        print(f"✅ Login successful")
        # return True

        # Validate License
        # with allure.step(f"Validating License Subscription for '{username}'"):
        validate_license_subscription(driver)
        if not dash_icon_validation:
            return True

        # Check Dashboard Icons
        if dash_icon_validation:
            with allure.step("Checking Dashboard Icons Visibility"):
                try:
                    with open(os.path.join("data", 'locators.json'), 'r') as f:
                        elements_details = json.load(f)

                    icon_locators = {k: elements_details[k] for k in [
                        "dashboard_icon", "special_task_icon", "calendar_icon", "notification_icon",
                        "compliance_hist_icon", "project_icon", "updates_icon", "audit_icon", "trash_icon",
                        "other_compliance_icon", "settings_icon", "suggestion_icon", "logout_icon"
                    ]}

                    invisible_icons = []
                    for icon_name, xpath in icon_locators.items():
                        try:
                            icon_element = WebDriverWait(driver, 5).until(
                                EC.visibility_of_element_located((By.XPATH, xpath))
                            )
                            highlight_element(driver, icon_element, duration=0.1)
                            print(f"✅ {icon_name} visible")
                        except Exception as e:
                            invisible_icons.append(icon_name)
                            allure.attach(str(e), name=f"{icon_name} Missing", attachment_type=allure.attachment_type.TEXT)

                    if invisible_icons:
                        # pytest.fail(f"❌ Missing icons: {', '.join(invisible_icons)}")
                        logging.warning(f"⚠️ Missing icons: {', '.join(invisible_icons)}")
                        return False
                    else:
                        print("✅ All dashboard icons visible")
                        return True

                except Exception as e:
                    allure.attach(str(e), name="Dashboard Icons Check Error", attachment_type=allure.attachment_type.TEXT)
                    pytest.fail("❌ Failed to validate dashboard icons")
                    return False

    # Error Toast during trials
    else:
        return False


def get_test_case_list(module=None):
    try:
        config = load_test_config_excel_data()
        print(f'Configurations: {config}')
        if not config:
            pytest.fail("test_case_selector.xlsx file not found")

        test_details = config.get("module_to_test", {})
        print(f'Module fetched: {test_details}')
        selected_test_types = test_details.get(module, [])
        print(f'Selected test types: {selected_test_types}')

        # 🔹 Load test cases sheet (NO execution columns here)
        test_case_details = pd.read_excel(
            os.path.join("data", "test_case_selector.xlsx"),
            sheet_name=f"{module}_test_cases"
        ).fillna("")

        test_case_list = []

        for _, row in test_case_details.iterrows():
            row_test_type = str(row.get("test_type", "")).strip().lower()

            if row_test_type not in selected_test_types:
                continue  # skip

            marks = []

            # Add the positive/negative mark based on test_type
            if row_test_type in ["positive", "negative"]:
                marks.append(getattr(pytest.mark, row_test_type))


            test_case_list.append(pytest.param(
                row['test_case_id'],
                row['test_case_description'],
                row['username'],
                row['password'],
                row['test_type'],
                marks=marks
            ))
        if not test_case_list:
            pytest.skip("No test cases matched the selected criteria", allow_module_level=True)

        return test_case_list

    except FileNotFoundError:
        pytest.fail("test_case_selector.xlsx file not found")
    except Exception as e:
        pytest.fail(f"Error reading test cases: {str(e)}")

