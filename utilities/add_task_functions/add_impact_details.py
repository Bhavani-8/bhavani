import allure
from utilities.add_task_functions.add_task_common import validate_file
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from utilities.other_utils_functions.highlight import highlight_element
import os
import time
from utilities.add_task_functions.add_task_common import task_value_store
import pyautogui as pg

def add_impact_details(driver, impact_button, fine_amount_editor, impact_details, impact_file_name,
                       attach_file_input, impact_file_save_btn, impact_fine_amount_view, impact_file_view, wait):
    
    # Step 1: Validate inputs
    if not impact_details or str(impact_details).strip() == '':
        msg = "❌ Impact details input is blank."
        print(msg)
        allure.attach(msg, name="Input Error: Impact Details", attachment_type=allure.attachment_type.TEXT)
        return 'blank'

    if not impact_file_name or str(impact_file_name).strip() == '':
        msg = "❌ Impact file input is blank."
        print(msg)
        allure.attach(msg, name="Input Error: Impact File", attachment_type=allure.attachment_type.TEXT)
        return 'blank'

    if not validate_file(impact_file_name):
        msg = f"❌ File does not have a valid extension: {impact_file_name}"
        print(msg)
        allure.attach(msg, name="Input Error: Impact File", attachment_type=allure.attachment_type.TEXT)
        return 'invalid'

    # Step 2: Click impact button
    try:
        # with allure.step("Clicking impact button"):
        impact_button_elem = wait.until(EC.presence_of_element_located((By.XPATH, impact_button)))
        highlight_element(driver, impact_button_elem)
        impact_button_elem.click()
        print("Clicked impact button")
    except Exception as e:
        msg = f"❌ Failed to click impact button: {e}"
        print(msg)
        allure.attach(msg, name="Impact Button Error", attachment_type=allure.attachment_type.TEXT)
        return False

    # Step 3: Enter impact details
    try:
        # with allure.step("Entering impact details"):
        fine_amount_editor_elem = wait.until(EC.presence_of_element_located((By.XPATH, fine_amount_editor)))
        highlight_element(driver, fine_amount_editor_elem)
        fine_amount_editor_elem.send_keys(impact_details)
        print(f"Sent impact details: {impact_details}")
    except Exception as e:
        msg = f"❌ Failed to enter impact details: {e}"
        print(msg)
        allure.attach(msg, name="Impact Details Input Error", attachment_type=allure.attachment_type.TEXT)
        return False

    # Step 4: Attach file
    try:
        # with allure.step("Attaching impact file"):
        impact_file_input_elem = wait.until(EC.presence_of_element_located((By.XPATH, "(//input[@type='file'])[last()]")))
        highlight_element(driver, impact_file_input_elem)
        file_path = os.path.abspath(os.path.join('data', impact_file_name))
        
        impact_file_input_elem.send_keys(file_path)
        print(f"Sent file path: {file_path}")
    except Exception as e:
        msg = f"❌ Failed to attach impact file: {e}"
        print(msg)
        allure.attach(msg, name="Impact File Error", attachment_type=allure.attachment_type.TEXT)
        return False
    
    try:
    # Wait for upload progress to disappear
        wait.until(EC.invisibility_of_element_located((By.XPATH, "//div[contains(@class,'ant-upload-list-item-progress')]")))
        print("✅ Upload complete")
        # Wait until Save button enabled
        wait.until(EC.presence_of_element_located((By.XPATH, "//button[.//span[text()='Save'] and not(@disabled)]")))

        # Re-fetch button
        impact_save_button = wait.until(EC.element_to_be_clickable((By.XPATH, "(//button[.//span[normalize-space()='Save']])[last()]")))
        highlight_element(driver, impact_save_button)

        # Scroll into view
        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", impact_save_button)
        time.sleep(1)
        impact_save_button.click()

        print("✅ Save button clicked successfully")

    except Exception as e:
        print(f"❌ Failed to Click Save Button: {e}")
        return False
   
    try:
    # with allure.step("Validating impact details"):
        impact_details_view_elem = wait.until(EC.presence_of_element_located((By.XPATH, impact_fine_amount_view)))
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", impact_details_view_elem)
        highlight_element(driver, impact_details_view_elem)

        impact_details_value = impact_details_view_elem.text.strip()
        print(f"Expected: {impact_details}, Found: {impact_details_value}")

        # ---- FIX START (normalize values) ----
        impact_details_value = impact_details_value.replace(",", "").strip()
        impact_details_expected = str(impact_details).replace(",", "").strip()

        if impact_details_value.endswith(".0"):
            impact_details_value = impact_details_value[:-2]

        if impact_details_expected.endswith(".0"):
            impact_details_expected = impact_details_expected[:-2]
        # ---- FIX END ----

        if impact_details_value != impact_details_expected:
            allure.attach("❌ Impact details mismatch", name="Impact Details Validation", attachment_type=allure.attachment_type.TEXT)
            return False
        else:
            allure.attach("✅ Impact details added correctly", name="Impact Details Validation", attachment_type=allure.attachment_type.TEXT)

    except Exception as e:
        msg = f"❌ Failed to validate impact details: {e}"
        print(msg)
        allure.attach(msg, name="Impact Details Validation Error", attachment_type=allure.attachment_type.TEXT)
        return False


    # Step 6: Validate uploaded file
    try:
        # with allure.step("Validating uploaded impact file"):
        impact_file_view_elem = wait.until(EC.presence_of_element_located((By.XPATH, impact_file_view)))
        highlight_element(driver, impact_file_view_elem)
        impact_file_value = impact_file_view_elem.text.strip()
        print(f"Expected: {impact_file_name}, Found: {impact_file_value}")

        if impact_file_value != impact_file_name:
            allure.attach("❌ File name mismatch", name="File Validation", attachment_type=allure.attachment_type.TEXT)
            return False

        if "." not in impact_file_name:
            msg = "❌ File name does not contain a valid file extension."
            print(msg)
            allure.attach(msg, name="File Validation Error", attachment_type=allure.attachment_type.TEXT)
            return False

        file_extension = impact_file_name.split(".")[-1].lower()
        print(f'File has extension: {file_extension}')
        allure.attach("✅ File attached correctly", name="File Validation", attachment_type=allure.attachment_type.TEXT)

        # Store values
        task_value_store("impact_details", impact_details)
        task_value_store("impact_file_name", impact_file_name)
        return True

    except Exception as e:
        msg = f"🔥 Unexpected error during file validation: {e}"
        print(msg)
        allure.attach(msg, name="Attach File Error", attachment_type=allure.attachment_type.TEXT)
        return False
