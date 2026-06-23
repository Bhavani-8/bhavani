

import os
import allure
import json
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from utilities.add_task_utils import wait_for_loader_to_disappear
from utilities.other_utils_functions.highlight import highlight_element
import pyautogui as pg



def lower_dashboard_validation(driver, wait):

    with open(os.path.join("data", 'locators.json'), 'r') as f:
        elements_details = json.load(f)
        dash_approval_pending_btn = elements_details['dash_approval_pending_btn']
        dash_rejected_task_btn = elements_details['dash_rejected_task_btn']
        dash_completed_btn = elements_details['dash_completed_btn']
        dash_title_label = elements_details['dash_title_label']
        dash_others_value_selector_template = elements_details['dash_others_value_selector_template']
        dash_value_validator_template = elements_details['dash_value_validator_template']
        dash_select_all_checkbox = elements_details['dash_select_all_checkbox']
        dash_in_time = elements_details['dash_in_time']
        dash_not_in_time = elements_details['dash_not_in_time']

    with allure.step("Loading locators from JSON"):
        with open(os.path.join("data", "locators.json"), "r") as f:
            elements_details = json.load(f)

        print("✅ Locators loaded successfully")

    dash_buttons_others = {
            'Approval Pending': dash_approval_pending_btn,
            'Rejected Tasks': dash_rejected_task_btn,
            'Completed': dash_completed_btn,
            'In Time': dash_in_time,
            'Not In Time': dash_not_in_time
        }


    titles_map = {
        'Approval Pending': ['Approval Pending by Me', 'Approval Pending by Others', 'CC', 'All'],
        'Rejected Tasks': ['Assigned To Me', 'Assigned To Others', 'CC', 'All'],
        'Completed': ['Completed By Me', 'Completed By Others', 'CC', 'All'],
        'In Time': ['Completed By Me', 'Completed By Others', 'CC', 'All'],
        'Not In Time': ['Completed By Me', 'Completed By Others', 'CC', 'All']
    }

    wait_for_loader_to_disappear(driver, wait)

    validation_failures = []

    for idx, (btn_name, btn_path) in enumerate(dash_buttons_others.items()):

        if btn_name == 'In Time':
            expand_btn = wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//button[@title='Completed']/following-sibling::button")
                )
            )
            driver.execute_script("arguments[0].click();", expand_btn)
            time.sleep(2)

    

        btn_elem = wait.until(EC.presence_of_element_located((By.XPATH, btn_path)))
        highlight_element(driver,btn_elem,duration=0.5)
        btn_elem.click()
        print()
        print(f"📊 {btn_name} button clicked.")
        time.sleep(2)

        wait_for_loader_to_disappear(driver, wait)

        dash_title_label_elem = wait.until(EC.presence_of_element_located((By.XPATH, dash_title_label)))
        title_text = dash_title_label_elem.text.strip()
        print(f"Button title fetched: {title_text}")

        dash_others_value_selector = (dash_others_value_selector_template.replace('{title}', btn_name))
        dash_others_value_selector_elem = wait.until(EC.presence_of_all_elements_located((By.XPATH, dash_others_value_selector)))
    
    
        # for i, (elem, title) in enumerate(zip(dash_others_value_selector_elem, titles[idx]), start=1):
        for i, (elem, title) in enumerate(zip(dash_others_value_selector_elem, titles_map[btn_name]), start=1):
            actual_value = 0
            expected_value = 0

            try:
                
                dash_value_validator = dash_value_validator_template.replace('{title}', title)
                dash_value_validator_elem = wait.until(EC.presence_of_element_located((By.XPATH, dash_value_validator)))
                
                # value_elem = dash_value_validator_elem[idx]
                actual_value = int(dash_value_validator_elem.text.replace(",", "").strip() or 0)
                with allure.step(f"Validating '{title}' in '{btn_name}' "f"(Dashboard Count: {actual_value})"):
                    highlight_element(driver, dash_value_validator_elem, duration=0.2)
                    driver.execute_script("arguments[0].click();",dash_value_validator_elem)

                    time.sleep(2)


                    wait_for_loader_to_disappear(driver, wait)

                    no_task_elements = driver.find_elements(
                    By.XPATH,
                    "//*[contains(text(),'No Task Found')]"
                )

                    if no_task_elements and no_task_elements[0].is_displayed():

                        if actual_value > 0:

                            error_msg = (
                                f"❌ {btn_name} - {title} - "
                                f"Dashboard Count: {actual_value} "
                                f"but page shows 'No Task Found'"
                            )

                            validation_failures.append(error_msg)

                            print(error_msg)

                            allure.attach(
                                error_msg,
                                name=f"{btn_name}-{title}-NoTaskFound",
                                attachment_type=allure.attachment_type.TEXT
                            )

                            allure.attach(
                                driver.get_screenshot_as_png(),
                                name=f"{btn_name}-{title}-NoTaskFound-Screenshot",
                                attachment_type=allure.attachment_type.PNG
                            )

                            raise AssertionError(error_msg)

                        else:

                            print(
                                f"✅ {btn_name} - {title} - "
                                f"No Task Found (0)"
                            )

                            continue

                    if actual_value == 0:
                        print(f"✅ {btn_name} - {title} - No data found (0)")
                        continue
                    select_all_elem = wait.until(EC.presence_of_element_located((By.XPATH, dash_select_all_checkbox)))
                    driver.execute_script("arguments[0].click();", select_all_elem)
                    time.sleep(3)
                    wait_for_loader_to_disappear(driver, wait)

                    selected_count_elem = wait.until(EC.presence_of_element_located((By.XPATH,'//div[contains(text(),"selected")]')))
                    highlight_element(driver,selected_count_elem,duration=0.2)
                    selected_text = selected_count_elem.text.strip()
                    expected_value = int(selected_text.replace(",", "").split()[0])
                    
                    # Output
                    if actual_value != expected_value:
                        error_msg = (f"❌ {btn_name} - {title} - Select all - mismatch (Actual: {actual_value}, Expected: {expected_value})")
                        validation_failures.append(error_msg)
                        allure.attach(error_msg,name=f"{btn_name}-{title}-Mismatch",attachment_type=allure.attachment_type.TEXT)
                        allure.attach(driver.get_screenshot_as_png(),name=f"{btn_name}-{title}-Screenshot",attachment_type=allure.attachment_type.PNG)
                        print(f"{error_msg} ")
                        raise AssertionError(error_msg)
                    else:
                        
                        print(f"✅ {btn_name} - {title} - Select all - matched ({actual_value})")
                        allure.attach((f"{btn_name} - {title}\n\n"f"Actual Count   : {actual_value}\n"f"Expected Count : {expected_value}\n"f"Status: MATCHED"),
                        name=f"{btn_name}-{title}-Matched",
                        attachment_type=allure.attachment_type.TEXT)
            except AssertionError:
                pass

            except Exception as e:

                error_msg = (
                    f"{btn_name} - {title} validation failed: {e}"
                )

                validation_failures.append(error_msg)

                print(f"❌ {error_msg}")

                allure.attach(
                    str(error_msg),
                    name=f"{btn_name}-{title}-Error", attachment_type=allure.attachment_type.TEXT
        )             


    
        total_value = 0

        for elem in dash_others_value_selector_elem[:3]:

            value = int(elem.text.replace(",", "").strip() or 0)

            total_value += value

        dash_sum_value_validator = (dash_value_validator_template.replace('{title}','All'))

        all_elem = wait.until(EC.presence_of_element_located((By.XPATH, dash_sum_value_validator)))
        dashboard_total = int(all_elem.text.replace(",", "").strip() or 0)
        try:
            with allure.step(f"Validating Total in '{btn_name}' "f"(Dashboard Total: {dashboard_total})"):
                highlight_element(driver,all_elem,duration=0.2)

                driver.execute_script("arguments[0].click();",all_elem)

                time.sleep(2)

                wait_for_loader_to_disappear(driver, wait)

                no_task_elements = driver.find_elements(
                By.XPATH,
                "//*[contains(text(),'No Task Found')]"
            )

                if no_task_elements and no_task_elements[0].is_displayed():

                    if actual_value > 0:

                        error_msg = (
                            f"❌ {btn_name} - {title} - "
                            f"Dashboard Count: {actual_value} "
                            f"but page shows 'No Task Found'"
                        )

                        validation_failures.append(error_msg)

                        print(error_msg)

                        allure.attach(
                            error_msg,
                            name=f"{btn_name}-{title}-NoTaskFound",
                            attachment_type=allure.attachment_type.TEXT
                        )

                        allure.attach(
                            driver.get_screenshot_as_png(),
                            name=f"{btn_name}-{title}-NoTaskFound-Screenshot",
                            attachment_type=allure.attachment_type.PNG
                        )

                        raise AssertionError(error_msg)

                    else:

                        print(
                        f"✅ {btn_name} - {title} - "
                        f"No Task Found (0)"
                    )

                    continue
                if total_value == 0:

                    print(f"✅ {btn_name} - Total "f"- No data found (0)")
                    continue
                select_all_elem = wait.until(EC.presence_of_element_located((By.XPATH, dash_select_all_checkbox)))

                highlight_element(driver,select_all_elem,duration=0.2)

                driver.execute_script("arguments[0].click();",select_all_elem)
                time.sleep(3)

                wait_for_loader_to_disappear(driver, wait)

                selected_count_elem = wait.until(EC.presence_of_element_located((By.XPATH,'//div[contains(text(),"selected")]')))

                highlight_element(driver,selected_count_elem,duration=0.2)
                selected_text = selected_count_elem.text.strip()

                expected_count = int(selected_text.replace(",", "").split()[0])

                if dashboard_total != expected_count:
                    error_msg = (f"❌ {btn_name} - Total mismatch "f"(Dashboard: {dashboard_total}, "f"Selected: {expected_count})")
                    
                    validation_failures.append(error_msg)
                    allure.attach(error_msg,name=f"{btn_name}-Total-Mismatch",attachment_type=allure.attachment_type.TEXT)
                    allure.attach(driver.get_screenshot_as_png(),name=f"{btn_name}-{title}-Screenshot",attachment_type=allure.attachment_type.PNG)
                    print(f"{error_msg}")
                    raise AssertionError(error_msg)
                    
                else:
                    print(f"✅ {btn_name} - Total "f"- Select all - matched "f"({dashboard_total})")
                    allure.attach((f"{btn_name} - Total\n\n"f"Dashboard Total : {dashboard_total}\n"f"Selected Count  : {expected_count}\n"f"Status          : MATCHED"),
                    name=f"{btn_name}-Total-Matched",
                    attachment_type=allure.attachment_type.TEXT)
                   
        except AssertionError:
            pass
        except Exception as e:

            error_msg = (
                f"{btn_name} - Total validation failed: {e}"
            )

            validation_failures.append(error_msg)

            print(f"❌ {error_msg}")

            allure.attach(
                str(error_msg),
                name=f"{btn_name}-Total-Error", attachment_type=allure.attachment_type.TEXT
    )
                
        
        
    if validation_failures:

        final_error = "\n".join(validation_failures)

        raise AssertionError(f"\n\nLower Dashboard Validation Failed:\n{final_error}")

    print("✅ Lower Dashboard validation successful")

    return True



