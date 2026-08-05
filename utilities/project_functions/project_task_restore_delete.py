
import allure
import json
import os
import time
import pandas as pd
import random
from utilities.add_task_functions.add_task_common import task_value_store
from utilities.add_task_functions.add_task_common import task_value_get
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from utilities.other_utils_functions.highlight import highlight_element
from utilities.add_task_utils import wait_for_loader_to_disappear
from utilities.add_task_functions.format_time_if_valid import format_time_if_valid
from utilities.add_task_functions.format_date_if_valid import format_date_if_valid
from utilities.add_task_utils import add_task_check

   
def project_task_restore_delete(driver, wait):

    with allure.step("Load locators.json"):
        try:
            with open(os.path.join("data", "locators.json"), "r") as f:
                elements_details = json.load(f)

            project_icon = elements_details["project_icon"]
            toast_msg = elements_details['toast_msg']
            trash_icon = elements_details['trash_icon']
            milestone_cancel_btn = elements_details['milestone_cancel_btn']
            add_new_task = elements_details['add_new_task']
            project_next_btn = elements_details['project_next_btn']
            task_delete_btn = elements_details['task_delete_btn']
            all_tasks_tab = elements_details['all_tasks_tab']

            print("✅ locators.json loaded")
        except FileNotFoundError as e:
            msg = f"locators.json file not found: {str(e)}"
            print(msg)
            allure.attach(msg, name="Locators File Missing", attachment_type=allure.attachment_type.TEXT)
            return False
        except json.JSONDecodeError as e:
            msg = f"Invalid JSON in locators.json: {str(e)}"
            print(msg)
            allure.attach(msg, name="Locators JSON Error", attachment_type=allure.attachment_type.TEXT)
            return False
        
    with allure.step("Click project icon"):
        try:
            driver.refresh()
            wait_for_loader_to_disappear(driver, wait)
            project_btn = wait.until(EC.presence_of_element_located((By.XPATH, project_icon)))
            highlight_element(driver, project_btn)
            project_btn.click()
            time.sleep(2)
        except Exception as e:
            msg = f"Failed to Click Project Icon: {str(e)}"
            print(msg)
            allure.attach(msg, name="Project Icon Error", attachment_type=allure.attachment_type.TEXT)
            raise Exception(msg)
    with allure.step("Click Project Task"):
        try:
            time.sleep(1)
            project_file = os.path.join("latest_data", "latest_project.txt")
            with open(project_file, "r") as f:
                created_project_name = f.read().strip()
            project_task = wait.until(EC.presence_of_element_located((By.XPATH, f"//div[@class='w-full truncate' and contains(@title,'{created_project_name}')]")))
            driver.execute_script("arguments[0].scrollIntoView({block:'center', inline:'center'});", project_task)
            highlight_element(driver, project_task)
            project_task.click()
            time.sleep(2)
        except Exception as e:
            msg = f"Failed to Click Project Task: {str(e)}"
            print(msg)
            allure.attach(msg, name="Project Task Error", attachment_type=allure.attachment_type.TEXT)
            raise Exception(msg)
    with allure.step("Click 'Add new task' button"):
        try:
            add_new_task_btn = wait.until(EC.presence_of_element_located((By.XPATH, add_new_task)))
            highlight_element(driver, add_new_task_btn)
            add_new_task_btn.click()
            time.sleep(1)
        except Exception as e:
            msg = f"Failed to Click Add new task button: {str(e)}"
            print(msg)
            allure.attach(msg, name="Add new task button Error", attachment_type=allure.attachment_type.TEXT)
            raise Exception(msg)
    with allure.step("Click 'Next' button"):
        try:
            next_btn = wait.until(EC.presence_of_element_located((By.XPATH, project_next_btn)))
            highlight_element(driver, next_btn)
            next_btn.click()
            print("✅ Project Submit clicked")
        except Exception as e:
            msg = f"Failed to Click 'Next' button: {str(e)}"
            print(msg)
            allure.attach(msg, name="'Next' button Error", attachment_type=allure.attachment_type.TEXT)
            raise Exception(msg)

    test_case_details = pd.read_excel(os.path.join("data", "test_case_selector.xlsx"), sheet_name=f"add_task_test_cases").fillna("")
    # test_case_details = pd.read_excel(os.path.join("data", "test_case_selector.xlsx")).fillna("")
    first_row = test_case_details.iloc[0]
    task_name = (f"{first_row.get('task_name')}_delete_{random.randint(100000, 999999)}")
    # task_name = project_task_name if project_task_name else "task_name"
    start_date = format_date_if_valid(first_row.get('start_date'))
    due_date = format_date_if_valid(first_row.get('due_date'))
    frequency = first_row.get('frequency')
    repeat_if_holiday = first_row.get('repeat_if_holiday')
    end_freq_date = first_row.get('end_freq_date')
    repeat_weekday = first_row.get('repeat_weekday')
    repeat_day_month = first_row.get('repeat_day_month')
    # end_time = first_row.get('end_time')
    end_time = format_time_if_valid(first_row.get('end_time')) if pd.notna(first_row.get('end_time')) else None
    internal_deadline = first_row.get('internal_deadline')
    assign_to = first_row.get('assign_to')
    approver = first_row.get('approver')
    cc = first_row.get('cc')
    risk_rating = first_row.get('risk_rating')
    license_name = first_row.get('license_name')
    description = first_row.get('description')
    attach_file_name= first_row.get('attach_file_name')
    impact_details = first_row.get('impact_details')
    impact_file_name = first_row.get('impact_file_name')
    circular_search = first_row.get('circular_search')
    test_type = first_row.get('test_type')

    with allure.step("Create Task"):
        try:
            if add_task_check(driver, task_name, start_date, due_date, frequency, repeat_if_holiday, end_freq_date,
                repeat_weekday, repeat_day_month, end_time, internal_deadline, assign_to, approver, cc,
                risk_rating, license_name, description, attach_file_name, impact_details, impact_file_name,
                circular_search, test_type, task_type='mandatory', direct_task_creation=True):
                print("✅ Task creation successful")
                task_name = task_value_get("task_name")
                print(f"Generated Unique Task Name: {task_name}")
                # return True
            else:
                allure.attach("Test case failed for Task Creation", name="Task Creation Validation Failed", attachment_type=allure.attachment_type.TEXT)
                return False
        except Exception as e:
            allure.attach(str(e), name="Add Task Error", attachment_type=allure.attachment_type.TEXT)
    with allure.step("Verify Project Task Creation"):
        try:
            time.sleep(3)
            task_name_element = wait.until(EC.visibility_of_element_located((By.XPATH, f"//div[contains(text(),'{task_name}')]")))
            highlight_element(driver, task_name_element)
            fetch_task_name = task_name_element.text.strip()
            print(f"✅ Task '{fetch_task_name}' created successfully")
        except Exception as e:
            msg = f"Failed to Verify Project Task Creation: {str(e)}"
            print(msg)
            allure.attach(msg, name="Verify Project Task Creation Error", attachment_type=allure.attachment_type.TEXT)
            raise Exception(msg)
    with allure.step("Click three dots menu"):
        try:
            three_dots_btn = wait.until(EC.presence_of_element_located((By.XPATH, f"//tr[contains(@class,'dx-data-row')][.//div[contains(@class,'font-weight-normal') and @title='{task_name}']]//button")))
            driver.execute_script("arguments[0].scrollIntoView({block:'center', inline:'center'});", three_dots_btn)
            highlight_element(driver, three_dots_btn)
            three_dots_btn.click()
            time.sleep(0.5)
        except Exception as e:
            msg = f"Failed to Click Project task three dots button: {str(e)}"
            print(msg)
            allure.attach(msg, name="Project task three dots button Error", attachment_type=allure.attachment_type.TEXT)
            raise Exception(msg)
    with allure.step("Click Delete Task"):
        try:
            delete_btn = wait.until(EC.presence_of_element_located((By.XPATH, task_delete_btn)))
            highlight_element(driver, delete_btn)
            delete_btn.click()
            print("🗑️ Delete button clicked")

            yes_btn = wait.until(EC.presence_of_element_located((By.XPATH,"//button//span[text()='Yes']")))
            highlight_element(driver, yes_btn)
            yes_btn.click()
            time.sleep(2)
            print("☑️ YES clicked — Task delete confirmed")

        except Exception as e:
            msg = f"Failed to Click Delete button: {str(e)}"
            print(msg)
            allure.attach(msg, name="Delete button Error", attachment_type=allure.attachment_type.TEXT)
            raise Exception(msg)
    
   
    with allure.step("Click Milestone close button on task details panel"):
        try:
            milestone_close_btn = wait.until(EC.presence_of_element_located((By.XPATH, milestone_cancel_btn)))
            highlight_element(driver, milestone_close_btn)
            milestone_close_btn.click()
            time.sleep(2)
            print("✅ Milestone Submit clicked")
        except Exception as e:
            msg = f"Failed to Click Milestone close button: {str(e)}"
            print(msg)
            allure.attach(msg, name="Milestone close button Error", attachment_type=allure.attachment_type.TEXT)
            raise Exception(msg)
    with allure.step("Click Trash Icon"):
        try:
            print()
            trash_btn = wait.until(EC.presence_of_element_located((By.XPATH, trash_icon)))
            highlight_element(driver, trash_btn)
            trash_btn.click()
            print("🗑️ Trash icon clicked")

        except Exception as e:
            msg = f"Failed to Click Thrash Icon: {str(e)}"
            print(msg)
            allure.attach(msg, name="Thrash Icon Error", attachment_type=allure.attachment_type.TEXT)
            raise Exception(msg)
    with allure.step("Click Tasks Tab"):
        try:
            time.sleep(3)
            tasks_tab = wait.until(EC.presence_of_element_located((By.XPATH, all_tasks_tab)))
            highlight_element(driver, tasks_tab)
            tasks_tab.click()
            print("📌 Tasks tab clicked")

        except Exception as e:
            msg = f"Failed to Click Task Tab: {str(e)}"
            print(msg)
            allure.attach(msg, name="Task Tab Error", attachment_type=allure.attachment_type.TEXT)
            raise Exception(msg)
    
    with allure.step("Verify Project Task in Trash"):
        try:
            task_name_elem = wait.until(EC.visibility_of_element_located((By.XPATH, f"//span[@title='{task_name}']")))
            highlight_element(driver, task_name_elem)
            fetch_task_name_elem = task_name_elem.text.strip()
            print(f"✅ Task '{fetch_task_name_elem}' found in Trash")
        except Exception as e:
            msg = f"Failed to Verify Deleted Task: {str(e)}"
            print(msg)
            allure.attach(msg, name="Deleted Task Error", attachment_type=allure.attachment_type.TEXT)
            raise Exception(msg)
    with allure.step("Click Restore Task"):
        try:
            time.sleep(3)
            restore_elem = wait.until(EC.presence_of_element_located((By.XPATH, f"//tr[@data-slot='table-row'][.//span[@title='{task_name}']]//button[@title='Restore Task']")))
            highlight_element(driver, restore_elem)
            restore_elem.click()
            time.sleep(3)
            print("📌 Restore Task button clicked")

        except Exception as e:
            msg = f"Failed to Click Restore Button: {str(e)}"
            print(msg)
            allure.attach(msg, name="Restore Button Error", attachment_type=allure.attachment_type.TEXT)
            raise Exception(msg)

    with allure.step("Click project icon"):
        try:
            project_btn = wait.until(EC.presence_of_element_located((By.XPATH, project_icon)))
            highlight_element(driver, project_btn)
            project_btn.click()
            time.sleep(2)
        except Exception as e:
            msg = f"Failed to Click Project Icon: {str(e)}"
            print(msg)
            allure.attach(msg, name="Project Icon Error", attachment_type=allure.attachment_type.TEXT)
            raise Exception(msg)

    with allure.step("Click Project Task"):
        try:
            time.sleep(1)
            project_file = os.path.join("latest_data", "latest_project.txt")
            with open(project_file, "r") as f:
                created_project_name = f.read().strip()
            project_task = wait.until(EC.presence_of_element_located((By.XPATH, f"//div[@class='w-full truncate' and contains(@title,'{created_project_name}')]")))
            driver.execute_script("arguments[0].scrollIntoView({block:'center', inline:'center'});", project_task)
            highlight_element(driver, project_task)
            project_task.click()
            time.sleep(2)
        except Exception as e:
            msg = f"Failed to Click newly created Project task: {str(e)}"
            print(msg)
            allure.attach(msg, name="newly created Project task Error", attachment_type=allure.attachment_type.TEXT)
            raise Exception(msg)
    
    with allure.step("Click project task three dots menu"):
        try:
            three_dots_btn = wait.until(EC.presence_of_element_located((By.XPATH, f"//tr[contains(@class,'dx-data-row')][.//div[contains(@class,'font-weight-normal') and @title='{task_name}']]//button")))
            driver.execute_script("arguments[0].scrollIntoView({block:'center', inline:'center'});", three_dots_btn)
            highlight_element(driver, three_dots_btn)
            three_dots_btn.click()
            time.sleep(1)
        except Exception as e:
            msg = f"Failed to Click project task three dots menu: {str(e)}"
            print(msg)
            allure.attach(msg, name="project task three dots menu Error", attachment_type=allure.attachment_type.TEXT)
            raise Exception(msg)
    with allure.step("Click Delete Task"):
        try:
            delete_btn = wait.until(EC.presence_of_element_located((By.XPATH, task_delete_btn)))
            highlight_element(driver, delete_btn)
            delete_btn.click()
            print("🗑️ Delete button clicked")

            yes_btn = wait.until(EC.presence_of_element_located((By.XPATH,"//button//span[text()='Yes']")))
            highlight_element(driver, yes_btn)
            yes_btn.click()
            time.sleep(3)
            print("☑️ YES clicked — Task delete confirmed")

        except Exception as e:
            msg = f"Failed to Click Delete button: {str(e)}"
            print(msg)
            allure.attach(msg, name="Delete button Error", attachment_type=allure.attachment_type.TEXT)
            raise Exception(msg)
    with allure.step("Click Milestone close button on task details"):
        try:
            milestone_close_btn = wait.until(EC.presence_of_element_located((By.XPATH, milestone_cancel_btn)))
            highlight_element(driver, milestone_close_btn)
            milestone_close_btn.click()
            print("✅ Milestone Submit clicked")
        except Exception as e:
            msg = f"Failed to Click Milestone close button: {str(e)}"
            print(msg)
            allure.attach(msg, name="Milestone close button Error", attachment_type=allure.attachment_type.TEXT)
            raise Exception(msg)
    return True