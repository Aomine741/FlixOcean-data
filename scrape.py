import requests
from bs4 import BeautifulSoup
import json
import os

BASE_URL = "https://hdhub4u.fail"
GPLINK_API = os.getenv("GPLINK_API")

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
}

def shorten_link(url):
    try:
        if GPLINK_API:
            print(f"ðŸ”— Shortening: {url}")
            res = requests.get(f"https://gplinks.in/api?api={GPLINK_API}&url={url}")
            data = res.json()
            return data.get("shortenedUrl", url)
    except Exception as e:
        print("GPLink Error:", e)
    return url

def run_scraper():
    try:
        print("ðŸ” Requesting HDHub4u homepage...")
        res = requests.get(BASE_URL, headers=HEADERS, timeout=20)
        if res.status_code != 200:
            print(f"âŒ Failed to load homepage. Status code: {res.status_code}")
            open("data.json", "w").write("[]")
            return
        soup = BeautifulSoup(res.text, 'html.parser')
        posts = soup.select('.post-title a')
        print(f"âœ… Found {len(posts)} posts")

        data = []
        for post in posts[:10]:
            try:
                title = post.get_text().strip()
                link = post['href']
                print(f"ðŸŽ¬ {title} - {link}")

                movie_page = requests.get(link, headers=HEADERS, timeout=20)
                movie_soup = BeautifulSoup(movie_page.text, 'html.parser')
                poster_tag = movie_soup.select_one('.entry-content img')
                poster = poster_tag['src'] if poster_tag else ""

                qualities = {"480p": "", "720p": "", "1080p": ""}
                for a in movie_soup.find_all('a', href=True):
                    text = a.get_text().lower()
                    if "480" in text:
                        qualities["480p"] = shorten_link(a['href'])
                    elif "720" in text:
                        qualities["720p"] = shorten_link(a['href'])
                    elif "1080" in text:
                        qualities["1080p"] = shorten_link(a['href'])

                data.append({
                    "title": title,
                    "poster": poster,
                    "links": qualities
                })

            except Exception as e:
                print(f"âŒ Error scraping post: {e}")
                continue

        with open("data.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

        print("âœ… Done. data.json saved")

    except Exception as e:
        print("âŒ Fatal error:", e)
        with open("data.json", "w", encoding="utf-8") as f:
            json.dump([], f)

if __name__ == "__main__":
    run_scraper()
