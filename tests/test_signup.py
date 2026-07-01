# test_signup.py
from datetime import datetime
import pyautogui as pg
import pytest
import allure
import os
import time

from utilities.signup_utils import get_test_case_list, signup_check
from utilities.driver_setup import setup
from utilities.screen_recorder import ScreenRecorder


signup_test_case_list = get_test_case_list(module='signup')

@allure.suite("Signup Test Suite")
@allure.sub_suite("Signup Flow")
@pytest.mark.parametrize("test_case_id,test_case_description,email,check_selection,test_type", signup_test_case_list)
def test_signup_flow(setup, test_case_id, test_case_description, email, check_selection, test_type):
    # allure.dynamic.title(f"Signup Module: Test Execution Flow For {'Valid Case' if test_type else 'Invalid Case'}")
    # allure.dynamic.description(f"This test checks signup functionality with {'valid' if test_type else 'invalid'} credential.")
    allure.dynamic.title(f"{test_case_id}")
    allure.dynamic.description(f'{test_case_description}')
    driver = setup
    test_name = f"signup_{email.replace('@', '_at_')}".replace(' ', 'blank')
    video_path = f"videos/{test_name}_{test_case_id}.mp4"
    os.makedirs("videos", exist_ok=True)
    recorder = ScreenRecorder(filename=video_path, fps=10)
    recorder.start()
    test_failed = False
    with allure.step(f"Signup Flow"):
        try:
            success = signup_check(driver, email=email, check_selection=check_selection, test_type=test_type)
            if test_type == "positive":
                assert success, "Signup failed with valid credentials"

            elif test_type == "negative":
                assert not success, "Signup succeeded with invalid credentials"
        except Exception as e:
            test_failed = True
            recorder.stop()

            time.sleep(2)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_path = f"screenshots/{test_name}_{timestamp}.png"
            os.makedirs("screenshots", exist_ok=True)
            screenshot = pg.screenshot()
            screenshot.save(screenshot_path)

            # ✅ Attach to Allure report
             # ✅ Attach to Allure report
            allure.attach.file(screenshot_path, name="Failure Screenshot", attachment_type=allure.attachment_type.PNG)
            # if os.path.exists(video_path) and os.path.getsize(video_path) > 0:
            #     allure.attach.file(video_path,name="Failure Video",attachment_type=allure.attachment_type.MP4)
            # else:
            #     print("❌ Video missing or empty")
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
# To Run This Test Script:
# > pytest tests/testing_and_reporting.py --alluredir=allure-results  >> To run all test cases
# > pytest -m login --alluredir=allure-results  >> To run all login test cases
# > pytest -m "login and positive" --alluredir=allure-results  >> To run all positive test cases
# > pytest -m "login and negative" --alluredir=allure-results  >> To run all negative test cases
# > allure generate allure-results -o allure-report --clean
# > allure open allure-report