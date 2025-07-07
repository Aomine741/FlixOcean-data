import requests
from bs4 import BeautifulSoup
import json
import os

VEGAMOVIES_URL = "https://vegamovies.day"
GPLINK_API = os.getenv("GPLINK_API")

def shorten_link(url):
    try:
        if GPLINK_API:
            res = requests.get(f"https://gplinks.in/api?api={GPLINK_API}&url={url}")
            data = res.json()
            return data.get("shortenedUrl", url)
    except Exception as e:
        print("GPLink Error:", e)
    return url

def run_scraper():
    try:
        res = requests.get(VEGAMOVIES_URL, timeout=10)
        soup = BeautifulSoup(res.text, 'html.parser')
        posts = soup.select('.post-title a')
        data = []

        for post in posts[:10]:
            title = post.get_text().strip()
            link = post['href']
            try:
                movie_page = requests.get(link, timeout=10)
                movie_soup = BeautifulSoup(movie_page.text, 'html.parser')
                poster_tag = movie_soup.select_one('.entry-content img')
                poster = poster_tag['src'] if poster_tag else ""
            except:
                poster = ""

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

        with open("data.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

        print("✅ Scraping done.")
    except Exception as e:
        print("❌ Scraper failed:", e)

if __name__ == "__main__":
    run_scraper()
