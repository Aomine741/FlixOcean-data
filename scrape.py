import requests
from bs4 import BeautifulSoup
import json

BASE_URL = "https://hdhub4u.fail"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

def run_scraper():
    try:
        print("🔍 Requesting HDHub4u homepage...")
        res = requests.get(BASE_URL, headers=HEADERS, timeout=20)
        if res.status_code != 200:
            print(f"❌ Failed to load homepage: HTTP {res.status_code}")
            open("data.json", "w").write("[]")
            return

        soup = BeautifulSoup(res.text, "html.parser")
        posts = soup.select(".post-title a")
        print(f"✅ Found {len(posts)} posts")

        data = []
        for post in posts[:10]:
            title = post.get_text(strip=True)
            link = post['href']
            data.append({"title": title, "link": link})
            print(f"🎬 {title}")

        with open("data.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

        print("✅ data.json saved")

    except Exception as e:
        print(f"❌ Fatal error: {e}")
        with open("data.json", "w", encoding="utf-8") as f:
            json.dump([], f)

if __name__ == "__main__":
    run_scraper()
