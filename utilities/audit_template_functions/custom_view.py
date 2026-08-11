import allure
import time
import os
import json
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from utilities.other_utils_functions.highlight import highlight_element
from selenium.webdriver.common.keys import Keys


class CustomViewColumnHeaders:

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

    def template_btn(self):
        with allure.step("Click Template Button"):
            try:
                click_template_btn = self.wait.until(EC.presence_of_element_located((By.XPATH, "//span[text() ='Templates']")))
                highlight_element(self.driver, click_template_btn)
                click_template_btn.click()
            except Exception as e:
                msg = f"Failed to click Template button: {str(e)}"
                allure.attach(msg, name = 'Template Error', attachment_type = allure.attachment_type.TEXT)
                raise Exception(msg)

    def custom_view_filter(self):
        with allure.step("Click View Filter"):
            try:
                # Click View button
                custom_view_filter = self.wait.until(EC.presence_of_element_located((By.XPATH,"//button[normalize-space()='View']")))
                highlight_element(self.driver, custom_view_filter)
                custom_view_filter.click()
                time.sleep(1)
                #search column input
                search_coloumn_name = self.wait.until(EC.presence_of_element_located((By.XPATH, "//div[@data-value='Checkpoints']")))
                highlight_element(self.driver, search_coloumn_name)
                time.sleep(1)
                column_name = search_coloumn_name.text.strip()
                print(f"Colummn name: {column_name}")

                search_column_input = self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Search columns...']")))
                highlight_element(self.driver, search_column_input)
                search_column_input.send_keys(column_name)
                time.sleep(0.5)
                allure.attach(column_name, name="Searched Company name", attachment_type=allure.attachment_type.TEXT)  
                search_column_input.send_keys(Keys.CONTROL, "a")
                search_column_input.send_keys(Keys.DELETE)
                time.sleep(2)
            except Exception as e:
                msg = f"Failed to Click View Button: {str(e)}"
                allure.attach(msg, name = 'View Button Error', attachment_type = allure.attachment_type.TEXT)
                raise Exception(msg)
            
    def deselect_all_cloumns(self): 
        with allure.step("Deselecting all columns"):
            try:
                column_names = ["Created On", "Questionnaire", "Checkpoints"]
                for column_name in column_names:
                    deselect_all_columns = self.wait.until(EC.visibility_of_element_located((By.XPATH, f"//div[@role='option' and @data-value='{column_name}']")))
                    highlight_element(self.driver, deselect_all_columns)
                    deselect_all_columns.click()
                    print(f"Deselected: {column_name}")
                    time.sleep(2) 
                company_header = self.wait.until(EC.presence_of_element_located((By.XPATH, "//h2[@class='text-2xl font-bold']")))
                company_header.click()
                allure.attach(", ".join(column_names),name="Deselected Columns",attachment_type=allure.attachment_type.TEXT)
            except Exception as e:
                msg = f"Failed to Deselect all columns: {str(e)}"
                allure.attach(msg, name = 'Deselect all columns Error', attachment_type = allure.attachment_type.TEXT)
                raise Exception(msg)
    
    def fetch_column_headers(self):
        with allure.step("Fecth all visible columns headers"):
            try:
                column_headers = ["Template Name", "Assignment", "Actions"]
                for column_header in column_headers:
                    if column_header in ["Actions", "Assignment"]:
                        xpath = f"//th[@data-slot='table-head'][normalize-space()='{column_header}']"
                    else:
                        xpath = f"//th[@data-slot='table-head'][.//button[normalize-space()='{column_header}']]"
                    header = self.wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))
                    highlight_element(self.driver, header)
                allure.attach(", ".join(column_headers),name="Visible Column Headers",attachment_type=allure.attachment_type.TEXT)
            except Exception as e:
                msg = f"Failed to Fetch all visible columns headers: {str(e)}"
                allure.attach(msg, name = 'Fetch all visible columns headers Error', attachment_type = allure.attachment_type.TEXT)
                raise Exception(msg)

    def view_filter_again(self):
        with allure.step("Click View Filter"):
            try:
                # Click View button
                view_filter = self.wait.until(EC.presence_of_element_located((By.XPATH,"//button[normalize-space()='View']")))
                highlight_element(self.driver, view_filter)
                view_filter.click()
                time.sleep(1)
            except Exception as e:
                msg = f"Failed to Click View Button: {str(e)}"
                allure.attach(msg, name = 'View Button Error', attachment_type = allure.attachment_type.TEXT)
                raise Exception(msg)
    
    def select_all_cloumns(self): 
        with allure.step("selecting all columns"):
            try:
                column_names = ["Created On", "Questionnaire", "Checkpoints"]
                for column_name in column_names:
                    select_all_columns = self.wait.until(EC.visibility_of_element_located((By.XPATH, f"//div[@role='option' and @data-value='{column_name}']")))
                    highlight_element(self.driver, select_all_columns)
                    select_all_columns.click()
                    print(f"selected: {column_name}")
                    time.sleep(2) 
                company_header = self.wait.until(EC.presence_of_element_located((By.XPATH, "//h2[@class='text-2xl font-bold']")))
                company_header.click()
                allure.attach(", ".join(column_names),name="selected Columns",attachment_type=allure.attachment_type.TEXT)
            except Exception as e:
                msg = f"Failed to Select all columns: {str(e)}"
                allure.attach(msg, name = 'Select all columns Error', attachment_type = allure.attachment_type.TEXT)
                raise Exception(msg)
    
    def fetch_column_headers_again(self):
        with allure.step("Fetch all visible columns headers"):
            try:

                column_headers = ["Template Name", "Created On", "Questionnaire", "Checkpoints", "Assignment", "Actions"]
                for column_header in column_headers:
                    if column_header in ["Assignment", "Actions"]:
                        xpath = f"//th[@data-slot='table-head'][normalize-space()='{column_header}']"
                    else:
                        xpath = f"//th[@data-slot='table-head'][.//button[normalize-space()='{column_header}']]"
                    header = self.wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))
                    self.driver.execute_script("arguments[0].scrollIntoView({block:'nearest', inline:'center'});",header)
                    
                    highlight_element(self.driver, header)
                    print(f"Column headers: {column_header}")
                allure.attach(", ".join(column_headers),name="Visible Column Headers",attachment_type=allure.attachment_type.TEXT)

            except Exception as e:
                msg = f"Failed to Fetch all visible columns headers: {str(e)}"
                allure.attach(msg, name = 'Fetch all visible columns headers Error', attachment_type = allure.attachment_type.TEXT)
                raise Exception(msg)
        

        
    def custom_view_column_headers(self):
        self.click_audit()
        self.template_btn()
        self.custom_view_filter()
        self.deselect_all_cloumns()
        self.fetch_column_headers()
        self.view_filter_again()
        self.select_all_cloumns()
        self.fetch_column_headers_again()
        

        return True

                
