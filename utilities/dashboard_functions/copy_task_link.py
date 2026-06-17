
from selenium.webdriver import ActionChains
from utilities.add_task_functions.wait_for_loader_to_disappear import wait_for_loader_to_disappear
from utilities.other_utils_functions.highlight import highlight_element
import json, os, time, pyperclip
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
import pytest
import allure
def copy_task_link(driver, wait):
    try:
        with open(os.path.join("data", "locators.json"), "r") as f:
            locators = json.load(f)
            dash_total_btn = locators["dash_total_btn"]
            toast_msg = locators["toast_msg"]
            column_chooser_btn = locators["column_chooser_btn"]
            column_chooser_save_btn = locators["column_chooser_save_btn"]
            select_all_checkbox = locators["select_all_checkbox"]
    except Exception as e:
        print(f"❌ Failed to load locators.json: {e}")
        return False

    with allure.step("Click Total button"):
        try:
            total_btn = wait.until(EC.element_to_be_clickable((By.XPATH, dash_total_btn)))
            highlight_element(driver, total_btn)
            total_btn.click()
            wait_for_loader_to_disappear(driver, wait)
            print("✅ Clicked Dashboard Total tab")
        except Exception as e:
            print(f"❌ Failed to click Total tab: {e}")
            return False

    with allure.step("Open Column Chooser"):  
        try:
            column_chooser_btn_elem = wait.until(EC.presence_of_element_located((By.XPATH, column_chooser_btn)))
            driver.execute_script("arguments[0].click();", column_chooser_btn_elem)
            wait_for_loader_to_disappear(driver, wait)
        except TimeoutException:
            pytest.fail("❌ Column Chooser button not found")
    with allure.step("Deselected 'Select All' checkbox"):
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
                return "mixed"   # usually 'mixed' or None
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
        except StaleElementReferenceException:
            pytest.fail("❌ Stale element while normalizing Select All")
    with allure.step("Click Save Button on Column Chooser"):
        try:
            save_btn = wait.until(EC.element_to_be_clickable((By.XPATH, column_chooser_save_btn)))
            highlight_element(driver, save_btn)
            save_btn.click()
            time.sleep(3)
            print("✅ Column Chooser saved")
        except TimeoutException:
            print("❌ 'Company / Project' not found in filter list")
    
    with allure.step("Click 'Copy Task Link' button"):
        try:
            copy_btn = wait.until(EC.presence_of_element_located((By.XPATH, "(//div[contains(@class,'justify-between') and .//p][1]//button[contains(@class,'ant-btn-icon-only')])[2]")))
            copy_btn.click()
            time.sleep(0.5)
            print("✅ Clicked Copy Task Link button")
        except Exception as e:
            print(f"❌ Failed to click Copy button: {e}")
            return False

    with allure.step("Get copied task link from clipboard"):
        main_window = driver.current_window_handle

        # Get copied link from clipboard
        copied_link = pyperclip.paste()
        time.sleep(0.5)
        if not copied_link:
            raise Exception("Clipboard is empty")

            print(f"🔗 Copied Link: {copied_link}")
    with allure.step("Open copied task link in new tab"):
        driver.execute_script("window.open('about:blank','_blank');")
        time.sleep(4)
        new_window = [w for w in driver.window_handles if w != main_window][0]
        driver.switch_to.window(new_window)
        driver.get(copied_link)
        time.sleep(4)
        # wait.until(EC.url_contains(copied_link.split("//")[-1]))
        print("✅ Task link opened successfully in new tab")


    with allure.step("Close new tab"):
        driver.close()
        driver.switch_to.window(main_window)
        time.sleep(3)
        wait_for_loader_to_disappear(driver, wait)


    return True

