from Backend.models import Listing
from urllib.parse import urlparse
from urllib.robotparser import RobotFileParser

class BaseScraper:
    URL = ""
    USER_AGENT = "Mozilla/5.0"

    def is_allowed(self) -> bool:
        parsed = urlparse(self.URL)
        robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"
        robots_parser = RobotFileParser()
        robots_parser.set_url(robots_url)
        try:
            robots_parser.read()
            url_path = parsed.path
            for rule in robots_parser.rules:
                for line in rule.lines:
                    disallowed = line.path
                    if (url_path == disallowed.rstrip('/') 
                        or url_path.startswith(disallowed) 
                        and disallowed.endswith('/')):
                            return False
            return True
        except:
            return True
    
    def get_crawl_delay(self) -> float:
        parsed = urlparse(self.URL)
        robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"
        robots_parser = RobotFileParser()
        robots_parser.set_url(robots_url)
        try:
            robots_parser.read()
            delay = robots_parser.crawl_delay(self.USER_AGENT)
            return float(delay) if delay is not None else 1.0
        except:
            return 1.0
    
    def search(self, query: str, limit: int = 10) -> list[Listing]:
        raise NotImplementedError