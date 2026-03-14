from Backend.Scrapers.base import BaseScraper
from Backend.Models import Listing
from bs4 import BeautifulSoup
import requests

class OLXScraper(BaseScraper):
    URL = "https://www.olx.ro/oferte/"

    def search(self, query, limit=10):
        # TODO: implement bs4 scraping
        return []