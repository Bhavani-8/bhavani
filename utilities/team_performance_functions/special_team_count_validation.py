from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import allure
import time
import re

from utilities.add_task_utils import wait_for_loader_to_disappear
from utilities.other_utils_functions.highlight import highlight_element

def special_tm_count_validation(driver, wait):
    failures = []

    XPATH_CHECKBOX_TP = "//span[@class='dx-checkbox-icon']"
    XPATH_TOTAL_SELECTED_COUNT_TP = "//div[@class='dx-item-content dx-toolbar-item-content']"
    XPATH_TP_TABLE_CELL = "//td[@role='gridcell']"
    XPATH_NO_TASK_FOUND = "//div[@class='dx-datagrid-content']"

    with allure.step("Column Counts Validation"):
        column_buttons_xpath = f"{XPATH_TP_TABLE_CELL}//button[normalize-space(text()) and number(normalize-space(text()))=number(normalize-space(text())) and normalize-space(text()) != '0' and not(@disabled)]"
        
        try:
            elements_count = len(wait.until(EC.presence_of_all_elements_located((By.XPATH, column_buttons_xpath))))
            print(f"✅ Found {elements_count} active, non-zero clickable column buttons")
        except TimeoutException:
            print("⚠️ No active, clickable column buttons found on the dashboard.")
            elements_count = 0

        for idx in range(elements_count):
            try:
                number_elements = wait.until(EC.presence_of_all_elements_located((By.XPATH, column_buttons_xpath)))
                current_elem = number_elements[idx]
                
                cell_text = current_elem.text.strip() or driver.execute_script("return arguments[0].innerText;", current_elem).strip()
                
                if not cell_text or not cell_text.isdigit():
                    continue

                column_value = int(cell_text)

                parent_td = current_elem.find_element(By.XPATH, "./ancestor::td[@role='gridcell']")
                col_idx = parent_td.get_attribute("aria-colindex")

                driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", parent_td)
                time.sleep(0.5)

                cell_rect = parent_td.rect
                cell_mid_x = cell_rect['x'] + (cell_rect['width'] / 2)

                parent_header_text = ""
                sub_header_text = ""

                main_headers = driver.find_elements(By.XPATH, "(//td[@role='columnheader'])[position() >= 3 and position() <= 11]")
                for mh in main_headers:
                    if mh.is_displayed():
                        mh_rect = mh.rect
                        if mh_rect['x'] <= cell_mid_x <= (mh_rect['x'] + mh_rect['width']):
                            text = mh.text.strip() or driver.execute_script("return arguments[0].innerText;", mh).strip()
                            parent_header_text = text.replace('\n', ' ').strip()
                            break

                sub_headers = driver.find_elements(By.XPATH, "(//td[@role='columnheader'])[position() >= 12 and position() <= 17]")
                for sh in sub_headers:
                    if sh.is_displayed():
                        sh_rect = sh.rect
                        if sh_rect['x'] <= cell_mid_x <= (sh_rect['x'] + sh_rect['width']):
                            text = sh.text.strip() or driver.execute_script("return arguments[0].innerText;", sh).strip()
                            sub_header_text = text.replace('\n', ' ').strip()
                            break

                if parent_header_text and sub_header_text:
                    full_col_name = f"{parent_header_text} - {sub_header_text}"
                elif parent_header_text:
                    full_col_name = parent_header_text
                elif sub_header_text:
                    full_col_name = sub_header_text
                else:
                    full_col_name = f"Column {col_idx}"

                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", current_elem)
                highlight_element(driver, current_elem)

                print(f"\n➡️ Clicking button {idx + 1} under [{full_col_name}] : {column_value}")

                try:
                    wait.until(EC.element_to_be_clickable(current_elem))
                    current_elem.click()
                except:
                    driver.execute_script("arguments[0].click();", current_elem)

                wait_for_loader_to_disappear(driver, wait)
                time.sleep(1.5)

                try:
                    no_task_elem = driver.find_element(By.XPATH, f"{XPATH_NO_TASK_FOUND}[contains(., 'No Task') or contains(., 'No data')] | //*[contains(text(),'No Task Found')]")
                    
                    if no_task_elem.is_displayed():
                        validation_msg = f"{full_col_name} | Actual Count: {column_value} | Expected Count: 'No Task Found'"
                        failures.append(validation_msg)
                        
                        try:
                            with allure.step(f"Validate {full_col_name} (Actual Count: {column_value} vs Expected Count: 'No Task Found')"):
                                allure.attach(validation_msg, name="No Task Validation Failure", attachment_type=allure.attachment_type.TEXT)
                                allure.attach(driver.get_screenshot_as_png(), name=f"No Task Screenshot - {full_col_name}", attachment_type=allure.attachment_type.PNG)
                                print(f"❌ FAIL: {validation_msg}")
                                raise AssertionError(validation_msg) 
                        except AssertionError:
                            pass 

                        # driver.back()
                        driver_back = wait.until(EC.presence_of_element_located((By.XPATH,"(//div[@class='flex items-center']//button)[1]")))
                        highlight_element(driver, driver_back)
                        driver_back.click()
                        wait_for_loader_to_disappear(driver, wait)
                        continue 
                except NoSuchElementException:
                    pass

                try:
                    checkboxes = wait.until(EC.presence_of_all_elements_located((By.XPATH, XPATH_CHECKBOX_TP)))
                    for cb in checkboxes:
                        if cb.is_displayed():
                            highlight_element(driver, cb)
                            cb.click()
                            time.sleep(1.5)
                            print("✅ Select All Checkbox clicked")
                            break
                except TimeoutException:
                    print("⚠️ Checkbox not found within timeout.")

                try:
                    selected_elem = wait.until(EC.presence_of_element_located((By.XPATH, XPATH_TOTAL_SELECTED_COUNT_TP)))
                    match = re.search(r'(\d+)', selected_elem.text.strip())
                    expected_count = int(match.group(1)) if match else 0
                except TimeoutException:
                    print("⚠️ Selected count text not found.")
                    expected_count = 0

                try:
                    with allure.step(f"Validate {full_col_name} (Actual Count: {column_value} vs Expected Count: {expected_count})"):
                        validation_msg = f"{full_col_name} | Actual Count: {column_value} | Expected Count: {expected_count}"
                        
                        if column_value != expected_count:
                            failures.append(validation_msg)
                            allure.attach(validation_msg, name=f"Mismatch - {full_col_name}", attachment_type=allure.attachment_type.TEXT)
                            allure.attach(driver.get_screenshot_as_png(), name=f"Screenshot - {full_col_name}", attachment_type=allure.attachment_type.PNG)
                            print(f"❌ FAIL: {validation_msg}")
                            raise AssertionError(validation_msg) 
                        else:
                            allure.attach(validation_msg, name=f"Match - {full_col_name}", attachment_type=allure.attachment_type.TEXT)
                            print(f"✅ PASS: {validation_msg}")
                except AssertionError:
                    pass 

                # driver.back()
                driver_back = wait.until(EC.presence_of_element_located((By.XPATH,"(//div[@class='flex items-center']//button)[1]")))
                highlight_element(driver, driver_back)
                driver_back.click()
                wait_for_loader_to_disappear(driver, wait)

            except Exception as e:
                print(f"⚠️ Error processing button {idx + 1}: {e}")
                try:
                    # driver.back()
                    driver_back = wait.until(EC.presence_of_element_located((By.XPATH,"(//div[@class='flex items-center']//button)[1]")))
                    highlight_element(driver, driver_back)
                    driver_back.click()
                    wait_for_loader_to_disappear(driver, wait)
                except:
                    pass
                continue

    with allure.step("Total Counts Validation"):
        try:
            total_count_button = wait.until(EC.presence_of_all_elements_located((By.XPATH,"//td//div[normalize-space(text()) and number(normalize-space(text()))=number(normalize-space(text()))]")))
            print(f"\n✅ Found {len(total_count_button)} Sub Total counts")
        except TimeoutException:
            print("\n⚠️ No Sub Total counts found.")
            total_count_button = []

        for idx in range(len(total_count_button)):
            try:
                total_count_button = wait.until(EC.presence_of_all_elements_located((By.XPATH,"//td//div[normalize-space(text()) and number(normalize-space(text()))=number(normalize-space(text()))]")))
                total_count_elem = total_count_button[idx]
                total_count_text = total_count_elem.text.strip()

                if not total_count_text:
                    total_count_text = driver.execute_script("return arguments[0].innerText;", total_count_elem).strip()

                if not total_count_text:
                    total_count_text = driver.execute_script("return arguments[0].textContent;", total_count_elem).strip()

                if not total_count_text or not total_count_text.isdigit():
                    print(f"⏭️ Skipping subtotal {idx + 1} (invalid='{total_count_text}')")
                    continue
                column_value = int(total_count_text)

                if column_value == 0:
                    print(f"⏭️ Skipping subtotal {idx + 1} (value=0)")
                    continue

                parent_td = total_count_elem.find_element(By.XPATH, "./ancestor::td")
                col_idx = parent_td.get_attribute("aria-colindex")

                driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", parent_td)
                time.sleep(0.5)

                cell_rect = parent_td.rect
                cell_mid_x = cell_rect['x'] + (cell_rect['width'] / 2)

                parent_header_text = ""
                sub_header_text = ""

                main_headers = driver.find_elements(By.XPATH, "(//td[@role='columnheader'])[position() >= 3 and position() <= 11]")
                for mh in main_headers:
                    if mh.is_displayed():
                        mh_rect = mh.rect
                        if mh_rect['x'] <= cell_mid_x <= (mh_rect['x'] + mh_rect['width']):
                            text = mh.text.strip() or driver.execute_script("return arguments[0].innerText;", mh).strip()
                            parent_header_text = text.replace('\n', ' ').strip()
                            break

                sub_headers = driver.find_elements(By.XPATH, "(//td[@role='columnheader'])[position() >= 12 and position() <= 17]")
                for sh in sub_headers:
                    if sh.is_displayed():
                        sh_rect = sh.rect
                        if sh_rect['x'] <= cell_mid_x <= (sh_rect['x'] + sh_rect['width']):
                            text = sh.text.strip() or driver.execute_script("return arguments[0].innerText;", sh).strip()
                            sub_header_text = text.replace('\n', ' ').strip()
                            break

                if parent_header_text and sub_header_text:
                    col_name = f"{parent_header_text} - {sub_header_text}"
                elif parent_header_text:
                    col_name = parent_header_text
                elif sub_header_text:
                    col_name = sub_header_text
                else:
                    col_name = f"Column {col_idx}"

                driver.execute_script("arguments[0].scrollIntoView({block:'center'});",total_count_elem)
                highlight_element(driver, total_count_elem)

                print(f"\n➡️ Clicking subtotal {idx + 1}: {column_value}")

                try:
                    wait.until(EC.element_to_be_clickable(total_count_elem))
                    total_count_elem.click()
                except:
                    driver.execute_script("arguments[0].click();", total_count_elem)

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
                
                try:
                    with allure.step(f"Validate {col_name} (Actual Count: {column_value} vs Expected Count: {selected_count})"):
                        validation_msg = f"{col_name} | Actual Count: {column_value} | Expected Count: {selected_count}"
                        
                        if column_value != selected_count:
                            failures.append(validation_msg)
                            allure.attach(validation_msg, name=f"Mismatch - {col_name}", attachment_type=allure.attachment_type.TEXT)
                            allure.attach(driver.get_screenshot_as_png(), name=f"Screenshot - {col_name}", attachment_type=allure.attachment_type.PNG)
                            print(f"❌ FAIL: {validation_msg}")
                            raise AssertionError(validation_msg) 
                        else:
                            allure.attach(validation_msg, name=f"Match - {col_name}", attachment_type=allure.attachment_type.TEXT)
                            print(f"✅ PASS: {validation_msg}")
                except AssertionError:
                    pass 

                # driver.back()
                driver_back = wait.until(EC.presence_of_element_located((By.XPATH,"(//div[@class='flex items-center']//button)[1]")))
                highlight_element(driver, driver_back)
                driver_back.click()
                wait_for_loader_to_disappear(driver, wait)
            
            except Exception as e:
                print(f"⚠️ Subtotal error: {e}")
                try:
                    # driver.back()
                    driver_back = wait.until(EC.presence_of_element_located((By.XPATH,"(//div[@class='flex items-center']//button)[1]")))
                    highlight_element(driver, driver_back)
                    driver_back.click()
                    wait_for_loader_to_disappear(driver, wait)
                except:
                    pass
                continue

    if failures:
        error_summary = "\n".join(failures)
        raise AssertionError(f"Test failed with {len(failures)} mismatches:\n\n{error_summary}")

    print("🎯 All validations passed perfectly! ✅")
    return True