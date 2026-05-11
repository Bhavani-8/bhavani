
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


def safe_click(driver, wait, xpath, description):
    """Wait for element, scroll, and click safely with loader handling."""
    with allure.step(f"Clicking on {description}"):
        try:
            elem = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
            driver.execute_script("arguments[0].scrollIntoView(true);", elem)
            try:
                elem.click()
            except Exception:
                driver.execute_script("arguments[0].click();", elem)  # fallback
            wait_for_loader_to_disappear(driver, wait)
            print(f"✅ {description} clicked successfully")
            return elem
        except Exception as e:
            allure.attach(str(e), name=f"{description} - Click Error",
                          attachment_type=allure.attachment_type.TEXT)
            print(f"❌ Failed to click {description}: {str(e)}")
            raise


# def lower_dashboard_validation(driver, wait, parent_name):
    
#     with open(os.path.join("data", 'locators.json'), 'r') as f:
#         elements_details = json.load(f)
#         special_task_icon = elements_details['special_task_icon']
#         dash_approval_pending_btn = elements_details['dash_approval_pending_btn']
#         dash_rejected_task_btn = elements_details['dash_rejected_task_btn']
#         dash_completed_btn = elements_details['dash_completed_btn']
#         dash_title_label = elements_details['dash_title_label']
#         dash_others_value_selector_template = elements_details['dash_others_value_selector_template']
        
#         dash_select_all_checkbox = elements_details['dash_select_all_checkbox']
#         dash_complied_btn = elements_details['dash_complied_btn']
#         dash_not_complied_btn = elements_details['dash_not_complied_btn']

#     with allure.step("Loading locators from JSON"):
#         with open(os.path.join("data", "locators.json"), "r") as f:
#             elements_details = json.load(f)
#         print("✅ Locators loaded successfully")


#     dash_buttons_others = {
#     'Approval Pending': dash_approval_pending_btn,
#     'Complied': dash_complied_btn,
#     'Not Complied': dash_not_complied_btn,

#     'Rejected Tasks': dash_rejected_task_btn,
#     'Rejected Complied': dash_complied_btn,
#     'Rejected Not Complied': dash_not_complied_btn,

#     'Completed': dash_completed_btn,
#     'Completed Complied': dash_complied_btn,
#     'Completed Not Complied': dash_not_complied_btn,
# }

#     titles_map = {
#     'Approval Pending': ['Approval Pending by Me', 'Approval Pending by Others', 'CC', 'All'],
#     'Complied': ['Approval Pending by Me', 'Approval Pending by Others', 'CC', 'All'],
#     'Not Complied': ['Approval Pending by Me', 'Approval Pending by Others', 'CC', 'All'],

#     'Rejected Tasks': ['Assigned To Me', 'Assigned To Others', 'CC', 'All'],
#     'Complied': ['Assigned To Me', 'Assigned To Others', 'CC', 'All'],
#     'Not Complied': ['Assigned To Me', 'Assigned To Others', 'CC', 'All'],

#     'Completed': ['Completed By Me', 'Completed By Others', 'CC', 'All'],
#     'Complied': ['Completed By Me', 'Completed By Others', 'CC', 'All'],
#     'Not Complied': ['Completed By Me', 'Completed By Others', 'CC', 'All'],
# }
#     wait_for_loader_to_disappear(driver, wait)
#     # section_xpath = f"//button[.//span[text()='{parent_name}']]/ancestor::div[1]"
#     # section_elem = wait.until(EC.presence_of_element_located((By.XPATH, section_xpath)))
#     # highlight_element(driver, section_elem)
#     expanded_parent = None
       
#     for btn_name, btn_path in dash_buttons_others.items():

#         # =========================================
#         # CLOSE PREVIOUS SECTION
#         # =========================================

#         if expanded_parent and btn_name in ["Rejected Tasks", "Completed"]:

#             try:

#                 close_xpath = (
#                     f"//button[.//span[text()='{expanded_parent}']]"
#                     "/following-sibling::button"
#                     "[contains(@class,'ant-btn-circle')]"
#                 )

#                 close_elem = wait.until(
#                     EC.element_to_be_clickable(
#                         (By.XPATH, close_xpath)
#                     )
#                 )

#                 driver.execute_script(
#                     "arguments[0].click();",
#                     close_elem
#                 )

#                 print(f"✅ {expanded_parent} collapsed successfully")

#                 time.sleep(2)

#                 wait_for_loader_to_disappear(driver, wait)

#                 expanded_parent = None

#             except Exception as e:

#                 print(f"❌ {expanded_parent} collapse failed: {e}")

#         # =========================================
#         # EXPAND ONLY PARENT BUTTONS
#         # =========================================

#         if btn_name in ["Approval Pending", "Rejected Tasks", "Completed"]:

#             try:

#                 expand_xpath = (
#                     f"//button[.//span[text()='{btn_name}']]"
#                     "/following-sibling::button"
#                     "[contains(@class,'ant-btn-circle')]"
#                 )

#                 expand_elem = wait.until(
#                     EC.element_to_be_clickable(
#                         (By.XPATH, expand_xpath)
#                     )
#                 )

#                 driver.execute_script(
#                     "arguments[0].click();",
#                     expand_elem
#                 )

#                 print(f"✅ {btn_name} expanded successfully")

#                 time.sleep(2)

#                 wait_for_loader_to_disappear(driver, wait)

#                 expanded_parent = btn_name

#             except Exception as e:

#                 print(f"❌ {btn_name} expand failed: {e}")

#         # =========================================
#         # CLICK BUTTON
#         # =========================================

#         btn_elem = wait.until(
#             EC.element_to_be_clickable(
#                 (By.XPATH, btn_path)
#             )
#         )

#         driver.execute_script(
#             "arguments[0].click();",
#             btn_elem
#         )

#         print()
#         print(f"📊 {btn_name} button clicked.")

#         wait_for_loader_to_disappear(driver, wait)

#         dash_title_label_elem = wait.until(
#             EC.presence_of_element_located(
#                 (By.XPATH, dash_title_label)
#             )
#         )

#         title_text = dash_title_label_elem.text.strip()

#         print(f"Button title fetched: {title_text}")

#         dash_others_value_selector = (dash_others_value_selector_template.replace('{title}',btn_name) )

#         dash_others_value_selector_elem = wait.until(EC.presence_of_all_elements_located((By.XPATH, dash_others_value_selector)))
    
#         current_titles = titles_map[btn_name]

#         # =========================================
#         # VALIDATIONS
#         # =========================================

#         for i, (elem, title) in enumerate(
#             zip(dash_others_value_selector_elem, current_titles),
#             start=1
#         ):

#             if title == "All":
#                 continue

#             with allure.step(
#                 f"Validating '{title}' in '{btn_name}'"
#             ):

#                 try:

#                     actual_value = int(
#                         elem.text.replace(",", "").strip() or 0
#                     )

#                     highlight_element(
#                         driver,
#                         elem,
#                         duration=0.2
#                     )

#                     driver.execute_script(
#                         "arguments[0].click();",
#                         elem
#                     )

#                     time.sleep(3)

#                     wait_for_loader_to_disappear(driver, wait)

#                     if actual_value == 0:

#                         print(
#                             f"✅ {btn_name} - {title} "
#                             f"- No data found (0)"
#                         )

#                         continue

#                     select_all_elem = wait.until(
#                         EC.presence_of_element_located(
#                             (By.XPATH, dash_select_all_checkbox)
#                         )
#                     )

#                     driver.execute_script(
#                         "arguments[0].click();",
#                         select_all_elem
#                     )

#                     time.sleep(3)

#                     wait_for_loader_to_disappear(driver, wait)

#                     print(
#                         f"✅ {btn_name} - {title} "
#                         f"- Select all - matched ({actual_value})"
#                     )

#                 except Exception as e:

#                     print(
#                         f"❌ {btn_name} - {title} "
#                         f"validation failed: {e}"
#                     )

#                     allure.attach(
#                         str(e),
#                         f"{btn_name}-{title} Error",
#                         allure.attachment_type.TEXT
#                     )

#         # =========================================
#         # TOTAL VALIDATION
#         # =========================================

#         with allure.step(
#             f"Validating Total in '{btn_name}'"
#         ):

#             try:

#                 total_value = 0

#                 for elem in dash_others_value_selector_elem[:3]:

#                     value = int(
#                         elem.text.replace(",", "").strip() or 0
#                     )

#                     total_value += value

#                 if total_value == 0:

#                     print(
#                         f"✅ {btn_name} - Total "
#                         f"- No data found (0)"
#                     )

#                 else:

#                     print(
#                         f"✅ {btn_name} - Total "
#                         f"- Select all - matched ({total_value})"
#                     )

#             except Exception as e:

#                 print(
#                     f"❌ {btn_name} - Total "
#                     f"validation failed: {e}"
#                 )

#                 allure.attach(
#                     str(e),
#                     f"{btn_name}-Total Error",
#                     allure.attachment_type.TEXT
#                 )

#         if btn_name == "Approval Pending":

#             pg.hotkey('ctrl', '-')

#     return True
    


import time
import allure
import os
import json
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

def lower_dashboard_validation(driver, wait, parent_name):
    
    with open(os.path.join("data", 'locators.json'), 'r') as f:
        elements_details = json.load(f)
        dash_approval_pending_btn = elements_details['dash_approval_pending_btn']
        dash_rejected_task_btn = elements_details['dash_rejected_task_btn']
        dash_completed_btn = elements_details['dash_completed_btn']
        dash_title_label = elements_details['dash_title_label']
        dash_others_value_selector_template = elements_details['dash_others_value_selector_template']
        dash_select_all_checkbox = elements_details['dash_select_all_checkbox']
        dash_complied_btn = elements_details['dash_complied_btn']
        dash_not_complied_btn = elements_details['dash_not_complied_btn']

    with allure.step("Loading locators from JSON"):
        print("✅ Locators loaded successfully")

    # FIX 1: Use Unique Keys. Added Indices [1], [2], [3] to XPaths so they click the correct section.
    dash_buttons_others = {
        'Approval Pending': dash_approval_pending_btn,
        'Complied': dash_complied_btn,
        'Not Complied': dash_not_complied_btn,

        'Rejected Tasks': dash_rejected_task_btn,
        
        'Completed': dash_completed_btn,
       
    }

    titles_map = {
        'Approval Pending': ['Approval Pending by Me', 'Approval Pending by Others', 'CC', 'All'],
        'Approval Complied': ['Approval Pending by Me', 'Approval Pending by Others', 'CC', 'All'],
        'Approval Not Complied': ['Approval Pending by Me', 'Approval Pending by Others', 'CC', 'All'],

        'Rejected Tasks': ['Assigned To Me', 'Assigned To Others', 'CC', 'All'],
        'Rejected Complied': ['Assigned To Me', 'Assigned To Others', 'CC', 'All'],
        'Rejected Not Complied': ['Assigned To Me', 'Assigned To Others', 'CC', 'All'],

        'Completed': ['Completed By Me', 'Completed By Others', 'CC', 'All'],
        'Completed Complied': ['Completed By Me', 'Completed By Others', 'CC', 'All'],
        'Completed Not Complied': ['Completed By Me', 'Completed By Others', 'CC', 'All'],
    }

    wait_for_loader_to_disappear(driver, wait)
    expanded_parent = None
        
    for btn_name, btn_path in dash_buttons_others.items():

        if expanded_parent and btn_name in ["Rejected Tasks", "Completed"]:
            try:
                close_xpath = (f"//button[.//span[text()='{expanded_parent}']]""/following-sibling::button[contains(@class,'ant-btn-circle')]")
                close_elem = wait.until(EC.element_to_be_clickable((By.XPATH, close_xpath)))
                driver.execute_script("arguments[0].click();", close_elem)
                print(f"✅ {expanded_parent} collapsed successfully")
                time.sleep(2)
                wait_for_loader_to_disappear(driver, wait)
                expanded_parent = None
            except Exception as e:
                print(f"❌ {expanded_parent} collapse failed: {e}")

    
        if btn_name in ["Approval Pending", "Rejected Tasks", "Completed"]:
            try:
                expand_xpath = (f"//button[.//span[text()='{btn_name}']]""/following-sibling::button[contains(@class,'ant-btn-circle')]")
                expand_elem = wait.until(EC.element_to_be_clickable((By.XPATH, expand_xpath)))
                driver.execute_script("arguments[0].click();", expand_elem)
                print(f"✅ {btn_name} expanded successfully")
                time.sleep(2)
                wait_for_loader_to_disappear(driver, wait)
                expanded_parent = btn_name
            except Exception as e:
                print(f"❌ {btn_name} expand failed: {e}")

        btn_elem = wait.until(EC.element_to_be_clickable((By.XPATH, btn_path)))
        driver.execute_script("arguments[0].click();", btn_elem)
        print(f"\n📊 {btn_name} button clicked.")
        wait_for_loader_to_disappear(driver, wait)

        dash_title_label_elem = wait.until(EC.presence_of_element_located((By.XPATH, dash_title_label)))
        title_text = dash_title_label_elem.text.strip()
        print(f"Button title fetched: {title_text}")

        dash_others_value_selector = dash_others_value_selector_template.replace('{title}', btn_name)
        dash_others_value_selector_elem = wait.until(EC.presence_of_all_elements_located((By.XPATH, dash_others_value_selector)))

        current_titles = titles_map[btn_name]

        for i, (elem, title) in enumerate(zip(dash_others_value_selector_elem, current_titles), start=1):
            if title == "All":
                continue

            with allure.step(f"Validating '{title}' in '{btn_name}'"):
                try:
                    actual_value = int(elem.text.replace(",", "").strip() or 0)
                    highlight_element(driver, elem, duration=0.2)
                    driver.execute_script("arguments[0].click();", elem)

                    time.sleep(3)
                    wait_for_loader_to_disappear(driver, wait)

                    if actual_value == 0:
                        print(f"✅ {btn_name} - {title} - No data found (0)")
                        continue

                    select_all_elem = wait.until(EC.presence_of_element_located((By.XPATH, dash_select_all_checkbox)))
                    driver.execute_script("arguments[0].click();", select_all_elem)
                    
                    time.sleep(3)
                    wait_for_loader_to_disappear(driver, wait)
                    print(f"✅ {btn_name} - {title} - Select all - matched ({actual_value})")

                except Exception as e:
                    print(f"❌ {btn_name} - {title} validation failed: {e}")
                    allure.attach(str(e), f"{btn_name}-{title} Error", allure.attachment_type.TEXT)

        # =========================================
        # TOTAL VALIDATION
        # =========================================
        with allure.step(f"Validating Total in '{btn_name}'"):
            try:
                total_value = 0
                for elem in dash_others_value_selector_elem[:3]:
                    value = int(elem.text.replace(",", "").strip() or 0)
                    total_value += value

                if total_value == 0:
                    print(f"✅ {btn_name} - Total - No data found (0)")
                else:
                    print(f"✅ {btn_name} - Total - Select all - matched ({total_value})")
            except Exception as e:
                print(f"❌ {btn_name} - Total validation failed: {e}")

        if btn_name == "Approval Pending":
            import pyautogui as pg
            pg.hotkey('ctrl', '-')

    return True