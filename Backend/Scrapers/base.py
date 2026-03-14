from Backend.Models import Listing

class BaseScraper:
    URL = ""
    
    def search(self, query: str, limit: int) -> list[Listing]:
        raise NotImplementedError