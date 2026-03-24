from Backend.Scrapers.base import BaseScraper
from Backend.models import Listing
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from thefuzz import fuzz
import requests
import time

class VintedScraper(BaseScraper):
    URL = "https://www.vinted.ro/catalog?search_text="

    def search(self, query, limit):
        if not self.is_allowed():
            print(f"[{self.URL}] Crawling not allowed by robots.txt")
            return []
        print(f"Searching allowed: Vinted")

        search_url = f"{self.URL}{query.replace(' ', '%20')}"
        response = requests.get(search_url,
                                headers={'User-Agent': self.USER_AGENT},
                                timeout=5)
        soup = BeautifulSoup(response.text, 'html.parser')
        parsed   = urlparse(self.URL)
        base     = f"{parsed.scheme}://{parsed.netloc}"
        platform = parsed.netloc

        listings = []
        cards = soup.find_all('div', class_= 'feed-grid__item-content')
        for card in cards[:limit]:
            #print(f"Processing card: {card}")
            try:
                tag = card.find('a', class_ = 'new-item-box__overlay')
                url = tag['href']

                title = tag['title'].split(',')[0].strip() if tag['title'] else "N/A"
                
                price_tag = card.find('p', attrs={'data-testid': lambda x: x and x.endswith('--price-text')})
                price = price_tag.text.strip() if price_tag else "N/A"

                image_tag = card.find('img', class_ = 'web_ui__Image__content')
                image = image_tag['src'] if image_tag and image_tag.get('src') else "/static/images/empty_jpeg.jpg"
                
                if any(query.lower() in title.lower() for query in query.split()):
                    listings.append(Listing(
                        title    = title,
                        platform = platform,
                        price    = price,
                        url      = url,
                        image    = image
                    ))

            except Exception as e:
                print(f"Error parsing Vinted listing: {e}")
                continue

            #time.sleep(self.get_crawl_delay())
        return listings