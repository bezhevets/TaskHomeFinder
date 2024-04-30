import asyncio

import aiohttp
from bs4 import BeautifulSoup

from core.schemas import Property
from scraping.config import USER_AGENT
from .property_card_scraper import PropertyCardScraper


class PropertiesScraper(PropertyCardScraper):

    @staticmethod
    async def fetch_url_content(session, url: str, timeout=10000) -> str:
        async with session.get(url, timeout=timeout) as response:
            return await response.text()

    async def create_property_instance(
        self, session, property_link: str, operation_type: str
    ) -> Property:
        text_response = await self.fetch_url_content(session, property_link)
        soup = BeautifulSoup(text_response, "html.parser")

        property_data = self.get_property_data(soup)
        return Property(
            operation_type=operation_type, url=property_link, **property_data
        )

    async def create_coroutines(self, properties_links: dict):
        headers = {"user-agent": USER_AGENT}

        async with aiohttp.ClientSession(headers=headers) as session:
            results = []
            for key, list_links in properties_links.items():
                tasks = [
                    self.create_property_instance(session, property_link, key)
                    for property_link in list_links
                ]
                results += await asyncio.gather(*tasks)
            return results

    def scrape_properties(self, properties_links: dict):
        return asyncio.run(self.create_coroutines(properties_links=properties_links))
