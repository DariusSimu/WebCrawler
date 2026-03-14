from Backend.Scrapers.base import BaseScraper
from Backend.models import Listing
from urllib.parse import urlparse
import time
import requests

class OpenLibraryScraper(BaseScraper):
    URL = "https://openlibrary.org/search.json"

    def search(self, query, limit):
        if not self.is_allowed():
            print(f"[{self.URL}] Crawling not allowed by robots.txt")
            return []
        
        response = requests.get(self.URL,
                                params={'q': query, 'limit': limit},
                                headers={'User-Agent': 'Mozilla/5.0'},
                                timeout=5)
        data = response.json()
        parsed   = urlparse(self.URL)
        base     = f"{parsed.scheme}://{parsed.netloc}"
        platform = parsed.netloc
        listings = []
        for doc in data["docs"]:
            title    = doc.get("title",       "Unknown Title").strip()
            key      = doc.get("key",         "").strip()
            page_url = f"{base}{key}"
            listings.append(Listing(
                title    = title,
                platform = platform,
                price    = "N/A",
                url      = page_url
            ))
        time.sleep(self.get_crawl_delay())
        return listings