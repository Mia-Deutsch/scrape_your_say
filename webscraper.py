from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.remote.webdriver import WebDriver

class WebScraper:

    def __init__(self, wait: WebDriverWait) -> None:
        self.wait: WebDriverWait = wait

    def get_elements(self, value: str, web_obj: WebDriver | WebElement, by: str = By.XPATH) -> list[WebElement]:
        self.wait.until(expected_conditions.presence_of_all_elements_located((by, value)))
        elements: list[WebElement] = web_obj.find_elements(by, value)
        return elements

    def get_element(self, value: str, web_obj: WebDriver | WebElement, by: str = By.XPATH) -> WebElement:
        self.wait.until(expected_conditions.presence_of_all_elements_located((by, value)))
        element: WebElement = web_obj.find_element(by, value)

        return element

    def click_element(self, web_obj: WebElement, driver: WebDriver) -> None:
        self.wait.until(expected_conditions.element_to_be_clickable(web_obj))
        driver.execute_script("arguments[0].click();", web_obj)