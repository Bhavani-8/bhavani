

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.common.exceptions import TimeoutException
import pytest
import allure
import time
import json
import os
import re

from utilities.add_task_utils import wait_for_loader_to_disappear
from utilities.other_utils_functions.highlight import highlight_element


def count_validation(driver, wait):

    failures = []

    with allure.step("Column Counts Validation"):
        column_buttons = wait.until(EC.presence_of_all_elements_located((By.XPATH,"//button[normalize-space(text()) and number(normalize-space(text()))=number(normalize-space(text()))]")))
        print(f"✅ Found {len(column_buttons)} column buttons")
        for idx in range(len(column_buttons)):
            
            try:
                column_buttons = driver.find_elements(
                    By.XPATH,
                    "//td[.//button[number(normalize-space(text())) = number(normalize-space(text()))]]//button"
                )

                if idx >= len(column_buttons):
                    break

                btn = column_buttons[idx]

                driver.execute_script(
                    "arguments[0].scrollIntoView({block:'center'});", btn)
                time.sleep(0.5)

                column_text = btn.text.strip()

                if not column_text.isdigit():
                    continue

                column_value = int(column_text)

                is_disabled = btn.get_attribute("disabled")

                if column_value == 0 or is_disabled:
                    print(f"⚠️ Skipping {column_value} (disabled/zero)")
                    continue

                # Column name
                try:
                    parent_td = btn.find_element(By.XPATH, "./ancestor::td")
                    col_index = parent_td.get_attribute("aria-colindex")

                    header_elem = driver.find_element(By.XPATH,f"//td[@role='columnheader' and @aria-colindex='{col_index}']")
                    col_name = header_elem.text.strip()

                except:
                    col_name = f"Column {idx+1}"


                highlight_element(driver, btn)

                # Click
                try:
                    btn.click()
                except:
                    driver.execute_script("arguments[0].click();", btn)

                wait_for_loader_to_disappear(driver, wait)

                try:
                    no_task_elem = driver.find_element(By.XPATH, "//*[contains(text(),'No Task Found')]")

                    if no_task_elem.is_displayed():
                        print(f"⚠️ No Task Found for value {column_value} ({col_name})")

                        with allure.step(f"{col_name} → Validate ({column_value} vs No Task Found)"):

                            validation_msg = f"{col_name}: actual='{column_value}', expected='No Task Found'"

                            # ✅ Attach message
                            allure.attach(
                                validation_msg,
                                name="No Task Validation",
                                attachment_type=allure.attachment_type.TEXT
                            )

                            # ✅ Attach screenshot
                            allure.attach(
                                driver.get_screenshot_as_png(),
                                name=f"No Task Screenshot - {col_name}",
                                attachment_type=allure.attachment_type.PNG
                            )

                            print(f"❌ FAIL: {validation_msg}")

                            # 🔴 THIS makes step RED
                            raise AssertionError(validation_msg)

                except AssertionError:
                    driver.back()
                    wait_for_loader_to_disappear(driver, wait)
                    
                    continue

                
                try:
                    dashboard_title = wait.until(EC.presence_of_element_located((By.XPATH,"//p[contains(@class,'_dashboardHeaderTitleActive')]")))
                    highlight_element(driver, dashboard_title)
                    print(f"📊 Dashboard: {dashboard_title.text.strip()}")
                except:
                    print("⚠️ Dashboard title not found")
                # Select All
                try:
                    select_all = wait.until(EC.presence_of_element_located((By.XPATH,"//div[@role='checkbox' and @aria-label='Select all']//span")))
                    highlight_element(driver, select_all)
                    select_all.click()
                    time.sleep(2)
                    print("✅ Select All clicked")
                except Exception as e:
                    print(f"❌ Select All failed: {e}")
                    allure.attach(
                        driver.get_screenshot_as_png(),
                        name=f"Select All Failed - {col_name}",
                        attachment_type=allure.attachment_type.PNG
                    )

                    driver.back()
                    wait_for_loader_to_disappear(driver, wait)
                    continue

                # Get selected count
                selected_elem = wait.until(EC.presence_of_element_located((By.XPATH,"//div[contains(@class,'dx-item-content') and contains(.,'selected')]")))
                selected_text = selected_elem.text.strip()
                match = re.search(r'(\d+)', selected_text)
                selected_count = int(match.group(1)) if match else 0
            

                # ---------------- VALIDATION ----------------
                with allure.step(f"{col_name} → Validate ({column_value} vs {selected_count})"):

                    validation_msg = f"{col_name}: actual='{column_value}', expected='{selected_count}'"

                    allure.attach(validation_msg,name=f" Validation - {col_name}",attachment_type=allure.attachment_type.TEXT)

                    if column_value != selected_count:
                        failures.append(validation_msg)

                        allure.attach(driver.get_screenshot_as_png(),name=f"Screenshot - {col_name}",attachment_type=allure.attachment_type.PNG)

                        print(f"❌ FAIL: {validation_msg}")
                        raise AssertionError(validation_msg) 

                    else:
                        print(f"✅ PASS: {validation_msg}")

                driver.back()
                wait_for_loader_to_disappear(driver, wait)
                

            except AssertionError:
                driver.back()
                wait_for_loader_to_disappear(driver, wait)
                
                continue

            except Exception as e:
                print(f"⚠️ Error: {e}")
                continue
       
    processed_indexes = set()

    with allure.step("Total Counts Validation"):

        for idx in range(30):  # safe limit

            try:
                total_count_button = wait.until(EC.presence_of_all_elements_located((By.XPATH,"//td//div[normalize-space(text())!='' and number(normalize-space(text()))=number(normalize-space(text()))]")))

                if idx >= len(total_count_button):
                    break

                if idx in processed_indexes:
                    continue

                total_count_elem = total_count_button[idx]

                driver.execute_script(
                    "arguments[0].scrollIntoView({block:'center'});",
                    total_count_elem
                )
                time.sleep(0.5)

                total_count_text = total_count_elem.text.strip()

                if not total_count_text.isdigit():
                    continue

                column_value = int(total_count_text)

                if column_value == 0:
                    print(f"⚠️ Skipping 0 value at index {idx}")
                    continue

                # Column name
                try:
                    parent_td = total_count_elem.find_element(By.XPATH, "./ancestor::td")
                    col_index = parent_td.get_attribute("aria-colindex")

                    header_elem = driver.find_element(By.XPATH,f"//td[@role='columnheader' and @aria-colindex='{col_index}']")
                    col_name = header_elem.text.strip()

                except:
                    col_name = f"Column {idx+1}"

                highlight_element(driver, total_count_elem)

                # Click subtotal
                try:
                    total_count_elem.click()
                except:
                    driver.execute_script("arguments[0].click();", total_count_elem)

                processed_indexes.add(idx)

                wait_for_loader_to_disappear(driver, wait)
                time.sleep(1)

                try:
                    no_task_elem = driver.find_element(By.XPATH, "//*[contains(text(),'No Task Found')]")

                    if no_task_elem.is_displayed():
                        validation_msg = f"{col_name}: actual='{column_value}', expected='No Task Found'"

                        allure.attach(validation_msg, "No Task Validation", allure.attachment_type.TEXT)
                        allure.attach(driver.get_screenshot_as_png(),
                                    name=f"No Task Screenshot - {col_name}",
                                    attachment_type=allure.attachment_type.PNG)

                        print(f"❌ FAIL: {validation_msg}")
                        raise AssertionError(validation_msg)

                except AssertionError:
                    driver.back()
                    wait_for_loader_to_disappear(driver, wait)
                    
                    continue

                except Exception:
                    pass
                try:
                    dashboard_title_elem = wait.until(EC.presence_of_element_located((By.XPATH, "//p[contains(@class,'_dashboardHeaderTitleActive')]")))
                    highlight_element(driver, dashboard_title_elem)
                    print(f"✅ Dashboard title: {dashboard_title_elem.text.strip()}")
                except Exception as e:
                    print(f"⚠️ Could not fetch dashboard title: {e}")


                # Select all
                try:
                    select_all_elem = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@role='checkbox' and @aria-label='Select all']//span")))
                    highlight_element(driver, select_all_elem)
                    select_all_elem.click()
                    time.sleep(2)
                    print("✅ Clicked 'Select All'")
                except Exception as e:
                    print(f"❌ Select All failed: {e}")
                    allure.attach(
                        driver.get_screenshot_as_png(),
                        name=f"Select All Failed - {col_name}",
                        attachment_type=allure.attachment_type.PNG
                    )

                    driver.back()
                    wait_for_loader_to_disappear(driver, wait)
                    continue

                # Get selected count
                selected_elem = wait.until(EC.presence_of_element_located((By.XPATH,"//div[contains(@class,'dx-item-content') and contains(.,'selected')]")))
                selected_text = selected_elem.text.strip()
                match = re.search(r'(\d+)', selected_text)
                selected_count = int(match.group(1)) if match else 0

                # ---------------- VALIDATION ----------------
                with allure.step(f"{col_name} → Validate ({column_value} vs {selected_count})"):
                # ✅ VALIDATION
                    validation_msg = f"{col_name}: actual='{column_value}', expected='{selected_count}'"

                    allure.attach(validation_msg,
                                name=f"Subtotal Validation - {col_name}",
                                attachment_type=allure.attachment_type.TEXT)

                    if column_value != selected_count:
                        failures.append(validation_msg)

                        allure.attach(driver.get_screenshot_as_png(),
                                    name=f"Screenshot - {col_name}",
                                    attachment_type=allure.attachment_type.PNG)

                        print(f"❌ FAIL: {validation_msg}")
                        raise AssertionError(validation_msg)

                    else:
                        print(f"✅ PASS: {validation_msg}")
                
                # Back + reapply search
                driver.back()
                wait_for_loader_to_disappear(driver, wait)
               

            except AssertionError:
                driver.back()
                wait_for_loader_to_disappear(driver, wait)
                
                continue

            except Exception as e:
                print(f"⚠️ Subtotal error: {e}")
                continue

    # -----------------------------
    # FINAL RESULT
    # -----------------------------
    if failures:
        raise AssertionError(f"Test failed with {len(failures)} mismatches")

    print("🎯 All validations passed ✅")
    return True