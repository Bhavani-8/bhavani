from utilities.other_utils_functions.highlight import highlight_element
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC

def wait_for_loader_to_disappear(driver, wait, loader_class="dx-loadpanel-content"):
    try:
        loader_elem = driver.find_element(By.CLASS_NAME, loader_class)
        highlight_element(driver, loader_elem)
        # print("🔍 Highlighted loader element.")
    except Exception:
        pass
        # print("❌ Could not find or highlight loader element.")

    try:
        wait.until(EC.invisibility_of_element_located((By.CLASS_NAME, loader_class)))
        # print("✅ Loader disappeared.")
    except TimeoutException:
        print("⚠️ Loader did not disappear in time.")