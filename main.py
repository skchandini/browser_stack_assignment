# main.py
import threading
from config import BROWSERS
from article_scraper import run_test

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
