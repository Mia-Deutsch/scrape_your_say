from webscraper import WebScraper
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from dev_webscraper import DevWebscraper
from mainpage import MainPage
from webbrowser_driver import WebBrowser
from mainpage_webscraper import MainPageWebScraper
from selenium.webdriver.remote.webdriver import WebDriver
from scrape_your_say import ScrapeYourSay
from data_handler import DataHandler

import yaml
import logging
import time


if __name__ == "__main__":
    start_time: float = time.time()
    driver_config: dict = yaml.safe_load(open("driver_config.yml"))
    xpaths: dict = yaml.safe_load(open("webelements_path.yml"))
    webscraper_args: dict = yaml.safe_load(open("webscraper_args.yml"))

    driver: WebDriver = WebBrowser(driver_config)
    wait: WebDriverWait = WebDriverWait(driver, timeout=driver_config["webdriver_wait"]["timeout"])
    data: list[tuple[dict, dict, dict, dict]] = ScrapeYourSay(xpaths, driver, webscraper_args["url"], wait)
    yaml_converter: DataHandler = DataHandler(data)
    yaml_converter.to_yaml()

    logging.warning(f"Finished in {((time.time() - start_time) / 60) // 60} hours {(time.time() - start_time) % 60} minutes")
    logging.warning(time.time() - start_time)
