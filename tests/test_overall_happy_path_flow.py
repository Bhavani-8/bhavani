# test_login.py
from datetime import datetime
import pyautogui as pg
import pytest
import allure
import os
import time

from utilities.overall_happy_path_flow_utils import overall_happy_path_check, get_test_case_list
from utilities.driver_setup import setup
from utilities.screen_recorder import ScreenRecorder

task_details = get_test_case_list(module='overall_happy_path_flow') 

@allure.suite("Overall Happy Path Flow Test Suite")
@allure.sub_suite("Credential Validation")
@pytest.mark.overall_happy_path_flow
@pytest.mark.positive
@pytest.mark.parametrize("task_details", task_details)
def test_overall_happy_path_flow(setup, task_details):
    allure.dynamic.title(f"Overall Happy Path Flow")
    allure.dynamic.description(f"This test validates the successful execution of the complete end-to-end workflow")
    driver = setup
    test_name = f"overall_happy_path_flow"
    video_path = f"videos/{test_name}.mp4"
    os.makedirs("videos", exist_ok=True)
    recorder = ScreenRecorder(filename=video_path, fps=10)
    recorder.start()
    time.sleep(2)
    test_failed = False
    with allure.step(f"Overall Happy Path Flow"):
        try:
            success = overall_happy_path_check(driver, task_details)
            assert success is True, "Overall Happy Path Flow failed."
        except Exception as e:
            test_failed = True
            time.sleep(2)
            recorder.stop()

            time.sleep(7)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_path = f"screenshots/{test_name}_{timestamp}.png"
            os.makedirs("screenshots", exist_ok=True)
            screenshot = pg.screenshot()
            screenshot.save(screenshot_path)

            allure.attach.file(screenshot_path, name="Failure Screenshot", attachment_type=allure.attachment_type.PNG)
            # if os.path.exists(video_path) and os.path.getsize(video_path) > 0:
            #     allure.attach.file(video_path,name="Failure Video",attachment_type=allure.attachment_type.MP4)
            # else:
            #     print("❌ Video missing or empty")
    
            allure.attach(str(e), name="Failure Reason", attachment_type=allure.attachment_type.TEXT)
            # pytest.fail('Failure')
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