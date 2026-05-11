# forgot_password_utils.py
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import pandas as pd
import numpy as np
import pytest
import allure
import json
import os

from utilities.other_utils_functions.highlight import highlight_element
from load_test_config_excel_data import load_test_config_excel_data

def signup_check(driver, email, check_selection, test_type):
    if pd.isna(email):
        email = ""
    wait = WebDriverWait(driver, 30)

    # --- Load locators ---
    # with allure.step("Loading locators from JSON"):
    try:
        with open(os.path.join("data", 'locators.json'), 'r') as f:
            elements_details = json.load(f)
            mail_input_path = elements_details['mail_input']
            terms_checkbox = elements_details['signup_checkbox']
            signup_btn_path = elements_details['signup_btn']
            input_err_msg = elements_details['input_err_msg']
            err_msg_toast_path = elements_details['err_msg_toast']
            acknowledgement_text_path = elements_details['signup_acknowledgement_txt']
            current_url = driver.current_url
            if 'preprod' in current_url:
                signup_acknowledgement_url = elements_details['preprod_urls']['signup_acknowledgement']
            else:
                signup_acknowledgement_url = elements_details['onprem_urls']['signup_acknowledgement']
    except FileNotFoundError:
        pytest.fail("❌ locators.json file not found")
    except json.JSONDecodeError:
        pytest.fail("❌ Invalid JSON in locators.json")

    # --- Enter email ---
    with allure.step(f"Entering Company Email: '{email}'"):
        mail_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, mail_input_path)))
        highlight_element(driver, mail_input)
        mail_input.clear()
        mail_input.send_keys(email)

    # --- Check inline validation ---
    with allure.step("Checking input validation errors"):
        try:
            input_err_msg_label = wait.until(EC.presence_of_element_located((By.CLASS_NAME, input_err_msg)))
            highlight_element(driver, input_err_msg_label)
            err_label = input_err_msg_label.text.strip().lower()
            if err_label and any(err in err_label for err in ["email already exists", "please enter valid email"]):
                allure.attach(err_label, name="Input Validation Error", attachment_type=allure.attachment_type.TEXT)
                return False
        except:
            pass  # No validation error shown

    # --- Handle Terms Checkbox ---
    with allure.step("Handling Terms & Conditions Checkbox"):
        checkbox = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, terms_checkbox)))
        highlight_element(driver, checkbox)
        is_checked = checkbox.is_selected()

        if check_selection == 1 and not is_checked:
            checkbox.click()
        elif check_selection == 0 and is_checked:
            checkbox.click()

    # --- Click Verify Email ---
    with allure.step("Clicking Verify Email Button"):
        try:
            verify_mail_btn = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, signup_btn_path)))
            highlight_element(driver, verify_mail_btn)

            # blank input
            if email.strip() == "":
                assert not verify_mail_btn.is_enabled(), "❌ Verify Email Button should be disabled for blank input"
                return False

            # whitespace in email
            if " " in email:
                return False

            # checkbox not selected
            if check_selection == 0:
                return False

            verify_mail_btn.click()
        except Exception as e:
            allure.attach(str(e), name="Verify Email Button Not Found", attachment_type=allure.attachment_type.TEXT)
            return False

    # --- Post click validation ---
    with allure.step("Validating Post-Click Behaviour"):
        try:
            wait.until(EC.url_to_be(signup_acknowledgement_url))
            ack_text = wait.until(EC.presence_of_element_located((By.CLASS_NAME, acknowledgement_text_path)))
            highlight_element(driver, ack_text)
            if email in ack_text.text:
                allure.attach(ack_text.text, name="Acknowledgement Page Text", attachment_type=allure.attachment_type.TEXT)
            return test_type
        except:
            try:
                toast = wait.until(EC.presence_of_element_located((By.CLASS_NAME, err_msg_toast_path)))
                highlight_element(driver, toast)
                msg = toast.text.strip()
                allure.attach(msg, name="Toast Message", attachment_type=allure.attachment_type.TEXT)
                return test_type if ("successfully" in msg.lower()) == test_type else False
            except Exception as e:
                allure.attach(str(e), name="Toast/Redirect Error", attachment_type=allure.attachment_type.TEXT)
                return False

# def load_test_config_excel_data():
#     df = pd.read_excel(os.path.join('data', 'test_case_selector.xlsx'), sheet_name='test_details')
#     print(f'Excel data loaded:\n{df}')

#     browser = str(df.iloc[0]['browser']).strip()
#     website = str(df.iloc[0]['website']).strip()

#     # detect if Excel is marker-driven (like smoke/regression only)
#     if "modules_to_test" in df.columns and df["modules_to_test"].str.strip().iloc[0].lower() in ["smoke", "regression"]:
#         return {
#             "browser": browser,
#             "website": website,
#             "modules_to_test": df["modules_to_test"].str.strip().iloc[0].lower()
#         }
    
#     # Build modules_to_test dict
#     modules_to_test = {}
#     for _, row in df.iterrows():
#         module = str(row['modules_to_test']).strip()
#         test_types = [t.strip() for t in str(row['test_type']).split(",") if t.strip()]
#         if not module:
#             continue
#         modules_to_test.setdefault(module, [])
#         for t in test_types:
#             if t not in modules_to_test[module]:
#                 modules_to_test[module].append(t)
    
#     return {
#         "browser": browser,
#         "website": website,
#         "modules_to_test": modules_to_test
#     }


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
                row['email'],
                row['check_selection'],
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
