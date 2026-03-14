from Backend.Scrapers.base import BaseScraper
from Backend.Models import Listing
from urllib.parse import urlparse
import requests

class OpenLibraryScraper(BaseScraper):
    URL = "https://openlibrary.org/search.json"

    def search(self, query, limit=10):
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
                seller   = "N/A",
                price    = "N/A",
                url      = page_url
            ))
        return listings