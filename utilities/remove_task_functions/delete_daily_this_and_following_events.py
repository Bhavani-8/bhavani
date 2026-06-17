from datetime import datetime, timedelta
import allure
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from utilities.other_utils_functions.highlight import highlight_element   
import time
import json
import pytest
import os
import pandas as pd
import pyautogui as pg
import glob
from utilities.add_task_functions.wait_for_loader_to_disappear import wait_for_loader_to_disappear
from selenium.common.exceptions import TimeoutException
from utilities.add_task_functions.format_time_if_valid import format_time_if_valid
from utilities.add_task_functions.format_date_if_valid import format_date_if_valid
from utilities.add_task_utils import add_task_check
from selenium.webdriver import ActionChains
from selenium.common.exceptions import StaleElementReferenceException


    
def delete_daily_this_and_following_events(driver, wait):
    
    with open(os.path.join("data", 'locators.json'), 'r') as f:
        elements_details = json.load(f)
        dash_total_btn = elements_details['dash_total_btn']
        dashboard_icon = elements_details['dashboard_icon']
        trash_icon = elements_details['trash_icon']
        task_search_btn = elements_details['task_search_btn']
        task_search_input = elements_details['task_search_input']
        task_open_btn = elements_details['task_open_btn']
        task_delete_btn = elements_details['task_delete_btn']
        toast_msg = elements_details['toast_msg']
        dash_total_btn = elements_details['dash_total_btn']
        task_search_btn = elements_details['task_search_btn']
        task_search_input = elements_details['task_search_input']
        export_btn = elements_details['export_btn']
        export_selected_rows_btn = elements_details['export_selected_rows_btn']
        dash_col_all_selection_btn = elements_details['dash_col_all_selection_btn']
        column_chooser_btn = elements_details['column_chooser_btn']
        column_chooser_save_btn = elements_details['column_chooser_save_btn']
        task_search_btn = elements_details['task_search_btn']
        task_search_input = elements_details['task_search_input']
        dash_total_btn = elements_details['dash_total_btn']
        toast_msg = elements_details['toast_msg']
        task_open_btn = elements_details['task_open_btn']
        column_chooser_internal_deadline = elements_details['column_chooser_internal_deadline']
        column_filter_internal_deadline = elements_details['column_filter_internal_deadline']
        date_filter_apply_btn = elements_details['date_filter_apply_btn']

    with allure.step("Validating Dashboard Widgets - Clicking Dashboard Icon"):
        dashboard_icon_elem = wait.until(EC.presence_of_element_located((By.XPATH, dashboard_icon)))
        highlight_element(driver, dashboard_icon_elem)
        dashboard_icon_elem.click()
        print("📊 Dashboard icon clicked.")
        allure.attach("Dashboard icon clicked",name="Dashboard Icon Clicked",attachment_type=allure.attachment_type.TEXT)

    test_case_details = pd.read_excel(os.path.join("data", "test_case_selector.xlsx"), sheet_name=f"add_task_test_cases").fillna("")
    # test_case_details = pd.read_excel(os.path.join("data", "test_case_selector.xlsx")).fillna("")
    first_row = test_case_details.iloc[0]
    task_name = first_row.get('task_name')
    
    start_date = format_date_if_valid(first_row.get('start_date'))
    due_date = format_date_if_valid(first_row.get('due_date'))
    frequency = "Daily"

    repeat_if_holiday = "Yes"
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
    description = first_row.get('description')
    attach_file_name= first_row.get('attach_file_name')
    impact_details = first_row.get('impact_details')
    impact_file_name = first_row.get('impact_file_name')
    circular_search = first_row.get('circular_search')
    test_type = first_row.get('test_type')

    

    with allure.step("Create Task"):
        task_name = f"{task_name}_daily_delte_task"
        try:
            if add_task_check(driver, task_name, start_date, due_date, frequency, repeat_if_holiday, end_freq_date,
                repeat_weekday, repeat_day_month, end_time, internal_deadline, assign_to, approver, cc,
                risk_rating, license_name, description, attach_file_name, impact_details, impact_file_name,
                circular_search, test_type, task_type='mandatory', direct_task_creation=False):
                print("✅ Task creation successful")
                time.sleep(6)
            else:
                allure.attach("Test case failed for Task Creation", name="Task Creation Validation Failed", attachment_type=allure.attachment_type.TEXT)
                return False
        except Exception as e:
            allure.attach(str(e), name="Add Task Error", attachment_type=allure.attachment_type.TEXT)
    
    with allure.step("Validating Dashboard - Click Search Icon and enter"):
        try:
            total_tab = wait.until(EC.presence_of_element_located((By.XPATH, dash_total_btn)))
            highlight_element(driver, total_tab)
            total_tab.click()
            wait_for_loader_to_disappear(driver, wait)
            # click search icon
            search_icon_btn = wait.until(EC.presence_of_element_located((By.XPATH, task_search_btn)))
            highlight_element(driver, search_icon_btn)
            search_icon_btn.click()

            search_input = wait.until(EC.visibility_of_element_located((By.XPATH, task_search_input)))
            highlight_element(driver, search_input)
            search_input.clear()
            search_input.send_keys(task_name)

            wait_for_loader_to_disappear(driver, wait)
            time.sleep(4)  # Extra wait to ensure results load

        except Exception as e:
            allure.attach(str(e), name="Total tab Error", attachment_type=allure.attachment_type.TEXT)

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
                pytest.fail("❌ Duplicate rows found in Excel")

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
            raise

    with allure.step("Open Column Chooser"):     
        try:     
            column_chooser_btn_elem = wait.until(EC.presence_of_element_located((By.XPATH, column_chooser_btn)))
            highlight_element(driver, column_chooser_btn_elem)
            driver.execute_script("arguments[0].click();", column_chooser_btn_elem)
            print("Clicked Column Chooser button")
            wait_for_loader_to_disappear(driver, wait)
        except TimeoutException:
            pytest.fail("❌ Column Chooser button not found")
        def get_state(elem):
            """
            Returns: 'selected', 'deselected', 'mixed'
            """
            aria = elem.get_attribute("aria-checked")
            if aria == "true":
                return "selected"
            elif aria == "false":
                return "deselected"
            else:
                return "mixed"   

        try:
            select_all_checkbox = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".dx-list-select-all-checkbox")))
            driver.execute_script("arguments[0].scrollIntoView(true);", select_all_checkbox)
            time.sleep(0.2)
            state = get_state(select_all_checkbox)
            if state == "deselected":
                print("✅ Already deselected, no action needed")
            elif state == "selected":
                print("🔁 Deselecting 'Select All'")
                driver.execute_script("arguments[0].click();", select_all_checkbox)
                wait_for_loader_to_disappear(driver, wait)
                time.sleep(0.3)
            elif state == "mixed":
                print("🔁 Mixed state detected → select all → deselect")
                driver.execute_script("arguments[0].click();", select_all_checkbox)
                wait_for_loader_to_disappear(driver, wait)
                time.sleep(0.3)
                select_all_checkbox = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".dx-list-select-all-checkbox")))
                driver.execute_script("arguments[0].click();", select_all_checkbox)
                wait_for_loader_to_disappear(driver, wait)
                time.sleep(0.3)
            select_all_checkbox = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".dx-list-select-all-checkbox")))
            final_state = get_state(select_all_checkbox)
            print(f"➤ Final 'Select All' state: {final_state}")
            if final_state != "deselected":
                pytest.fail(f"❌ Select All normalization failed, state: {final_state}")
            print("✅ 'Select All' normalized successfully")
        except StaleElementReferenceException:
            pytest.fail("❌ Stale element while normalizing Select All")
    
    with allure.step("Select 'Internal Deadline' from Column Chooser"):    
        try:
            internal_deadline_option_elm = wait.until(EC.presence_of_element_located((By.XPATH, column_chooser_internal_deadline)))
            actions = ActionChains(driver)
            actions.move_to_element(internal_deadline_option_elm).perform()
            time.sleep(0.5)
            wait.until(EC.element_to_be_clickable((By.XPATH, column_chooser_internal_deadline)))
            internal_deadline_option_elm.click()

        except TimeoutException:
            print("❌ 'Company / Project', Approver, CC, Creator not found in filter list")
        try:
            save_btn = wait.until(EC.element_to_be_clickable((By.XPATH, column_chooser_save_btn)))
            highlight_element(driver, save_btn)
            save_btn.click()
            print("✅ Column Chooser saved")
        except TimeoutException:
            pytest.fail("❌ Save button not available / not clickable")

    with allure.step(f"Open Company/Project filter and search for '{task_name}'"):
        try:
            internal_deadline_filter_btn = wait.until(EC.presence_of_element_located((By.XPATH, column_filter_internal_deadline)))
            internal_deadline_filter_btn.click()
            highlight_element(driver, internal_deadline_filter_btn)
            time.sleep(2)
        except Exception as e:
            allure.attach(str(e),name="Internal Deadline Filter Error",attachment_type=allure.attachment_type.TEXT)

        try:
            today = datetime.today().strftime("%Y-%m-%d")

            base = "//input[@placeholder='{range}']"

            from_input = wait.until(EC.presence_of_element_located((By.XPATH, base.replace("{range}", "From"))))
            from_input.click()
            from_input.send_keys(today)
            time.sleep(0.3)

            to_input = wait.until(EC.presence_of_element_located((By.XPATH, base.replace("{range}", "To"))))
            to_input.click()
            to_input.send_keys(today)
            time.sleep(0.3)

            apply_button = wait.until(EC.element_to_be_clickable((By.XPATH, date_filter_apply_btn)))
            apply_button.click()
            time.sleep(5)
            print(f"Internal Deadline : Applied date range {today} → {today}")
            time.sleep(1)
        
        except Exception as e:
            allure.attach(str(e),name="Apply date Error",attachment_type=allure.attachment_type.TEXT)

        
        try:
            task_open_btn_elem = wait.until(EC.presence_of_element_located((By.XPATH, task_open_btn)))
            highlight_element(driver, task_open_btn_elem)
            task_open_btn_elem.click()
            time.sleep(2)
            wait_for_loader_to_disappear(driver, wait)
        except Exception as e:
            allure.attach(str(e),name="Task Open button Error",attachment_type=allure.attachment_type.TEXT)

        
    with allure.step("Validating Dashboard - Checking Delete Button"):
        delete = wait.until(EC.presence_of_element_located((By.XPATH, task_delete_btn)))
        highlight_element(driver, delete)
        delete.click()
        print("🗑️ Delete button clicked.")
   
    with allure.step("Validating Dashboard - Confirming Task Deactivation"):

        this_and_following_events_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='This and following events']")))
        highlight_element(driver, this_and_following_events_btn)
        this_and_following_events_btn.click()
        print("✅This Event Button Clicked")

        delete_btn = wait.until(EC.presence_of_element_located((By.XPATH, "//button[span='Delete']")))
        highlight_element(driver, delete_btn)
        delete_btn.click()

    with allure.step("Validate toast message after saving"):
        toast_msg_elem = wait.until(EC.presence_of_element_located((By.XPATH, toast_msg)))
        msg = toast_msg_elem.text.strip()
        time.sleep(6)
        print(f"📢 Toast message after saving: {msg}")
        
    #  Validating Dashboard Widgets - Clicking Trash Icon
    with allure.step("Validating Dashboard - Clicking Trash Icon"):
       trash_icon_elem = wait.until(EC.presence_of_element_located((By.XPATH, trash_icon)))
       highlight_element(driver, trash_icon_elem)
       trash_icon_elem.click()
       print("🗑️ Trash icon clicked.")
        
    with allure.step("Click Tasks Tab"):
        try:
            time.sleep(3)
            tasks_tab = wait.until(EC.presence_of_element_located((By.XPATH, "//button[text()='Tasks']")))
            highlight_element(driver, tasks_tab)
            tasks_tab.click()
            print("📌 Tasks tab clicked")

        except Exception as e:
            allure.attach(str(e), name="Tasks Tab Error", attachment_type=allure.attachment_type.TEXT)
           
    
    with allure.step("Validating Dashboard - Clicking Restore Button"):
        try:
            task_name_elem = wait.until(EC.visibility_of_element_located((By.XPATH, f"//span[@title='{task_name}']")))
            highlight_element(driver, task_name_elem)
            fetch_task_name_elem = task_name_elem.text.strip()
            print(f"✅ Task '{fetch_task_name_elem}' found in Trash")
        except Exception as e:
            allure.attach(str(e), name="Task name Error", attachment_type=allure.attachment_type.TEXT)
    
    with allure.step("Click Restore Task"):
        try:
            time.sleep(3)
            restore_elem = wait.until(EC.presence_of_element_located((By.XPATH, f"//tr[@data-slot='table-row'][.//span[@title='{task_name}']]//button[@title='Restore Task']")))
            highlight_element(driver, restore_elem)
            restore_elem.click()
            time.sleep(3)
            print("📌 Restore Task button clicked")

        except Exception as e:
            allure.attach(str(e), name="Restore Error", attachment_type=allure.attachment_type.TEXT)
    # ---- Wait for Toast Message ----
    with allure.step("Validate toast message after saving"):
        toast_msg_elem = wait.until(EC.presence_of_element_located((By.XPATH, toast_msg)))
        msg = toast_msg_elem.text.strip()
        time.sleep(6)
        print(f"📢 Toast message after saving: {msg}")
    
    with allure.step("Verify created task by searching and validating data"):
        try:
            dashboard_icon_elem = wait.until(EC.presence_of_element_located((By.XPATH, dashboard_icon)))
            highlight_element(driver, dashboard_icon_elem)
            dashboard_icon_elem.click()
            print("✅ Dashboard icon clicked")
            wait_for_loader_to_disappear(driver, wait)
            
            total_tab = wait.until(EC.presence_of_element_located((By.XPATH, dash_total_btn)))
            highlight_element(driver, total_tab)
            total_tab.click()
            wait_for_loader_to_disappear(driver, wait)
            # click search icon
            search_icon_btn = wait.until(EC.presence_of_element_located((By.XPATH, task_search_btn)))
            highlight_element(driver, search_icon_btn)
            search_icon_btn.click()

            search_input = wait.until(EC.visibility_of_element_located((By.XPATH, task_search_input)))
            highlight_element(driver, search_input)
            search_input.clear()
            search_input.send_keys(task_name)

            wait_for_loader_to_disappear(driver, wait)
            time.sleep(4)  # Extra wait to ensure results load
    
        except Exception as e:
            allure.attach(str(e), name="Restore Error", attachment_type=allure.attachment_type.TEXT)

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
                pytest.fail("❌ Duplicate rows found in Excel")

            else:
                print("✅ No duplicate rows found")


            expected_start_date = datetime.today().date()

            invalid_rows = []

            for idx, row in final_df.iterrows():

                internal_deadline = pd.to_datetime(
                    row["Internal Deadline"],
                    dayfirst=True,
                    errors="coerce"
                ).date()

                if internal_deadline < expected_start_date:

                    msg = (
                        f"❌ Invalid Internal Deadline Found → "
                        f"Row {idx + 1}, "
                        f"Task='{row['Task Name']}', "
                        f"Internal Deadline='{row['Internal Deadline']}' "
                        f"is below expected date '{expected_start_date}'"
                    )

                    print(msg)

                    allure.attach(
                        msg,
                        name=f"Invalid Date Row {idx + 1}",
                        attachment_type=allure.attachment_type.TEXT
                    )

                    invalid_rows.append(msg)

            if invalid_rows:
                pytest.fail(
                    f"❌ Found {len(invalid_rows)} rows with Internal Deadline below expected start date"
                )

            else:
                print("✅ All Internal Deadline dates are valid")


            for idx, row in final_df.reset_index(drop=True).iterrows():

                msg = (
                    f"Row {idx + 1} → "
                    f"Task='{row['Task Name']}', "
                    f"Internal Deadline='{row['Internal Deadline']}', "
                    f"Due Date='{row['Due Date']}'"
                )

                print(msg)

            allure.attach(
                msg,
                name=f"Task {idx + 1}",
                attachment_type=allure.attachment_type.TEXT
            )
        
        except Exception as e: 
            allure.attach(str(e),name="Excel Validation Error",attachment_type=allure.attachment_type.TEXT) 
            print("❌ ERROR:", str(e)) 
            raise

        try:

            task_open_btn_elem = wait.until(EC.presence_of_element_located((By.XPATH, task_open_btn)))
            highlight_element(driver, task_open_btn_elem)
            task_open_btn_elem.click()
            time.sleep(2)
            wait_for_loader_to_disappear(driver, wait)
        except Exception as e:
            allure.attach(str(e),name="Task Open button Error",attachment_type=allure.attachment_type.TEXT)
    with allure.step("Validating Dashboard - Checking Delete Button"):
        delete = wait.until(EC.presence_of_element_located((By.XPATH, task_delete_btn)))
        highlight_element(driver, delete)
        delete.click()
        print("🗑️ Delete button clicked.")
   
    with allure.step("Validating Dashboard - Confirming Task Deactivation"):

        this_and_following_events_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='This and following events']")))
        highlight_element(driver, this_and_following_events_btn)
        this_and_following_events_btn.click()
        print("✅This Event Button Clicked")

        delete_btn = wait.until(EC.presence_of_element_located((By.XPATH, "//button[span='Delete']")))
        highlight_element(driver, delete_btn)
        delete_btn.click()

    return True

        
   
    