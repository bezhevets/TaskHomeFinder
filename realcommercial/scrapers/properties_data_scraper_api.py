import asyncio

import aiohttp

from scraping.config import USER_AGENT
from realcommercial.settings import BASE_API_CHANNEL


class PropertiesDataScraperAPI:
    def __init__(self) -> None:
        self.headers = {"user-agent": USER_AGENT}

    @staticmethod
    async def fetch_data(session, url, payload) -> dict:
        async with session.post(url, json=payload) as response:
            return await response.json()

    async def get_json_data(self) -> list:
        result = []
        for channel in BASE_API_CHANNEL:
            url = "https://api.realcommercial.com.au/listing-ui/nearby-searches"
            payload = {
                "channel": channel,
                "filters": {
                    "within-radius": "includesurrounding",
                    "surrounding-suburbs": True,
                },
                "sort": {"order": "listing-date-newest-first"},
                "page-size": 100,
            }

            async with aiohttp.ClientSession(headers=self.headers) as session:
                page = 1
                while True:
                    payload["page"] = page
                    responses = await self.fetch_data(session, url, payload.copy())
                    result_responses = responses["listings"]
                    result += result_responses
                    page += 1
                    await asyncio.sleep(0.1)
                    if len(result_responses) == 0:
                        break
        return result

    def scrape_properties_data(self) -> list:
        return asyncio.run(self.get_json_data())
