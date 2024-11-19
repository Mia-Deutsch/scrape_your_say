from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.remote.webdriver import WebDriver
import time

def build_chrome_driver(arguments: list[str]) -> WebDriver:
    options: Options = Options()
    [options.add_argument(arg) for arg in arguments]
    driver: WebDriver = webdriver.Chrome(options)
    
    return driver

def get_elements(driver: WebDriver, wait: WebDriverWait, xpath: str) -> list[WebElement]:
    wait.until(EC.presence_of_all_elements_located((By.XPATH, xpath)))
    elements: list[WebElement] = driver.find_elements(By.XPATH, xpath)
    
    return elements

def get_links(driver: WebDriver, wait: WebDriverWait, xpath: str, url: str) -> list[str]:
    links: list[str] = []
    driver.get(url)
    elements: list[WebElement] = get_elements(driver, wait, xpath)

    for element in elements:
        links.append(element.get_attribute("href"))

    return links

def main() -> None:
    url: str = "https://ec.europa.eu/info/law/better-regulation/have-your-say/initiatives_en"
    xpath_links: str = "//a[@class=\"ecl-u-pt-xs ecl-u-type-none\"]"
    driver: WebDriver = build_chrome_driver(["--window-size=1920,1080", "start-maximized", "headless"])
    wait: WebDriverWait = WebDriverWait(driver, timeout=10)
    
    links: list[str] = get_links(driver, wait, xpath_links, url)


if __name__ == "__main__":
    main()