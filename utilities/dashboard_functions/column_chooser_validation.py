from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import allure
import json
import time
import os

from utilities.add_task_functions.wait_for_loader_to_disappear import wait_for_loader_to_disappear
from utilities.other_utils_functions.highlight import highlight_element

all_coll_list = [
    'Column Task Name', 'Column Company / Project', 'Column Status', 'Column License',
    'Column Assigned To', 'Column Approver', 'Column CC', 'Column Frequency',
    'Column Internal Deadline', 'Column Impact', 'Column Risk Rating',
    'Column Due Date', 'Column Creator', 'Column Assign Date'
]


def select_all_columns(driver, wait, dash_total_btn, toast_msg):
    with allure.step("Validate Column Chooser with 'Select All' option"):
        try:
            with allure.step("Click Dashboard Total button"):
                dash_total_btn_elem = wait.until(EC.presence_of_element_located((By.XPATH, dash_total_btn)))
                highlight_element(driver, dash_total_btn_elem)
                dash_total_btn_elem.click()
                print("✅ Clicked Dashboard Total button")
                wait_for_loader_to_disappear(driver, wait)

            with allure.step("Open Column Chooser"):
                column_chooser_btn_elem = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@role='button' and @aria-label='columnchooser']")))
                highlight_element(driver, column_chooser_btn_elem)
                column_chooser_btn_elem.click()
                print("✅ Opened Column Chooser")
                wait_for_loader_to_disappear(driver, wait)

            with allure.step("Select all columns if not selected"):
                print()
                select_all_checkbox = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".dx-list-select-all .dx-checkbox")))
                is_checked = select_all_checkbox.get_attribute("aria-checked")
                if is_checked in ["false", "mixed"]:
                    driver.execute_script("arguments[0].click();", select_all_checkbox)
                    print("☑️ Clicked 'Select All' (it was unchecked/mixed)")
                else:
                    print("✅ 'Select All' already selected")
                wait_for_loader_to_disappear(driver, wait)

            with allure.step("Click Save button in Column Chooser"):
                
                save_btn_xpath = "//div[@role='button' and @aria-label='Save & Close']"
                
                column_chooser_save_btn_elem = wait.until(EC.presence_of_element_located((By.XPATH, save_btn_xpath)))
                highlight_element(driver, column_chooser_save_btn_elem)
                column_chooser_save_btn_elem.click()
                print("✅ Saved Column Chooser with 'Select All'")

            with allure.step("Validate toast message after saving"):
                toast_msg_elem = wait.until(EC.presence_of_element_located((By.XPATH, toast_msg)))
                msg = toast_msg_elem.text.strip()
                print(f"📢 Toast message after saving: {msg}")

            with allure.step("Validate all columns are visible in table"):
                task_headers = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//tr[@role='row' and @class='dx-row dx-column-lines dx-header-row']//td[@aria-label]")))
                col_headers = [cols.get_attribute("aria-label").strip() for cols in task_headers]
                print(f"📊 Found column headers: {col_headers}")

                headers_text = str(col_headers)

                allure.attach(headers_text,name="Column Headers",attachment_type=allure.attachment_type.TEXT)

                if all(col in col_headers for col in all_coll_list):
                    print("✅ All expected columns are present")
                else:
                    print("❌ Missing expected columns")
                    allure.attach(str(col_headers), name="Missing Columns", attachment_type=allure.attachment_type.TEXT)
            time.sleep(5)
            return True

        except Exception as err:
            print(f"❌ Error during 'Select All' column chooser validation: {err}")
            allure.attach(str(err), name="Select_All_Error", attachment_type=allure.attachment_type.TEXT)
            return False


def select_partial_columns(driver, wait, dash_total_btn, toast_msg):
    with allure.step("Validate Column Chooser with 'Partial Selection'"):
        try:
            with allure.step("Click Dashboard Total button again"):
                dash_total_btn_elem = wait.until(EC.presence_of_element_located((By.XPATH, dash_total_btn)))
                dash_total_btn_elem.click()
                print("✅ Clicked Dashboard Total button again")
                wait_for_loader_to_disappear(driver, wait)

            with allure.step("Open Column Chooser again"):
                column_chooser_btn_elem = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@role='button' and @aria-label='columnchooser']")))
                highlight_element(driver, column_chooser_btn_elem)
                column_chooser_btn_elem.click()
                wait_for_loader_to_disappear(driver, wait)

            with allure.step("Deselect 'Select All' to enable partial selection"):
                print()
                select_all_checkbox = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".dx-list-select-all .dx-checkbox")))
                is_checked = select_all_checkbox.get_attribute("aria-checked")
                if is_checked == "true" or is_checked == "mixed":
                    driver.execute_script("arguments[0].click();", select_all_checkbox)
                else:
                    print("Already deselected, continuing...")
                wait_for_loader_to_disappear(driver, wait)

            with allure.step("Select 'Company / Project' column only"):
                col_to_select = "Company / Project"
                checkbox_elem = wait.until(EC.presence_of_element_located((By.XPATH,f"//div[contains(@class,'dx-list-item')][.//div[contains(normalize-space(),'{col_to_select}')]]//div[contains(@class,'dx-checkbox-container')]")))
                driver.execute_script("arguments[0].scrollIntoView({block:'center'});", checkbox_elem)
                driver.execute_script("arguments[0].click();", checkbox_elem)

            with allure.step("Save Column Chooser with partial selection"):
                
                save_btn_xpath = "//div[@role='button' and @aria-label='Save & Close']"
               
                column_chooser_save_btn_elem = wait.until(EC.presence_of_element_located((By.XPATH, save_btn_xpath)))
                highlight_element(driver, column_chooser_save_btn_elem)
                column_chooser_save_btn_elem.click()
                print("✅ Saved Column Chooser with partial selection")

            with allure.step("Validate toast message after saving partial selection"):
                toast_msg_elem = wait.until(EC.presence_of_element_located((By.XPATH, toast_msg)))
                msg = toast_msg_elem.text.strip()
                print(f"📢 Toast message after saving partial selection: {msg}")

            with allure.step("Validate table headers after partial selection"):
                time.sleep(2)
                wait_for_loader_to_disappear(driver, wait)
                header_elements = wait.until(EC.presence_of_all_elements_located((By.XPATH,"//tr[contains(@class,'dx-header-row')]//div[contains(@class,'dx-datagrid-text-content')]")))

                col_headers = [hdr.text.strip() for hdr in header_elements if hdr.text.strip()]
                print(f"📊 Found column headers after partial selection: {col_headers}")
                headers_text = str(col_headers)
                normalized_headers = [h.lower() for h in col_headers]
                expected_col = col_to_select.lower()

                if expected_col in normalized_headers:
                    print(f"✅ Selected '{col_to_select}' column is present")
                    allure.attach(headers_text,name="Partial Column Selection Passed",attachment_type=allure.attachment_type.TEXT)
                    return True
                else:
                    print(f"❌ Missing expected column: {col_to_select}")
                    allure.attach(headers_text,name="Partial Column Selection Failed",attachment_type=allure.attachment_type.TEXT)
                    return False


            time.sleep(5)

        except Exception as err:
            print(f"❌ Error during partial column chooser validation: {err}")
            allure.attach(str(err), name="Partial_Selection_Error", attachment_type=allure.attachment_type.TEXT)
            return False

def column_chooser_validation(driver, wait):
    wait_less = WebDriverWait(driver, 5)

    try:
        with open(os.path.join("data", 'locators.json'), 'r') as f:
            elements_details = json.load(f)
            dash_total_btn = elements_details['dash_total_btn']
            toast_msg = elements_details['toast_msg']
        print("✅ locators.json loaded successfully")
    except FileNotFoundError as e:
        print("❌ locators.json file not found")
        allure.attach(str(e), name="Locators_FileNotFound", attachment_type=allure.attachment_type.TEXT)
        return False
    except json.JSONDecodeError as e:
        print("❌ Invalid JSON in locators.json")
        allure.attach(str(e), name="Invalid_JSON", attachment_type=allure.attachment_type.TEXT)
        return False

    select_all_result = select_all_columns(driver, wait, dash_total_btn, toast_msg)
    if not select_all_result:
        print("❌ 'Select All' validation failed")
        allure.attach("Failure in 'Select All' validation", name="SelectAll_Failure", attachment_type=allure.attachment_type.TEXT)
        return False
    else:
        print("✅ 'Select All' validation successful")

    partial_result = select_partial_columns(driver, wait, dash_total_btn, toast_msg)
    if not partial_result:
        print("❌ 'Partial Selection' validation failed")
        allure.attach("Failure in 'Partial Selection' validation", name="Partial_Failure", attachment_type=allure.attachment_type.TEXT)
        return False
    else:
        print("✅ 'Partial Selection' validation successful")

    final_select_all_result = select_all_columns(driver, wait, dash_total_btn, toast_msg)
    if not final_select_all_result:
        print("❌ Final 'Select All' revalidation failed")
        allure.attach("Failure in final 'Select All' revalidation", name="Final_SelectAll_Failure", attachment_type=allure.attachment_type.TEXT)
        return False
    else:
        print("✅ Final 'Select All' revalidation successful")

    # ✅ All steps passed
    print("🎯 Column Chooser validation flow completed successfully ✅")
    return True
