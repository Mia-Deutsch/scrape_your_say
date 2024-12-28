from mainpage_webscraper import MainPageWebScraper
class MainPage:
    def __init__(self) -> None:
        self.main_page_webscraper = MainPageWebScraper()
        self.main_page_boxes: list[dict] = []