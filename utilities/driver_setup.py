# driver_setup.py
import pytest
import json
import sys
import time
from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.firefox import GeckoDriverManager
import allure
import pandas as pd
import os


def load_test_config_excel_data():
    df = pd.read_excel(os.path.join('data', 'test_case_selector.xlsx'), sheet_name='test_details', skiprows=1)
    print(f'Test Details:\n{df}')

@pytest.fixture
def setup(request):
    try:
        df = pd.read_excel(os.path.join('data', 'test_case_selector.xlsx'), sheet_name='credentials')
        print(f'Test Details from setup():\n{df}')
        browser = str(df['browser'].iloc[0])
        # print(f'Selected browser: {browser}')
        website = str(df['website'].iloc[0]).strip().lower()

        print(f"Selected browser: {browser}")
        print(f"Selected website: {website}")

        # with open(os.path.join('data', 'test_data.json'), 'r') as f:
        #     test_data = json.load(f)
        # browser = test_data['browser']
        # modules = test_data.get("module_to_test", [])
        # website = test_data.get('website')

        module_marker = None
        calling_file = request.node.fspath.basename  # e.g., test_login.py
        if "login" in calling_file:
            module_marker = "login"
        elif "forgot" in calling_file:
            module_marker = "forgot_password"
        elif "signup" in calling_file:
            module_marker = "signup"
        elif "dashboard" in calling_file:
            module_marker = "dashboard"
        elif "remove_task" in calling_file:
            module_marker = "trash"
        elif "special_add_task" in calling_file:
            module_marker = "special_task_dashboard"
        elif "special_dashboard" in calling_file:
            module_marker = "special_dashboard"
        elif "normal_tp" in calling_file:
            module_marker = "team_performance"
        elif "special_tp" in calling_file:
            module_marker = "special_team_performance"  
        elif "calendar" in calling_file:
            module_marker = "calendar_dashboard" 
        elif "notifications" in calling_file:
            module_marker = "notifications"
        elif "compliance_history" in calling_file:
            module_marker = "compliance_history"
        elif "normal_task_sections" in calling_file:
            module_marker = "dashboard"
        elif "special_task_sections" in calling_file:
            module_marker = "dashboard"
        elif "updates" in calling_file:
            module_marker = "updates"
        elif "project" in calling_file:
            module_marker = "project_management"
        elif "settings" in calling_file:
            module_marker = "settings"
        elif "audit" in calling_file:
            module_marker = "audit"
        elif "overall_happy_path_flow" in calling_file:
            module_marker = "dashboard"
        else:
            module_marker = "login"  # default fallback

        # Load locators.json to get URL
        with open(os.path.join('data', 'locators.json'), 'r') as f:
            locators = json.load(f)
        # urls_data = locators['new_server_urls']
        # if website == "new_server":
        #     urls_data = locators['new_server_urls']
        
        # elif website == "preprod":
        #     urls_data = locators['preprod_urls']
        # else:
        #     pytest.fail("Invalid website in config files, please check your configuration.")
        if website == "new_server":
            urls_data = locators["new_server_urls"]
        elif website == "preprod":
            urls_data = locators["preprod_urls"]
        elif website == "onprem":
            urls_data = locators['onprem_urls']
        else:
            pytest.fail(f"Invalid website: {website}. Please use 'new_server' or 'preprod'.")
        target_url = urls_data.get(module_marker)   # To select Target URL

        if not target_url:
            pytest.fail(f"No URL found for module: {module_marker}")

    except FileNotFoundError as e:
        pytest.fail(f"Missing config file: {e.filename}")
    except json.JSONDecodeError:
        pytest.fail("Invalid JSON in config files")

    # Setup browser
    driver = None
    current_dir = os.getcwd()
    download_path = os.path.join(current_dir, "downloads")  # Downloads folder inside current dir

    if browser == "edge":
        edge_driver_path = os.path.join(os.getcwd(), "utilities/drivers", "msedgedriver.exe")
        if not os.path.exists(edge_driver_path):
            pytest.fail(f"Edge driver not found at: {edge_driver_path}")
        
        options = webdriver.EdgeOptions()
        prefs = {"profile.default_content_setting_values.notifications": 2,
                 "download.default_directory": download_path,
                 "download.prompt_for_download": False,
                "download.directory_upgrade": True,
                "safebrowsing.enabled": True
            }
        options.add_experimental_option("prefs", prefs)
        options.add_argument("--start-maximized")
        service = EdgeService(executable_path=edge_driver_path)
        # driver = webdriver.Edge(options=options)
        driver = webdriver.Edge(service=service, options=options)

    elif browser == "chrome":
        options = webdriver.ChromeOptions()
        prefs = {"profile.default_content_setting_values.notifications": 2,
                "download.default_directory": download_path,
                "download.prompt_for_download": False,
                "download.directory_upgrade": True,
                "safebrowsing.enabled": True
            }
        options.add_experimental_option("prefs", prefs)
        options.add_argument("--start-maximized")
        options.add_argument("--guest")
        driver = webdriver.Chrome(options=options)

    elif browser == "firefox":
        options = webdriver.FirefoxOptions()
        # Firefox needs a bit different preference setup
        options.set_preference("permissions.default.desktop-notification", 2)  # Block notifications
        options.set_preference("browser.download.folderList", 2)  # 2 = use custom location
        options.set_preference("browser.download.dir", download_path)
        options.set_preference("browser.download.manager.showWhenStarting", False)
        options.set_preference("browser.helperApps.neverAsk.saveToDisk",
                            "application/pdf,application/octet-stream")  # add MIME types as needed
        driver = webdriver.Firefox(options=options, service=FirefoxService(GeckoDriverManager().install()))
        driver.maximize_window()

    else:
        print(f"❌ Unsupported browser: {browser}")
        sys.exit(1)

    driver.get(target_url)
    allure.attach(browser, name="🖥️ Browser Used", attachment_type=allure.attachment_type.TEXT)
    time.sleep(1)
    
    yield driver
    driver.quit()
