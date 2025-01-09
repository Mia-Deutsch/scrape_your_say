from mainpage import MainPage
from subpage import SubPage
from selenium.webdriver.remote.webdriver import WebDriver
from mainpage_webscraper import MainPageWebScraper
from selenium.webdriver.support.ui import WebDriverWait

class ScrapeYourSay:
    def __new__(cls, xpaths: dict, driver: WebDriver, url: str, wait: WebDriverWait) -> list[tuple[dict, dict, dict, dict]]:
        instance: ScrapeYourSay = super().__new__(cls)

        main_scraper: MainPageWebScraper = MainPageWebScraper(wait)
        mainpage_scraper: MainPage = MainPage(xpaths, driver, main_scraper, url)
        all_data: list[tuple[dict, dict, dict, dict]] = []
        initiatives: list[dict] = instance.mainpage_infos(mainpage_scraper)
        
        for index, initiative in enumerate(initiatives):
            subpage: tuple[dict, dict, dict] = SubPage(wait, initiative["link"], driver, xpaths)
            all_data.append((initiative, subpage[0], subpage[1], subpage[2]))

        return all_data

    def mainpage_infos(self, mainpage_scraper: MainPage) -> list[dict]:
        mainpage_scraper.scrape_boxes()
        return mainpage_scraper.main_page_boxes
