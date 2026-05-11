from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
import pyautogui as pg
import allure
import pytest
import json
import time
import os

from utilities.add_task_functions.wait_for_loader_to_disappear import wait_for_loader_to_disappear
from utilities.other_utils_functions.highlight import highlight_element
def step_fail(driver, step_name, error):
    allure.attach(str(error), name=f"{step_name} Error", attachment_type=allure.attachment_type.TEXT)
    allure.attach(driver.get_screenshot_as_png(), name=f"{step_name} Screenshot", attachment_type=allure.attachment_type.PNG)
    pytest.fail(f"❌ {step_name} failed")
   
all_coll_list = [
    'Column Project Name', 'Column Owner', 'Column Department', 'Column Team',
    'Column Total Task', 'Column Completed', 'Column Pending', 'Column Complete %',
    'Column Deadline', 'Column Overdue'
]

def select_all_columns(driver, wait, project_icon, toast_msg):
    
    with allure.step("Click project icon"):
        try:
            project_btn = wait.until(EC.presence_of_element_located((By.XPATH, project_icon)))
            highlight_element(driver, project_btn)
            project_btn.click()
            time.sleep(3)
        except Exception as e:
            step_fail(driver, "Click project icon", e)
    
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
        
        save_btn_xpath = "//div[@role='button' and @aria-label='Save as Default View']"
        
        column_chooser_save_btn_elem = wait.until(EC.presence_of_element_located((By.XPATH, save_btn_xpath)))
        highlight_element(driver, column_chooser_save_btn_elem)
        column_chooser_save_btn_elem.click()
        print("✅ Saved Column Chooser with 'Select All'")

    with allure.step("Validate toast message after saving"):
        toast_msg_elem = wait.until(EC.presence_of_element_located((By.XPATH, toast_msg)))
        msg = toast_msg_elem.text.strip()
        time.sleep(6)
        print(f"📢 Toast message after saving: {msg}")

    # with allure.step("Validate all columns are visible in table"):
    #     try:
    #         task_headers = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//tr[@role='row' and @class='dx-row dx-header-row']//td[@aria-label]")))
    #         col_headers = [cols.get_attribute("aria-label").strip() for cols in task_headers]
    #         print(f"📊 Found column headers: {col_headers}")
    #         if all(col in col_headers for col in all_coll_list):
    #             print("✅ All expected columns are present")
    #         else:
    #             print("❌ Missing expected columns")
    #             allure.attach(str(col_headers), name="Missing Columns", attachment_type=allure.attachment_type.TEXT)
    #             return False
    #     except Exception as e:
    #         step_fail(driver, "Validate all columns are visible", e)
    #         # continue

    with allure.step("Validate expected columns using header row XPath"):
        try:
            # ✅ Get headers using YOUR XPath
            task_headers = wait.until(EC.presence_of_all_elements_located((
                By.XPATH,
                "//tr[@role='row' and contains(@class,'dx-header-row')]//td[@aria-label]"
            )))

            # ✅ Extract column names
            col_headers = [
                header.get_attribute("aria-label").strip()
                for header in task_headers
            ]

            print(f"📊 Available columns: {col_headers}")

            # ✅ Check ONLY expected columns
            missing_cols = [col for col in all_coll_list if col not in col_headers]

            if not missing_cols:
                print("✅ All expected columns are present")

                allure.attach(
                    f"Expected columns found:\n{all_coll_list}",
                    name="Column Validation",
                    attachment_type=allure.attachment_type.TEXT
                )

            else:
                print(f"❌ Missing expected columns: {missing_cols}")

                allure.attach(
                    f"Missing: {missing_cols}\nAvailable: {col_headers}",
                    name="Column Validation Failed",
                    attachment_type=allure.attachment_type.TEXT
                )

                pytest.fail(f"Missing columns: {missing_cols}")

        except Exception as e:
            step_fail(driver, "Validate expected columns", e)
    time.sleep(5)
    return True


def select_partial_columns(driver, wait, project_icon, toast_msg):
    with allure.step("Validate Column Chooser with 'Partial Selection'"):
        try:
            
            with allure.step("Click project icon"):
                try:
                    project_btn = wait.until(EC.presence_of_element_located((By.XPATH, project_icon)))
                    highlight_element(driver, project_btn)
                    project_btn.click()
                    time.sleep(2)
                except Exception as e:
                    step_fail(driver, "Click project icon", e)
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
                col_to_select = "Owner"
                checkbox_elem = wait.until(EC.presence_of_element_located((By.XPATH,f"//div[contains(@class,'dx-list-item')][.//div[contains(normalize-space(),'{col_to_select}')]]//div[contains(@class,'dx-checkbox-container')]")))
                driver.execute_script("arguments[0].scrollIntoView({block:'center'});", checkbox_elem)
                driver.execute_script("arguments[0].click();", checkbox_elem)

            with allure.step("Save Column Chooser with partial selection"):
                
                save_btn_xpath = "//div[@role='button' and @aria-label='Save as Default View']"
               
                column_chooser_save_btn_elem = wait.until(EC.presence_of_element_located((By.XPATH, save_btn_xpath)))
                highlight_element(driver, column_chooser_save_btn_elem)
                column_chooser_save_btn_elem.click()
                print("✅ Saved Column Chooser with partial selection")

            with allure.step("Validate toast message after saving partial selection"):
                toast_msg_elem = wait.until(EC.presence_of_element_located((By.XPATH, toast_msg)))
                msg = toast_msg_elem.text.strip()
                time.sleep(6)
                print(f"📢 Toast message after saving partial selection: {msg}")

            with allure.step("Validate table headers after partial selection"):
                time.sleep(2)
                wait_for_loader_to_disappear(driver, wait)
                header_elements = wait.until(EC.presence_of_all_elements_located((By.XPATH,"//tr[contains(@class,'dx-header-row')]//div[contains(@class,'dx-datagrid-text-content')]")))

                col_headers = [hdr.text.strip() for hdr in header_elements if hdr.text.strip()]
                print(f"📊 Found column headers after partial selection: {col_headers}")
                normalized_headers = [h.lower() for h in col_headers]
                expected_col = col_to_select.lower()

                if expected_col in normalized_headers:
                    print(f"✅ Selected '{col_to_select}' column is present")
                    return True
                else:
                    print(f"❌ Missing expected column: {col_to_select}")
                    allure.attach("\n".join(col_headers),name="Partial Column Selection Failed",attachment_type=allure.attachment_type.TEXT)
                    return False


            time.sleep(5)

        except Exception as err:
            print(f"❌ Error during partial column chooser validation: {err}")
            allure.attach(str(err), name="Partial_Selection_Error", attachment_type=allure.attachment_type.TEXT)
            return False

def project_column_chooser_validation(driver, wait):
    wait_less = WebDriverWait(driver, 5)
    failed_steps = []
    try:
        with open(os.path.join("data", 'locators.json'), 'r') as f:
            elements_details = json.load(f)
            project_icon = elements_details['project_icon']
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

    select_all_result = select_all_columns(driver, wait, project_icon, toast_msg)
    if not select_all_result:
        print("❌ 'Select All' validation failed")
        allure.attach("Failure in 'Select All' validation", name="SelectAll_Failure", attachment_type=allure.attachment_type.TEXT)
        # return False
        failed_steps.append("Select All")
    else:
        print("✅ 'Select All' validation successful")

    partial_result = select_partial_columns(driver, wait, project_icon,toast_msg)
    if not partial_result:
        print("❌ 'Partial Selection' validation failed")
        allure.attach("Failure in 'Partial Selection' validation", name="Partial_Failure", attachment_type=allure.attachment_type.TEXT)
        # return False
        failed_steps.append("Partial Selection")
    else:
        print("✅ 'Partial Selection' validation successful")

    final_select_all_result = select_all_columns(driver, wait, project_icon, toast_msg)
    if not final_select_all_result:
        print("❌ Final 'Select All' revalidation failed")
        allure.attach("Failure in final 'Select All' revalidation", name="Final_SelectAll_Failure", attachment_type=allure.attachment_type.TEXT)
        # return False
        failed_steps.append("Final Select All Revalidation")
    else:
        print("✅ Final 'Select All' revalidation successful")

    if failed_steps:
        pytest.fail(f"❌ Failed Steps: {failed_steps}")   # ✅ fail at end
    else:
        print("🎯 All validations passed ✅")
    # ✅ All steps passed
    print("🎯 Column Chooser validation flow completed successfully ✅")
    return True
