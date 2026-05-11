import allure
import os
import json
import time
import pyautogui as pg
import pytest
import pandas as pd
import glob
from datetime import datetime

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys

from utilities.other_utils_functions.highlight import highlight_element
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import ActionChains
from selenium.common.exceptions import StaleElementReferenceException
from utilities.other_utils_functions.license_utils import validate_license_subscription
from utilities.add_task_utils import wait_for_loader_to_disappear

def step_fail(driver, step_name, error):
    allure.attach(str(error), name=f"{step_name} Error", attachment_type=allure.attachment_type.TEXT)
    allure.attach(driver.get_screenshot_as_png(), name=f"{step_name} Screenshot", attachment_type=allure.attachment_type.PNG)
    pytest.fail(f"❌ {step_name} failed")

def check_license_task(driver, wait, company_name, license_name, task_name):

    with allure.step("Load locators.json"):
        try:
            with open(os.path.join("data", "locators.json"), "r") as f:
                elements_details = json.load(f)
            settings_icon = elements_details["settings_icon"]
            dash_total_btn = elements_details['dash_total_btn']
            company_project_option = elements_details['company_project_option']
            column_chooser_save_btn = elements_details['column_chooser_save_btn']
            company_project_filter = elements_details['company_project_filter']
            column_filter_ok_btn = elements_details['column_filter_ok_btn']
            task_open_btn = elements_details['task_open_btn']
            task_frequency_label = elements_details.get('task_frequency_label')
            dashboard_icon = elements_details['dashboard_icon']
            task_license_close_btn = elements_details['task_license_close_btn']
            task_update_tab = elements_details['task_update_tab']
            task_title_label = elements_details['task_title_label']
            column_chooser_btn = elements_details['column_chooser_btn']
            task_license_label = elements_details['task_license_label']
            onprem_task_license_label = elements_details['onprem_task_license_label']
            export_btn = elements_details['export_btn']
            export_selected_rows_btn = elements_details['export_selected_rows_btn']
            dash_col_all_selection_btn = elements_details['dash_col_all_selection_btn']
            print("✅ locators.json loaded successfully")
        except Exception as e:
            allure.attach(str(e), name="Locators Load Error", attachment_type=allure.attachment_type.TEXT)
            return False

    with allure.step("Click Settings Button"):
        
        print()
        settings_btn = wait.until(EC.presence_of_element_located((By.XPATH, settings_icon)))
        highlight_element(driver, settings_btn)
        settings_btn.click()
        print("✅ Settings Icon Clicked")
        time.sleep(2)
        
        company_btn = wait.until(EC.presence_of_element_located((By.XPATH, "//span[text()='Company']")))
        highlight_element(driver, company_btn)
        company_btn.click()
        print("✅ Company Button Clicked")
        time.sleep(2)   

        license_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@id='editLicense0']")))
        driver.execute_script("arguments[0].click();", license_btn)

        license_elements = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//p[contains(@class,'Category')]")))
        for elem in license_elements:
            driver.execute_script("arguments[0].scrollIntoView(true);", elem)
            time.sleep(0.2)
        # ---------------- Collect license names ----------------
        license_names = [elem.text.strip() for elem in license_elements]
        total_licenses = len(license_names)
        print(f"🔹 Total Licenses Found: {total_licenses}")
        print("🔹 License Names:")

        close_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@class,'MuiIconButton-root')]")))
        highlight_element(driver, close_btn)
        close_btn.click()

        previous_license_name = None

        for idx, license_name in enumerate(license_names):

            try:
                print(f"➡ Processing License {idx+1}/{total_licenses}: {license_name}")
                # Always reopen Settings → Company → Edit License
                settings_btn = wait.until(EC.element_to_be_clickable((By.XPATH, settings_icon)))
                driver.execute_script("arguments[0].click();", settings_btn)
                wait_for_loader_to_disappear(driver, wait)
                time.sleep(1)

                company_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Company']")))
                driver.execute_script("arguments[0].click();", company_btn)
                wait_for_loader_to_disappear(driver, wait)
                time.sleep(1)

                license_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@id='editLicense0']")))
                driver.execute_script("arguments[0].click();", license_btn)
                wait_for_loader_to_disappear(driver, wait)


        # ================= DESELECT PREVIOUS LICENSE =================
                if previous_license_name:

                    print(f"🔁 Deselecting Previous License: {previous_license_name}")

                    license_elements = wait.until(
                        EC.presence_of_all_elements_located(
                            (By.XPATH, "//p[contains(@class,'Category')]")
                        )
                    )

                    for elem in license_elements:
                        ui_license_name = elem.text.strip()

                        if ui_license_name == previous_license_name:

                            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", elem)
                            highlight_element(driver, elem)
                            driver.execute_script("arguments[0].click();", elem)
                            time.sleep(1)

                            checkboxes = wait.until(
                                EC.presence_of_all_elements_located(
                                    (By.XPATH, "//div[contains(@class,'columns-license')]//input[@type='checkbox']")
                                )
                            )

                            for checkbox in checkboxes:
                                is_checked = (
                                    checkbox.get_attribute("checked") == "true"
                                    or checkbox.get_attribute("aria-checked") == "true"
                                    or checkbox.is_selected()
                                )

                                if is_checked:
                                    driver.execute_script("arguments[0].click();", checkbox)
                                    time.sleep(0.2)

                            print(f"✅ Deselected all checkboxes for {previous_license_name}")
                            break

            # ================= SELECT CURRENT LICENSE =================

                license_elements = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//p[contains(@class,'Category')]")))
                current_elem = None

                for elem in license_elements:
                    ui_license_name = elem.text.strip()

                    if ui_license_name == license_name.strip():
                        current_elem = elem
                        break

                if not current_elem:
                    print(f"❌ License not found in UI: {license_name}")
                    continue

                driver.execute_script("arguments[0].scrollIntoView({block:'center'});", current_elem)
                highlight_element(driver, current_elem)
                driver.execute_script("arguments[0].click();", current_elem)
                time.sleep(1)


                # Update previous_license_name ONLY from UI text
                previous_license_name = current_elem.text.strip()
                print(f"🔁 Updated previous_license_name = {previous_license_name}")

                # ================= SELECT ALL CHECKBOXES =================

                checkboxes = wait.until(
                    EC.presence_of_all_elements_located(
                        (By.XPATH, "//div[contains(@class,'columns-license')]//input[@type='checkbox']")
                    )
                )

                for checkbox in checkboxes:

                    is_checked = (
                        checkbox.get_attribute("checked") == "true"
                        or checkbox.get_attribute("aria-checked") == "true"
                        or checkbox.is_selected()
                    )

                    if not is_checked:
                        driver.execute_script("arguments[0].click();", checkbox)
                        time.sleep(0.2)

                print(f"✅ Selected all checkboxes for {previous_license_name}")

                add_license_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Add license']")))
                driver.execute_script("arguments[0].click();", add_license_btn)
                wait_for_loader_to_disappear(driver, wait)
                time.sleep(4)


                save_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//img[@alt='check Icon']")))
                driver.execute_script("arguments[0].click();", save_btn)
                time.sleep(14)

                print("✅ Company Saved Successfully")
            except Exception as e:
                step_fail(driver, f"Processing license {license_name}", e)

            with allure.step("Open Dashboard"):
                try:
                    dashboard_icon_elem = wait.until(EC.element_to_be_clickable((By.XPATH, dashboard_icon)))
                    highlight_element(driver, dashboard_icon_elem)
                    dashboard_icon_elem.click()
                    time.sleep(2)
                    print("✅ Dashboard icon clicked")

                except Exception as e:
                    allure.attach(str(e),name="Dashboard Open Error",attachment_type=allure.attachment_type.TEXT)
                    return False

            with allure.step("Validate License Subscription after login"):
                try:
                    if validate_license_subscription(driver):
                        print("✅ License present")
                    else:
                        print("ℹ️ License not present — continue")
                except Exception as e:
                    print(f"⚠️ Error occurred — continue: {e}") 

            with allure.step("Clicking Dashboard Total button"):
                try:
                    total_tab = wait.until(EC.presence_of_element_located((By.XPATH, dash_total_btn)))
                    highlight_element(driver, total_tab)
                    total_tab.click()
                    time.sleep(3)
                except Exception as err:
                    allure.attach(str(err), "Total tab error", allure.attachment_type.TEXT)
                    pytest.fail("Failed to click Total tab")
    
            with allure.step("Open Column Chooser from task list"):
                column_chooser_btn_elem = wait.until(EC.presence_of_element_located((By.XPATH, column_chooser_btn)))
                highlight_element(driver, column_chooser_btn_elem)
                driver.execute_script("arguments[0].click();", column_chooser_btn_elem)
                print("Clicked Column Chooser button")
                wait_for_loader_to_disappear(driver, wait)
            
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
                    print(f"➤ Initial 'Select All' state: {state}")
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
                    
            with allure.step("Select 'Company / Project, License' from Column Chooser"): 
                try:
                    company_project_option_elm = wait.until(EC.presence_of_element_located((By.XPATH, company_project_option)))
                    actions = ActionChains(driver)
                    actions.move_to_element(company_project_option_elm).perform()
                    time.sleep(0.5)
                    company_project_option_elm.click()

                    license_option = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='dx-item-content dx-list-item-content' and normalize-space()='License']")))
                    actions = ActionChains(driver)
                    actions.move_to_element(license_option).perform()
                    time.sleep(0.5)
                    license_option.click()

                    save_btn = wait.until(EC.element_to_be_clickable((By.XPATH, column_chooser_save_btn)))
                    highlight_element(driver, save_btn)
                    save_btn.click()
                    time.sleep(2)
                    print("✅ Column Chooser saved")
                    wait_for_loader_to_disappear(driver, wait)

                except TimeoutException:
                    print("❌ 'Company / Project' not found in filter list")

            with allure.step("No Task Found"):
                try:
                    try:
                        data_rows = wait.until(EC.presence_of_all_elements_located((By.XPATH,"//tr[@role='row' and not(contains(@class,'dx-header-row'))]")))
                    except TimeoutException:
                        print("ℹ️ No Task Found in Dashboard. Skipping export & validation.")
                        continue  
                    visible_rows = [row for row in data_rows if row.is_displayed()]

                    if len(visible_rows) == 0:
                        print("ℹ️ No visible rows. Skipping export.")
                        continue

                    print(f"✅ {len(visible_rows)} Tasks found. Proceeding with export.")

                except Exception as e:
                    print(f"⚠ Error while checking dashboard data: {e}")
                    continue
            with allure.step("Select all rows in Dashboard Table"):
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
        
            with allure.step("Export Selected Rows after selecting rows"):
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
        
            task_names_list = []
            company_names_list = []
            license_names_list = []
            with allure.step("Validate Exported Excel Data (Task Name + Frequency)"):
                try:
                    downloads_path = os.path.join(os.getcwd(), "downloads")
                    files = glob.glob(os.path.join(downloads_path, "*.xlsx"))
                    if not files:
                        raise Exception("No Excel files found in downloads folder.")
                    latest_file = max(files, key=os.path.getctime)
                    # print(f"📁 Latest Excel File: {latest_file}")
                    excel_df = pd.read_excel(latest_file)
                    if excel_df.empty:
                        raise Exception("Exported Excel is empty.")
                    print(f"📊 Total Rows in Excel: {len(excel_df)}")
                    final_df = excel_df[["Task Name", "Frequency", "Company /  Project", "License"]]
                    final_df.drop_duplicates(inplace=True, keep="first")
                    task_names_list = [" ".join(str(name).split())for name in final_df["Task Name"].tolist()]
                    company_names_list = [" ".join(str(name).split()) for name in final_df["Company /  Project"].tolist()]
                    license_names_list = [" ".join(str(name).split()) for name in final_df["License"].tolist()]
                    print(f"Task names in DataGrid: {task_names_list}")
                    print(f"Company names in DataGrid: {company_names_list}")
                    print(f"License names in DataGrid: {license_names_list}")

                except Exception as e:
                    allure.attach(str(e),name="Excel Validation Error",attachment_type=allure.attachment_type.TEXT)
                    print(str(e))
                    raise
            for task_name, company_name, license_name in zip(task_names_list, company_names_list, license_names_list):
                task_name = str(task_name).strip()
                company_name = str(company_name).strip()
                license_name = str(license_name).strip() 
                with allure.step(f"Task: {task_name}, Company: {company_name}, License: {license_name}"):
                    try:
                        task_name_filter_btn = wait.until(EC.element_to_be_clickable((By.XPATH,"//td[@role='columnheader'][.//text()[normalize-space()='Task Name']]//span[contains(@class,'dx-header-filter')]")))
                        highlight_element(driver, task_name_filter_btn)
                        task_name_filter_btn.click()
                        wait_for_loader_to_disappear(driver, wait)
                        time.sleep(1)

                        search_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@aria-label='Search']")))
                        search_input.clear()
                        search_input.send_keys(task_name)
                        wait_for_loader_to_disappear(driver, wait)
                        time.sleep(3)
                        
                        try:
                            license_task_option = wait.until(EC.presence_of_element_located((By.XPATH, f"//div[@role='option' and normalize-space()='{task_name}'][.//div[contains(@class,'dx-checkbox-container')]]")))
                            scroll_container = wait.until(EC.presence_of_element_located((By.XPATH, "(//div[@class='dx-scrollable-scroll-content'])[3]")))
                            driver.execute_script("""arguments[0].scrollTop = arguments[1].offsetTop - arguments[0].offsetTop;""", scroll_container, license_task_option)
                            time.sleep(0.5)  
                            highlight_element(driver, license_task_option)
                            driver.execute_script("arguments[0].click();", license_task_option)
                            wait_for_loader_to_disappear(driver, wait)
                        except Exception as e:
                            print(f"❌ Failed to click task '{task_name}' option: {e}")
                            try:
                                cancel_btn = wait.until(EC.element_to_be_clickable((By.XPATH,"//div[@aria-label='Cancel']")))
                                highlight_element(driver, cancel_btn)
                                driver.execute_script("arguments[0].click();", cancel_btn)
                                print("🔁 Clicked Cancel button after failure")
                                wait_for_loader_to_disappear(driver, wait)
                            except Exception as cancel_error:
                                print(f"⚠️ Failed to click Cancel button: {cancel_error}")
                            continue

                        column_filter_ok = wait.until(EC.presence_of_element_located((By.XPATH, column_filter_ok_btn)))
                        column_filter_ok.click()
                        wait_for_loader_to_disappear(driver, wait)
                        time.sleep(5)
                        # --- Company Filter ---
                        company_project_filter_btn = wait.until(EC.presence_of_element_located((By.XPATH, company_project_filter)))
                        time.sleep(2)
                        highlight_element(driver, company_project_filter_btn)
                        company_project_filter_btn.click()
                        wait_for_loader_to_disappear(driver, wait)
                        
                        search_input = wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@aria-label='Search' and contains(@class,'dx-texteditor-input')]")))
                        search_input.clear()
                        search_input.send_keys(company_name)
                        wait_for_loader_to_disappear(driver, wait)
                        time.sleep(5)

                        company_option = wait.until(EC.element_to_be_clickable((By.XPATH, f"//div[contains(@class,'dx-list-item-content') and normalize-space()='{company_name}']")))
                        highlight_element(driver, company_option)
                        company_option.click()
                        
                        column_filter_ok = wait.until(EC.presence_of_element_located((By.XPATH, column_filter_ok_btn)))
                        column_filter_ok.click()
                        wait_for_loader_to_disappear(driver, wait)
                        time.sleep(5)
                        # --- License Filter ---
                        license_filter_btn = wait.until(EC.presence_of_element_located((By.XPATH, "//td[@role='columnheader'][.//text()[normalize-space()='License']]//span[contains(@class,'dx-header-filter')]")))
                        time.sleep(2)
                        highlight_element(driver, license_filter_btn)
                        license_filter_btn.click()
                        wait_for_loader_to_disappear(driver, wait)
                    
                        search_input = wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@aria-label='Search' and contains(@class,'dx-texteditor-input')]")))
                        search_input.clear()
                        search_input.send_keys(license_name)
                        wait_for_loader_to_disappear(driver, wait)
                        time.sleep(5)

                        license_option = wait.until(EC.element_to_be_clickable((By.XPATH, f"//div[contains(@class,'dx-list-item-content') and normalize-space()='{license_name}']")))
                        highlight_element(driver, license_option)
                        license_option.click()  
                    
                        column_filter_ok = wait.until(EC.presence_of_element_located((By.XPATH, column_filter_ok_btn)))
                        column_filter_ok.click()
                        
                        wait_for_loader_to_disappear(driver, wait)
                        time.sleep(5)
                    except Exception as e:
                        print(f"❌ Failed for task: {task_name}")
                        print(str(e))
                        allure.attach(str(e),name=f"Error - {task_name}",attachment_type=allure.attachment_type.TEXT)
                        continue
            
                    try:
                        time.sleep(2)
                        task_open_btn_elem = wait.until(EC.element_to_be_clickable((By.XPATH, task_open_btn)))
                        highlight_element(driver, task_open_btn_elem)
                        task_open_btn_elem.click()
                    except Exception as e:
                        step_fail(driver, "Select License", e)

                    wait_for_loader_to_disappear(driver, wait)
                with allure.step("Validate Company and License in Task Details"):
                    try:
                        task_name_label_elem = wait.until(EC.visibility_of_element_located((By.XPATH, task_title_label)))
                        highlight_element(driver, task_name_label_elem, 0.2)
                        fetched_task_name = task_name_label_elem.text.strip()
                        print(f"🔹Task Title: {fetched_task_name}")

                        task_license_label_elem = wait.until(EC.visibility_of_element_located((By.XPATH, task_license_label)))
                        # task_license_label_elem = wait.until(EC.visibility_of_element_located((By.XPATH, onprem_task_license_label)))
                        highlight_element(driver, task_license_label_elem, 0.2)
                        fetched_license = task_license_label_elem.text.strip()
                        print(f"🔸License: {fetched_license}")

                        task_frequency_label_elem = wait.until(EC.visibility_of_element_located((By.XPATH, task_frequency_label)))
                        highlight_element(driver, task_frequency_label_elem, 0.2)
                        fetched_frequency = task_frequency_label_elem.text.strip()
                        print(f"🔹Task Frequency: {fetched_frequency}")
                    
                    except Exception as e:
                        step_fail(driver, "Validate License in Task Details", e)
                with allure.step("Validate Circular in Task Updates Tab"):
                    try:
                        elems = driver.find_elements(By.XPATH, task_update_tab)

                        if elems:
                            highlight_element(driver, elems[0])
                            elems[0].click()
                            print("✅ Update tab clicked")
                            allure.attach("Update tab is present and clicked", name="Update Tab Status", attachment_type=allure.attachment_type.TEXT)

                            try:
                                circular = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='checkbox-title']")))
                                highlight_element(driver, circular)
                                fetched_circular_text = circular.text.strip()
                                print(f"Circular Text: {fetched_circular_text}")
                                allure.attach(fetched_circular_text, name="Circular Text", attachment_type=allure.attachment_type.TEXT)
                            except:
                                print("Circular not present")
                                allure.attach("Circular not present", name="Circular Text", attachment_type=allure.attachment_type.TEXT)
                        else:
                            print("📍 Update tab not found")
                            allure.attach("Update tab not found", name="Circular Text", attachment_type=allure.attachment_type.TEXT)

                    except Exception as e:
                        print(f"Update check error: {e}")

                    try:
                        close_btn = wait.until(EC.element_to_be_clickable((By.XPATH, task_license_close_btn)))
                        close_btn.click()
                        wait_for_loader_to_disappear(driver, wait)
                    except Exception as e:
                        step_fail(driver, "Validate License in Task Details", e)
                    try:
                        reset_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@title='Reset Filters']")))
                        highlight_element(driver, reset_btn)
                        reset_btn.click()
                        wait_for_loader_to_disappear(driver, wait)
                        print()
                        time.sleep(5)
                        
                        # previous_license_name = license_name
                        # print()
                        # time.sleep(5)
                    except Exception as e:
                        step_fail(driver, "Validate License in Task Details", e)
            