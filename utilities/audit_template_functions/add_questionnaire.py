import allure
import time
import os
import json
import random
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

class CreateQuestionnaire:

    def __init__(self, driver, wait):
        self.driver = driver
        self.wait = wait
        self.load_locators()
        self.validation_text_field = QuestionnaireTextField(self.driver,self.wait)
        self.validation_checkbox = QuestionnaireCheckboxField(self.driver,self.wait)
        self.validation_date = QuestionnaireDateField(self.driver,self.wait)
        self.validation_long_answer = QuestionnaireLongAnswer(self.driver,self.wait)
        self.validation_short_answer = QuestionnaireShortAnswer(self.driver, self.wait)
        self.validation_drop_down = QuestionnaireDropDownField(self.driver, self.wait)
        self.validation_price = QuestionnairePrice(self.driver, self.wait)
        self.validation_first_last_name = QuestionnaireFirstLastName(self.driver, self.wait)
        self.other_fields = QuestionnaireOtherFields(self.driver, self.wait)
        
        

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

    def click_add_section(self):
        with allure.step("Click Add Section button"):
            try:
                add_section_btn = self.wait.until(EC.presence_of_element_located((By.XPATH, "//button[normalize-space()='Section']")))
                highlight_element(self.driver, add_section_btn)
                add_section_btn.click()
            except Exception as e:
                msg = f"Failed to click Add Section Button : {str(e)}"
                allure.attach(msg, name="Add Section Button Error", attachment_type=allure.attachment_type.TEXT)
                raise Exception(msg)
    
    def enter_question_name(self):
        with allure.step("Enter Template Details"):
            try:
                question_section = self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@id='questionnaire_section']")))
                highlight_element(self.driver, question_section)
                unique_questionnaire_name = f"Test Automation Question {random.randint(1000, 9999)}"
                question_section.send_keys(unique_questionnaire_name)
                questionnaire_file = os.path.join("latest_data", "latest_question.txt")
                with open(questionnaire_file, "w") as f:
                    f.write(unique_questionnaire_name)
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

    def click_q_button(self):
        with allure.step("Click Q Button"):
            try:
                q_file = os.path.join("latest_data", "latest_question.txt")
                with open(q_file, "r") as f:
                    created_question_name = f.read().strip()
                q_btn = self.wait.until(EC.presence_of_element_located((By.XPATH, f"//p[starts-with(normalize-space(.), '{created_question_name}') and (substring-after(normalize-space(.), '{created_question_name}') = '' or starts-with(substring-after(normalize-space(.), '{created_question_name}'), ' '))]/parent::div//button[normalize-space(.)='Q']")))
                highlight_element(self.driver, q_btn)
                q_btn.click()

            except Exception as e:
                msg = f"failed to Click Q Button: {str(e)}"
                allure.attach(msg, name = "Q Button Error", attachment_type=allure.attachment_type.TEXT)
                raise Exception(msg) 
         

    def select_field_type(self, field_type):
        with allure.step(f"Select Field Type: {field_type}"):
            try:
                field_type_dropdown = self.wait.until(EC.presence_of_element_located((By.XPATH, "//button[@id='field_type']")))
                highlight_element(self.driver, field_type_dropdown)
                field_type_dropdown.click()
                time.sleep(1)

                select_option = self.wait.until(EC.presence_of_element_located((By.XPATH, f"//div[text()='{field_type}']")))
                
                self.driver.execute_script(
                "arguments[0].scrollIntoView({block: 'center'});", select_option
            )
                time.sleep(0.5)

                highlight_element(self.driver, select_option)
                select_option.click()

                
            except Exception as e:
                msg = f"Failed to click field type '{field_type}': {str(e)}"
                allure.attach(msg, name="Field Type Error", attachment_type=allure.attachment_type.TEXT)
                raise Exception(msg)

    def enter_description(self):
        with allure.step("Enter Description"):
            try:
                enter_desc = self.wait.until(EC.presence_of_element_located((By.XPATH, "//div[@id='general_description']//div[@contenteditable='true']")))
                highlight_element(self.driver, enter_desc)
                enter_desc.click()
                enter_desc.send_keys("Test Description")
                time.sleep(1)
            except Exception as e:
                msg = f"Failed to add description: {str(e)}"
                allure.attach(msg,name="add description Error",attachment_type=allure.attachment_type.TEXT)
                raise Exception(msg)
    
    def document_file(self):
        with allure.step("Attach Document File"):
            try:
                drag_document_file = self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='file']")))
                highlight_element(self.driver, drag_document_file)
                file_path = os.path.abspath(os.path.join("data", "dummy_use_file.pdf"))
                drag_document_file.send_keys(file_path)
                time.sleep(3)
                print(f"File selected: {file_path}")
            except Exception as e:
                msg = f"failed to Attach PDF Document File: {str(e)}"
                allure.attach(msg, name = "Attach PDF Document File Error", attachment_type=allure.attachment_type.TEXT)
                raise Exception(msg)
    
    def validation(self):
        with allure.step("Click on Validation"):
            try:
                validation_btn = self.wait.until(EC.presence_of_element_located((By.XPATH, "//button[@role='tab' and normalize-space()='Validation']")))
                highlight_element(self.driver, validation_btn)
                validation_btn.click()
                time.sleep(1)
        
            except Exception as e:
                msg = f"failed to Attach PDF Document File: {str(e)}"
                allure.attach(msg, name = "Attach PDF Document File Error", attachment_type=allure.attachment_type.TEXT)
                raise Exception(msg)

    def attachment_feild(self):
        try:
    
            attach_type_dropdown = self.wait.until(EC.presence_of_element_located((By.XPATH, "//button[@id='attachment_file_types']")))
            highlight_element(self.driver, attach_type_dropdown)
            attach_type_dropdown.click()
            time.sleep(1)

            select_option = self.wait.until(EC.presence_of_element_located((By.XPATH, f"//div[text()='PDF']")))
            highlight_element(self.driver, select_option)
            select_option.click()
            time.sleep(1)

            add_question_label = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//h2[text()='Add Questionnaire']")))
            highlight_element(self.driver, add_question_label)
            add_question_label.click()
            time.sleep(2)
        except Exception as e:
            msg = f"Failed to click Attach type': {str(e)}"
            allure.attach(msg, name="Attach Type Error", attachment_type=allure.attachment_type.TEXT)
            raise Exception(msg)

    def max_num(self, max_files="1", max_size_mb="5"):
        try:
            enter_max_num = self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Enter max files']")))
            highlight_element(self.driver, enter_max_num)
            enter_max_num.click()
            enter_max_num.send_keys(max_files)
            time.sleep(1)

            enter_max_size = self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Enter max size']")))
            highlight_element(self.driver, enter_max_size)
            enter_max_size.click()
            enter_max_size.send_keys(max_size_mb)
            
        except Exception as e:
            msg = f"Failed to Enter Maximum number': {str(e)}"
            allure.attach(msg, name="Maximum Number Error", attachment_type=allure.attachment_type.TEXT)
            raise Exception(msg)

    def radio(self):

        try:
            unique_radio = f"Test Radio: {random.randint(1000, 9999)}"
            enter_checkbox = self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Enter radio option']")))
            highlight_element(self.driver, enter_checkbox)
            enter_checkbox.click()
            enter_checkbox.send_keys(unique_radio)
            time.sleep(1)

            click_add_more = self.wait.until(EC.presence_of_element_located((By.XPATH, "//button[normalize-space()='Add More']")))
            highlight_element(self.driver, click_add_more)
            click_add_more.click()

            unique_radio2 = f"Test Radio2: {random.randint(1000, 9999)}"
            enter_checkbox2 = self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Enter radio option']")))
            highlight_element(self.driver, enter_checkbox2)
            enter_checkbox2.click()
            enter_checkbox2.send_keys(unique_radio2)
            time.sleep(1)
              
        except Exception as e:
            msg = f"Failed to Enter Radio': {str(e)}"
            allure.attach(msg, name="Enter Radio Error", attachment_type=allure.attachment_type.TEXT)
            raise Exception(msg)  

    def document_file(self):
        with allure.step("Attach PDF Document File"):
            try:
                drag_document_file = self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='file']")))
                highlight_element(self.driver, drag_document_file)
                # drag_document_file.click()
                first_file_path = os.path.abspath(os.path.join("data", "automation_file.pdf"))
                drag_document_file.send_keys(first_file_path)
                
                time.sleep(3)
                print(f"File selected: {first_file_path}")
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

    def add_questions_for_all_field_types(self, field_types=None):
        if field_types is None:
            field_types = [
                "Text Field", "Date Range", "Checkbox", "Attachment", "Date",
                "Radio", "Long Answer", "Short Answer", "Drop Down", "First/Last Name",
                "Phone Number", "Price", "Address", "URL", "PAN", "Email"
            ]

        text_entry_map = {
        "Text Field":       self.validation_text_field.add_text,
        "Date Range":       self.other_fields.add_date_range,
        "Checkbox":         self.validation_checkbox.add_checkbox,
        "Attachment":       self.other_fields.add_attachment,
        "Date":             self.validation_date.add_date,
        "Radio":            self.other_fields.add_radio,
        "Long Answer":      self.validation_long_answer.add_long_answer,
        "Short Answer":     self.validation_short_answer.add_short_answer,
        "Drop Down":        self.validation_drop_down.add_drop_down,
        "First/Last Name":  self.validation_first_last_name.add_name,
        "Phone Number":     self.other_fields.add_phone_number,
        "Price":            self.validation_price.add_price,
        "Address":          self.other_fields.add_address,
        "URL":              self.other_fields.add_url,
        "PAN":              self.other_fields.add_pan,
        "Email":            self.other_fields.add_email,   
        }

        with allure.step(f"Add questions (without validation) for field types: {field_types}"):
            for field_type in field_types:
                with allure.step(f"Add question with field type: {field_type}"):
                    try:
                        entry_fn = text_entry_map.get(field_type)
                        if entry_fn is None:
                            msg = f"No text-entry method mapped for field type '{field_type}'"
                            allure.attach(msg, name=f"{field_type} Not Implemented", attachment_type=allure.attachment_type.TEXT)
                            raise Exception(msg)

                        self.click_q_button()
                        entry_fn()
                        self.select_field_type(field_type)
                        self.enter_description()
                        self.document_file()

                        if field_type == "Attachment":
                            self.attachment_feild()
                            self.max_num()
                        
                        elif field_type == "Checkbox":
                            self.validation_checkbox.checkbox_options()
                        elif field_type == "Radio":
                            self.radio()          # this is separate from other_fields.add_radio (question text)
                        elif field_type == "Drop Down":
                            self.validation_drop_down.dropdown_options()
                        
                        self.apply_button()

                    except Exception as e:
                        msg = f"Failed processing field type '{field_type}': {str(e)}"
                        allure.attach(msg, name=f"{field_type} Loop Error", attachment_type=allure.attachment_type.TEXT)
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

    
    
    def add_questionnaire(self, field_types=None):
        self.click_audit()
        self.template_btn()
        self.edit_template_btn()
        self.click_add_section()
        self.enter_question_name()
        self.submit_btn()
        self.add_questions_for_all_field_types(field_types)
        self.done_button()
        
        

        return True

                
