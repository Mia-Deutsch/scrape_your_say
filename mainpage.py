from mainpage_webscraper import MainPageWebScraper
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

class MainPage:
    def __init__(self, xpaths: dict, driver: WebDriver, scraper: MainPageWebScraper, url: str) -> None:
        self.main_page_webscraper: MainPageWebScraper = scraper
        self.main_page_boxes: list[dict] = []
        self.xpaths: dict = xpaths
        self.driver: WebDriver = driver
        self.url: str = url

    def scrape_boxes(self):
        self.driver.get(self.url)

        amount_pages: int = self.main_page_webscraper.get_amount_pages(xpath=self.xpaths["page_numbers"], driver=self.driver)
        dynamic_url: str = self.url
        for page in range(amount_pages):
            self.driver.get(dynamic_url + str(page))
            web_obj_boxes: list[WebElement] = self.main_page_webscraper.get_elements(value=self.xpaths["boxes"], web_obj=self.driver)
            for box in web_obj_boxes:
                self.main_page_boxes.append(self.main_page_webscraper.scrape_box(box=box, xpath=self.xpaths))