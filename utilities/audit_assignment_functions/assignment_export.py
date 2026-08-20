import allure
import time
import os
import json
import random
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from utilities.other_utils_functions.highlight import highlight_element


class AssignExportData:

    def __init__(self, driver, wait):
        self.driver = driver
        self.wait = wait
        self.load_locators()

    def load_locators(self):
        try:
            with open(os.path.join("data", "locators.json"), "r") as f:
                locators = json.load(f)
            self.audit_icon = locators["audit_icon"]

        except FileNotFoundError as e:
            allure.attach(str(e),name="Locators File Missing",attachment_type=allure.attachment_type.TEXT)
            raise
        
        except json.JSONDecodeError as e:
            allure.attach(str(e),name="Invalid JSON",attachment_type=allure.attachment_type.TEXT)
            raise


    def click_audit(self):
        with allure.step("Click Audit"):
            try:
                audit_btn = self.wait.until(EC.presence_of_element_located((By.XPATH, self.audit_icon)))
                highlight_element(self.driver, audit_btn)
                audit_btn.click()
            except Exception as e:
                msg = f"Failed to click Audit Icon: {str(e)}"
                allure.attach(msg, name = "Audit Icon Error", attachment_type = allure.attachment_type.TEXT)
                raise Exception(msg)

    def click_assignment(self):
        with allure.step("Click Assignment"):
            try:
                audit_assignment_btn = self.wait.until(EC.presence_of_element_located((By.XPATH, "//span[text() = 'Assignments']")))
                highlight_element(self.driver, audit_assignment_btn)
                audit_assignment_btn.click()
            except Exception as e:
                msg = f"Failed to click Assignment button: {str(e)}"
                allure.attach(msg, name = 'Audit Assignment Error', attachment_type = allure.attachment_type.TEXT)
                raise Exception(msg)

    def click_assign_export(self):
        with allure.step("Assign Export All Data"):
            try:
                assign_export_data_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, "(//button[@data-slot='dropdown-menu-trigger'])[1]")))
                highlight_element(self.driver, assign_export_data_btn)
                # self.driver.execute_script("arguments[0].click();", audit_export_data_btn)
                assign_export_data_btn.click()
                time.sleep(2)
                export_all = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//div[text()='Export all data']")))
                export_all.click()
                print("Assign Exported All Data")
                time.sleep(3)
            except Exception as e:
                msg = f"Failed to Assign export all data: {str(e)}"
                allure.attach(str(e), name="Assign Export_All_Error", attachment_type=allure.attachment_type.TEXT)
                raise Exception(msg)

    def select_all_rows(self):
        with allure.step("Select all rows"):
            try:
                dash_col_all_selection_btn_elem = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//th//span[@role='checkbox']")))
                highlight_element(self.driver, dash_col_all_selection_btn_elem)
                dash_col_all_selection_btn_elem.click()
                print("✅ Selected all rows in Dashboard")
                time.sleep(3)
            except Exception as e:
                msg = f"Failed to select all rows: {str(e)}"
                allure.attach(str(e), name="Select_All_Error", attachment_type=allure.attachment_type.TEXT)
                raise Exception(msg)
        
    def selected_rows(self):
        with allure.step("Export Selected Rows after selecting rows"):
            try:
                time.sleep(2)
                export_data_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, "(//button[@data-slot='dropdown-menu-trigger'])[1]")))
                export_data_btn.click()
                time.sleep(2)
                export_selected_rows = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@role='menuitem' and contains(text(),'Export selected rows')]")))
                export_selected_rows.click()
                print("✅ Exported Selected Rows (after selecting rows)")
                time.sleep(3)
                return True
            except Exception as e:
                msg = f"Failed to export selected rows after selection: {str(e)}"
                allure.attach(str(e), name="Export_Selected_After", attachment_type=allure.attachment_type.TEXT)
                raise Exception(msg)
        
        
    def assign_export_data(self):
        self.click_audit()
        self.click_assignment()
        self.click_assign_export()
        self.select_all_rows()
        self.selected_rows()

        return True

                
