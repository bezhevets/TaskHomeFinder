import asyncio

import httpx
from bs4 import BeautifulSoup

from scraping.config import USER_AGENT
from commercialrealestate.settings import BASE_URL, BASE_SEARCH_URLS, TIMEOUT


class PropertiesLinksScraper:
    def __init__(self) -> None:
        self.headers = {"user-agent": USER_AGENT}

    async def get_properties_links(self, session, page_link) -> list[str] | None:
        text_response = await session.get(page_link, timeout=TIMEOUT)
        soup = BeautifulSoup(text_response.content, "html.parser")

        containers = soup.find_all("a", {"class": "css-1s611kr"})
        if not containers:
            return None
        links = [container.get("href") for container in containers]
        if links:
            return [BASE_URL[:-1] + link for link in links]
        return []

    async def create_coroutines(self) -> list:
        results = []
        # Aiohttp does not work with this site
        async with httpx.AsyncClient(headers=self.headers) as session:
            for region_link in BASE_SEARCH_URLS:
                index = 1
                while True:
                    if index == 1:
                        result = await self.get_properties_links(
                            session, f"{region_link}"
                        )
                    else:
                        result = await self.get_properties_links(
                            session, f"{region_link}?pn={index}"
                        )
                    if not result:
                        break
                    # count_duplicate_links = 0
                    # for el in result:
                    #     if el in results:
                    #         count_duplicate_links += 1
                    # if len(result) == count_duplicate_links:
                    #     break
                    results += result

                    index += 1
        return results

    def scrape_properties_links(self) -> list:
        return asyncio.run(self.create_coroutines())
