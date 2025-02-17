import logging
from pprint import pprint

from scrapers.properties_scraper import PropertiesScraper
from scrapers.properties_links_scraper import PropertiesLinksScraper

from scraping.config import configure_logging, save_data_to_json, time_counter

configure_logging()


@time_counter
def main() -> None:
    logging.info("Scrape properties links...")
    scraper = PropertiesLinksScraper()
    properties_links = scraper.scrape_properties_links()

    logging.info("Scrape properties...")
    scraper = PropertiesScraper().scrape_properties(properties_links)

    save_data_to_json(scraper, "data.json")
    logging.info("Data were saved successfully")


if __name__ == "__main__":
    main()
