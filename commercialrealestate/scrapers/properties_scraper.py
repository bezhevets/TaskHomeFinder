import asyncio

import httpx
from bs4 import BeautifulSoup

from core.schemas import Property
from scraping.config import USER_AGENT
from commercialrealestate.settings import TIMEOUT
from .property_card_scraper import PropertyCardScraper


class PropertiesScraper(PropertyCardScraper):

    async def create_property_instance(self, session, property_link: str) -> Property:
        text_response = await session.get(property_link, timeout=TIMEOUT)
        soup = BeautifulSoup(text_response.content, "html.parser")

        property_data = self.get_property_data(soup)
        return Property(url=property_link, **property_data)

    async def create_coroutines(self, properties_links: list):
        headers = {"user-agent": USER_AGENT}

        async with httpx.AsyncClient(headers=headers) as session:
            results = []
            step = 30
            for i in range(0, len(properties_links), step):
                tasks = [
                    self.create_property_instance(session, property_link)
                    for property_link in properties_links[i : i + step]
                ]
                results += await asyncio.gather(*tasks)
                await asyncio.sleep(0.5)
        return results

    def scrape_properties(self, properties_links: list):
        return asyncio.run(self.create_coroutines(properties_links=properties_links))
