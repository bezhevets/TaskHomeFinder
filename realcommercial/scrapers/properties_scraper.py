import asyncio

import aiohttp
from aiohttp.client_exceptions import ClientConnectorError
from bs4 import BeautifulSoup

from core.schemas import Property
from scraping.config import USER_AGENT
from .property_card_scraper import PropertyCardScraper


class PropertiesScraper(PropertyCardScraper):
    @staticmethod
    async def fetch_url_content(session, url: str, timeout=10000) -> str:
        async with session.get(url, timeout=timeout) as response:
            return await response.text()

    async def property_descripton(self, session, property_object: Property) -> Property:
        try:
            text_response = await self.fetch_url_content(session, property_object.url)
            soup = BeautifulSoup(text_response, "html.parser")
        except ClientConnectorError:
            property_object.url = None
            return property_object

        try:
            property_object.description = self.get_description(soup)
        except AttributeError:
            property_object.description = None
        return property_object

    def create_property_instance(self, property_data: dict) -> Property:
        property_data = self.get_property_data(property_data)
        return Property(**property_data)

    async def create_coroutines(self, properties_data: list) -> list:
        headers = {"user-agent": USER_AGENT}

        list_properties = []
        for property_data in properties_data:
            list_properties.append(self.create_property_instance(property_data))

        results = []
        async with aiohttp.ClientSession(headers=headers) as session:
            for i in range(0, len(list_properties), 10):
                tasks = [
                    self.property_descripton(session, property_object)
                    for property_object in list_properties[i : i + 10]
                ]
                partial_results = await asyncio.gather(*tasks)
                results.extend(partial_results)
                await asyncio.sleep(1)
            return results

    def scrape_properties(self, properties_data: list):
        return asyncio.run(self.create_coroutines(properties_data=properties_data))
