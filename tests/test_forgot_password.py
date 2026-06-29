# test_login.py
from datetime import datetime
import pyautogui as pg
import pytest
import allure
import os
import time# test_forgot_password.py
from datetime import datetime
import pyautogui as pg
import pytest
import allure
import os

from utilities.forgot_password_utils import get_test_case_list, forgot_password_check
from utilities.driver_setup import setup
from utilities.screen_recorder import ScreenRecorder

fp_test_case_list = get_test_case_list(module='forgot_password')

@allure.suite("Forgot Password Test Suite")
@allure.sub_suite("Forgot Password Flow")
@pytest.mark.parametrize("test_case_id,test_case_description,email,test_type", fp_test_case_list)
def test_forgot_password_flow(setup, test_case_id, test_case_description, email,  test_type):
    allure.dynamic.title(f"{test_case_id}")
    allure.dynamic.description(f'{test_case_description}')
    driver = setup
    test_name = f"forgot_{email.replace('@', '_at_')}".replace(' ', 'blank')
    video_path = f"videos/{test_name}_{test_case_id}.mp4"
    os.makedirs("videos", exist_ok=True)
    recorder = ScreenRecorder(filename=video_path, fps=10)
    recorder.start()
    test_failed = False
    with allure.step(f"Forgot Password Flow"):
        try:
            success = forgot_password_check(driver, email=email, test_type=test_type)
            if test_type == "positive":
                assert success, "Forgot Password failed with valid credentials"

            elif test_type == "negative":
                assert not success, "Forgot succeeded with invalid credentials"
        except Exception as e:
            test_failed = True
            recorder.stop()

            time.sleep(1) 
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_path = f"screenshots/{test_name}_{timestamp}.png"
            os.makedirs("screenshots", exist_ok=True)
            # screenshot = pg.screenshot()
            driver.save_screenshot(screenshot_path) 

            # ✅ Attach to Allure report
            allure.attach.file(screenshot_path, name="Failure Screenshot", attachment_type=allure.attachment_type.PNG)
            if os.path.exists(video_path) and os.path.getsize(video_path) > 0:
                allure.attach.file(video_path,name="Failure Video",attachment_type=allure.attachment_type.MP4)
            else:
                print("❌ Video missing or empty")
            allure.attach(str(e), name="Failure Reason", attachment_type=allure.attachment_type.TEXT)
            pytest.fail(f"Failure reason: {e}")
            
        finally:
            try:
                recorder.stop()
            except:
                pass

            # 🔗 Attach final URL no matter success or failure
            allure.attach(driver.current_url, name="Final URL", attachment_type=allure.attachment_type.TEXT)
            if test_failed:
                if os.path.exists(video_path) and os.path.getsize(video_path) > 0:
                    allure.attach.file(
                        video_path,
                        name="Failure Video",
                        attachment_type=allure.attachment_type.MP4
                    )
                else:
                    print("❌ Video missing or empty")
            else:
                if os.path.exists(video_path):
                    os.remove(video_path)