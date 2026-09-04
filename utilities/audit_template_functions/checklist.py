import allure
import time
import os
import json
import random
from functools import partial
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from utilities.other_utils_functions.highlight import highlight_element
from utilities.audit_template_functions.validation_text_field import QuestionnaireTextField
from utilities.audit_template_functions.validation_checkbox import QuestionnaireCheckboxField
from utilities.audit_template_functions.validation_date import QuestionnaireDateField
from utilities.audit_template_functions.validation_long_answer import QuestionnaireLongAnswer
from utilities.audit_template_functions.validation_short_answer import QuestionnaireShortAnswer
from utilities.audit_template_functions.validation_drop_down import QuestionnaireDropDownField
from utilities.audit_template_functions.validation_price import QuestionnairePrice
from utilities.audit_template_functions.validation_first_last_name import QuestionnaireFirstLastName
from utilities.audit_template_functions.other_fields import QuestionnaireOtherFields

class CreateChecklist:

    def __init__(self, driver, wait):
        self.driver = driver
        self.wait = wait
        self.load_locators()
        

    def load_locators(self):
        try:
            with open(os.path.join("data", "locators.json"), "r") as f:
                locators = json.load(f)
            self.audit_icon = locators["audit_icon"]
            self.toast_msg = locators["toast_msg"]
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

    def edit_template_btn(self):
        with allure.step("Click Edit Template Button"):
            try:
                template_file = os.path.join("latest_data", "latest_template.txt")
                with open(template_file, "r") as f:
                    created_template_name = f.read().strip()
                edit_template_elem = self.wait.until(EC.presence_of_element_located((By.XPATH, f"//tr[.//*[contains(normalize-space(),'{created_template_name}')]]//button[.//*[contains(@class,'lucide-pencil')]]")))
                highlight_element(self.driver, edit_template_elem)
                edit_template_elem.click()
            except Exception as e:
                msg = f"Failed to click Edit Template button: {str(e)}"
                allure.attach(msg, name ="Edit Template button Error", attachment_type=allure.attachment_type.TEXT)
                raise Exception(msg)

    def click_checklist(self):
        with allure.step("Click Checklist Button"):
            try:
                checklist_btn = self.wait.until(EC.presence_of_element_located((By.XPATH, "//button[text()='Checklist']")))
                highlight_element(self.driver, checklist_btn)
                checklist_btn.click()
                time.sleep(1)
            except Exception as e:
                msg = f"Failed to click Checklist Button : {str(e)}"
                allure.attach(msg, name="checklist Button Error", attachment_type=allure.attachment_type.TEXT)
                raise Exception(msg)


    def click_add_section(self):
        with allure.step("Click Add Section button"):
            try:
                add_section_btn = self.wait.until(EC.presence_of_element_located((By.XPATH, "(//button[@type='button' and normalize-space()='Section'])[1]")))
                highlight_element(self.driver, add_section_btn)
                add_section_btn.click()
            except Exception as e:
                msg = f"Failed to click Add Section Button : {str(e)}"
                allure.attach(msg, name="Add Section Button Error", attachment_type=allure.attachment_type.TEXT)
                raise Exception(msg)
    
    def enter_question_name(self):
        with allure.step("Enter Template Details"):
            try:
                question_section = self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@id='checklist_section']")))
                highlight_element(self.driver, question_section)
                unique_questionnaire_name = f"Test Automation Checklist {random.randint(1000, 9999)}"
                question_section.send_keys(unique_questionnaire_name)
                questionnaire_file = os.path.join("latest_data", "latest_question.txt")
                with open(questionnaire_file, "w") as f:
                    f.write(unique_questionnaire_name)
                expected_checklist_section = question_section.get_attribute("value").strip()
                allure.attach(expected_checklist_section,name="Entered Checklist Name",attachment_type=allure.attachment_type.TEXT)

                print(f"Expected Checklist Name: "f"{expected_checklist_section}")
                return expected_checklist_section
            except Exception as e:
                msg = f"failed to Enter Template name: {str(e)}"
                allure.attach(msg, name = "Template name Error", attachment_type=allure.attachment_type.TEXT)
                raise Exception(msg) 
            
    def submit_btn(self):
        try:
            submit_btn = self.wait.until(EC.presence_of_element_located((By.XPATH, "(//div[@class='flex items-center flex-row gap-1']//button[@type='submit'])")))
            highlight_element(self.driver, submit_btn)
            submit_btn.click()

        except Exception as e:
            msg = f"failed to Click Submit Button: {str(e)}"
            allure.attach(msg, name = "Submit Button Error", attachment_type=allure.attachment_type.TEXT)
            raise Exception(msg) 

    def click_c_button(self):
        with allure.step("Click Q Button"):
            try:
                c_file = os.path.join("latest_data", "latest_question.txt")
                with open(c_file, "r") as f:
                    created_question_name = f.read().strip()
                c_btn = self.wait.until(EC.presence_of_element_located((By.XPATH, f"//p[starts-with(normalize-space(.), '{created_question_name}') and (substring-after(normalize-space(.), '{created_question_name}') = '' or starts-with(substring-after(normalize-space(.), '{created_question_name}'), ' '))]/parent::div//button[normalize-space(.)='C']")))
                highlight_element(self.driver, c_btn)
                c_btn.click()

            except Exception as e:
                msg = f"failed to Click Q Button: {str(e)}"
                allure.attach(msg, name = "Q Button Error", attachment_type=allure.attachment_type.TEXT)
                raise Exception(msg) 

    def add_checklist_question(self):
        with allure.step("Enter Checklist"):
            try:
                unique_text = f"Test Automation Checklist {random.randint(100, 999)}"
                enter_text = self.wait.until(EC.presence_of_element_located((By.XPATH, "//textarea[@id='check_point']")))
                highlight_element(self.driver, enter_text)
                enter_text.click()
                enter_text.send_keys(unique_text)
                expected_checkpoint_name = enter_text.get_attribute("value").strip()
                allure.attach(expected_checkpoint_name,name="Entered Checklist Name",attachment_type=allure.attachment_type.TEXT)
                print(f"Expected Checklist Name: "f"{expected_checkpoint_name}")
                return expected_checkpoint_name
            except Exception as e:
                msg = f"Failed to Enter Checklist: {str(e)}"
                allure.attach(msg,name="Checklist Error",attachment_type=allure.attachment_type.TEXT)
                raise Exception(msg)

    def select_severity(self):
        with allure.step("Select Severity"):
            try:
                severity_dropdown = self.wait.until(EC.presence_of_element_located((By.XPATH, "//button[@id='severity']")))
                highlight_element(self.driver, severity_dropdown)
                severity_dropdown.click()
                time.sleep(1)

                select_option = self.wait.until(EC.presence_of_element_located((By.XPATH, "//div[text()='Medium']")))
                highlight_element(self.driver, select_option)
                select_option.click()
                expected_severity = select_option.text.strip()
                allure.attach(expected_severity,name="Entered Checklist Name",attachment_type=allure.attachment_type.TEXT)
                
                print(f"Expected Company Category: {expected_severity}")
                return expected_severity

                
            except Exception as e:
                msg = f"Failed to click Severity: {str(e)}"
                allure.attach(msg, name="Severity Error", attachment_type=allure.attachment_type.TEXT)
                raise Exception(msg)

    def documents_relied_upon(self):
        with allure.step("Select Documents"):
            try:
                documents_dropdown = self.wait.until(EC.presence_of_element_located((By.XPATH, "//button[@id='documents_relied_upon']")))
                highlight_element(self.driver, documents_dropdown)
                documents_dropdown.click()

                select_document = self.wait.until(EC.presence_of_element_located((By.XPATH, "(//div[@data-slot='select-item'])[1]")))
                highlight_element(self.driver, select_document)
                expected_document_relied = select_document.text.strip()
                select_document.click()
                time.sleep(1)
                self.driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ESCAPE)
                # expected_document_relied = select_document.text.strip()
                allure.attach(expected_document_relied,name="Entered Checklist Name",attachment_type=allure.attachment_type.TEXT)
                                
                print(f"Selected Document : {expected_document_relied}")
                return expected_document_relied

            except Exception as e:
                msg = f"Failed to Select Document: {str(e)}"
                allure.attach(msg, name="Document Relied Upon Error", attachment_type=allure.attachment_type.TEXT)
                raise Exception(msg)

    def attachment_format(self):
        with allure.step("Select Attachment Format"):
            try:
        
                attach_format_dropdown = self.wait.until(EC.presence_of_element_located((By.XPATH, "//button[@id='attachment_format']")))
                highlight_element(self.driver, attach_format_dropdown)
                attach_format_dropdown.click()
                time.sleep(1)

                select_option = self.wait.until(EC.presence_of_element_located((By.XPATH, f"//div[@role='option' and normalize-space()='PDF']")))
                highlight_element(self.driver, select_option)
                select_option.click()
                time.sleep(1)
                self.driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ESCAPE)

            except Exception as e:
                msg = f"Failed to select Attachment type': {str(e)}"
                allure.attach(msg, name="Attach Type Error", attachment_type=allure.attachment_type.TEXT)
                raise Exception(msg)

    def enter_how_to_verify(self):
        with allure.step("Enter Description"):
            try:
                enter_desc = self.wait.until(EC.presence_of_element_located((By.XPATH, "//div[@id='how_to_verify']//div[@contenteditable='true']")))
                highlight_element(self.driver, enter_desc)
                enter_desc.click()
                enter_desc.send_keys("Test Automation Checklist Description")
                time.sleep(1)
                expected_description = enter_desc.text.strip()
                allure.attach( expected_description,name="Entered Checklist Name",attachment_type=allure.attachment_type.TEXT)
                                  
                print(f"Enter Description : {expected_description}")
                return expected_description
            except Exception as e:
                msg = f"Failed to add description: {str(e)}"
                allure.attach(msg,name="add description Error",attachment_type=allure.attachment_type.TEXT)
                raise Exception(msg)

    def penalty(self, penalty_num = '1000'):
        with allure.step("Enter Penalty"):
            try:
                enter_penalty = self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@id='penalty']")))
                highlight_element(self.driver, enter_penalty)
                enter_penalty.click()
                enter_penalty.send_keys(penalty_num)
                time.sleep(1)
                expected_penalty = enter_penalty.get_attribute("value").strip()
                allure.attach(expected_penalty,name="Entered Checklist Name",attachment_type=allure.attachment_type.TEXT)
                                  
                print(f"Enter Penalty : {expected_penalty}")
                return expected_penalty
            except Exception as e:
                msg = f"Failed to add description: {str(e)}"
                allure.attach(msg,name="add description Error",attachment_type=allure.attachment_type.TEXT)
                raise Exception(msg)
            

    def checklist_document_file(self):
        with allure.step("Attach PDF Document File"):
            try:
                
                drag_document_file = self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='file']")))
                highlight_element(self.driver, drag_document_file)
                # drag_document_file.click()
                file_path = os.path.abspath(os.path.join("data", "dummy_use_file.pdf"))
                drag_document_file.send_keys(file_path)
                time.sleep(3)
                fetch_file = self.wait.until(EC.presence_of_element_located((By.XPATH, "//p[@class='text-xs text-gray-500 line-clamp-1 grow']")))
                highlight_element(self.driver, fetch_file)
                expected_file = fetch_file.text.strip()
                allure.attach(expected_file,name="Entered Checklist Name",attachment_type=allure.attachment_type.TEXT)               
                print(f"File Selected : {expected_file}")
                return expected_file
            except Exception as e:
                msg = f"failed to Attach PDF Document File: {str(e)}"
                allure.attach(msg, name = "Attach PDF Document File Error", attachment_type=allure.attachment_type.TEXT)
                raise Exception(msg)
    
    def apply_button(self):
        with allure.step("Click Apply Button"):
            try:
                apply_button = self.wait.until(EC.presence_of_element_located((By.XPATH, "//button[text()='Apply']")))
                highlight_element(self.driver, apply_button)
                apply_button.click()
                time.sleep(1)
            except Exception as e:
                msg = f"failed to click Apply button: {str(e)}"
                allure.attach(msg, name = "Apply button Error", attachment_type=allure.attachment_type.TEXT)
                raise Exception(msg)

    def check_toast_msg(self):
        with allure.step("Verify Toast Message"):
            try:
                toast = self.wait.until(EC.presence_of_element_located((By.XPATH, self.toast_msg)))
                highlight_element(self.driver, toast)
                toast_text = toast.text.strip()
                allure.attach(toast_text,name="Toast Message Text",attachment_type=allure.attachment_type.TEXT)
                print(f"Toast Message: {toast_text}")
                time.sleep(6)

            except Exception as e:
                msg = f"Toast message not found: {str(e)}"
                print(msg)
                allure.attach(str(e), name="Toast message Error", attachment_type=allure.attachment_type.TEXT)
                raise Exception(msg)
   

    def done_button(self):
        with allure.step("Click Done Button"):
            try:
                done_button = self.wait.until(EC.presence_of_element_located((By.XPATH, "//button[text()='Done']")))
                highlight_element(self.driver, done_button)
                done_button.click()
                time.sleep(2)
            except Exception as e:
                msg = f"failed to click save button: {str(e)}"
                allure.attach(msg, name = "Save button Error", attachment_type=allure.attachment_type.TEXT)
                raise Exception(msg)
    def click_verify_checklist(self):
        with allure.step("Click Verify Checklist"):
            try:
                checkpoints_btn = os.path.join("latest_data", "latest_template.txt")
                with open(checkpoints_btn, 'r')as f:
                    created_checklist = f.read().strip()
                verify_checklist_btn = self.wait.until(EC.presence_of_element_located((By.XPATH, f"//tr[.//*[contains(normalize-space(),'{created_checklist}')]]//button[text()='Checklist']")))
                highlight_element(self.driver, verify_checklist_btn)
                verify_checklist_btn.click()
                time.sleep(2)
            except Exception as e:
                msg = f"failed to click Verify Checkist button: {str(e)}"
                allure.attach(msg, name = "Verify Checklist button Error", attachment_type=allure.attachment_type.TEXT)
                raise Exception(msg)

    def validate_checklist_details(self, expected_checklist_section, expected_checkpoint_name, expected_severity, expected_description, expected_penalty, expected_document_relied, expected_file):
        with allure.step("Validate Checklist name"):
            try:
                actual_checklist_name = self.wait.until(EC.presence_of_element_located((By.XPATH, f"//tr[.//td[normalize-space()='{expected_checklist_section}']]//td[2]")))
                highlight_element(self.driver, actual_checklist_name)
                actual_checklist_section = actual_checklist_name.text.strip()
                print(f"Expected Checklist Name     : {expected_checklist_section}")
                print(f"Actual Checklist Name       : {actual_checklist_section}")

                if expected_checklist_section !=  actual_checklist_section:
                    allure.attach(
                        f"Expected : {expected_checklist_section}\n"
                        f"Actual   : {actual_checklist_section}\n",
                        name="Checklist Name - PASS",attachment_type=allure.attachment_type.TEXT)
                    raise AssertionError(
                        f"Checkpoint mismatch. "
                        f"Expected: '{expected_checklist_section}', "
                        f"Actual: '{actual_checklist_section}'"
                                    )
                allure.attach(
                    f"Expected : {expected_checklist_section}\n"
                    f"Actual   : {actual_checklist_section}",
                    name="Checkpoint Name - PASS", attachment_type=allure.attachment_type.TEXT)

            except Exception as e:
                if not isinstance(e, AssertionError):
                    allure.attach(
                        f"Expected : {expected_checklist_section}\n"
                        f"Actual   : Not Found\n",
                        name="Checklist - FAIL",attachment_type=allure.attachment_type.TEXT)
                raise

        with allure.step("Validate Checkpoint name"):
            try:
                actual_checkpoint_name = self.wait.until(EC.presence_of_element_located((By.XPATH, f"//tr[.//td[normalize-space()='{expected_checkpoint_name}']]//td[3]")))
                highlight_element(self.driver, actual_checkpoint_name)
                actual_checkpoint = actual_checkpoint_name.text.strip()
                print(f"Expected Checkpoint Name     : {expected_checkpoint_name}")
                print(f"Actual Checkpoint Name       : {actual_checkpoint}")

                if expected_checkpoint_name !=  actual_checkpoint:

                    allure.attach(
                        f"Expected : {expected_checkpoint_name}\n"
                        f"Actual   : { actual_checkpoint}",
                        name="Checkpoint Name - FAIL",
                        attachment_type=allure.attachment_type.TEXT
                    )

                    raise AssertionError(
                        f"Checkpoint mismatch. "
                        f"Expected: '{expected_checkpoint_name}', "
                        f"Actual: '{ actual_checkpoint}'"
                    )

                allure.attach(
                    f"Expected : {expected_checkpoint_name}\n"
                    f"Actual   : { actual_checkpoint}",
                    name="Checkpoint Name - PASS", attachment_type=allure.attachment_type.TEXT)
                    

            except Exception as e:
                if not isinstance(e, AssertionError):
                    allure.attach(
                        f"Expected : {expected_checkpoint_name}\n"
                        f"Actual   : Not Found\n",
                        name="Checkpoint Name - FAIL",attachment_type=allure.attachment_type.TEXT)
                raise

        with allure.step("Validate Severity name"):
            try:
                actual_severity_name = self.wait.until(EC.presence_of_element_located((By.XPATH, f"//tr[.//td[normalize-space()='{expected_checkpoint_name}']]//td[5]")))
                highlight_element(self.driver, actual_severity_name)
                actual_severity = actual_severity_name.text.strip()
                print(f"Expected Severity Name     : {expected_severity}")
                print(f"Actual Severity Name       : {actual_severity}")

                if expected_severity != actual_severity:

                    allure.attach(
                        f"Expected : {expected_severity}\n"
                        f"Actual   : {actual_severity}",
                        name="Severity Name - FAIL",
                        attachment_type=allure.attachment_type.TEXT
                    )

                    raise AssertionError(
                        f"Severity mismatch. "
                        f"Expected: '{expected_severity}', "
                        f"Actual: '{actual_severity}'"
                    )

                allure.attach(
                    f"Expected : {expected_severity}\n"
                    f"Actual   : {actual_severity}",
                    name="Severity Name - PASS",
                    attachment_type=allure.attachment_type.TEXT
                )

            except Exception as e:
                if not isinstance(e, AssertionError):
                    allure.attach(
                        f"Expected : {expected_severity}\n"
                        f"Actual   : Not Found\n",
                        name="Severity Name - FAIL",attachment_type=allure.attachment_type.TEXT)
                raise
                
        with allure.step("Validate Decription"):
            try:
                actual_description_name = self.wait.until(EC.presence_of_element_located((By.XPATH, f"//tr[.//td[normalize-space()='{expected_description}']]//td[6]")))
                highlight_element(self.driver, actual_description_name)
                actual_description = actual_description_name.text.strip()
               
                print(f"Expected Description Name     : {expected_description}")
                print(f"Actual Description Name       : {actual_description}")

                if expected_description != actual_description:

                    allure.attach(
                        f"Expected : {expected_description}\n"
                        f"Actual   : {actual_description}",
                        name="Description Name - FAIL",
                        attachment_type=allure.attachment_type.TEXT
                    )

                    raise AssertionError(
                        f"Description mismatch. "
                        f"Expected: '{expected_description}', "
                        f"Actual: '{actual_description}'"
                    )

                allure.attach(
                    f"Expected : {expected_description}\n"
                    f"Actual   : {actual_description}",
                    name="Description Name - PASS",
                    attachment_type=allure.attachment_type.TEXT
                )

            except Exception as e:
                if not isinstance(e, AssertionError):
                    allure.attach(
                        f"Expected : {expected_description}\n"
                        f"Actual   : Not Found\n",
                        name="Description Name - FAIL",attachment_type=allure.attachment_type.TEXT)
                raise

        with allure.step("Validate Penalty"):
            try:
                actual_penalty_name = self.wait.until(EC.presence_of_element_located((By.XPATH, f"//tr[.//td[normalize-space()='{expected_penalty}']]//td[7]")))
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", actual_penalty_name)
                highlight_element(self.driver, actual_penalty_name)
                actual_penalty = actual_penalty_name.text.strip()
                print(f"Expected Penalty Name     : {expected_penalty}")
                print(f"Actual Penalty Name       : {actual_penalty}")

                if str(expected_penalty).strip() != actual_penalty:

                    allure.attach(
                        f"Expected : {expected_penalty}\n"
                        f"Actual   : {actual_penalty}",
                        name="Penalty Name - FAIL",
                        attachment_type=allure.attachment_type.TEXT
                    )

                    raise AssertionError(
                        f"Penalty mismatch. "
                        f"Expected: '{expected_penalty}', "
                        f"Actual: '{actual_penalty}'"
                    )

                allure.attach(
                    f"Expected : {expected_penalty}\n"
                    f"Actual   : {actual_penalty}",
                    name="Penalty Name - PASS",
                    attachment_type=allure.attachment_type.TEXT
                )

            except Exception as e:
                
                if not isinstance(e, AssertionError):
                    allure.attach(
                        f"Expected : {expected_penalty}\n"
                        f"Actual   : Not Found\n",
                        name="Penalty Name - FAIL",attachment_type=allure.attachment_type.TEXT)
                raise
                                
        with allure.step("Validate Documents Relied Upon"):
            try:
                actual_documents_name = self.wait.until(EC.presence_of_element_located((By.XPATH, f"//tr[.//td[normalize-space()='{expected_document_relied}']]//td[8]")))
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", actual_documents_name)
                highlight_element(self.driver, actual_documents_name)
                actual_documents_relied = actual_documents_name.text.strip()
                print(f"Expected Documents Name     : {expected_document_relied}")
                print(f"Actual Documents Name       : {actual_documents_relied}")

                if expected_document_relied != actual_documents_relied:

                    allure.attach(
                        f"Expected : {expected_document_relied}\n"
                        f"Actual   : {actual_documents_relied}",
                        name="Documents Relied Upon - FAIL",
                        attachment_type=allure.attachment_type.TEXT
                    )

                    raise AssertionError(
                        f"Documents Relied Upon mismatch. "
                        f"Expected: "
                        f"'{expected_document_relied}', "
                        f"Actual: '{actual_documents_relied}'"
                    )

                allure.attach(
                    f"Expected : {expected_document_relied}\n"
                    f"Actual   : {actual_documents_relied}",
                    name="Documents Relied Upon - PASS",
                    attachment_type=allure.attachment_type.TEXT
                )

            except Exception as e:
                if not isinstance(e, AssertionError):
                    allure.attach(
                        f"Expected : {expected_document_relied}\n"
                        f"Actual   : Not Found\n",
                        name="Documents Relied Upon - FAIL",attachment_type=allure.attachment_type.TEXT)
                raise
                                                           
        with allure.step("Validate Reference Documents"):
            try:
                ref_file = os.path.join("latest_data", "latest_question.txt")
                with open(ref_file, "r") as f:
                    created_ref_doc = f.read().strip()
                ref_doc_name = self.wait.until(EC.presence_of_element_located((By.XPATH, f"//tr[.//td[normalize-space()='{created_ref_doc}']]//td[9]")))
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", ref_doc_name)
                highlight_element(self.driver, ref_doc_name)
                ref_doc_name.click()
                actual_ref_doc_file = self.wait.until(EC.presence_of_element_located((By.XPATH, "//p[@class='text-xs text-gray-500 line-clamp-1 grow']")))
                highlight_element(self.driver, actual_ref_doc_file)
                actual_ref_doc = actual_ref_doc_file.text.strip()
                print(f"Expected Reference Name     : {expected_file}")
                print(f"Actual Reference Name       : {actual_ref_doc}")

                if expected_file != actual_ref_doc:

                    allure.attach(
                        f"Expected : {expected_file}\n"
                        f"Actual   : {actual_ref_doc}",
                        name="Reference Document - FAIL",
                        attachment_type=allure.attachment_type.TEXT
                    )

                    raise AssertionError(
                        f"Reference document mismatch. "
                        f"Expected: '{expected_file}', "
                        f"Actual: '{actual_ref_doc}'"
                    )

                allure.attach(
                    f"Expected : {expected_file}\n"
                    f"Actual   : {actual_ref_doc}",
                    name="Reference Document - PASS",
                    attachment_type=allure.attachment_type.TEXT
                )

            except Exception as e:
                if not isinstance(e, AssertionError):
                    allure.attach(
                        f"Expected : {expected_file}\n"
                        f"Actual   : Not Found\n",
                        name="Reference Document - FAIL",attachment_type=allure.attachment_type.TEXT)
                raise
                                  
      
    def add_checklist(self):
        self.click_audit()
        self.template_btn()
        self.edit_template_btn()
        self.click_checklist()
        self.click_add_section()
        expected_checklist_section = self.enter_question_name()
        self.submit_btn()
        self.click_c_button()
        expected_checkpoint_name = self.add_checklist_question()
        expected_severity = self.select_severity()
        expected_document_relied = self.documents_relied_upon()
        self.attachment_format()
        expected_description = self.enter_how_to_verify()
        expected_penalty = self.penalty()
        expected_file = self.checklist_document_file()
        self.apply_button()
        self.check_toast_msg()
        self.done_button()
        self.click_verify_checklist()
        self.validate_checklist_details(expected_checklist_section, expected_checkpoint_name, 
        expected_severity, expected_description, expected_penalty, expected_document_relied, expected_file)
        return True