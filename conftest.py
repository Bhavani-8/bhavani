# conftest.py
import pytest
import sys
import os

from setup_logger import setup_logger

# logger = setup_logger("TA")
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def pytest_collection_modifyitems(config, items):
    for item in items:
        # Add module markers
        if 'test_forgot_password.py' in item.nodeid:
            item.add_marker(pytest.mark.forgot_password)
        elif 'test_login.py' in item.nodeid:
            item.add_marker(pytest.mark.login)
        elif 'test_signup.py' in item.nodeid:
            item.add_marker(pytest.mark.signup)
        elif 'test_add_task.py' in item.nodeid:
            item.add_marker(pytest.mark.add_task)
        elif 'test_special_add_task.py' in item.nodeid:
            item.add_marker(pytest.mark.special_add_task)
        elif 'test_dashboard.py' in item.nodeid:
            item.add_marker(pytest.mark.dashboard)
        elif 'test_remove_task.py' in item.nodeid:
            item.add_marker(pytest.mark.delete_task)
        elif 'test_special_dashboard.py' in item.nodeid:
            item.add_marker(pytest.mark.special_dashboard)
        elif 'test_normal_tp.py' in item.nodeid:
            item.add_marker(pytest.mark.normal_tp)
        elif 'test_special_tp.py' in item.nodeid:
            item.add_marker(pytest.mark.special_tp)
        elif 'test_notifications.py' in item.nodeid:
            item.add_marker(pytest.mark.notifications)
        elif 'test_calendar.py' in item.nodeid:
            item.add_marker(pytest.mark.calendar)
        elif 'test_compliance_history.py' in item.nodeid:
            item.add_marker(pytest.mark.compliance_history)
        elif 'test_normal_task_sections.py' in item.nodeid:
            item.add_marker(pytest.mark.normal_task_sections)
        elif 'test_special_task_sections.py' in item.nodeid:
            item.add_marker(pytest.mark.special_task_sections)
        elif 'test_updates.py' in item.nodeid:
            item.add_marker(pytest.mark.updates)
        elif 'test_project.py' in item.nodeid:
            item.add_marker(pytest.mark.project)
        elif 'test_settings.py' in item.nodeid:
            item.add_marker(pytest.mark.settings)
        elif 'test_overall_flow_path.py' in item.nodeid:
            item.add_marker(pytest.mark.overall_flow_path)
        elif 'test_notification.py' in item.nodeid:
            item.add_marker(pytest.mark.notification)
        elif 'test_audit.py' in item.nodeid:
            item.add_marker(pytest.mark.audit)


# @pytest.hookimpl(hookwrapper=True)
# def pytest_runtest_makereport(item, call):
#     """
#     Automatically log test execution status.
#     """
#     outcome = yield
#     report = outcome.get_result()

#     if report.when == "setup":
#         logger.info("=" * 100)
#         logger.info(f"STARTING TEST : {item.nodeid}")

#     elif report.when == "call":
#         if report.passed:
#             logger.info(f"TEST PASSED : {item.nodeid}")

#         elif report.failed:
#             logger.error(f"TEST FAILED : {item.nodeid}")

#         elif report.skipped:
#             logger.warning(f"TEST SKIPPED : {item.nodeid}")

#     elif report.when == "teardown":
#         logger.info(f"FINISHED TEST : {item.nodeid}")
#         logger.info("=" * 100 + "\n")