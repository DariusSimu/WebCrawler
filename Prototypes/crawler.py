from bs4 import BeautifulSoup
from urllib.parse import urljoin
import requests
import time

BASE_URL = "https://en.wikipedia.org/wiki/Warhammer_40,000"
MAX_LINKS = 10
IGNORE = ('Wikipedia:', 'File:', 'Help:', 'Portal:', 'Special:', 'Main_Page', 'Talk:')

def get_page_name(url):
    try:
        response = requests.get(url,headers={'User-Agent': 'Mozilla/5.0'}, timeout=5)
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup.title.text.strip() if soup.title else "No Title"
    except Exception as e:
        print(f"Error fetching page name for {url}: {e}")
        return None
    
def crawl():
    response = requests.get(BASE_URL, headers={'User-Agent': 'Mozilla/5.0'}, timeout=5)
    soup = BeautifulSoup(response.text, 'html.parser')

    print(f"Base URL: {soup.title.text.strip()}")
    print(f"Found {len(soup.find_all('a'))} links on the page.")

    links = []
    visited = set()
    for a in soup.find_all('a', href=True):
        href = a['href']
        if href.startswith('/wiki/'):
            href = urljoin(BASE_URL, href)
        if (href.startswith('https://en.wikipedia.org/wiki/')
            and not any(skip in href for skip in IGNORE)
            and href != BASE_URL
            and href not in visited):
                links.append(href)
                visited.add(href)
                if len(links) >= MAX_LINKS:
                    break
    
    print(f"Crawling {len(links)} links:")

    for i, link in enumerate(links):
        page_name = get_page_name(link)
        print(f"[{i+1}/{MAX_LINKS}] {page_name} - {link}")
        time.sleep(1)

crawl()