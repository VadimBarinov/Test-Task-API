import datetime

from pydantic import BaseModel


class Shop(BaseModel):
    id: int
    name: str
    city_id: int
    street_id: int
    house: int
    opening_time: str = "00:00:00"
    closing_time: str = "23:59:59"


class ShopGet(BaseModel):
    id: int
    name: str
    city: str
    street: str
    house: int
    opening_time: datetime.time = "00:00:00"
    closing_time: datetime.time = "23:59:59"


class City(BaseModel):
    id: int
    name: str


class Street(BaseModel):
    id: int
    name: str
    city_id: int