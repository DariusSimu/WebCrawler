from Backend.Scrapers.open_library import OpenLibraryScraper
from Backend.Scrapers.olx import OLXScraper
from Backend.Scrapers.ebay import EbayScraper
from Backend.Scrapers.vinted import VintedScraper

SCRAPERS = [
   # OpenLibraryScraper(),
    OLXScraper(),
    EbayScraper(),
    VintedScraper(),
]

def search_all(query, limit=10):
    results = []
    for scraper in SCRAPERS:
        results += scraper.search(query, limit)
    return results