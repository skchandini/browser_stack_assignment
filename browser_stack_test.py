import threading
import time
import os
import json
import requests
from collections import Counter
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions

BROWSERSTACK_USERNAME = 'schandini902@gmail.com'
BROWSERSTACK_ACCESS_KEY = 'THGJTk2DzfB5HzzHkqXs'

BROWSERS = [
    {"browser": "Chrome", "browser_version": "latest", "os": "Windows", "os_version": "11",
     "name": "Desktop Chrome Test", "build": "Parallel BrowserStack Test", "debug": True},
    {"browser": "Firefox", "browser_version": "latest", "os": "Windows", "os_version": "10",
     "name": "Desktop Firefox Test", "build": "Parallel BrowserStack Test", "debug": True},
    {"device": "iPhone 14", "os_version": "16", "real_mobile": "true",
     "name": "iPhone 14 Mobile Test", "build": "Parallel BrowserStack Test", "debug": True},
    {"device": "Samsung Galaxy S23", "os_version": "13.0", "real_mobile": "true",
     "name": "Samsung S23 Mobile Test", "build": "Parallel BrowserStack Test", "debug": True},
    {"browser": "Edge", "browser_version": "latest", "os": "Windows", "os_version": "10",
     "name": "Desktop Edge Test", "build": "Parallel BrowserStack Test", "debug": True}
]

def translate_rapidapi(text, source_lang='es', target_lang='en'):
    url = "https://rapid-translate-multi-traduction.p.rapidapi.com/t"
    headers = {
        "Content-Type": "application/json",
        "x-rapidapi-host": "rapid-translate-multi-traduction.p.rapidapi.com",
        "x-rapidapi-key": "8af040fa32mshfe22ef56a1e39d9p11b224jsnce1058c0a1eb"
    }
    payload = {"from": source_lang, "to": target_lang, "q": text}
    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        result = response.json()
        if isinstance(result, list) and result:
            return result[0]
        print("⚠️ Unexpected translation response:", result)
    except Exception as e:
        print("❌ Translation API error:", e)
    return text

def get_options(cap):
    browser = cap.get("browser", "").lower()
    if browser == "chrome":
        options = ChromeOptions()
    elif browser == "firefox":
        options = FirefoxOptions()
    elif browser == "edge":
        options = EdgeOptions()
    else:
        options = ChromeOptions()  # default fallback for mobile or unknown

    for key, value in cap.items():
        options.set_capability(key, value)
    return options

def download_image(img_url, filename):
    if not img_url.startswith("http"):
        print(f"❌ Invalid image URL: {img_url}")
        return
    headers = {"User-Agent": "Mozilla/5.0"}
    resp = requests.get(img_url, headers=headers)
    if resp.status_code == 200:
        with open(filename, "wb") as f:
            f.write(resp.content)
        print(f"✅ Image downloaded: {filename}")
    else:
        print(f"❌ Failed to download image. HTTP status code: {resp.status_code}")

def run_test(cap):
    print(f"Starting test on {cap.get('name')}")
    url = f"https://{BROWSERSTACK_USERNAME}:{BROWSERSTACK_ACCESS_KEY}@hub-cloud.browserstack.com/wd/hub"
    options = get_options(cap)
    driver = webdriver.Remote(command_executor=url, options=options)
    wait = WebDriverWait(driver, 20)

    try:
        driver.get("https://elpais.com/")

        # Accept cookie
        try:
            accept_btn = wait.until(EC.element_to_be_clickable((By.ID, "didomi-notice-agree-button")))
            accept_btn.click()
            print(f"✅ Cookie policy accepted on {cap.get('name')}")
        except Exception:
            print(f"⚠️ Cookie button not found or clickable on {cap.get('name')}, continuing...")

        # Navigate to Opinión section
        try:
            opinion_link = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[normalize-space(text())='Opinión']")))
            opinion_link.click()
            print(f"✅ Navigated to 'Opinión' on {cap.get('name')}")
        except Exception:
            print(f"⚠️ 'Opinión' link not found or clickable on {cap.get('name')}, continuing...")

        time.sleep(3)  # wait for articles to load

        articles = driver.find_elements(By.CSS_SELECTOR, "article")[:5]
        os.makedirs("images", exist_ok=True)
        translated_titles = []

        for i, article in enumerate(articles, 1):
            try:
                title = article.find_element(By.CSS_SELECTOR, "h2").text.strip()
                content = article.find_element(By.CSS_SELECTOR, "p").text.strip()
                print(f"\n📰 Article {i} on {cap.get('name')}")
                print("Title (Spanish):", title)
                print("Content:", content)

                eng_title = translate_rapidapi(title)
                print("Translated Title (English):", eng_title)
                translated_titles.append(eng_title)

                try:
                    img = article.find_element(By.CSS_SELECTOR, "img")
                    img_url = img.get_attribute("src")
                    filename = f"images/{cap.get('name').replace(' ', '_')}_article_{i}_cover.jpg"
                    download_image(img_url, filename)
                except Exception:
                    print("⚠️ No image found in this article")

            except Exception as e:
                print(f"❌ Error processing article {i} on {cap.get('name')}: {e}")

        # Word count for repeated words
        all_words = " ".join(translated_titles).lower().replace("’","").replace("'","").replace('"','').split()
        counts = Counter(all_words)
        repeated = {w: c for w, c in counts.items() if c > 2}
        if repeated:
            print(f"\n🔁 Repeated words (>2 times) on {cap.get('name')}:")
            for w, c in repeated.items():
                print(f"  {w}: {c}")
        else:
            print(f"\n🔁 No words repeated more than twice on {cap.get('name')}")

    finally:
        driver.quit()
        print(f"Test finished on {cap.get('name')}")

def main():
    threads = []
    for cap in BROWSERS:
        t = threading.Thread(target=run_test, args=(cap,))
        t.start()
        threads.append(t)
    for t in threads:
        t.join()

if __name__ == "__main__":
    main()
