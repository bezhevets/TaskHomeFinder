import asyncio

import aiohttp
from bs4 import BeautifulSoup

from scraping.config import USER_AGENT
from zango.settings import BASE_URL, BASE_SEARCH_URLS


class PropertiesLinksScraper:
    def __init__(self) -> None:
        self.headers = {"user-agent": USER_AGENT}

    @staticmethod
    async def fetch_url_content(session, url: str, timeout=10000) -> str:
        async with session.get(url, timeout=timeout) as response:
            return await response.text()

    async def get_properties_links(self, session, page_link) -> list[str] | None:
        text_response = await self.fetch_url_content(session, page_link)
        soup = BeautifulSoup(text_response, "html.parser")

        containers = soup.find_all(
            "a", {"class": "PropertyLinkstyled__SLink-sc-lm9gjx-0 dCVOWP"}
        )
        if not containers:
            return None
        links = [container.get("href") for container in containers]
        if links:
            return [BASE_URL[:-1] + link for link in links]
        return []

    async def create_coroutines(self) -> dict:
        results = {"For Buy": [], "For Rent": []}
        async with aiohttp.ClientSession(headers=self.headers) as session:
            for region_link in BASE_SEARCH_URLS:
                index = 1
                while True:
                    result = await self.get_properties_links(
                        session, f"{region_link}{index}"
                    )
                    a = 0
                    for el in result:
                        if el in results["For Buy"] or el in results["For Rent"]:
                            a += 1
                    if len(result) == a:
                        break
                    if "buy" in region_link:
                        results["For Buy"] += result
                    if "lease" in region_link:
                        results["For Rent"] += result

                    index += 1
        return results

    def scrape_properties_links(self) -> dict:
        return asyncio.run(self.create_coroutines())
