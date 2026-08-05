import allure
import time
import re
import os
import json
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from utilities.other_utils_functions.highlight import highlight_element
from utilities.add_task_utils import wait_for_loader_to_disappear

def apply_search(driver, wait, username):
    try:
        search_box = wait.until(EC.presence_of_element_located(
            (By.XPATH, "//input[contains(@class,'dx-texteditor-input') and @type='text']")
        ))
        highlight_element(driver, search_box)

        search_box.click()
        search_box.clear()
        search_box.send_keys(username)

        wait_for_loader_to_disappear(driver, wait)
        time.sleep(1)

        print(f"🔁 Re-applied search: {username}")

    except Exception as e:
        print(f"⚠️ Failed to re-apply search: {e}")


# -----------------------------
# 🔥 MAIN FUNCTION
# -----------------------------
def special_search_validation(driver, wait):

    failures = []

    # -----------------------------
    # Load locators
    # -----------------------------
    try:
        with open(os.path.join("data", 'locators.json'), 'r') as f:
            elements_details = json.load(f)

        dashboard_icon = elements_details['dashboard_icon']
        special_task_icon = elements_details['special_task_icon']
        team_performance_btn = elements_details['team_performance_btn']

        print("✅ locators.json loaded successfully")

    except Exception as e:
        allure.attach(str(e), name="Locators Load Error",
                      attachment_type=allure.attachment_type.TEXT)
        return False

    # -----------------------------
    # Open Dashboard
    # -----------------------------
    dashboard_icon_elem = wait.until(
        EC.element_to_be_clickable((By.XPATH, dashboard_icon)))
    highlight_element(driver, dashboard_icon_elem)
    dashboard_icon_elem.click()
    print("✅ Dashboard icon clicked")

    # -----------------------------
    # Get Username (ONLY ONCE)
    # -----------------------------
    with allure.step("👤 Reading User Title"):
        user_title_elem = wait.until(
            EC.presence_of_element_located((By.XPATH, "//div[@class='user-title']"))
        )
        highlight_element(driver, user_title_elem)

        username = user_title_elem.text.strip()
        username = (username.replace('Hi', '')
                              .replace('Hello', '')
                              .replace(',', '')
                              .replace(';', '')
                              .strip())
        username = " ".join(username.split())

        print(f"✅ Username: {username}")
        allure.attach(username, "Logged-in Username",
                      allure.attachment_type.TEXT)

    # -----------------------------
    # Open Team Performance
    # -----------------------------
    with allure.step("Open Special Task Dashboard → Special Team Performance"):
        try:
            print("📍 Opening Special Task Dashboard...")
            special_task_icon_elem = wait.until(EC.element_to_be_clickable((By.XPATH, special_task_icon)))
            highlight_element(driver, special_task_icon_elem)
            special_task_icon_elem.click()
            print("✅ Special Task Dashboard icon clicked")

            wait_for_loader_to_disappear(driver, wait)
            special_team_perf_elem = wait.until(EC.element_to_be_clickable((By.XPATH, team_performance_btn)))
            highlight_element(driver, special_team_perf_elem)
            special_team_perf_elem.click()
            print("✅ Special Team Performance clicked")
            wait_for_loader_to_disappear(driver, wait)
        except Exception as e:
            allure.attach(str(e), name="Dashboard Open Error", attachment_type=allure.attachment_type.TEXT)
            return False

    apply_search(driver, wait, username)

    with allure.step("Column Counts Validation"):
        column_buttons = wait.until(EC.presence_of_all_elements_located((By.XPATH,"//button[normalize-space(text()) and number(normalize-space(text()))=number(normalize-space(text()))]")))
        print(f"✅ Found {len(column_buttons)} column buttons")
        for idx in range(len(column_buttons)):


            try:
                # 🔁 Re-fetch elements (avoid stale)
                column_buttons = wait.until(EC.presence_of_all_elements_located((By.XPATH,"//button[normalize-space(text()) and number(normalize-space(text()))=number(normalize-space(text()))]")))

                column_button_elem = column_buttons[idx]
                column_text = column_button_elem.text.strip()

                if not column_text:
                    column_text = driver.execute_script("return arguments[0].innerText;", column_button_elem).strip()

                if not column_text:
                    column_text = driver.execute_script("return arguments[0].textContent;", column_button_elem).strip()

                # 🚨 VALIDATE TEXT
                if not column_text or not column_text.isdigit():
                    print(f"⏭️ Skipping button {idx + 1} (invalid='{column_text}')")
                    continue

                
                column_value = int(column_text)

                # ✅ Skip ZERO
                if column_value == "0":
                    print(f"⏭️ Skipping button {idx + 1} (value = 0)")
                    continue

                # ✅ Skip Disabled
                if column_button_elem.get_attribute("disabled") or \
                    "disabled" in (column_button_elem.get_attribute("class") or "").lower():
                    print(f"⏭️ Skipping disabled button at index {idx + 1}")
                    continue

                # with allure.step(f"Click button (value = {numeric_value})"):
                # ✅ Get column name using index
                parent_td = column_button_elem.find_element(By.XPATH, "./ancestor::td")
                col_idx = parent_td.get_attribute("aria-colindex")

                header_cells = driver.find_elements(By.XPATH, f"//td[@role='columnheader'][@aria-colindex='{col_idx}']")
                # Combine text from parent and child (e.g., "Completed" + "Complied")
                col_name = " ".join([h.text.strip().lower() for h in header_cells if h.text.strip()]).replace("\n", " ")
                if not col_name: col_name = f"Column {col_idx}"

                    
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", column_button_elem)
                highlight_element(driver, column_button_elem)

                print(f"\n➡️ Clicking button {idx + 1}: {column_value}")

                    # ✅ Click
                try:
                    wait.until(EC.element_to_be_clickable(column_button_elem))
                    column_button_elem.click()
                except Exception:
                    driver.execute_script("arguments[0].click();", column_button_elem)

                wait_for_loader_to_disappear(driver, wait)
                time.sleep(1)
                try:
                    no_task_elem = driver.find_element(By.XPATH, "//*[contains(text(),'No Task Found')]")

                    if no_task_elem.is_displayed():
                        print(f"⚠️ No Task Found for value {column_value} ({col_name})")

                        with allure.step(f"{col_name} → Validate ({column_value} vs No Task Found)"):

                            validation_msg = f"{col_name}: actual='{column_value}', expected='No Task Found'"
                            allure.attach(validation_msg,name="No Task Validation",attachment_type=allure.attachment_type.TEXT)

                            allure.attach(driver.get_screenshot_as_png(),name=f"No Task Screenshot - {col_name}",attachment_type=allure.attachment_type.PNG)
                            print(f"❌ FAIL: {validation_msg}")
                            raise AssertionError(validation_msg)

                except AssertionError:
                    driver.back()
                    wait_for_loader_to_disappear(driver, wait)
                    apply_search(driver, wait, username)
                    continue
                try:
                    dashboard_title_elem = wait.until(EC.presence_of_element_located((By.XPATH,"//p[contains(@class,'_dashboardHeaderTitleActive')]")))
                    highlight_element(driver, dashboard_title_elem)
                    print(f"✅ Dashboard title: {dashboard_title_elem.text.strip()}")
                except Exception:
                    print("⚠️ Dashboard title not found")

                try:
                    select_all = wait.until(EC.presence_of_element_located((By.XPATH,"//div[@role='checkbox' and @aria-label='Select all']//span")))
                    highlight_element(driver, select_all)
                    select_all.click()
                    time.sleep(2)
                    print("✅ Select All clicked")
                except Exception as e:
                    print(f"⚠️ Select All failed: {e}")


               
                selected_elem = wait.until(EC.presence_of_element_located((By.XPATH,"//div[contains(@class,'dx-item-content') and contains(.,'selected')]")))
                selected_text = selected_elem.text.strip()
                match = re.search(r'(\d+)', selected_text)
                selected_count = int(match.group(1)) if match else 0
            

                
                with allure.step(f"{col_name} → Validate ({column_value} vs {selected_count})"):
                    # ✅ VALIDATION
                    validation_msg = f"{col_name}: actual='{column_value}', expected='{selected_count}'"

                    allure.attach(validation_msg,name=f" Validation - {col_name}",attachment_type=allure.attachment_type.TEXT)

                    if column_value != selected_count:
                        failures.append(validation_msg)

                        allure.attach(driver.get_screenshot_as_png(),name=f"Screenshot - {col_name}",attachment_type=allure.attachment_type.PNG)

                        print(f"❌ FAIL: {validation_msg}")
                        raise AssertionError(validation_msg)

                    else:
                        print(f"✅ PASS: {validation_msg}")

                    # ✅ Back
                driver.back()
                wait_for_loader_to_disappear(driver, wait)
                apply_search(driver, wait, username)

            except AssertionError:
                driver.back()
                wait_for_loader_to_disappear(driver, wait)
                apply_search(driver, wait, username)
                continue

            except Exception as e:
                print(f"⚠️ Error: {e}")
                continue
    with allure.step("Total Counts Validation"):

        total_count_button = wait.until(EC.presence_of_all_elements_located((
            By.XPATH,
            "//td//div[normalize-space(text()) and number(normalize-space(text()))=number(normalize-space(text()))]"
        )))

        print(f"\n✅ Found {len(total_count_button)} Sub Total counts")

        for idx in range(len(total_count_button)):

            try:
                # 🔁 Re-fetch (avoid stale)
                total_count_button = wait.until(EC.presence_of_all_elements_located((
                    By.XPATH,
                    "//td//div[normalize-space(text()) and number(normalize-space(text()))=number(normalize-space(text()))]"
                )))

                total_count_elem = total_count_button[idx]

                # 🔥 Get text FIRST (string)
                total_count_text = total_count_elem.text.strip()

                if not total_count_text:
                    total_count_text = driver.execute_script("return arguments[0].innerText;", total_count_elem).strip()

                if not total_count_text:
                    total_count_text = driver.execute_script("return arguments[0].textContent;", total_count_elem).strip()

                # 🚨 Validate
                if not total_count_text or not total_count_text.isdigit():
                    print(f"⏭️ Skipping subtotal {idx + 1} (invalid='{total_count_text}')")
                    continue

                # ✅ Convert AFTER validation
                column_value = int(total_count_text)

                if column_value == 0:
                    print(f"⏭️ Skipping subtotal {idx + 1} (value=0)")
                    continue

                # ✅ Column name
                parent_td = total_count_elem.find_element(By.XPATH, "./ancestor::td")
                col_idx = parent_td.get_attribute("aria-colindex")

                header_cells = driver.find_elements(
                    By.XPATH,
                    f"//td[@role='columnheader'][@aria-colindex='{col_idx}']"
                )

                col_name = " ".join([
                    h.text.strip().lower()
                    for h in header_cells if h.text.strip()
                ]).replace("\n", " ")

                if not col_name:
                    col_name = f"Column {col_idx}"

                # ✅ Scroll + highlight
                driver.execute_script(
                    "arguments[0].scrollIntoView({block:'center'});",
                    total_count_elem
                )
                highlight_element(driver, total_count_elem)

                print(f"\n➡️ Clicking subtotal {idx + 1}: {column_value}")

                # ✅ Click
                try:
                    wait.until(EC.element_to_be_clickable(total_count_elem))
                    total_count_elem.click()
                except:
                    driver.execute_script("arguments[0].click();", total_count_elem)

                wait_for_loader_to_disappear(driver, wait)
                time.sleep(1)

                # ✅ No Task Found
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
                    apply_search(driver, wait, username)
                    continue
                try:
                    dashboard_title_elem = wait.until(EC.presence_of_element_located((By.XPATH,"//p[contains(@class,'_dashboardHeaderTitleActive')]")))
                    highlight_element(driver, dashboard_title_elem)
                    print(f"✅ Dashboard title: {dashboard_title_elem.text.strip()}")
                except Exception:
                    print("⚠️ Dashboard title not found")
                try:
                    select_all = wait.until(EC.presence_of_element_located((By.XPATH,"//div[@role='checkbox' and @aria-label='Select all']//span")))
                    highlight_element(driver, select_all)
                    select_all.click()
                    time.sleep(2)
                    print("✅ Select All clicked")
                except Exception as e:
                    print(f"⚠️ Select All failed: {e}")
                # ✅ Get selected count
                selected_elem = wait.until(EC.presence_of_element_located((
                    By.XPATH, "//div[contains(@class,'dx-item-content') and contains(.,'selected')]"
                )))

                selected_text = selected_elem.text.strip()
                match = re.search(r'(\d+)', selected_text)
                selected_count = int(match.group(1)) if match else 0
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

                # 🔙 Back
                driver.back()
                wait_for_loader_to_disappear(driver, wait)
                apply_search(driver, wait, username)

            except AssertionError:
                driver.back()
                wait_for_loader_to_disappear(driver, wait)
                apply_search(driver, wait, username)
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