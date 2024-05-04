import re

from bs4 import BeautifulSoup


class PropertyCardScraper:

    @staticmethod
    def find_info(pattern, block_info: list) -> str | None:
        text_list = [row.text for row in block_info]
        for item in text_list:
            match = re.search(pattern, item)
            if match:
                info = match.group(1)
                return info

    @staticmethod
    def get_property_description(soup: BeautifulSoup) -> str | None:
        try:
            description_container = soup.find(
                "div", {"class": "indexstyled__Box-sc-13fwbvx-2 kVyafJ"}
            )
            first_row_description = description_container.find(
                "h1", {"class": "indexstyled__HeadingH1-sc-13fwbvx-5 iIgaYA"}
            ).get_text(strip=True)
            full_description = description_container.find(
                "div", {"class": "ViewMoreAndLessstyled__Collapse-sc-8f0p8f-3 gvTwcp"}
            ).get_text(strip=True)
            description = f"{first_row_description}\n{full_description}"

            return description
        except AttributeError:
            return None

    @staticmethod
    def get_property_address(soup: BeautifulSoup) -> str | None:
        try:
            return soup.find(
                "h1", {"class": "PriceBlockstyled__Address-sc-19x5iq3-1 bREaBX"}
            ).text.strip()
        except AttributeError:
            return None

    @staticmethod
    def get_property_region(address: str) -> str | None:
        try:
            return address.split(", ", 1)[-1] if address else None
        except IndexError:
            return None

    @staticmethod
    def get_property_price(soup: BeautifulSoup) -> str | None:
        try:
            price = soup.find(
                "span", {"class": "PriceBlockstyled__Price-sc-19x5iq3-5 eoWgNX"}
            ).text.strip()
            return price
        except AttributeError:
            return None

    @staticmethod
    def get_property_images(soup: BeautifulSoup) -> list[str]:
        containers = soup.find("div", {"class": "slider-wrapper axis-horizontal"})

        return list(set(image_url.get("data-swiper-image") for image_url in containers))

    @staticmethod
    def get_property_type(soup: BeautifulSoup) -> str:
        block_property_type = soup.find(
            "div",
            {
                "class": "Descriptionsstyled__AboutSectionContentWrapper-sc-1hf9zfm-10 jrmxSX"
            },
        )
        all_item = block_property_type.find_all(
            "li", {"class": "Descriptionsstyled__ListItem-sc-1hf9zfm-2 kORMIG"}
        )
        pattern = r"Property type(\S+)"
        property_type = PropertyCardScraper.find_info(pattern, all_item)
        return property_type

    @staticmethod
    def get_property_features(soup: BeautifulSoup) -> int:
        features_container = soup.find(
            "div", {"class": "PriceBlockstyled__DetailGroup-sc-19x5iq3-9 zroeH"}
        )
        features = features_container.find_all("span")
        rooms = 0
        for feature in features:
            feature_text = feature.text[0]
            if feature_text.isdigit():
                rooms += int(feature_text)
        return rooms

    @staticmethod
    def get_property_area(soup: BeautifulSoup) -> str | None:
        block_with_area = soup.find("div", {"class": "col-md-12 col-lg-6 col-xl-7"})
        try:
            block_info = block_with_area.find_all(
                "span", {"class": "PriceBlockstyled__Info-sc-19x5iq3-6 dIVXng"}
            )
            pattern = r"Block size:(\d+\.?\d*m²)"
            block_size = PropertyCardScraper.find_info(pattern, block_info)
            return block_size
        except AttributeError:
            return None

    def get_property_data(self, soup: BeautifulSoup) -> dict:
        address = self.get_property_address(soup)
        return {
            "title": None,
            "property_type": self.get_property_type(soup),
            "address": address,
            "region": self.get_property_region(address),
            "description": self.get_property_description(soup),
            "pictures": [],
            "price": self.get_property_price(soup),
            "rooms_cnt": self.get_property_features(soup),
            "area": self.get_property_area(soup),
        }
