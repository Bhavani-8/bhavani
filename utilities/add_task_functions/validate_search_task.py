from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import pandas as pd
import pytest
import allure
import time
import json
import os
import pyautogui as pg
import glob

from utilities.other_utils_functions.highlight import highlight_element
from utilities.add_task_functions.wait_for_loader_to_disappear import wait_for_loader_to_disappear


def validate_search_task(driver, wait, task_name):

    try:
        with open(os.path.join("data", 'locators.json'), 'r') as f:
            elements_details = json.load(f)
            task_close_btn = elements_details['task_close_btn']
            dash_total_btn = elements_details['dash_total_btn']
            task_search_btn = elements_details['task_search_btn']
            task_search_input = elements_details['task_search_input']
            export_btn = elements_details['export_btn']
            export_selected_rows_btn = elements_details['export_selected_rows_btn']
            dash_col_all_selection_btn = elements_details['dash_col_all_selection_btn']

    except FileNotFoundError:
        pytest.fail("locators.json file not found")
    except json.JSONDecodeError:
        pytest.fail("Invalid JSON in locators.json")
    # with allure.step("Click close Button in Task details"):
    try:
        close_task_btn = wait.until(EC.presence_of_element_located((By.XPATH, task_close_btn)))
        highlight_element(driver, close_task_btn)
        close_task_btn.click()
        print("✅ Task closed successfully.")
        wait_for_loader_to_disappear(driver, wait)
        time.sleep(1)

        wait_for_loader_to_disappear(driver, wait)
        total_tab = wait.until(EC.element_to_be_clickable((By.XPATH, dash_total_btn)))
        highlight_element(driver, total_tab)
        total_tab.click()
        wait_for_loader_to_disappear(driver, wait)
        time.sleep(3)
    except Exception as err:
        allure.attach(str(err), "Close Button error", allure.attachment_type.TEXT)
        return False

    try:
        search_icon_btn = wait.until(EC.presence_of_element_located((By.XPATH, task_search_btn)))
        highlight_element(driver, search_icon_btn)
        search_icon_btn.click()

        # Enter task name
        search_input = wait.until(EC.visibility_of_element_located((By.XPATH, task_search_input)))
        highlight_element(driver, search_input)
        search_input.clear()
        search_input.send_keys(task_name)

        wait_for_loader_to_disappear(driver, wait)
        time.sleep(4)
    except Exception as e:
        msg = f"🔥 Error Searching Task: {e}"
        print(msg)
        allure.attach(msg, name="Search Task Failure", attachment_type=allure.attachment_type.TEXT)
        return False

    try:
        dash_col_all_selection_btn_elem = wait.until(EC.presence_of_element_located((By.XPATH, dash_col_all_selection_btn)))
        highlight_element(driver, dash_col_all_selection_btn_elem)
        dash_col_all_selection_btn_elem.click()
        print("✅ Selected all rows in Dashboard")
        time.sleep(4)
        wait_for_loader_to_disappear(driver, wait)
    except Exception as e:
        print("❌ Failed to select all rows in Dashboard")
        allure.attach(str(e), name="Select_All_Error", attachment_type=allure.attachment_type.TEXT)
        raise
   
    try:
        wait_for_loader_to_disappear(driver, wait)
        time.sleep(4)
        export_data_btn = wait.until(EC.presence_of_element_located((By.XPATH, export_btn)))
        export_data_btn.click()
        export_selected_rows = wait.until(EC.presence_of_element_located((By.XPATH, export_selected_rows_btn)))
        export_selected_rows.click()
        print("✅ Exported Selected Rows (after selecting rows)")
        pg.press('esc')
        wait_for_loader_to_disappear(driver, wait)
        time.sleep(5)  
        pg.press('esc')
    except Exception as e:
        print("❌ Failed to export selected rows after selection")
        allure.attach(str(e), name="Export_Selected_After_Error", attachment_type=allure.attachment_type.TEXT)
        return False

    try:
        
        downloads_path = os.path.join(os.getcwd(), "downloads")
        files = glob.glob(os.path.join(downloads_path, "*.xlsx"))

        if not files:
            raise Exception("No Excel files found in downloads folder.")

        latest_file = max(files, key=os.path.getctime)
        excel_df = pd.read_excel(latest_file, sheet_name=0)

        if excel_df.empty:
            raise Exception("Exported Excel is empty.")

        print(f"📊 Total Rows: {len(excel_df)}")

        excel_df.columns = (
            excel_df.columns
            .astype(str)
            .str.replace("\n", " ")
            .str.replace("\xa0", " ")   
            .str.replace(r"\s+", " ", regex=True)
            .str.strip()
        )

        required_cols = [
            "Task Name",
            "Internal Deadline",
            "Due Date"
        ]

        missing_cols = [col for col in required_cols if col not in excel_df.columns]

        if missing_cols:
            raise Exception(f"Missing columns in Excel: {missing_cols}")

        final_df = excel_df[required_cols].copy()

        def clean(val):
            return " ".join(str(val).split())

        for col in final_df.columns:
            final_df[col] = final_df[col].apply(clean)

        # -----------------------------
        # DUPLICATE CHECK
        # -----------------------------
        duplicate_df = final_df[final_df.duplicated(keep=False)]

        if not duplicate_df.empty:

            print("\n❌ Duplicate Rows Found:\n")

            for idx, row in duplicate_df.iterrows():

                msg = (
                    
                    f"Task='{row['Task Name']}', "
                    f"Internal Deadline='{row['Internal Deadline']}', "
                    f"Due Date='{row['Due Date']}'"
                )

                print(msg)
                allure.attach(msg,name=f"Duplicate Row {idx + 1}",attachment_type=allure.attachment_type.TEXT)
                return False

        else:
            print("✅ No duplicate rows found")

        for idx, row in final_df.reset_index(drop=True).iterrows():
            msg = (f"Row {idx + 1} → "
                f"Task='{row['Task Name']}',"
                f"Internal Deadline='{row['Internal Deadline']}', "
                f"Due Date='{row['Due Date']}'")
            print(msg)
            allure.attach(msg,name=f"Task  {idx + 1}",attachment_type=allure.attachment_type.TEXT)

    except Exception as e:
        allure.attach(str(e),name="Excel Validation Error",attachment_type=allure.attachment_type.TEXT)
        print("❌ ERROR:", str(e))
        return False

    return True