from dataclasses import dataclass

@dataclass
class Listing:
    title:    str
    platform: str
    seller:   str
    price:    str
    url:      str
    image:   str = ""