from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import allure 
import os
import json
import pytest
import time
from datetime import datetime
from utilities.other_utils_functions.highlight import highlight_element


def check_filters(driver, wait):
    
    with allure.step("Load locators.json"):
        try:
            with open(os.path.join("data", 'locators.json'), 'r') as f:
                elements_details = json.load(f)
                update_filter_btn = elements_details['update_filter_btn']
                issuer_btn = elements_details['issuer_btn']
                select_first_issuer = elements_details['select_first_issuer']
                filter_label = elements_details['filter_label']
                industry_btn = elements_details['industry_btn']
                select_first_industry = elements_details['select_first_industry']
                select_topic = elements_details['select_topic']
                select_first_topic = elements_details['select_first_topic']
                select_status = elements_details['select_status']
                select_first_status = elements_details['select_first_status']
                from_date = elements_details['from_date']
                to_date = elements_details['to_date']
                view_update = elements_details['view_update']
                fetch_applied_issuer_elem = elements_details['fetch_applied_issuer_elem']
                fetch_applied_industry_elem = elements_details['fetch_applied_industry_elem']
                fetch_applied_topic_elem = elements_details['fetch_applied_topic_elem'] 
                rest_all_btn = elements_details['rest_all_btn'] 
                fetch_applied_status_elem = elements_details['fetch_applied_status_elem']


            print("✅ locators.json loaded successfully")
        except Exception as e:
            allure.attach(str(e), name="Locators Error", attachment_type=allure.attachment_type.TEXT)
            pytest.fail("Failed to load locators.json")

    with allure.step("Select Update Checkbox"):
        try:
            filters_btn = wait.until(EC.presence_of_element_located((By.XPATH, update_filter_btn)))
            highlight_element(driver, filters_btn)
            filters_btn.click()
            print("🟦 First checkbox clicked")
            time.sleep(2)
        except Exception as e:
            allure.attach(str(e), name="Updates Section Error", attachment_type=allure.attachment_type.TEXT)
            return False
    
    with allure.step("Click on Select Issuer Dropdown"):
        try:
            select_issuer = wait.until(EC.element_to_be_clickable((By.XPATH, issuer_btn)))
            highlight_element(driver, select_issuer)
            select_issuer.click()
            time.sleep(2)
            print("🟦 Select Issuer clicked")
        except Exception as e:
            allure.attach(str(e), name="Select Issuer Error", attachment_type=allure.attachment_type.TEXT)
            return False
        
        try :
            select_first_issuer = wait.until(EC.element_to_be_clickable((By.XPATH, select_first_issuer)))
            highlight_element(driver, select_first_issuer)  
            fetch_issuer_name = select_first_issuer.text
            select_first_issuer.click()
            time.sleep(1)
            print(f"🟦 First issuer selected: {fetch_issuer_name}")
            allure.attach(f"Issuer: {fetch_issuer_name}",name="Selected Issuer",attachment_type=allure.attachment_type.TEXT)
            filters_label = wait.until(EC.element_to_be_clickable((By.XPATH, filter_label))) 
            filters_label.click()
            time.sleep(2)     
        except Exception as e:
            allure.attach(str(e), name="Select First Issuer Error", attachment_type=allure.attachment_type.TEXT)
            return False     

    with allure.step("Click on Select Industry Dropdown"):
        try:
            select_industry = wait.until(EC.element_to_be_clickable((By.XPATH, industry_btn)))
            highlight_element(driver, select_industry)
            select_industry.click()
            time.sleep(2)
            print("🟦 Select Industry clicked")
        except Exception as e:
            allure.attach(str(e), name="Select Industry Error", attachment_type=allure.attachment_type.TEXT)
            return False
        
        try :
            select_first_industry = wait.until(EC.element_to_be_clickable((By.XPATH, select_first_industry)))
            highlight_element(driver, select_first_industry)
            fetch_industry_name = select_first_industry.text  
            select_first_industry.click()
            time.sleep(1)
            print(f"🟦 First industry selected: {fetch_industry_name}")
            allure.attach(f"Industry: {fetch_industry_name}",name="Selected Industry",attachment_type=allure.attachment_type.TEXT)
            filters_label = wait.until(EC.element_to_be_clickable((By.XPATH, filter_label))) 
            filters_label.click()
            time.sleep(2)     
        except Exception as e:
            allure.attach(str(e), name="Select First Industry Error", attachment_type=allure.attachment_type.TEXT)
            return False 
    
    with allure.step("Click on Select Topic Dropdown"):
        try:
            select_topic = wait.until(EC.element_to_be_clickable((By.XPATH, select_topic)))
            highlight_element(driver, select_topic)
            select_topic.click()
            time.sleep(2)
            print("🟦 Select Topic clicked")
        except Exception as e:
            allure.attach(str(e), name="Select Topic Error", attachment_type=allure.attachment_type.TEXT)
            return False
        
        try :
            select_first_topic = wait.until(EC.element_to_be_clickable((By.XPATH, select_first_topic)))
            highlight_element(driver, select_first_topic)  
            fetch_topic_name = select_first_topic.text
            select_first_topic.click()
            time.sleep(1)
            print(f"🟦 First topic selected: {fetch_topic_name}")
            allure.attach(f"Topic: {fetch_topic_name}",name="Selected Topic",attachment_type=allure.attachment_type.TEXT)
            filters_label = wait.until(EC.element_to_be_clickable((By.XPATH, filter_label))) 
            filters_label.click()
            time.sleep(2)     
        except Exception as e:
            allure.attach(str(e), name="Select First Topic Error", attachment_type=allure.attachment_type.TEXT)
            return False 
    
    with allure.step("Click on Select Status"):
        try:
            status_dropdown = wait.until(EC.element_to_be_clickable((By.XPATH, select_status)))
            highlight_element(driver,  status_dropdown)
            status_dropdown.click()
            time.sleep(2)
            print("🟦 Select Topic clicked")
        except Exception as e:
            allure.attach(str(e), name="Select Satus Error", attachment_type=allure.attachment_type.TEXT)
            return False

        try :
            select_first_status = wait.until(EC.element_to_be_clickable((By.XPATH, select_first_status)))
            highlight_element(driver, select_first_status)  
            fetch_status_name = select_first_status.text
            select_first_status.click()
            time.sleep(1)
            print(f"🟦 First status selected: {fetch_status_name}")
            allure.attach(f"Status: {fetch_status_name}",name="Selected Status",attachment_type=allure.attachment_type.TEXT)
            filters_label = wait.until(EC.element_to_be_clickable((By.XPATH, filter_label))) 
            filters_label.click()
            time.sleep(2)     
        except Exception as e:
            allure.attach(str(e), name="Select First Topic Error", attachment_type=allure.attachment_type.TEXT)
            return False 
        
    with allure.step("Click on Select Date calendar"):
        try:
            select_from_date = wait.until(EC.element_to_be_clickable((By.XPATH, from_date)))
            highlight_element(driver, select_from_date)
            select_from_date.click()
            time.sleep(2)

            today = datetime.today()
            today_str = today.strftime("%#d/%#m/%Y")  

            date_btn = wait.until(EC.element_to_be_clickable((By.XPATH, f"//button[@data-day='{today_str}']")))

            highlight_element(driver, date_btn)

            # Click twice
            date_btn.click()
            time.sleep(2)
            print("🟦 Select Date clicked")
        except Exception as e:
            allure.attach(str(e), name="Select Date Error", attachment_type=allure.attachment_type.TEXT)
            return False
        try :
            select_to_date = wait.until(EC.element_to_be_clickable((By.XPATH, to_date)))
            highlight_element(driver, select_to_date)
            select_to_date.click()
            time.sleep(2)

            today = datetime.today()
            today_str = today.strftime("%#d/%#m/%Y")  # use %-m on Mac/Linux

            date_btn = wait.until(EC.element_to_be_clickable((By.XPATH, f"//button[@data-day='{today_str}']")))

            highlight_element(driver, date_btn)

            # Click twice
            date_btn.click()
            time.sleep(2)
            print("🟦 Select Date clicked")
        except Exception as e:
            allure.attach(str(e), name="Select Date Error", attachment_type=allure.attachment_type.TEXT)
            return False
        
    with allure.step("Click on View Updates button"):
        try:
            updates_btn = wait.until(EC.element_to_be_clickable((By.XPATH, view_update)))
            highlight_element(driver, updates_btn)
            updates_btn.click()
            time.sleep(2)
            print("🟦 View Updates button clicked")
        except Exception as e:
            allure.attach(str(e), name="Updates Button Error", attachment_type=allure.attachment_type.TEXT)
            return False
        
    with allure.step("Validate Issuer filter applied correctly"):   
        applied_issuer = wait.until(EC.visibility_of_element_located((By.XPATH, fetch_applied_issuer_elem)))
        highlight_element(driver, applied_issuer)
        fetch_applied_issuer = applied_issuer.text
        if fetch_applied_issuer == fetch_issuer_name:
            print(f"✅ validated {fetch_applied_issuer} : {fetch_issuer_name}  ")
            allure.attach(f"Issuer: {fetch_issuer_name}",name="Issuer Check",attachment_type=allure.attachment_type.TEXT)
        else:
            print(f"❌ Issuer Mismatch!: {fetch_applied_issuer}: {fetch_issuer_name}")
            allure.attach(f"Grid: {fetch_applied_issuer}: {fetch_issuer_name}",name="Issuer Mismatch",attachment_type=allure.attachment_type.TEXT)

    with allure.step("Validate Industry filter applied correctly"):
        applied_industry = wait.until(EC.visibility_of_element_located((By.XPATH, fetch_applied_industry_elem)))
        highlight_element(driver, applied_industry)
        fetch_applied_industry = applied_industry.text
        if fetch_applied_industry == fetch_industry_name:
            print(f"✅ validated {fetch_applied_industry} : {fetch_industry_name}  ")
            allure.attach(f"Industry: {fetch_industry_name}",name="Industry Check",attachment_type=allure.attachment_type.TEXT)
        else:
            print(f"❌ Industry Mismatch!: {fetch_applied_industry}: {fetch_industry_name}")
            allure.attach(f"Grid: {fetch_applied_industry}: {fetch_industry_name}",name="Industry Mismatch",attachment_type=allure.attachment_type.TEXT)

    with allure.step("Validate Topic filter applied correctly"):
        applied_topic = wait.until(EC.visibility_of_element_located((By.XPATH, fetch_applied_topic_elem)))
        highlight_element(driver, applied_topic)
        fetch_applied_topic = applied_topic.text
        if fetch_applied_topic == fetch_topic_name:
            print(f"✅ validated {fetch_applied_topic} : {fetch_topic_name}  ")
            allure.attach(f"Topic: {fetch_topic_name}",name="Topic Check",attachment_type=allure.attachment_type.TEXT)
        else:
            print(f"❌ Topic Mismatch!: {fetch_applied_topic}: {fetch_topic_name}")
            allure.attach(f"Grid: {fetch_applied_topic}: {fetch_topic_name}",name="Topic Mismatch",attachment_type=allure.attachment_type.TEXT)
    
    with allure.step("Validate Status filter applied correctly"):
        applied_status = wait.until(EC.visibility_of_element_located((By.XPATH, fetch_applied_status_elem)))
        highlight_element(driver, applied_status)
        fetch_applied_status = applied_status.text
        if fetch_applied_status == fetch_status_name:
            print(f"✅ validated {fetch_applied_status} : {fetch_status_name}  ")
            allure.attach(f"Status: {fetch_status_name}",name="Status Check",attachment_type=allure.attachment_type.TEXT)
        else:
            print(f"❌ Status Mismatch!: {fetch_applied_status}: {fetch_status_name}")
            allure.attach(f"Grid: {fetch_applied_status}: {fetch_status_name}",name="Status Mismatch",attachment_type=allure.attachment_type.TEXT)
    
    with allure.step("Click on Reset Button"):
        try:
            reset_btn = wait.until(EC.element_to_be_clickable((By.XPATH, rest_all_btn)))
            highlight_element(driver, reset_btn)
            reset_btn.click()
            time.sleep(2)
            print("🟦 Reset button clicked")
        except Exception as e:
            allure.attach(str(e), name="Reset Button Error", attachment_type=allure.attachment_type.TEXT)
            return False
    
    return True