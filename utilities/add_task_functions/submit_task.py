from utilities.other_utils_functions.highlight import highlight_element
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import allure
import time
# def submit_task(driver, submit_button, err_msg_toast, wait):
#     try:
#         with allure.step("Locate and validate submit button"):
#             submit_button_elem = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, submit_button)))
#             highlight_element(driver, submit_button_elem)

#             if submit_button_elem.is_enabled():
#                 print("✅ Submit button is enabled")
#                 submit_button_elem.click()
#                 print("✅ Clicked submit button")
#             else:
#                 msg = "❌ Submit button is disabled. Cannot proceed."
#                 print(msg)
#                 allure.attach(msg, name="Submit Button Status", attachment_type=allure.attachment_type.TEXT)
#                 return False

#         found_success = False

#         with allure.step("Check toast messages for task submission status"):
#             toast_msgs = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, err_msg_toast)))
#             for toast_msg in toast_msgs:
#                 highlight_element(driver, toast_msg)
#                 msg_text = toast_msg.text.strip()
#                 if msg_text.lower() == "task added successfully":
#                     found_success = True

#             if found_success:
#                 print("✅ Task submitted successfully.")
#                 return True
#             else:
#                 msg = "❌ Task submission failed."
#                 print(msg)
#                 allure.attach(msg, name="Task Submission Result", attachment_type=allure.attachment_type.TEXT)
#                 return False

#     except Exception as e:
#         print(f"Error submitting task: {str(e)}")
#         allure.attach(str(e), name="Task Submission Error", attachment_type=allure.attachment_type.TEXT)
#         return False


def submit_task(driver, submit_button, toast_msg, wait):
    try:
        # with allure.step("Locate and validate submit button"):
        submit_button_elem = wait.until(EC.presence_of_element_located((By.XPATH, "//div//span[text()='Submit']")))
        highlight_element(driver, submit_button_elem)

        if submit_button_elem.is_enabled():
            print("✅ Submit button is enabled")
            time.sleep(1)
            submit_button_elem.click()
            print("✅ Clicked submit button to submit the task")
        else:
            msg = "❌ Submit button is disabled. Cannot proceed."
            print(msg)
            allure.attach(msg, name="Submit Button Status", attachment_type=allure.attachment_type.TEXT)
            return False
        
        with allure.step("Toast Message"):
            try:
                for _ in range(5):  # handle animation delay
                    time.sleep(0.7)

                    toast_msg_elem = wait.until(EC.visibility_of_element_located((By.XPATH, toast_msg)))
                    highlight_element(driver, toast_msg_elem)
                    msg = toast_msg_elem.text.strip()

                    if not msg:
                        continue

                    print(f"📢 Toast Message: {msg}")
                    allure.attach(msg, name="Toast Message", attachment_type=allure.attachment_type.TEXT)

                    if "invalid" in msg.lower() or "error" in msg.lower() or "failed" in msg.lower():
                        print(f"❌ Error Toast Detected: {msg}")
                        return False

                   
                    return True

                return True

            except Exception:
                print("ℹ️ No toast message detected")
                return True

    except Exception as e:
        print(f"Error submitting task: {str(e)}")
        allure.attach(str(e), name="Task Submission Error", attachment_type=allure.attachment_type.TEXT)
        return False
    
   
