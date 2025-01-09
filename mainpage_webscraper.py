from selenium.common import NoSuchElementException
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from webscraper import WebScraper
from selenium.webdriver.remote.webelement import WebElement
import logging

class MainPageWebScraper(WebScraper):
    def __init__(self, wait: WebDriverWait) -> None:
        super().__init__(wait)
        self.logger: logging.Logger = logging.getLogger(__name__)

    def get_text(self, key: str, box_infos: list[str]) -> str:
        for index, info in enumerate(box_infos):
            if info == key:
                return box_infos[index + 1]
        self.logger.warning(f"\n>>>Could not find {key} in {box_infos}<<<\n")
        return ""

    def get_href(self, xpath: str, box: WebElement) -> str:
        try:
            element_of_link: WebElement = self.get_element(xpath, box)
            return element_of_link.get_attribute("href")

        except NoSuchElementException:
            self.logger.warning(f"\n>>>Link not found! WebElement: {box} | text: {box.text}<<<\n")
            return ""

    def get_feedback_period(self, key: str, box_infos: list[str], position: int) -> str:
        feedback_period = self.get_text(key, box_infos)
        if feedback_period == "":
            self.logger.warning(f"\n>>>Could not find {key} in {box_infos}<<<\n")
            return ""
        if position: return feedback_period.split("-")[1][1::]
        return feedback_period.split("-")[0][0:-1]

    def get_stage_status(self, box_infos: list[str]) -> list[tuple[str, str]]:
        stage_status: list[tuple[str, str]] = []
        for info in box_infos:
            if ":" in info:
                stage_status.append((info.split(":")[0], info.split(":")[1]))
            else:
                if not stage_status: self.logger.warning(f"\n>>>Could not find the Stage or the feedback status in {box_infos}<<<\n")
                return stage_status


    def scrape_box(self, box: WebElement, xpath: dict) -> dict:
        box_infos: list[str] = box.text.split("\n")

        return {"link": self.get_href(xpath["links"], box),
                "stage_and_feedback_status": [stage_feedback_status for stage_feedback_status in self.get_stage_status(box_infos)],
                "topic": self.get_text("Topic", box_infos),
                "type_of_act": self.get_text("Type of act", box_infos),
                "feedback_period_from": self.get_feedback_period("Feedback period", box_infos, 0),
                "feedback_period_to": self.get_feedback_period("Feedback period", box_infos, 1)
        }

    def get_amount_pages(self, xpath: str, driver: WebDriver) -> int:
        page_numbers: list[WebElement] = self.get_elements(xpath, driver)
        amount_pages: int = int(page_numbers[0].text)

        return amount_pages