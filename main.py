from webscraper import WebScraper
import yaml

if __name__ == "__main__":
    new_webscraper = WebScraper(yaml.safe_load(open("webscraper_config.yml")))