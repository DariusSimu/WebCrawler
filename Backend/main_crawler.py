from Backend.Scrapers.open_library import OpenLibraryScraper
from Backend.Scrapers.olx import OLXScraper
from Backend.Scrapers.ebay import EbayScraper

SCRAPERS = [
   # OpenLibraryScraper(),
    OLXScraper(),
    EbayScraper(),
]

def search_all(query, limit=10):
    results = []
    for scraper in SCRAPERS:
        results += scraper.search(query, limit)
    return results