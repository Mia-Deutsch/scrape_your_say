from webscraper import WebScraper
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from dev_webscraper import DevWebscraper
from mainpage import MainPage
from webbrowser_driver import WebBrowser
from mainpage_webscraper import MainPageWebScraper
from selenium.webdriver.remote.webdriver import WebDriver

import yaml
import logging

def load_config() -> MainPage:

    if webscraper_args["dev_settings"] == "on":
        logging.basicConfig(level=logging.DEBUG)
        logging.info("dev mode is ON")
        scraper: DevWebscraper = DevWebscraper(wait)

    elif webscraper_args["dev_settings"] == "off":
        scraper: MainPageWebScraper = MainPageWebScraper(wait)

    else:
        raise Exception("Undefined setting in webscraper_args.yml > dev_settings [\"on\"/\"off\"]")

    new_webscraper: MainPage = MainPage(xpaths, driver, scraper, url=webscraper_args["url"])

    return new_webscraper

if __name__ == "__main__":
    driver_config: dict = yaml.safe_load(open("driver_config.yml"))
    xpaths: dict = yaml.safe_load(open("xpaths.yml"))
    webscraper_args: dict = yaml.safe_load(open("webscraper_args.yml"))

    driver: WebDriver = WebBrowser(driver_config)
    wait: WebDriverWait = WebDriverWait(driver, timeout=driver_config["webdriver_wait"]["timeout"])
    mainpage_scraper: MainPage = load_config()
    mainpage_scraper.scrape_boxes()
    [logging.debug(box) for box in mainpage_scraper.main_page_boxes]
