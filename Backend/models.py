from dataclasses import dataclass, field
from urllib.parse import urlparse
import hashlib

@dataclass
class Listing:
    title:    str
    platform: str
    price:    str
    url:      str
    image:    str = "/static/images/empty_jpeg.jpg"
    condition: str = "NONE"
    listing_id: str = field(init=False)

    def __post_init__(self):
        parsed = urlparse(self.url)
        clean_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
        self.listing_id = hashlib.md5(clean_url.encode()).hexdigest()