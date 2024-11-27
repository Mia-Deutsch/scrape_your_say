from webscraper import WebScraper

class DevWebscraper(WebScraper):
    def __init__(self, config:  dict) -> None:
        super().__init__(config)

    def get_amount_pages(self) -> int:
        return 1