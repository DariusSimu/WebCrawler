from Backend.Scrapers.open_library import OpenLibraryScraper
from Backend.Scrapers.olx import OLXScraper

SCRAPERS = [
    OpenLibraryScraper(),
    OLXScraper(),
]

def search_all(query, limit=10):
    results = []
    for scraper in SCRAPERS:
        results += scraper.search(query, limit)
    return results