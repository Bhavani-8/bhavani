import allure
from utilities.add_task_functions.add_task_common import validate_file
from utilities.other_utils_functions.highlight import highlight_element
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import os
import time
from utilities.add_task_functions.add_task_common import task_value_store


def attach_file(driver, attach_file_btn, attach_file_input, attach_file_name, attach_file_save_btn, attach_file_view, wait):
    # Step 1: Validate input
    if not attach_file_name or str(attach_file_name).strip() == '':
        msg = "❌ File input is blank."
        print(msg)
        allure.attach(msg, name="Input Error", attachment_type=allure.attachment_type.TEXT)
        return 'blank'
    
    if not validate_file(attach_file_name):
        msg = f"❌ File does not have a valid extension: {attach_file_name}"
        print(msg)
        allure.attach(msg, name="Input Error", attachment_type=allure.attachment_type.TEXT)
        return 'invalid'

    # Step 2: Click attach file button
    try:
        # with allure.step("Clicking attach file button"):
        attach_file_btn_elem = wait.until(EC.presence_of_element_located((By.XPATH, attach_file_btn)))
        highlight_element(driver, attach_file_btn_elem)
        attach_file_btn_elem.click()
        print("Clicked attach file button")
    except Exception as e:
        msg = f"❌ Failed to click attach file button: {e}"
        print(msg)
        allure.attach(msg, name="Attach Button Error", attachment_type=allure.attachment_type.TEXT)
        return False

    # Step 3: Send file path
    try:
        # with allure.step("Sending file path to input"):
        attach_file_input_elem = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='file' and contains(@style,'position: absolute')]")))
        highlight_element(driver, attach_file_input_elem)
        file_path = os.path.abspath(os.path.join('data', attach_file_name))
        driver.execute_script("arguments[0].style.display = 'block';", attach_file_input_elem)
        attach_file_input_elem.send_keys(file_path)
        print(f"Sent file path: {file_path}")
    except Exception as e:
        msg = f"❌ Failed to send file path: {e}"
        print(msg)
        allure.attach(msg, name="File Input Error", attachment_type=allure.attachment_type.TEXT)
        return False

    # Step 4: Click save button
    # try:

    #     # with allure.step("Clicking save button"):
    #     attach_file_save_btn_elem = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@class,'ant-modal')]//button[.//span[text()='Save']]")))
    #     highlight_element(driver, attach_file_save_btn_elem)
    #     time.sleep(1)
    #     attach_file_save_btn_elem.click()
    # except Exception as e:
    #     msg = f"❌ Failed to click save button: {e}"
    #     print(msg)
    #     allure.attach(msg, name="Save Button Error", attachment_type=allure.attachment_type.TEXT)
    #     return False

    try:
        # Wait for upload complete
        wait.until(EC.invisibility_of_element_located(
            (By.XPATH, "//div[contains(@class,'ant-upload-list-item-progress')]")
        ))
        print("✅ Upload complete")

        # # Wait for visible modal
        # modal = wait.until(EC.visibility_of_element_located(
        #     (By.XPATH, "//div[contains(@class,'ant-modal') and contains(@class,'open')]")
        # ))

        # Find Save button ONLY inside active modal
        attach_file_save_btn = wait.until(
            EC.element_to_be_clickable((
                By.XPATH,
                "//div[text()='Attach Files']/ancestor::div[contains(@class,'ant-modal-content')]//button[.//span[normalize-space()='Save']]"
            ))
        )

        highlight_element(driver, attach_file_save_btn)

        # Scroll
        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", attach_file_save_btn)
        time.sleep(1)

    # ✅ Normal click
        try:
            attach_file_save_btn.click()
        except:
            # 🔥 Force click (VERY IMPORTANT)
            driver.execute_script("arguments[0].click();", attach_file_save_btn)

        print("✅ Save button clicked successfully")

    except Exception as e:
        print(f"❌ Failed to Click Save Button: {e}")
        return False
    # Step 5: Validate uploaded file
    try:
        # with allure.step("Validating uploaded file"):
        attach_file_view_elem = wait.until(EC.presence_of_element_located((By.XPATH, attach_file_view)))
        highlight_element(driver, attach_file_view_elem)
        attach_file_value = attach_file_view_elem.text.strip()
        print(f"Expected: {attach_file_name}, Found: {attach_file_value}")

        if attach_file_value != attach_file_name:
            msg = "❌ File name mismatch"
            print(msg)
            allure.attach(msg, name="File Validation Error", attachment_type=allure.attachment_type.TEXT)
            return False

        if "." in attach_file_name:
            file_extension = attach_file_name.split(".")[-1].lower()
            print(f"File has extension: {file_extension}")
        else:
            msg = "❌ File name does not contain a valid file extension."
            print(msg)
            allure.attach(msg, name="File Validation Error", attachment_type=allure.attachment_type.TEXT)
            return False

        allure.attach("✅ File attached correctly", name="File Validation", attachment_type=allure.attachment_type.TEXT)
        task_value_store("attach_file_name", attach_file_name)
        return True

    except Exception as e:
        msg = f"🔥 Unexpected error during file validation: {e}"
        print(msg)
        allure.attach(msg, name="Attach File Error", attachment_type=allure.attachment_type.TEXT)
        return False
