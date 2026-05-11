
from utilities.other_utils_functions.highlight import highlight_element
import allure
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from utilities.add_task_functions.add_task_common import task_value_store

def search_and_add_circulars(driver, regulatory_btn, regulatory_checkboxes, circular_search,
                             regulatory_save_btn, regulatory_cancel_btn, regulatory_search_btn, wait):

    try:
        regulatory_btn_elem = wait.until(EC.presence_of_element_located((By.XPATH, regulatory_btn)))
        highlight_element(driver, regulatory_btn_elem)
        regulatory_btn_elem.click()
        print("Clicked regulatory button")

        search_input = driver.find_element(By.XPATH, regulatory_search_btn)
        highlight_element(driver, search_input)
        search_input.click()
        search_input.send_keys(circular_search)
        print(f"Searched for circular: {circular_search}")
        time.sleep(2)

        try:
            regulatory_checkboxes_elem = wait.until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, regulatory_checkboxes))
            )
        except TimeoutException:
            regulatory_checkboxes_elem = []
            print('No checkboxes found')

        if not regulatory_checkboxes_elem:
            print(f"No regulatory references found for {circular_search}")
            try:
                cancel_btn_elem = wait.until(EC.element_to_be_clickable((By.XPATH, regulatory_cancel_btn)))
                highlight_element(driver, cancel_btn_elem)
                cancel_btn_elem.click()
                print("Clicked Cancel")
            except Exception as e:
                msg = f"❌ Failed to click Cancel button: {e}"
                print(msg)
                allure.attach(msg, name="Cancel Button Error", attachment_type=allure.attachment_type.TEXT)
            return False

        print(f"Found {len(regulatory_checkboxes_elem)} regulatory references")

        # ✅ Select first checkbox
        first_checkbox = regulatory_checkboxes_elem[0]
        highlight_element(driver, first_checkbox)
        first_checkbox.click()
        time.sleep(2)
        print("Selected first regulatory reference")

        # 🔥 Expected value (store before save)
        expected_circular = circular_search.strip()

        regulatory_save_btn_elem = wait.until(EC.element_to_be_clickable((By.XPATH, regulatory_save_btn)))
        highlight_element(driver, regulatory_save_btn_elem)
        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", regulatory_save_btn_elem)
        time.sleep(1)

        try:
            regulatory_save_btn_elem.click()
            time.sleep(2)
        except:
            driver.execute_script("arguments[0].click();", regulatory_save_btn_elem)

        print("✅ Saved regulatory references")

        # ✅ Validate selected circular
        try:
            update_circular_checkbox = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='checkbox-title']")))
            highlight_element(driver, update_circular_checkbox)

            actual_circular = update_circular_checkbox.text.strip()

            allure.attach(f"Validating actual='{actual_circular}' with expected='{expected_circular}'",name="Circular Validation",attachment_type=allure.attachment_type.TEXT)

            if expected_circular.lower() in actual_circular.lower():
                print(f"✅ Circular matched: {actual_circular}")
                task_value_store("circular_search", actual_circular)
                return True
            else:
                msg = f"❌ Circular mismatch. Expected: {expected_circular}, Found: {actual_circular}"
                print(msg)
                allure.attach(msg, name="Circular Error", attachment_type=allure.attachment_type.TEXT)
                return False

        except Exception as e:
            msg = f"❌ Circular validation failed: {e}"
            print(msg)
            allure.attach(msg, name="Validation Error", attachment_type=allure.attachment_type.TEXT)
            return False

    except Exception as e:
        msg = f"❌ Error adding circulars: {str(e)}"
        print(msg)
        allure.attach(msg, name="Attach Circular Error", attachment_type=allure.attachment_type.TEXT)
        return False