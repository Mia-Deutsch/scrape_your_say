from mainpage_webscraper import MainPageWebScraper
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webdriver import WebDriver

class DevWebscraper(MainPageWebScraper):
    def __init__(self, driver: WebDriver, wait: WebDriverWait) -> None:
        super().__init__(driver, wait)

    def get_amount_pages(self, xpath: str = None, url: str = None) -> int:
        return 1