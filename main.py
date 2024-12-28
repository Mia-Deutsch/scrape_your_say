from webscraper import WebScraper
from dev_webscraper import DevWebscraper
import yaml
import logging

def load_config(config: dict) -> DevWebscraper | WebScraper:

    if (config["dev_settings"] == "on"):
        logging.basicConfig(level=logging.DEBUG)
        logging.info("dev mode is ON")
        new_webscraper: DevWebscraper = DevWebscraper(config)

    elif (config["dev_settings"] == "off"):
        new_webscraper: WebScraper = WebScraper(config)
    
    else:
        raise Exception("Undefined setting in driver_config.yml > dev_settings [\"on\"/\"off\"]")
    
    return new_webscraper

if __name__ == "__main__":
    new_webscraper: DevWebscraper | WebScraper = load_config(yaml.safe_load(open("driver_config.yml")))
    new_webscraper.get_links()