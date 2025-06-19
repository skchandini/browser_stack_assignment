# downloader.py
import requests

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
