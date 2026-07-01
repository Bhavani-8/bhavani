# test_updates.py
from datetime import datetime
import pyautogui as pg
import pytest
import time
import allure
import os

from selenium.webdriver.support.ui import WebDriverWait
from utilities.compliance_history import get_test_case_list, compliance_history_check
from utilities.driver_setup import setup
from utilities.screen_recorder import ScreenRecorder

at_test_case_list = get_test_case_list(module='compliance_history')
@allure.suite("Compliance History Test Suite")
@allure.sub_suite("Compliance History Validation")
@pytest.mark.parametrize("test_case_id,module_name,test_case_description,test_type", at_test_case_list)
def test_compliance_history_flow(setup, test_case_id, module_name, test_case_description, test_type):
    allure.dynamic.title(f"{test_case_id}_{module_name}")
    allure.dynamic.description(f'{test_case_description}')
    driver = setup
    # wait = WebDriverWait(driver, 30)
    test_name = f"compliance_history_validation"
    video_path = f"videos/{test_name}_{test_case_id}.mp4"
    os.makedirs("videos", exist_ok=True)
    recorder = ScreenRecorder(filename=video_path, fps=10)
    recorder.start()
    time.sleep(2)
    test_failed = False
    with allure.step(f"Compliance History Flow"):
        try:
            success = compliance_history_check(driver, module_name=module_name, test_case_id=test_case_id)
            # if success and test_type == 'positive':
            if test_type == 'positive':
                # assert True
                   assert success, "Compliance History failed with valid scenario"
            elif test_type == 'negative':
                assert not success, "Compliance History succeeded with invalid scenario"
        except Exception as e:
            test_failed = True
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