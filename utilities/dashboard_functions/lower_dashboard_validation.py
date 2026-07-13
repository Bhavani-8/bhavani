

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
            expand_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@title='Completed']/following-sibling::button")))
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
    
        # actual_value = int(dash_others_value_selector_elem.text.replace(",", "").strip() or 0)
        # for i, (elem, title) in enumerate(zip(dash_others_value_selector_elem, titles[idx]), start=1):
        for i, (elem, title) in enumerate(zip(dash_others_value_selector_elem, titles_map[btn_name]), start=1):
            actual_value = int(elem.text.replace(",", "").strip() or 0)
            expected_value = 0
            selected_count = None


            try:
                
                dash_value_validator = dash_value_validator_template.replace('{title}', title)
                dash_value_validator_elem = wait.until(EC.presence_of_element_located((By.XPATH, dash_value_validator)))
                
                # value_elem = dash_value_validator_elem[idx]
                expected_value = int(dash_value_validator_elem.text.replace(",", "").strip() or 0)
                with allure.step(f"Validating '{title}' in '{btn_name}' "f"(Dashboard Count: {actual_value})"):
                    highlight_element(driver, dash_value_validator_elem, duration=0.2)
                    driver.execute_script("arguments[0].click();",dash_value_validator_elem)

                    time.sleep(2)


                    wait_for_loader_to_disappear(driver, wait)

                    if actual_value == 0 and expected_value == 0:
                        success_msg = (
                            f"✅ {btn_name} - {title} - "
                            f"Dashboard Count : {actual_value}, "
                            f"Header Count : {expected_value}, "
                            f"Select All Count : No Tasks"
                        )
                        print(success_msg)
                        allure.attach(
                            success_msg,
                            name=f"{btn_name}-{title}-Matched",
                            attachment_type=allure.attachment_type.TEXT
                        )
                        continue


                    if actual_value != expected_value:
                        error_msg = (
                            f"❌ {btn_name} - {title} Count Mismatch\n"
                            f"Dashboard Count : {actual_value}\n"
                            f"Header Count    : {expected_value}"
                        )
                        print(error_msg)
                        allure.attach(
                        error_msg,
                        name=f"{btn_name}-{title}-Mismatch",
                        attachment_type=allure.attachment_type.TEXT
                    )
                        raise AssertionError(error_msg)
                    select_all_elem = wait.until(EC.presence_of_element_located((By.XPATH, dash_select_all_checkbox)))
                    driver.execute_script("arguments[0].click();", select_all_elem)
                    time.sleep(3)
                    wait_for_loader_to_disappear(driver, wait)

                    selected_count_elem = wait.until(EC.presence_of_element_located((By.XPATH,'//div[contains(text(),"selected")]')))
                    highlight_element(driver,selected_count_elem,duration=0.2)
                    selected_text = selected_count_elem.text.strip()
                    selected_count = int(selected_text.replace(",", "").split()[0])
                    
                    # Output
                    if actual_value == expected_value == selected_count:

                        success_msg = (
                            f"✅ {btn_name} - {title} - MATCHED\n\n"
                            f"Dashboard Count : {actual_value}\n"
                            f"Header Count    : {expected_value}\n"
                            f"Select All Count: {selected_count}"
                        )

                        print(success_msg)

                        allure.attach(
                            success_msg,
                            name=f"{btn_name}-{title}-Matched",
                            attachment_type=allure.attachment_type.TEXT
                        )

                    else:
                        error_msg = (
                            f"❌ {btn_name} - {title} Count Mismatch\n"
                            f"Dashboard Count : {actual_value}\n"
                            f"Header Count    : {expected_value}\n"
                            f"Select All Count: {selected_count}"
                        )
                        print(error_msg)
                        allure.attach(
                            error_msg,
                            name=f"{btn_name}-{title}-Mismatch",
                            attachment_type=allure.attachment_type.TEXT
                        )
                        raise AssertionError(error_msg)
            except Exception as e:
                print(f"❌ {btn_name} - {title} validation failed: {e}")
                # allure.attach(str(e), f"{btn_name}-{title} Error", allure.attachment_type.TEXT)
                raise
        
        total_value = 0

        for elem in dash_others_value_selector_elem[:3]:
            value = int(elem.text.replace(",", "").strip() or 0)
            total_value += value

        dash_sum_value_validator = (dash_value_validator_template.replace('{title}','All'))

        all_elem = wait.until(EC.presence_of_element_located((By.XPATH, dash_sum_value_validator)))
        dashboard_total = int(all_elem.text.replace(",", "").strip() or 0)

        try:
            with allure.step(f"Validating Total in '{btn_name}' (Dashboard Count: {total_value})"):

                highlight_element(driver, all_elem, duration=0.2)
                driver.execute_script("arguments[0].click();", all_elem)
                time.sleep(2)
                wait_for_loader_to_disappear(driver, wait)

                # Zero count validation
                if total_value == 0 and dashboard_total == 0:

                    success_msg = (
                        f"✅ {btn_name} - Total - MATCHED\n\n"
                        f"Dashboard Count : {total_value}\n"
                        f"Header Count    : {dashboard_total}\n"
                        f"Select All Count: N/A (No Tasks)"
                    )

                    print(success_msg)

                    allure.attach(
                        success_msg,
                        name=f"{btn_name}-Total-Matched",
                        attachment_type=allure.attachment_type.TEXT
                    )

                    continue

                # Dashboard vs Header validation
                if total_value != dashboard_total:

                    error_msg = (
                        f"❌ {btn_name} - Total Count Mismatch\n"
                        f"Dashboard Count : {total_value}\n"
                        f"Header Count    : {dashboard_total}"
                    )

                    print(error_msg)

                    allure.attach(
                        error_msg,
                        name=f"{btn_name}-Total-Mismatch",
                        attachment_type=allure.attachment_type.TEXT
                    )

                    raise AssertionError(error_msg)

                # Click Select All
                select_all_elem = wait.until(
                    EC.presence_of_element_located((By.XPATH, dash_select_all_checkbox))
                )

                driver.execute_script("arguments[0].click();", select_all_elem)
                time.sleep(3)
                wait_for_loader_to_disappear(driver, wait)

                selected_count_elem = wait.until(
                    EC.presence_of_element_located(
                        (By.XPATH, "//div[contains(text(),'selected')]")
                    )
                )

                highlight_element(driver, selected_count_elem, duration=0.2)

                selected_text = selected_count_elem.text.strip()
                selected_count = int(selected_text.replace(",", "").split()[0])

                # Final validation
                if total_value == dashboard_total == selected_count:

                    success_msg = (
                        f"✅ {btn_name} - Total - MATCHED\n\n"
                        f"Dashboard Count : {total_value}\n"
                        f"Header Count    : {dashboard_total}\n"
                        f"Select All Count: {selected_count}"
                    )

                    print(success_msg)

                    allure.attach(
                        success_msg,
                        name=f"{btn_name}-Total-Matched",
                        attachment_type=allure.attachment_type.TEXT
                    )

                else:

                    error_msg = (
                        f"❌ {btn_name} - Total Count Mismatch\n"
                        f"Dashboard Count : {total_value}\n"
                        f"Header Count    : {dashboard_total}\n"
                        f"Select All Count: {selected_count}"
                    )

                    print(error_msg)

                    allure.attach(
                        error_msg,
                        name=f"{btn_name}-Total-Mismatch",
                        attachment_type=allure.attachment_type.TEXT
                    )

                    allure.attach(
                        driver.get_screenshot_as_png(),
                        name=f"{btn_name}-Total-Screenshot",
                        attachment_type=allure.attachment_type.PNG
                    )

                    raise AssertionError(error_msg)

        except Exception as e:

            print(f"❌ {btn_name} - Total validation failed: {e}")

            allure.attach(
                str(e),
                name=f"{btn_name}-Total-Error",
                attachment_type=allure.attachment_type.TEXT
            )

            raise
    return True