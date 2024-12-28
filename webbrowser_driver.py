from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webdriver import WebDriver


class WebBrowser:
    def __new__(cls, config: dict) -> WebDriver:
        settings: list[str] = config["chrome_settings"]
        options: Options = Options()
        [options.add_argument(arg) for arg in settings]
        driver: WebDriver = webdriver.Chrome(options)

        return driver

