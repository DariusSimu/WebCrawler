from Backend.Scrapers.base import BaseScraper
from Backend.models import Listing
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from thefuzz import fuzz
import requests
import time

class OLXScraper(BaseScraper):
    URL = "https://www.olx.ro/oferte/q-"

    def search(self, query, limit):
        if not self.is_allowed():
            print(f"[{self.URL}] Crawling not allowed by robots.txt")
            return []
        print(f"Searching allowed: OLX")

        search_url = f"{self.URL}{query.replace(' ', '-')}/"
        response = requests.get(search_url,
                                headers={'User-Agent': self.USER_AGENT},
                                timeout=5)
        soup = BeautifulSoup(response.text, 'html.parser')
        parsed   = urlparse(self.URL)
        base     = f"{parsed.scheme}://{parsed.netloc}"
        platform = parsed.netloc

        listings = []
        cards = soup.find_all('div', attrs={'data-testid': 'ad-card-title'})

        for card in cards[:limit]:
            try:
                tag = card.find('a')
                title = tag.find('h4').text.strip()
                url =base + tag['href']
                price_tag = card.find('p', attrs={'data-testid': 'ad-price'})
                price = price_tag.contents[0].strip() if price_tag else "N/A"
                l_card = card.find_parent('div', attrs={'data-testid': 'l-card'})
                image_tag = l_card.find('img') if l_card else None
                #print(f"Image tag: {image_tag}")
                if image_tag and image_tag.get('src') and 'no_thumbnail' not in image_tag['src']:
                    image = image_tag['src'].strip()
                else:
                    image = "/static/images/empty_jpeg.jpg"

                if any(query.lower() in title.lower() for query in query.split()):
                    listings.append(Listing(
                        title    = title,
                        platform = platform,
                        price    = price,
                        url      = url,
                        image    = image
                    ))
            except Exception as e:
                print(f"Error parsing OLX listing: {e}")
                continue

            #time.sleep(self.get_crawl_delay())
        
        return listings
