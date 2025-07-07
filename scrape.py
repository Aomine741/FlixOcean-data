import asyncio
import json
import os
from playwright.async_api import async_playwright

VEGAMOVIES_URL = "https://vegamovies.day"
GPLINK_API = os.getenv("GPLINK_API")

async def shorten_link(url):
    if not GPLINK_API:
        return url
    try:
        import requests
        res = requests.get(f"https://gplinks.in/api?api={GPLINK_API}&url={url}")
        data = res.json()
        return data.get("shortenedUrl", url)
    except Exception as e:
        print(f"[GPLinks] Error: {e}")
        return url

async def run():
    async with async_playwright() as p:
        print("🚀 Launching browser...")
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto(VEGAMOVIES_URL, timeout=60000)
        await page.wait_for_selector(".post-title a", timeout=20000)
        print("✅ Page loaded")

        posts = await page.query_selector_all(".post-title a")
        print(f"🎯 Found {len(posts)} posts")

        data = []
        for post in posts[:10]:
            title = (await post.inner_text()).strip()
            link = await post.get_attribute("href")
            print(f"🎬 Scraping: {title}")

            movie_page = await browser.new_page()
            await movie_page.goto(link, timeout=60000)
            poster = ""
            try:
                img = await movie_page.query_selector(".entry-content img")
                if img:
                    poster = await img.get_attribute("src")
            except:
                pass

            qualities = {"480p": "", "720p": "", "1080p": ""}
            anchors = await movie_page.query_selector_all("a")
            for a in anchors:
                text = (await a.inner_text()).lower()
                href = await a.get_attribute("href")
                if not href or not href.startswith("http"):
                    continue
                if "480" in text:
                    qualities["480p"] = await shorten_link(href)
                elif "720" in text:
                    qualities["720p"] = await shorten_link(href)
                elif "1080" in text:
                    qualities["1080p"] = await shorten_link(href)

            data.append({
                "title": title,
                "poster": poster,
                "links": qualities
            })

            await movie_page.close()

        with open("data.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

        print("✅ Scraping complete. Saved to data.json")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(run())
