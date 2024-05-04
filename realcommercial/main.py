import logging

from scrapers.properties_scraper import PropertiesScraper
from scrapers.properties_data_scraper_api import PropertiesDataScraperAPI

from scraping.config import configure_logging, save_data_to_json, time_counter

configure_logging()


@time_counter
def main() -> None:
    logging.info("Scrape properties links...")
    scraper = PropertiesDataScraperAPI()
    properties_data = scraper.scrape_properties_data()

    logging.info("Scrape properties...")
    scraper = PropertiesScraper().scrape_properties(properties_data)

    actual_properties = [_property for _property in scraper if _property.url]

    save_data_to_json(actual_properties, "data.json")
    logging.info("Data were saved successfully")


if __name__ == "__main__":
    main()
