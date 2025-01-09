from logging import Logger

from selenium.common import TimeoutException, ElementClickInterceptedException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from webscraper import WebScraper
from selenium.webdriver.remote.webelement import WebElement
import logging
import time


class SubPageFeedback(WebScraper):
    def __init__(self, wait: WebDriverWait, url: str, driver: WebDriver):
        super().__init__(wait)
        self.url: str = url
        self.driver: WebDriver = driver
        self.logger: Logger = logging.getLogger(__name__)


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

            by_category: str = elements[0].get_attribute("id")

            try:
                by_country: str = elements[1].get_attribute("id")
            except IndexError:
                by_country: str = ""

            return by_category, by_country

        except TimeoutException as timeout_exception:
            self.logger.warning(timeout_exception)
            return "", ""

    def get_webelelement_list_with_dynamic_selector(self, selector: str, element_id: str) -> list[WebElement]:
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

        elements: list[WebElement] = self.get_webelelement_list_with_dynamic_selector(selector, element_id)
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


    def get_data_by_country_respondent(self, xpath_id: str, selector: str, selector_text: str) -> dict:
        data_feedback_by_country: dict = {}
        element_id: str = self.get_id(xpath_id)[1]
        if not element_id: return data_feedback_by_country

        countries: list[WebElement] = []
        [countries.append(country) for country in self.get_webelelement_list_with_dynamic_selector(selector, element_id)]
        for index, country in enumerate(countries):
            try:
                new_selector: str = selector_text.format(id=element_id, index=index+1)
                time.sleep(0.5)
                data_feedback_by_country[country.text] = self.get_element(new_selector, self.driver, By.CSS_SELECTOR).text
            except TimeoutException as timeout_exception:
                self.logger.warning(timeout_exception)

        return data_feedback_by_country

    def get_amount_feedback_two(self, xpath: str) -> int:
        try:
            amount: str = self.get_element(xpath, self.driver).text
            return int(amount.split(":")[1])
        except TimeoutException as timeout_exception:
            self.logger.warning(timeout_exception)
            return 0