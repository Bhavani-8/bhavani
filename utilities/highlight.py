# hightlight.py
import time

def highlight_element(driver, element, duration=1):
    original_style = element.get_attribute("style")
    highlight_style = "border: 3px solid red; background: yellow;"
    driver.execute_script("arguments[0].setAttribute('style', arguments[1])", element, highlight_style)
    time.sleep(duration)
    driver.execute_script("arguments[0].setAttribute('style', arguments[1])", element, original_style)