from selenium.common import NoSuchElementException, TimeoutException, ElementClickInterceptedException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from webscraper import WebScraper
from selenium.webdriver.remote.webelement import WebElement
import logging


class SubPageFeedbackOne(WebScraper):
    def __init__(self, wait: WebDriverWait, url: str, driver: WebDriver):
        super().__init__(wait)
        self.url = url
        self.driver = driver
        self.logger = logging.getLogger(__name__)


    def click_statistics_button(self, xpath: str) -> int:
        try:
            button: WebElement = self.get_element(xpath, self.driver)
            self.click_element(button, self.driver)
            return 1
        except ElementClickInterceptedException as click_exception:
            self.logger.warning(click_exception)
            return 0
        except TimeoutException as timeout_exception:
            self.logger.warning(timeout_exception)
            return 0

    def get_id(self, xpath: str) -> tuple[str, str]:
        try:
            elements: list[WebElement] = self.get_elements(xpath, self.driver)
            return elements[0].get_attribute("id"), elements[1].get_attribute("id")
        except TimeoutException as timeout_exception:
            self.logger.warning(timeout_exception)
            return "", ""

    def get_by_category_respondent(self, selector: str, element_id: str) -> list[WebElement]:
        elements: list[WebElement] = []
        css_selector: str = selector.format(id=element_id)
        try:
            [elements.append(webelement) for webelement in self.get_elements(css_selector, self.driver, By.CSS_SELECTOR)]
            return elements
        except TimeoutException as timeout_exception:
            self.logger.warning(timeout_exception)
            return elements

    def get_data_by_category_respondent(self, xpath_id: str, selector: str, selector_text: str) -> dict:
        data_feedback_one: dict = {}
        element_id: str = self.get_id(xpath_id)[0]
        if not element_id: return data_feedback_one

        elements: list[WebElement] = self.get_by_category_respondent(selector, element_id)
        if not elements: return data_feedback_one
        text_elements: list[WebElement] = []

        for index, element in enumerate(elements):
            try:
                new_selector: str = selector_text.format(id=element_id, index=index)
                text_elements.append(self.get_element(new_selector, self.driver, By.CSS_SELECTOR))
            except TimeoutException as timeout_exception:
                self.logger.warning(timeout_exception)

        for text_element in text_elements:
            try:
                # example for text_element.text: "Company/business: 26 (33.77 %)"
                text: list[str] = text_element.text.split(":")
                key: str = text[0]
                data: int = int(text[1][1::].split("(")[0])
                data_feedback_one[key] = data
            except ValueError as value_exception:
                self.logger.warning(value_exception)
            except IndexError as index_exception:
                self.logger.warning(index_exception)

        return data_feedback_one

