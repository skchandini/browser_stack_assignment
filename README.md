**🌐 BrowserStack Parallel News Scraper Assignment**

This project is a parallel web automation and scraping script built using Selenium and BrowserStack. It extracts the top five articles from the "Opinión" section of [elpais.com](https://elpais.com), translates the Spanish titles to English using RapidAPI, downloads the article images (if available), and logs frequently used words.

---

**🚀 Features**

- ✅ Runs across multiple browsers and devices in parallel using `threading`
- 🌍 Tests in Chrome, Firefox, Edge, iPhone 14, and Samsung Galaxy S23 using BrowserStack
- 📰 Scrapes the latest 5 opinion articles from `elpais.com`
- 🔤 Translates Spanish headlines to English using RapidAPI
- 🖼️ Downloads cover images for each article
- 📊 Counts and displays frequently repeated words in the translated titles

---

**📁 Project Structure**

browser_stack_assignment/
├── main.py # Entry point to start parallel browser threads
├── article_scraper.py # Main logic to scrape, translate, download images, and log output
├── config.py # BrowserStack credentials and browser/device capabilities
├── translator.py # Contains translation API integration (RapidAPI)
├── downloader.py # Contains function to download images
├── browser_utils.py # WebDriver options setup per browser/device
├── requirements.txt # Required Python packages
└── README.md # Project documentation

---

**Setup Instructions**

1. Clone the Repository
git clone https://github.com/skchandini/browser_stack_assignment.git
cd browser_stack_assignment

2. Install Dependencies
pip install -r requirements.txt

3. Configure Credentials
Edit the config.py file and enter your credentials:
BROWSERSTACK_USERNAME = 'your_browserstack_username'
BROWSERSTACK_ACCESS_KEY = 'your_browserstack_access_key'

---

**Running the Script**
python main.py

---

**Output Details**
Console will show:
Original (Spanish) and translated (English) titles
Article content (brief)
Download status of images
Repeated word counts in translated titles

---

**Tools & Technologies Used**

Selenium - Browser automation
BrowserStack - Cloud-based cross-browser/device testing
RapidAPI Translation API - Spanish to English translation
Python (threading) - Parallel execution


