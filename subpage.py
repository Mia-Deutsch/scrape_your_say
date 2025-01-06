from subpage_feedback import SubPageFeedback
from subpage_webscraper import SubpageWebscraper
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait

class SubPage:
    def __new__(cls, wait: WebDriverWait, url: str, driver: WebDriver, xpaths: dict):
        instance: SubPage = super().__new__(cls)
        subpage_scraper: SubpageWebscraper = SubpageWebscraper(wait, url, driver)
        driver.get(url)

        subpage_infos: dict = instance.get_subpage(xpaths, subpage_scraper)
        subpage_feedback_one: dict = dict()
        subpage_feedback_two: dict = dict()

        link_feedback_one = subpage_scraper.get_href_feedback_1(xpaths["feedback_1_button"])
        if link_feedback_one:
            feedback_one: SubPageFeedback = SubPageFeedback(wait, link_feedback_one, driver)
            feedback_one.driver.get(link_feedback_one)
            if feedback_one.click_statistics_button(xpaths["statistics_button"]):
                feedback_one_data: dict = feedback_one.get_data_by_category_respondent(xpaths["high_charts"], xpaths["info_by_category"], xpaths["text_by_category"])
                for key, value in feedback_one_data.items():
                    subpage_feedback_one[key] = value

        driver.get(url)
        link_feedback_two: str = subpage_scraper.click_button_feedback_2(xpaths["feedback_2_button"])
        if link_feedback_two:
            feedback_two: SubPageFeedback = SubPageFeedback(wait, link_feedback_two, driver)
            feedback_two_data: dict = feedback_two.get_data_by_country_respondent(xpaths["high_charts"], xpaths["text_by_country_list"], xpaths["text_by_country"])
            for key, value in feedback_two_data.items():
                subpage_feedback_two[key] = value

        #instance.subpage_all_infos: tuple[dict, dict, dict] = (subpage_infos, subpage_feedback_one, subpage_feedback_two)
        return subpage_infos, subpage_feedback_one, subpage_feedback_two

    def get_subpage(self, xpaths: dict, subpage_scraper: SubpageWebscraper) -> dict:
        category: str = subpage_scraper.get_category(xpaths["subpage_box"])
        file_name: list[str] = subpage_scraper.get_document_names(xpaths["file_box"])
        amount_feedback: int = subpage_scraper.get_feedback_number(xpaths["feedback_count"])
        return {"category": category,
                "file_name": file_name,
                "amount_feedback_one": amount_feedback
                }

    def get_feedback_infos(self, xpaths: dict, subpage_feedback: SubPageFeedback, data: dict) -> dict:
        feedback: dict = dict()

        for key, value in data.items():
            feedback[key] = value

        return feedback
        #subpage_feedback.get_data_by_country_respondent(xpaths["high_charts"], xpaths["text_by_country_list"], xpaths["text_by_country"])
