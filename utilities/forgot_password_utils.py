# forgot_password_utils.py
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import pandas as pd
import pytest
import allure
import json
import os
import time

from utilities.other_utils_functions.highlight import highlight_element
from load_test_config_excel_data import load_test_config_excel_data

def forgot_password_check(driver, email, test_type):
    if pd.isna(email):
        email = ""
    wait = WebDriverWait(driver, 30)

    # --- Load locators ---
    # with allure.step("Loading locators from JSON"):
    try:
        with open(os.path.join("data", 'locators.json'), 'r') as f:
            elements_details = json.load(f)
            fp_mail_input_path = elements_details['forgot_pass_mail_input']
            forgot_pass_btn = elements_details['forgot_pass_btn']
            input_err_msg = elements_details['input_err_msg']
            err_msg_toast_path = elements_details['err_msg_toast']
        print("✅ Locators loaded successfully")
    except FileNotFoundError:
        print("❌ locators.json file not found")
        pytest.fail("locators.json file not found")
    except json.JSONDecodeError:
        print("❌ Invalid JSON in locators.json")
        pytest.fail("Invalid JSON in locators.json")

    # --- Enter email ---
    with allure.step(f"Entering Company Email: '{email}'"):
        try:
            fp_mail_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, fp_mail_input_path)))
            highlight_element(driver, fp_mail_input)
            fp_mail_input.clear()
            fp_mail_input.send_keys(email)
            print(f"✅ Entered email: {email if email else '<blank>'}")
        except Exception as e:
            print(f"❌ Failed to enter email: {e}")
            allure.attach(str(e), name="Email Input Error", attachment_type=allure.attachment_type.TEXT)
            return False

    # --- Click send link ---
    with allure.step("Clicking on Send Link Button"):
        try:
            send_link_btn = wait.until(EC.presence_of_element_located((By.XPATH, forgot_pass_btn)))
            highlight_element(driver, send_link_btn)
            print("✅ Send Link button located")
            time.sleep(3)
        except Exception as e:
            print(f"❌ Send Link button not found: {e}")
            allure.attach(str(e), name="Send Link Button Error", attachment_type=allure.attachment_type.TEXT)
            return False

        # Blank input
        if email.strip() == "":
            if not send_link_btn.is_enabled():
                print("✅ Send Link Button is disabled for blank input (expected)")
                return False
            else:
                print("❌ Send Link Button should be disabled for blank input")
                return False

        # Whitespace in email
        if " " in email:
            if send_link_btn.is_enabled():
                with allure.step("Checking validation error for whitespace email"):
                    try:
                        input_err_msg_label = wait.until(EC.presence_of_element_located((By.CLASS_NAME, input_err_msg)))
                        highlight_element(driver, input_err_msg_label)
                        err_label = input_err_msg_label.text.strip().lower()
                        if any(err in err_label for err in ["email already exists", "Email is invalid", "please enter valid email"]):
                            allure.attach(err_label, name="Error Message After Input", attachment_type=allure.attachment_type.TEXT)
                            print(f"✅ Validation error shown for whitespace email: {err_label}")
                            return False
                        else:
                            print("❌ No proper validation error shown for whitespace email")
                            return False
                    except Exception:
                        print("❌ No validation error element found for whitespace email")
                        return False
            else:
                print("✅ Send Link button disabled for whitespace email (expected)")
                return False

        try:
            send_link_btn.click()
            # send_link_btn.click()
            print("✅ Clicked on Send Link button")
            time.sleep(3)
        except Exception as e:
            print(f"❌ Failed to click Send Link button: {e}")
            allure.attach(str(e), name="Click Error", attachment_type=allure.attachment_type.TEXT)
            return False
    

    # --- Validate toast message ---
    with allure.step("Validating Toast Message"):
        try:
            toast_msg = wait.until(EC.presence_of_element_located((By.CLASS_NAME, err_msg_toast_path)))
            highlight_element(driver, toast_msg)
            msg_text = toast_msg.text.strip()
            allure.attach(msg_text, name="Toast Message", attachment_type=allure.attachment_type.TEXT)
            print(f"✅ Toast message found: {msg_text}")

            if test_type:
                if "successfully" in msg_text.lower():
                    print("✅ Success toast validated")
                    return True
                else:
                    print("❌ Expected success but got failure toast")
                    return False
            else:
                if any(x in msg_text.lower() for x in ["invalid user", "does not exist"]):
                    print("✅ Failure toast validated")
                    return False
                else:
                    print("❌ Expected failure but got success toast")
                    return False

        except Exception as e:
            print(f"❌ Toast message not found within timeout: {e}")
            allure.attach(str(e), name="Toast Missing", attachment_type=allure.attachment_type.TEXT)
            return False

# def load_test_config_excel_data():
#     df = pd.read_excel(os.path.join('data', 'test_case_selector.xlsx'), sheet_name='test_details')
#     print(f'Excel data loaded:\n{df}')

#     browser = str(df.iloc[0]['browser']).strip()
#     website = str(df.iloc[0]['website']).strip()

#     # detect if Excel is marker-driven (like smoke/regression only)
#     if "module_to_test" in df.columns and df["module_to_test"].str.strip().iloc[0].lower() in ["smoke", "regression"]:
#         return {
#             "browser": browser,
#             "website": website,
#             "module_to_test": df["module_to_test"].str.strip().iloc[0].lower()
#         }
    
#     # Build module_to_test dict
#     module_to_test = {}
#     for _, row in df.iterrows():
#         module = str(row['module_to_test']).strip()
#         test_types = [t.strip() for t in str(row['test_type']).split(",") if t.strip()]
#         if not module:
#             continue
#         module_to_test.setdefault(module, [])
#         for t in test_types:
#             if t not in module_to_test[module]:
#                 module_to_test[module].append(t)
    
#     return {
#         "browser": browser,
#         "website": website,
#         "module_to_test": module_to_test
#     }

def get_test_case_list(module=None):
    try:
        # with open(os.path.join("data", "test_data.json")) as f:
        #     config = json.load(f)
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
                row['email'],
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