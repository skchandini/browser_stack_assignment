# config.py
BROWSERSTACK_USERNAME = 'schandini902@gmail.com'
BROWSERSTACK_ACCESS_KEY = 'THGJTk2DzfB5HzzHkqXs'

BROWSERS = [
    {"browser": "Chrome", "browser_version": "latest", "os": "Windows", "os_version": "11", "name": "Desktop Chrome Test", "build": "Parallel BrowserStack Test", "debug": True},
    {"browser": "Firefox", "browser_version": "latest", "os": "Windows", "os_version": "10", "name": "Desktop Firefox Test", "build": "Parallel BrowserStack Test", "debug": True},
    {"device": "iPhone 14", "os_version": "16", "real_mobile": "true", "name": "iPhone 14 Mobile Test", "build": "Parallel BrowserStack Test", "debug": True},
    {"device": "Samsung Galaxy S23", "os_version": "13.0", "real_mobile": "true", "name": "Samsung S23 Mobile Test", "build": "Parallel BrowserStack Test", "debug": True},
    {"browser": "Edge", "browser_version": "latest", "os": "Windows", "os_version": "10", "name": "Desktop Edge Test", "build": "Parallel BrowserStack Test", "debug": True}
]
