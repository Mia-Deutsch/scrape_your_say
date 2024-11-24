from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.remote.webdriver import WebDriver

class WebScraper():

    def __init__(self, config:  dict) -> None:
        self.url: str = config["url"]
        self.xpath_links: str = config["xpath"]["links"]
        self.xpath_page_numbers: str = config["xpath"]["page_numbers"]
        self.driver: WebDriver = self.build_chrome_driver(config["chrome_settings"])
        self.wait: WebDriverWait = WebDriverWait(self.driver, timeout=config["webdriver_wait"]["timeout"])
    
        self.links: list[str] = self.get_links()

        print(len(self.links))

    def build_chrome_driver(self, arguments: list[str]) -> WebDriver:
        options: Options = Options()
        [options.add_argument(arg) for arg in arguments]
        driver: WebDriver = webdriver.Chrome(options)
    
        return driver

    def get_elements(self, xpath: str) -> list[WebElement]:
        self.wait.until(EC.presence_of_all_elements_located((By.XPATH, xpath)))
        elements: list[WebElement] = self.driver.find_elements(By.XPATH, xpath)
    
        return elements

    def get_links(self) -> list[str]:
        links: list[str] = []
        amount_pages: int = self.get_amount_pages()

        for page_number in range(amount_pages):
            self.driver.get(self.url + str(page_number))
            links_on_page: list[WebElement] = self.get_elements(self.xpath_links)

            for link in links_on_page:
                links.append(link.get_attribute("href"))

        return links
    
    def get_amount_pages(self) -> int:
        self.driver.get(self.url)
        page_numbers: list[WebElement] = self.get_elements(self.xpath_page_numbers)
        amount_pages: int = int(page_numbers[0].text)

        return amount_pages