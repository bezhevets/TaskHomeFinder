import re

from bs4 import BeautifulSoup


class PropertyCardScraper:

    @staticmethod
    def find_info(pattern, block_info: list) -> str | None:
        text_list = [row.get_text(strip=True) for row in block_info]
        for item in text_list:
            match = re.search(pattern, item)
            if match:
                info = match.group(1)
                return info

    @staticmethod
    def get_property_description(soup: BeautifulSoup) -> str | None:
        try:
            description_container = soup.find("section", {"id": "description"})
            first_row_description = description_container.find(
                "h2", {"class": "css-19g4ee7"}
            ).get_text(strip=True)
            list_characters = description_container.find(
                "ul", {"class": "css-hp4qv"}
            ).find_all("li")
            characters = "".join(
                [
                    f"{row.find("span").get_text(strip=True)}\n"
                    for row in list_characters
                ]
            )
            more_description = description_container.find(
                "div", {"class": "vDetailsDescription css-1fn9tp1"}
            ).get_text(strip=True)
            description = f"{first_row_description}\n{characters}\n{more_description}"

            return description
        except AttributeError:
            return None

    @staticmethod
    def get_property_address(soup: BeautifulSoup) -> str | None:
        try:
            return soup.find("h1", {"class": "css-1mysost"}).text.strip()
        except AttributeError:
            return None

    @staticmethod
    def get_property_region(address: str) -> str | None:
        try:
            return " ".join(address.split()[-2:]) if address else None
        except IndexError:
            return None

    @staticmethod
    def get_property_price_operation_type(soup: BeautifulSoup) -> tuple:
        try:
            price_operation_type_block = soup.find("div", {"class": "css-1bcq2y2"})
            price_operation_type = price_operation_type_block.find("span").get_text(
                strip=True
            )
            list_data = price_operation_type.split(", ")
            operation_type = list_data[0] if len(list_data) >= 1 else None
            price = list_data[1] if len(list_data) >= 2 else None

            if price and operation_type == price:
                price = None

            return price, operation_type
        except AttributeError:
            return None, None

    @staticmethod
    def get_property_images(soup: BeautifulSoup) -> list[str]:
        try:
            containers = soup.find("div", {"id": "gallery"})
            list_image = containers.find_all("picture", {"class": "css-1y5c43y"})

            return list(
                set(image_url.find("img").get("src") for image_url in list_image)
            )
        except AttributeError:
            return []

    @staticmethod
    def get_property_type(soup: BeautifulSoup) -> str | None:
        try:
            block_property_type = soup.find("div", {"class": "css-12ndkug"})
            property_type = block_property_type.find("span").get_text(strip=True)
            return property_type
        except AttributeError:
            return None

    @staticmethod
    def get_property_area(soup: BeautifulSoup) -> str | None:

        try:
            block_with_area = soup.find("section", {"id": "description"}).find(
                "ul", {"class": "css-1pkuoet"}
            )
            block_info = block_with_area.find_all("div", {"class": "css-12ndkug"})
            list_info = [el for el in block_info]
            pattern = r"(?:Floor|Land)\sSize(.*$)"
            area = PropertyCardScraper.find_info(pattern, list_info)
            return area
        except AttributeError:
            return None

    def get_property_data(self, soup: BeautifulSoup) -> dict:
        address = self.get_property_address(soup)
        price, operation_type = self.get_property_price_operation_type(soup)
        return {
            "title": None,
            "property_type": self.get_property_type(soup),
            "address": address,
            "region": self.get_property_region(address),
            "description": self.get_property_description(soup),
            "pictures": self.get_property_images(soup),
            "operation_type": operation_type,
            "price": price,
            "rooms_cnt": None,
            "area": self.get_property_area(soup),
        }
