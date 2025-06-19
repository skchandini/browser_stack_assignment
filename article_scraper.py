# article_scraper.py
import os
import time
import json 
from collections import Counter
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from config import BROWSERSTACK_USERNAME, BROWSERSTACK_ACCESS_KEY
from browser_utils import get_options
from translator import translate_rapidapi
from downloader import download_image

def run_test(cap):
    print(f"Starting test on {cap.get('name')}")
    url = f"https://{BROWSERSTACK_USERNAME}:{BROWSERSTACK_ACCESS_KEY}@hub-cloud.browserstack.com/wd/hub"
    options = get_options(cap)
    driver = webdriver.Remote(command_executor=url, options=options)
    wait = WebDriverWait(driver, 20)

    try:
        driver.get("https://elpais.com/")

        try:
            accept_btn = wait.until(EC.element_to_be_clickable((By.ID, "didomi-notice-agree-button")))
            accept_btn.click()
        except Exception:
            print(f"⚠️ Cookie button not found or clickable on {cap.get('name')}")

        try:
            opinion_link = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[normalize-space(text())='Opinión']")))
            opinion_link.click()
        except Exception:
            print(f"⚠️ 'Opinión' link not clickable on {cap.get('name')}")

        time.sleep(3)
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

        all_words = " ".join(translated_titles).lower().split()
        repeated = {w: c for w, c in Counter(all_words).items() if c > 2}
        if repeated:
            print(f"\nRepeated words (>2 times) on {cap.get('name')}:")
            for w, c in repeated.items():
                print(f"  {w}: {c}")
        else:
            print(f"\nNo repeated words >2 on {cap.get('name')}")

        driver.execute_script(
            'browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"passed","reason": "Articles scraped successfully"}}'
        )

    except Exception as e:
        print(f" Error during test on {cap.get('name')}: {e}")
        driver.execute_script(
            f'browserstack_executor: {{"action": "setSessionStatus", "arguments": {{"status":"failed","reason": "Test failed: {str(e)}"}}}}'
        )

    finally:
        try:
            driver.quit()
        except Exception as e:
            print("⚠️ Error quitting driver:", e)

        print(f"✅ Test finished on {cap.get('name')}")
