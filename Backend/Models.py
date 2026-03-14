from dataclasses import dataclass

@dataclass
class Listing:
    title:    str
    platform: str
    price:    str
    url:      str
    image:    str = "/static/images/empty_jpeg.jpg"