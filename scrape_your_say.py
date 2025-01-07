from mainpage import MainPage
from subpage import SubPage
from selenium.webdriver.remote.webdriver import WebDriver
from mainpage_webscraper import MainPageWebScraper
from selenium.webdriver.support.ui import WebDriverWait

class ScrapeYourSay:
    def __new__(cls, xpaths: dict, driver: WebDriver, url: str, wait: WebDriverWait) -> list[tuple[dict, dict, dict, dict]]:
        instance: ScrapeYourSay = super().__new__(cls)
        """
        main_scraper: MainPageWebScraper = MainPageWebScraper(wait)
        mainpage_scraper: MainPage = MainPage(xpaths, driver, main_scraper, url)
        all_data: list[tuple[dict, dict, dict, dict]] = []
        initiatives: list[dict] = instance.mainpage_infos(mainpage_scraper)
        
        for index, initiative in enumerate(initiatives):
            subpage: tuple[dict, dict, dict] = SubPage(wait, initiative["link"], driver, xpaths)
            all_data.append((initiative, subpage[0], subpage[1], subpage[2]))
            """
        all_data: list[tuple[dict, dict, dict, dict]] = []
        for website in ["https://ec.europa.eu/info/law/better-regulation/have-your-say/initiatives/13915-State-aid-in-the-aviation-sector-Commission-guidelines-on-airports-and-airlines-revision-_en", "https://ec.europa.eu/info/law/better-regulation/have-your-say/initiatives/13195-Performance-of-pharmacovigilance-activities-for-human-medicines-update-of-Implementing-Regulation-EU-520-2012-_en", "https://ec.europa.eu/info/law/better-regulation/have-your-say/initiatives/14465-Measures-related-to-the-containment-of-specific-plant-pests-Grapevine-flavescence-doree_en", "https://ec.europa.eu/info/law/better-regulation/have-your-say/initiatives/13278-Commercial-vehicles-weights-and-dimensions-evaluation-_en"]:
            subpage: tuple[dict, dict, dict] = SubPage(wait, website, driver, xpaths)
            all_data.append(({"link": website, "more_infos": "cant be scraped rn"}, subpage[0], subpage[1], subpage[2]))

        return all_data

    def mainpage_infos(self, mainpage_scraper: MainPage) -> list[dict]:
        mainpage_scraper.scrape_boxes()
        return mainpage_scraper.main_page_boxes
