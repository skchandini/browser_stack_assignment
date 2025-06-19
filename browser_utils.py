# browser_utils.py
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions

def get_options(cap):
    browser = cap.get("browser", "").lower()
    if browser == "chrome":
        options = ChromeOptions()
    elif browser == "firefox":
        options = FirefoxOptions()
    elif browser == "edge":
        options = EdgeOptions()
    else:
        options = ChromeOptions()
    
    for key, value in cap.items():
        options.set_capability(key, value)
    return options
