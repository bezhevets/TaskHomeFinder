from bs4 import BeautifulSoup

from realcommercial.settings import BASE_URL


class PropertyCardScraper:

    @staticmethod
    def get_property_images(data_image: list) -> list[str]:
        return [picture_url["url"] for picture_url in data_image]

    @staticmethod
    def get_operation_type(data: str) -> str:
        if "for lease" in data:
            return "For Rent"
        if "for sale" in data:
            return "For Buy"

    @staticmethod
    def get_description(soup: BeautifulSoup) -> str:
        description = ""
        description_primary_data = []
        description_primary_block = soup.find(
            "div", {"class": "PrimaryDetailsBottom_detailsWrapper_Q1KTD"}
        )
        if description_primary_block:
            description_primary_data.append(
                description_primary_block.find(
                    "h2", {"class": "PrimaryDetailsBottom_headline_3oTbK"}
                )
            )
            description_primary_data += description_primary_block.find_all(
                "li", {"class": "PrimaryDetailsBottom_highlight_1U_wa"}
            )

        for element in description_primary_data:
            if element:
                description += element.text + "\n"

        description += soup.find(
            "div", {"class": "DescriptionPanel_description_20faq"}
        ).text
        return description

    def get_property_data(self, data: dict) -> dict:
        url_property = BASE_URL[:-1] + data["pdpUrl"]
        return {
            "url": url_property,
            "operation_type": self.get_operation_type(data["omniture"]["channel"]),
            "title": data["title"],
            "property_type": data["attributes"]["propertyTypes"][0],
            "address": data["address"]["streetAddress"],
            "region": data["address"]["suburbAddress"],
            "description": None,
            "pictures": self.get_property_images(data["photos"]),
            "price": data["details"]["price"],
            "rooms_cnt": 0,
            "area": data["attributes"]["area"],
        }
