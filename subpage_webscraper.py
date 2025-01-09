from selenium.common import TimeoutException, ElementClickInterceptedException
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from webscraper import WebScraper
from selenium.webdriver.remote.webelement import WebElement
import logging

class SubpageWebscraper(WebScraper):
    def __init__(self, wait: WebDriverWait, url: str, driver: WebDriver) -> None:
        super().__init__(wait)
        self.url = url
        self.driver = driver
        self.logger: logging.Logger = logging.getLogger(__name__)

    def get_feedback_number(self, xpath: str) -> int:
        try:
            feedback_number_webelement: WebElement = self.get_element(xpath, self.driver)
            feedback_number: int = int(feedback_number_webelement.text.split("(")[1][:-1])
            return feedback_number
        except TimeoutException:
            return 0

    def get_category(self, xpath: str) -> str:
        try:
            subpage_box: list[WebElement] = self.get_elements(xpath, self.driver)
            for index, subpage_element in enumerate(subpage_box):
                if subpage_element.text == "Category":
                    return subpage_box[index+1].text
            return ""
        except TimeoutException as timout_exception:
            self.logger.warning(timout_exception)
            return "THIS WAS NOT SUPPOSED TO HAPPEN"

    def get_document_names(self, xpath: str) -> list[str]:
        document_names: list[str] = []
        try:
            document_list: list[WebElement] = self.get_elements(xpath, self.driver)
            [document_names.append(name.text) for name in document_list]
            return document_names
        except TimeoutException:
            self.logger.warning("No files found")
            return document_names

    def click_button_feedback_2(self, xpath: str) -> str:
        try:
            button: WebElement = self.get_element(xpath, self.driver)
            self.click_element(button, self.driver)
            return self.driver.current_url
        except ElementClickInterceptedException as click_exception:
            self.logger.warning(click_exception)
            return ""
        except TimeoutException:
            return ""

    def get_href_feedback_1(self, xpath: str) -> str:
        try:
            link_element: WebElement = self.get_element(xpath, self.driver)
            link_text: str = link_element.get_attribute("href")
            return link_text
        except TimeoutException:
            self.logger.warning("No link found")
            return ""