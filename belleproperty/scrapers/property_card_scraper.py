from bs4 import BeautifulSoup


class PropertyCardScraper:

    @staticmethod
    def get_property_description(soup: BeautifulSoup) -> str | None:
        try:
            description_container = soup.find("section", {"class": "property-summary"})
            first_row_description = description_container.find(
                "div", {"class": "row"}
            ).get_text(strip=True)
            full_description = description_container.find(
                "div", {"class": "summary"}
            ).text.strip()
            description = f"{first_row_description}\n{full_description}"

            return description
        except AttributeError:
            return None

    @staticmethod
    def get_property_address(soup: BeautifulSoup) -> str | None:
        try:
            return soup.select_one('h1[class="address"]').text.strip()
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
            price = soup.select_one('div[class="price"]').text.strip()
            return price
        except AttributeError:
            return None

    @staticmethod
    def get_property_images(soup: BeautifulSoup) -> list[str]:
        containers = soup.find_all("div", {"class": "hero-item"})
        return list(set(image_url.get("data-swiper-image") for image_url in containers))

    @staticmethod
    def get_property_info(soup: BeautifulSoup) -> dict:
        try:
            block_property_type = soup.find("div", {"class": "property-info"})

            all_item = block_property_type.find_all("div", {"class": "item"})
        except AttributeError:
            return {}
        result = {
            item.find("div", {"class": "label"})
            .text: item.find("div", {"class": "value"})
            .text
            for item in all_item
        }
        return result

    @staticmethod
    def get_property_features(soup: BeautifulSoup) -> int:
        features = soup.find_all("div", {"class": "feature"})
        rooms = 0
        for feature in features:
            feature_text = feature.text
            if feature_text.isdigit():
                rooms += int(feature_text)
        return rooms

    def get_property_data(self, soup: BeautifulSoup) -> dict:
        address = self.get_property_address(soup)
        property_info = self.get_property_info(soup)
        return {
            "title": None,
            "property_type": property_info.get("Property type"),
            "address": address,
            "region": self.get_property_region(address),
            "description": self.get_property_description(soup),
            "pictures": self.get_property_images(soup),
            "price": self.get_property_price(soup),
            "rooms_cnt": self.get_property_features(soup),
            "area": property_info.get("Home size"),
        }
