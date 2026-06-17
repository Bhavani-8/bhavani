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
@pytest.mark.parametrize("test_case_id,module_name,test_case_description,test_type,task_details", at_test_case_list)
def test_dashboard_flow(setup, test_case_id, module_name, test_case_description, test_type, task_details):
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
            time.sleep(2)
            recorder.stop()

            time.sleep(7) 
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_path = f"screenshots/{test_name}_{timestamp}.png"
            os.makedirs("screenshots", exist_ok=True)
            time.sleep(0.5)
            driver.save_screenshot(screenshot_path) 


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

# at_test_case_list = get_test_case_list(module='dashboard')
# @allure.suite("Dashboard Test Suite")
# @allure.sub_suite("Dashboard Validation")
# @pytest.mark.parametrize("test_case_id,module_name,test_case_description,test_type", at_test_case_list)
# def test_dashboard_flow(setup, test_case_id, module_name, test_case_description, test_type):

#     allure.dynamic.title(f"{test_case_id}_{module_name}")
#     allure.dynamic.description(f'{test_case_description}')

#     driver = setup
#     test_name = f"dashboard_validation"

#     # 🎥 Create recorder
#     video_path = f"videos/{test_name}_{test_case_id}.mp4"
#     os.makedirs("videos", exist_ok=True)

   
#     recorder = ScreenRecorder(filename=video_path, fps=10)
#     recorder.start()

#     try:
#         with allure.step("Dashboard Flow"):
#             success = dashboard_check(driver, dash_type='QCC', module_name=module_name, test_case_id=test_case_id)

#             if test_type == 'positive':
#                 assert success, "Dashboard failed with valid scenario"
#             elif test_type == 'negative':
#                 assert not success, "Dashboard succeeded with invalid scenario"

#     except Exception as e:
#         recorder.stop()   # ✅ stop immediately on failure

#         time.sleep(3)     # give time to finalize video

#         # 📸 Screenshot
#         timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
#         screenshot_path = f"screenshots/{test_name}_{timestamp}.png"
#         os.makedirs("screenshots", exist_ok=True)

#         screenshot = pg.screenshot()
#         screenshot.save(screenshot_path)

#         allure.attach.file(
#             screenshot_path,
#             name="Failure Screenshot",
#             attachment_type=allure.attachment_type.PNG
#         )

#         # 🎥 Attach video ONLY on failure
#         if os.path.exists(video_path) and os.path.getsize(video_path) > 0:
#             with open(video_path, "rb") as f:
#                 allure.attach(
#                     f.read(),
#                     name="Failure Video",
#                     attachment_type=allure.attachment_type.MP4
#                 )

#         # 📝 Error
#         allure.attach(str(e), name="Failure Reason", attachment_type=allure.attachment_type.TEXT)

#         pytest.fail(f"Failure reason: {e}")

#     finally:
#         # ✅ Stop recorder if not already stopped
#         try:
#             recorder.stop()
#         except:
#             pass

#         # 🔗 Always attach URL
#         allure.attach(
#             driver.current_url,
#             name="Final URL",
#             attachment_type=allure.attachment_type.TEXT
#         )