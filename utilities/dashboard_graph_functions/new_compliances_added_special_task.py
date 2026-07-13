from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import allure
import json
import os
import time
import pytest
from datetime import datetime

import pandas as pd
import pyautogui as pg
import glob
from utilities.add_task_functions.add_task_common import task_value_store
from utilities.add_task_functions.add_task_common import task_value_get
from utilities.add_task_functions.format_time_if_valid import format_time_if_valid
from utilities.add_task_functions.format_date_if_valid import format_date_if_valid
from utilities.special_add_task_utils import special_task_check
from utilities.other_utils_functions.highlight import highlight_element
from utilities.add_task_functions.wait_for_loader_to_disappear import wait_for_loader_to_disappear


def new_compliances_special_task(driver, wait, new_compliance_sp_task):
    with allure.step("Loading locators from JSON"):
        try:
            with open(os.path.join("data", 'locators.json'), 'r') as f:
                elements_details = json.load(f)
                new_compliances_added_btn = elements_details["new_compliances_added_btn"]
                task_close_btn = elements_details['task_close_btn']
                export_btn = elements_details['export_btn']
                export_all_data_btn = elements_details['export_all_data_btn']
                dashboard_icon = elements_details['dashboard_icon']
            print("✅ locators.json loaded successfully")
        except FileNotFoundError as e:
            print("❌ locators.json file not found")
            allure.attach(str(e), name="Locators_FileNotFound", attachment_type=allure.attachment_type.TEXT)
            pytest.fail("locators.json file not found")
        except json.JSONDecodeError as e:
            print("❌ Invalid JSON in locators.json")
            allure.attach(str(e), name="Invalid_JSON", attachment_type=allure.attachment_type.TEXT)
            pytest.fail("Invalid JSON in locators.json")

    test_case_details = pd.read_excel(os.path.join("data", "test_case_selector.xlsx"), sheet_name=f"special_add_task_test_cases").fillna("")
    # test_case_details = pd.read_excel(os.path.join("data", "test_case_selector.xlsx")).fillna("")
    first_row = test_case_details.iloc[0]
    # task_name = first_row.get('task_name')
    # task_name = str(first_row.get('task_name', '')).strip()
    current_task_name = new_compliance_sp_task.strip() if new_compliance_sp_task else "task_name"
    task_name = current_task_name
    task_value_store("task_name", task_name)
    start_date = format_date_if_valid(first_row.get('start_date'))
    due_date = format_date_if_valid(first_row.get('due_date'))
    frequency = first_row.get('frequency')
    repeat_if_holiday = first_row.get('repeat_if_holiday')
    end_freq_date = first_row.get('end_freq_date')
    repeat_weekday = first_row.get('repeat_weekday')
    repeat_day_month = first_row.get('repeat_day_month')
    # end_time = first_row.get('end_time')
    end_time = format_time_if_valid(first_row.get('end_time')) if pd.notna(first_row.get('end_time')) else None
    internal_deadline = first_row.get('internal_deadline')
    assign_to = first_row.get('assign_to')
    approver = first_row.get('approver')
    cc = first_row.get('cc')
    risk_rating = first_row.get('risk_rating')
    license_name = first_row.get('license_name')
    task_category = first_row.get('task_category')
    description = first_row.get('description')
    attach_file_name= first_row.get('attach_file_name')
    impact_details = first_row.get('impact_details')
    impact_file_name = first_row.get('impact_file_name')
    circular_search = first_row.get('circular_search')
    test_type = first_row.get('test_type')

    with allure.step("Create Task"):
        try:
            if special_task_check(driver, task_name, start_date, due_date, frequency, repeat_if_holiday, end_freq_date,
                repeat_weekday, repeat_day_month, end_time, internal_deadline, assign_to, approver, cc,
                risk_rating, license_name, task_category, description, attach_file_name, impact_details, impact_file_name,
                circular_search, test_type, task_type='mandatory', login_required=False):
                print("✅ Task creation successful")
                created_task = task_value_get("task_name")
            else:
                allure.attach("Test case failed for Task Creation", name="Task Creation Validation Failed", attachment_type=allure.attachment_type.TEXT)
                return False
        except Exception as e:
            allure.attach(str(e), name="Add Task Error", attachment_type=allure.attachment_type.TEXT)
    
        try:
            close_task_btn = wait.until(EC.presence_of_element_located((By.XPATH, task_close_btn)))
            highlight_element(driver, close_task_btn)
            close_task_btn.click()
            print("✅ Task closed successfully.")
            wait_for_loader_to_disappear(driver, wait)
            time.sleep(1)

        
        except Exception as err:
            allure.attach(str(err), "Close Button error", allure.attachment_type.TEXT)
            pytest.fail("Failed to click Close Button")
    with allure.step("Open Dashboard"):
        try:
            time.sleep(2)
            dashboard_icon_elem = wait.until(EC.presence_of_element_located((By.XPATH, dashboard_icon)))
            highlight_element(driver, dashboard_icon_elem)
            dashboard_icon_elem.click()
            time.sleep(1)
            print("✅ Dashboard icon clicked")
        except Exception as e:
            allure.attach(str(e), name="Dashboard Open Error", attachment_type=allure.attachment_type.TEXT)
            return False
    with allure.step("Open New Compliance Added"):
        try:
            new_compliances_added = wait.until(EC.presence_of_element_located((By.XPATH, new_compliances_added_btn)))
            highlight_element(driver, new_compliances_added)
            new_compliances_added.click()
            time.sleep(2)
        except Exception as e:
            allure.attach(str(e), name="New Compliances added Error", attachment_type=allure.attachment_type.TEXT)    
    
    with allure.step("Check Today's Date Tasks"):
        try:
            dashboard_header = wait.until(EC.presence_of_element_located((By.XPATH, "//p[text()='New Compliances']")))
            header_text = dashboard_header.text.strip()
            date_element = wait.until(EC.presence_of_element_located((By.XPATH, "//p[@class='ml-2 mb-0 mt-1 text-muted']")))
            dashboard_date = date_element.text.strip()
            highlight_element(driver, date_element)
            
            today_date = datetime.now().strftime("%d %b %Y")
            
            assert today_date in dashboard_date, (f"Expected today's date: {today_date}, "f"but found: {dashboard_date}")

            allure.attach(f"{header_text} {dashboard_date}",name="Today's Date Validation",attachment_type=allure.attachment_type.TEXT)

        except Exception as e:
            allure.attach(str(e),name="Today's Date Error",attachment_type=allure.attachment_type.TEXT)
    
        try:
            wait_for_loader_to_disappear(driver, wait)
            time.sleep(4)
            export_data_btn = wait.until(EC.presence_of_element_located((By.XPATH, export_btn)))
            export_data_btn.click()
            time.sleep(2)
            export_all = wait.until(EC.presence_of_element_located((By.XPATH, export_all_data_btn)))
            export_all.click()
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

            # Get latest exported Excel
            latest_file = max(files, key=os.path.getctime)
            print(f"📄 Validating Excel: {latest_file}")

            excel_df = pd.read_excel(latest_file, sheet_name=0)

            if excel_df.empty:
                raise Exception("Exported Excel is empty.")

            print(f"📊 Total Rows in Excel: {len(excel_df)}")

            # -----------------------------
            # Normalize column names
            # -----------------------------
            excel_df.columns = (
                excel_df.columns.astype(str)
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

            # -----------------------------
            # Find Newly Created Task
            # -----------------------------
            final_df = excel_df[
                excel_df["Task Name"].astype(str).str.strip() == created_task.strip()
            ][required_cols].copy()

            if final_df.empty:
                msg = (
                    f"❌ Newly created task '{created_task}' "
                    f"not found in exported Excel."
                )

                print(msg)

                allure.attach(
                    msg,
                    name="Task Not Found",
                    attachment_type=allure.attachment_type.TEXT
                )

                pytest.fail(msg)

            print(f"✅ Found {len(final_df)} row(s) for task: {task_name}")

            # -----------------------------
            # Clean Values
            # -----------------------------
            def clean(val):
                return " ".join(str(val).split())

            for col in final_df.columns:
                final_df[col] = final_df[col].apply(clean)

            # -----------------------------
            # Duplicate Validation
            # -----------------------------
            duplicate_df = final_df[final_df.duplicated(keep=False)]

            if not duplicate_df.empty:

                print("\n❌ Duplicate rows found for newly created task:\n")

                for idx, row in duplicate_df.reset_index(drop=True).iterrows():

                    msg = (
                        f"Duplicate Row {idx + 1}:\n"
                        f"Task Name='{row['Task Name']}'\n"
                        f"Internal Deadline='{row['Internal Deadline']}'\n"
                        f"Due Date='{row['Due Date']}'"
                    )

                    print(msg)

                    allure.attach(
                        msg,
                        name=f"Duplicate Row {idx + 1}",
                        attachment_type=allure.attachment_type.TEXT
                    )

                pytest.fail(
                    f"❌ Duplicate records found for task '{task_name}' "
                    f"in exported Excel."
                )

            else:
                print("✅ No duplicate records found.")

            # -----------------------------
            # Validate Internal Deadline
            # -----------------------------
            expected_date = datetime.today().date()

            for idx, row in final_df.reset_index(drop=True).iterrows():

                internal_deadline = pd.to_datetime(
                    row["Internal Deadline"],
                    dayfirst=True,
                    errors="coerce"
                )

                if pd.isna(internal_deadline):

                    msg = (
                        f"❌ Invalid Internal Deadline format "
                        f"for task '{row['Task Name']}'"
                    )

                    allure.attach(
                        msg,
                        name="Invalid Internal Deadline",
                        attachment_type=allure.attachment_type.TEXT
                    )

                    pytest.fail(msg)

                internal_deadline = internal_deadline.date()

                if internal_deadline < expected_date:

                    msg = (
                        f"❌ Internal Deadline Validation Failed\n"
                        f"Task Name : {row['Task Name']}\n"
                        f"Internal Deadline : {row['Internal Deadline']}\n"
                        f"Expected Date >= {expected_date}"
                    )

                    print(msg)

                    allure.attach(
                        msg,
                        name="Internal Deadline Validation",
                        attachment_type=allure.attachment_type.TEXT
                    )

                    pytest.fail(msg)

            print("✅ Internal Deadline validation passed.")

            # -----------------------------
            # Validate Due Date
            # -----------------------------
            for idx, row in final_df.reset_index(drop=True).iterrows():

                due_date = pd.to_datetime(
                    row["Due Date"],
                    dayfirst=True,
                    errors="coerce"
                )

                if pd.isna(due_date):

                    msg = (
                        f"❌ Invalid Due Date format "
                        f"for task '{row['Task Name']}'"
                    )

                    allure.attach(
                        msg,
                        name="Invalid Due Date",
                        attachment_type=allure.attachment_type.TEXT
                    )

                    pytest.fail(msg)

                due_date = due_date.date()

                if due_date < expected_date:

                    msg = (
                        f"❌ Due Date Validation Failed\n"
                        f"Task Name : {row['Task Name']}\n"
                        f"Due Date : {row['Due Date']}\n"
                        f"Expected Date >= {expected_date}"
                    )

                    print(msg)

                    allure.attach(
                        msg,
                        name="Due Date Validation",
                        attachment_type=allure.attachment_type.TEXT
                    )

                    pytest.fail(msg)

            print("✅ Due Date validation passed.")

            # -----------------------------
            # Attach Validated Task Details
            # -----------------------------
            for idx, row in final_df.reset_index(drop=True).iterrows():

                msg = (
                    f"Task Name='{row['Task Name']}'\n"
                    f"Internal Deadline='{row['Internal Deadline']}'\n"
                    f"Due Date='{row['Due Date']}'"
                )

                print(msg)

                allure.attach(
                    msg,
                    name=f"Validated Task {idx + 1}",
                    attachment_type=allure.attachment_type.TEXT
                )

            print("✅ Excel validation completed successfully.")

        except Exception as e:
            allure.attach(
                str(e),
                name="Excel Validation Error",
                attachment_type=allure.attachment_type.TEXT
            )

            print("❌ ERROR:", str(e))
            raise
    return True