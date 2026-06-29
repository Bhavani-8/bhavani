# test_add_task.py
from datetime import datetime
import pyautogui as pg
import pytest
import time
import allure
import os

from utilities.driver_setup import setup 
from utilities.special_add_task_utils import get_test_case_list, special_task_check
from utilities.screen_recorder import ScreenRecorder

at_test_case_list = get_test_case_list(module='special_add_task')

@allure.suite("Special Add Task Test Suite")
@allure.sub_suite("Special Add Task Flow")
@pytest.mark.parametrize("test_case_id,task_name,test_case_description,start_date,due_date,frequency,repeat_if_due_date_is_on_holiday,end_frequency_date,weekday_name,repeat_day_and_month,end_time,internal_deadline,assign_to,approver,cc,risk_rating,license_name,task_category,description,attach_file_name,impact_details,impact_file_name,circular_search,test_type", at_test_case_list)
def test_special_task_flow(setup, test_case_id, task_name, test_case_description, start_date, due_date, frequency, repeat_if_due_date_is_on_holiday, end_frequency_date, weekday_name, repeat_day_and_month, end_time, internal_deadline, assign_to, approver, cc, risk_rating, license_name, task_category, description, attach_file_name, impact_details, impact_file_name, circular_search, test_type):
    # allure.dynamic.title(f"Special Add Task Module: Test Execution Flow For {'Valid Case' if test_type else 'Invalid Case'}")
    # allure.dynamic.description(f"This test checks add task functionality with {'valid' if test_type else 'invalid'} information.")
    allure.dynamic.title(f"{test_case_id}_{task_name}")
    allure.dynamic.description(f'{test_case_description}')
    driver = setup
    test_name = f"add_task_{'valid' if test_type else 'invalid'}".replace(' ', 'blank')
    video_path = f"videos/{test_name}_{test_case_id}.mp4"
    os.makedirs("videos", exist_ok=True)
    recorder = ScreenRecorder(filename=video_path, fps=10)
    recorder.start()
    time.sleep(2)
    test_failed = False
    with allure.step(f"Special Add Task Flow"):
        try:
            success = special_task_check(driver, task_name, start_date, due_date, frequency, repeat_if_due_date_is_on_holiday, end_frequency_date, weekday_name, repeat_day_and_month, end_time, internal_deadline, assign_to, approver, cc, risk_rating, license_name, task_category, description, attach_file_name, impact_details, impact_file_name, circular_search, test_type)
            # assert success == test_type, f"Expected status={'Success' if test_type else 'Failure'} but got {'Success' if success else 'Failure'}"
            if test_type == 'positive':
                # assert True
                assert success, "Special Add Task failed with valid scenario"
            elif test_type == 'negative':
                assert not success, "Dashboard Special Add Task succeeded with invalid scenario"

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