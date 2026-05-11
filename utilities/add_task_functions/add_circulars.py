from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from utilities.other_utils_functions.highlight import highlight_element
import allure
import time
from utilities.add_task_functions.add_task_common import task_value_store


def add_circulars(driver, regulatory_btn, regulatory_checkboxes, regulatory_save_btn, count, wait):
    try:
        with allure.step("Locate and click regulatory button"):
            regulatory_btn_elem = wait.until(EC.presence_of_element_located((By.XPATH, regulatory_btn)))
            highlight_element(driver, regulatory_btn_elem)
            regulatory_btn_elem.click()
            print("✅ Clicked regulatory button")

        with allure.step("Locate all regulatory checkboxes"):
            regulatory_checkboxes_elem = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, regulatory_checkboxes)))
            if len(regulatory_checkboxes_elem) < count:
                print(f"⚠️ Only {len(regulatory_checkboxes_elem)} items found, not {count}.")

        with allure.step("Select required checkboxes"):
            for i in range(min(count, len(regulatory_checkboxes_elem))):
                checkbox = regulatory_checkboxes_elem[i]
                driver.execute_script("arguments[0].scrollIntoView(true);", checkbox)
                highlight_element(driver, checkbox)
                time.sleep(0.5)
                checkbox.click()
                print(f"✅ Selected item {i+1}")

        with allure.step("Click save button for selected regulatory references"):
            regulatory_save_btn_elem = wait.until(EC.element_to_be_clickable((By.XPATH, regulatory_save_btn)))
            highlight_element(driver, regulatory_save_btn_elem)
            regulatory_save_btn_elem.click()
            print("✅ Regulatory references saved")

        # with allure.step("Validate regulation cards count after save"):
            regulation_details_view = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "regulations-scroll")))
            actual_count = len(regulation_details_view)
            print(f"Expected count: {count}, Found: {actual_count}")
            task_value_store("circular_count", actual_count)

            if actual_count == count:
                print(f"✅ Regulation count matched: {actual_count}")
                return True
            else:
                msg = f"❌ Regulation count mismatch. Expected: {count}, Found: {actual_count}"
                print(msg)
                allure.attach(msg, name="Regulation Count Mismatch", attachment_type=allure.attachment_type.TEXT)
                return False

    except Exception as e:
        print(f"Error adding circulars: {str(e)}")
        allure.attach(str(e), name="Add Circulars Error", attachment_type=allure.attachment_type.TEXT)
        return False
