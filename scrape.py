import requests, json, base64
from bs4 import BeautifulSoup
import os

BASE_URL = "https://hdhub4u.fail"
HEADERS = {"User-Agent": "Mozilla/5.0"}

def scrape():
    print("Scraping HDHub4u...")
    res = requests.get(BASE_URL, headers=HEADERS)
    soup = BeautifulSoup(res.text, "html.parser")
    posts = soup.select(".post-title a")

    movies = []
    for post in posts[:10]:
        title = post.get_text(strip=True)
        url = post['href']
        mres = requests.get(url, headers=HEADERS)
        msoup = BeautifulSoup(mres.text, "html.parser")

        poster = msoup.select_one(".entry-content img")
        poster = poster["src"] if poster else ""

        qualities = {"480p": "", "720p": "", "1080p": ""}
        for a in msoup.find_all("a", href=True):
            txt = a.get_text().lower()
            if "480" in txt: qualities["480p"] = a["href"]
            if "720" in txt: qualities["720p"] = a["href"]
            if "1080" in txt: qualities["1080p"] = a["href"]

        movies.append({
            "title": title,
            "poster": poster,
            "links": qualities
        })

    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(movies, f, indent=2)

    print("✅ data.json created.")

if __name__ == "__main__":
    scrape()
