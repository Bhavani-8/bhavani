# test_dashboard.py
from datetime import datetime
import pyautogui as pg
import pytest
import time
import allure
import os

from utilities.dashboard_utils import get_test_case_list, dashboard_check
from utilities.driver_setup import setup
from utilities.screen_recorder import ScreenRecorder

at_test_case_list = get_test_case_list(module='special_dashboard')

@allure.suite("Special Dashboard Test Suite")
@allure.sub_suite("Special Dashboard Validation")
@pytest.mark.parametrize("test_case_id,module_name,test_case_description,test_type", at_test_case_list)
def test_special_dashboard_flow(setup, test_case_id, module_name, test_case_description, test_type):
    # allure.dynamic.title(f"Dashboard Validation")
    # allure.dynamic.description(f"This test checks dashboard functionality.")
    allure.dynamic.title(f"{test_case_id}_{module_name}")
    allure.dynamic.description(f'{test_case_description}')
    driver = setup
    test_name = f"dashboard_validation"
    video_path = f"videos/{test_name}_{test_case_id}.mp4"
    os.makedirs("videos", exist_ok=True)
    recorder = ScreenRecorder(filename=video_path, fps=10)
    recorder.start()
    time.sleep(2)
    with allure.step(f"Special Dashboard Flow"):
        try:
            success = dashboard_check(driver, dash_type='special', module_name=module_name, test_case_id=test_case_id)
            # if success and test_type == 'positive':
            if test_type == 'positive':
                assert success, "Special Dashboard failed with valid scenario"
            elif test_type == 'negative':
                assert not success, "Special Dashboard succeeded with invalid scenario"
        except Exception as e:
            time.sleep(2)
            recorder.stop()

            time.sleep(7)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_path = f"screenshots/{test_name}_{timestamp}.png"
            os.makedirs("screenshots", exist_ok=True)
            time.sleep(0.5)
            screenshot = pg.screenshot()
            screenshot.save(screenshot_path)

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
