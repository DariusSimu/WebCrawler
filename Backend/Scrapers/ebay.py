from Backend.Scrapers.base import BaseScraper
from Backend.models import Listing
from thefuzz import fuzz
import time
import requests
import base64
from config import EBAY_APP_ID, EBAY_CERT_ID

class EbayScraper(BaseScraper):
    URL = "https://api.ebay.com/buy/browse/v1/item_summary/search"
    TOKEN_URL = "https://api.ebay.com/identity/v1/oauth2/token"
    MARKETPLACES = ['EBAY_DE', 'EBAY_GB', 'EBAY_FR', 'EBAY_IT', 'EBAY_ES']

    def __init__(self):
        self.app_id = EBAY_APP_ID
        self.cert_id = EBAY_CERT_ID
        self.access_token = None

    def get_access_token(self):
        credentials = base64.b64encode(f"{self.app_id}:{self.cert_id}".encode()).decode()
        response = requests.post(self.TOKEN_URL,
                                    headers={
                                        'Authorization': f'Basic {credentials}',
                                        'Content-Type': 'application/x-www-form-urlencoded'
                                        },
                                    data={'grant_type': 'client_credentials',
                                        'scope': 'https://api.ebay.com/oauth/api_scope'
                                        }
                                )
        #print(f"Token response status: {response.status_code}")
        #print(f"Token response: {response.json()}")
        self.access_token = response.json().get('access_token')
    
    def search(self, query, limit):
        if not self.is_allowed():
            print(f"[{self.URL}] Crawling not allowed by robots.txt")
            return []
        print(f"Searching allowed: Ebay")
        
        if not self.access_token:
            self.get_access_token()

        #print(f"Token: {self.access_token}")
        all_listings = []
        seen_ids = set()
        
        for marketplace in self.MARKETPLACES:
            response = requests.get(self.URL,
                                params={'q': query, 'limit': limit},
                                headers={
                                    'Authorization': f'Bearer {self.access_token}',
                                    'Content-Type': 'application/json',
                                    'X-EBAY-C-MARKETPLACE-ID': marketplace
                                },
                                timeout=5)
        
            #print(f"Status code: {response.status_code}")  # check response status
            #print(f"Search response: {response.text}")  # print raw response for debugging
            #print(f"Response: {response.json()}")

            data = response.json()
            listings = []

            for item in data.get('itemSummaries', []):
                item_id = item.get('itemId', '')
                if item_id in seen_ids:
                    continue
                seen_ids.add(item_id)
                title    = item.get('title', 'Unknown Title').strip()
                price    = item.get("price", {}).get("value", "N/A") + " " + item.get("price", {}).get("currency", "")
                url      = item.get('itemWebUrl', '').strip()
                image    = item.get('image', {}).get('imageUrl', '').strip()
                platform = f"www.ebay.{marketplace.split('_')[1].lower()}"

                if any(query.lower() in title.lower() for query in query.split()):
                    listings.append(Listing(
                        title    = title,
                        platform = platform,
                        price    = price,
                        url      = url,
                        image    = image
                    ))
            
            all_listings += listings
            time.sleep(self.get_crawl_delay())

        
        return all_listings