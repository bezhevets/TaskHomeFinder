from dataclasses import dataclass


@dataclass
class Picture:
    original_url: str


@dataclass
class Property:
    url: str
    title: str
    property_type: str
    operation_type: str
    region: str
    address: str
    description: str
    pictures: list[Picture]
    price: str
    rooms_cnt: int
    area: str
