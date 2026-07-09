# test_login.py
from datetime import datetime
import pyautogui as pg
import pytest
import allure
import os
import time

from utilities.login_utils import get_test_case_list, login_check
from utilities.driver_setup import setup
from utilities.screen_recorder import ScreenRecorder
test_case_list = get_test_case_list(module='login') 

@allure.suite("Login Test Suite")
@allure.sub_suite("Credential Validation")
@pytest.mark.parametrize("test_case_id,test_case_description,username,password,test_type,test_case_execution", test_case_list)
def test_login_flow(setup, test_case_id, test_case_description, username, password,  test_type, test_case_execution):
    allure.dynamic.title(f"{test_case_id}")
    allure.dynamic.description(f'{test_case_description}')
    driver = setup

    test_name = f"login_{username.replace('@', '_at_')}_{password}".replace(' ', 'blank')
    video_path = f"videos/{test_name}_{test_case_id}.mp4"
    os.makedirs("videos", exist_ok=True)
    recorder = ScreenRecorder(filename=video_path, fps=10)
    recorder.start()
    test_failed = False

    with allure.step(f"Login Flow"):
        try:
            success = login_check(driver, waittime=2, trial=3, username=username, password=password)
            if test_type == "positive":
                assert success, "Login failed with valid credentials"

            elif test_type == "negative":
                
                assert not success, "Login succeeded with invalid credentials"
        except Exception as e:
            test_failed = True
            # recorder.stop()

            time.sleep(0.5) 
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_path = f"screenshots/{test_name}_{timestamp}.png"
            os.makedirs("screenshots", exist_ok=True)
            # screenshot = pg.screenshot()
            driver.save_screenshot(screenshot_path) 

            # ✅ Attach to Allure report
            allure.attach.file(screenshot_path, name="Failure Screenshot", attachment_type=allure.attachment_type.PNG)
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