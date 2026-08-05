
    
import allure
import json
import os
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from utilities.other_utils_functions.highlight import highlight_element

class BulkInvitationDownloadTemplate:

    def __init__(self, driver, wait):
        self.driver = driver
        self.wait = wait
        self.load_locators()

    def load_locators(self):
        """Load locators from JSON file."""
        try:
            with open(os.path.join("data", "locators.json"), "r") as f:
                locators = json.load(f)

            self.settings_icon = locators["settings_icon"]
            self.team_members_btn = locators["team_members_btn"]
            self.invitations_tab_btn = locators["invitations_tab_btn"]
            self.bulk_download_template = locators["bulk_download_template"]

            print("✅ locators.json loaded")

        except FileNotFoundError as e:
            allure.attach(str(e),name="Locators File Missing",attachment_type=allure.attachment_type.TEXT)
            raise

        except json.JSONDecodeError as e:
            allure.attach(str(e),name="Invalid JSON",attachment_type=allure.attachment_type.TEXT)
            raise

    def click_settings(self):
        with allure.step("Click Settings"):
            try:
                settings_btn = self.wait.until(EC.presence_of_element_located((By.XPATH, self.settings_icon)))
                highlight_element(self.driver, settings_btn)
                settings_btn.click()
            except Exception as e:
                msg = f"Failed to Click Settings Icon: {str(e)}"
                print(msg)
                allure.attach(msg, name="Settings Icon Error", attachment_type=allure.attachment_type.TEXT)
                raise Exception(msg)

    def click_team_members(self):
        with allure.step("Click Team Members"):
            try:
                team_members = self.wait.until(EC.presence_of_element_located((By.XPATH, self.team_members_btn)))
                highlight_element(self.driver, team_members)
                team_members.click()
                time.sleep(2)
            except Exception as e:
                msg = f"Failed to Click Team Member Tab: {str(e)}"
                print(msg)
                allure.attach(msg, name="Team Member tab Error", attachment_type=allure.attachment_type.TEXT)
                raise Exception(msg)

    def click_invitations_tab(self):
        with allure.step("Click Invitations Tab"):
            try:
                invitations_tab = self.wait.until(EC.presence_of_element_located((By.XPATH, self.invitations_tab_btn)))
                highlight_element(self.driver, invitations_tab)
                invitations_tab.click()
                time.sleep(2)
            except Exception as e:
                msg = f"Failed to Click Invitations Tab: {str(e)}"
                print(msg)
                allure.attach(msg, name="Invitations tab Error", attachment_type=allure.attachment_type.TEXT)
                raise Exception(msg)

    def click_download_template(self):
        with allure.step("Click Download Template"):
            try:
                download_template = self.wait.until(EC.presence_of_element_located((By.XPATH, self.bulk_download_template)))
                highlight_element(self.driver, download_template)
                download_template.click()
                time.sleep(2)
            except Exception as e:
                msg = f"Failed to Click Download Template: {str(e)}"
                print(msg)
                allure.attach(msg, name="Download Template Error", attachment_type=allure.attachment_type.TEXT)
                raise Exception(msg)

    def bulk_invitation_download_template(self):
        self.click_settings()
        self.click_team_members()
        self.click_invitations_tab()
        self.click_download_template()

        return True
        