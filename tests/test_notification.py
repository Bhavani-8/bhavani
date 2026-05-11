import pytest
import allure
import os
import time
from datetime import datetime
import pyautogui as pg

from utilities.driver_setup import setup
from utilities.notification_utils import get_test_case_list, notifications_check
from utilities.screen_recorder import ScreenRecorder

at_test_case_list = get_test_case_list(module='notification')

@allure.suite("Notification Test Suite")
@allure.sub_suite("Notification Validation")
@pytest.mark.parametrize("test_case_id, module_name, test_case_description, test_type", at_test_case_list)
def test_notifications_flow(setup, test_case_id, module_name, test_case_description, test_type):
    
    allure.dynamic.title(f"{test_case_id}_{module_name}")
    allure.dynamic.description(f"{test_case_description}")
    
    driver = setup
    test_name = f"notification_validation"
    
    video_path = f"videos/{test_name}_{test_case_id}.mp4"
    os.makedirs("videos", exist_ok=True)
    recorder = ScreenRecorder(filename=video_path, fps=10)
    recorder.start()
    time.sleep(2)
    

    with allure.step("Notification Flow"):
        try:
            
            success = notifications_check(driver, module_name=module_name, test_case_id=test_case_id)
    
            if test_type == 'positive':
                # assert True
                assert success, "Dashboard failed with valid scenario"
            elif test_type == 'negative':
                assert not success, "Dashboard succeeded with invalid scenario"

        except Exception as e:
            time.sleep(2)
            recorder.stop()

            time.sleep(7)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            os.makedirs("screenshots", exist_ok=True)
            screenshot_path = f"screenshots/{test_name}_{timestamp}.png"
            time.sleep(0.5)
            pg.screenshot().save(screenshot_path)

            allure.attach.file(screenshot_path, name="Failure Screenshot", attachment_type=allure.attachment_type.PNG)
            if os.path.exists(video_path) and os.path.getsize(video_path) > 0:
                allure.attach.file(video_path,name="Failure Video",attachment_type=allure.attachment_type.MP4)
            else:
                print("❌ Video missing or empty")
    
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
