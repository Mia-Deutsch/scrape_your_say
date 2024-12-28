from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from webscraper import WebScraper
from selenium.webdriver.remote.webelement import WebElement

class MainPageWebScraper(WebScraper):
    def __init__(self, wait: WebDriverWait) -> None:
        super().__init__(wait)

    def get_text(self, xpath: str, box: WebElement) -> list[str]:
        box_web_elements_text: list[str] = [element.text for element in self.get_elements(xpath, box)]

        return box_web_elements_text

    def get_href(self, xpath: str, box: WebElement) -> str:
        box_web_element: WebElement = self.get_element(xpath, box)

        return box_web_element.get_attribute('href')

    def scrape_box(self, box: WebElement, xpath: dict) -> dict:
        link: str = self.get_href(xpath["links"], box)[0]
        topic: str = self.get_text(xpath["topics"], box)[0]
        stage: list[str] = [text.split(":")[0] for text in self.get_text(xpath["stage_and_feedback_status"], box)]
        feedback_status: list[str] = [text.split(":")[1][1::] for text in self.get_text(xpath["stage_and_feedback_status"], box)]
        type_of_act: str = self.get_text(xpath["type_of_act"], box)[0]
        feedback_period_from: str = self.get_text(xpath["feedback_period"], box)[0].split("-")[0][0:-1]
        feedback_period_to: str = self.get_text(xpath["feedback_period"], box)[0].split("-")[1][1::]

        return {"link": link,
                "topic": topic,
                "stage": stage,
                "feedback_status": feedback_status,
                "type_of_act": type_of_act,
                "feedback_period_from": feedback_period_from,
                "feedback_period_to": feedback_period_to,
        }

    def get_amount_pages(self, xpath: str, driver: WebDriver) -> int:
        page_numbers: list[WebElement] = self.get_elements(xpath, driver)
        amount_pages: int = int(page_numbers[0].text)

        return amount_pages