# test_dashboard.py
from datetime import datetime
import pyautogui as pg
import pytest
import time
import allure
import os

# from utilities.add_task_utils import get_test_case_list, add_task_check
from utilities.dashboard_utils import get_test_case_list, dashboard_check
from utilities.driver_setup import setup
from utilities.screen_recorder import ScreenRecorder

at_test_case_list = get_test_case_list(module='dashboard')

@allure.suite("Dashboard Test Suite")
@allure.sub_suite("Dashboard Validation")
@pytest.mark.parametrize("test_case_id,module_name,test_case_description,test_type,task_details,test_case_execution", at_test_case_list)
def test_dashboard_flow(setup, test_case_id, module_name, test_case_description, test_type, task_details, test_case_execution):
    # allure.dynamic.title(f"Dashboard Validation")
    allure.dynamic.title(f"{test_case_id}_{module_name}")
    allure.dynamic.description(f'{test_case_description}')
    driver = setup

    test_name = f"dashboard_validation"
    video_path = f"videos/{test_name}_{test_case_id}.mp4"
    os.makedirs("videos", exist_ok=True)
    recorder = ScreenRecorder(filename=video_path, fps=10)
    recorder.start()
    time.sleep(2)
    test_failed = False

    with allure.step(f"Dashboard Flow"):
        try:
            
            success = dashboard_check(driver, dash_type='QCC', module_name=module_name, test_case_id=test_case_id, task_details=task_details)
            # if success and test_type == 'positive':
            if test_type == 'positive':
                # assert True
                assert success, "Dashboard failed with valid scenario"
            elif test_type == 'negative':
                assert not success, "Dashboard succeeded with invalid scenario"

        except Exception as e:
            test_failed = True
            time.sleep(4) 
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_path = f"screenshots/{test_name}_{timestamp}.png"
            os.makedirs("screenshots", exist_ok=True)
            time.sleep(1)
            driver.save_screenshot(screenshot_path) 


            # ✅ Attach to Allure report
            allure.attach.file(screenshot_path, name="Failure Screenshot", attachment_type=allure.attachment_type.PNG)
    
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