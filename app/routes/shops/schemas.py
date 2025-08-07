import datetime
import re

from fastapi import HTTPException
from pydantic import BaseModel, Field, field_validator

from app.routes.cities.schemas import SCityGet
from app.routes.streets.schemas import SStreetGet


class SShopGet(BaseModel):
    id: int = Field(..., description="ID магазина")
    name: str = Field(..., min_length=1, description="Название магазина")
    city: SCityGet = Field(..., description="Город")
    street: SStreetGet = Field(..., description="Улица")
    house: str = Field(..., min_length=1, description="Номер дома в формате 'НОМЕРбуква'")
    opening_time: str | datetime.time = Field(..., description="Время открытия магазина в формате 'ЧЧ:ММ:СС'")
    closing_time: str | datetime.time = Field(..., description="Время закрытия магазина в формате 'ЧЧ:ММ:СС'")


class SShopAdd(BaseModel):
    name: str = Field(..., min_length=1, description="Название магазина")
    city_id: int = Field(..., description="ID города")
    street_id: int = Field(..., description="ID улицы")
    house: str = Field(..., min_length=1, description="Номер дома в формате 'НОМЕРбуква'")
    opening_time: str | datetime.time = Field(..., description="Время открытия магазина в формате 'ЧЧ:ММ:СС'")
    closing_time: str | datetime.time = Field(..., description="Время закрытия магазина в формате 'ЧЧ:ММ:СС'")

    @field_validator("house")
    @classmethod
    def house_validator(cls, values: str) -> str:
        if not re.match(r"^[0-9]{1,10}[A-Za-zА-Яа-я]?$", values):
            raise HTTPException(detail="Номер дома должен быть в формате 'НОМЕРбуква'", status_code=400)
        return values

    @field_validator("opening_time", "closing_time")
    @classmethod
    def time_validator(cls, values: str) -> datetime.time:
        try:
            hours, minutes, seconds = map(int, values.split(":"))
            if -1 < hours < 24 and -1 < minutes < 60 and -1 < seconds <= 60:
                return datetime.time(hours, minutes, seconds)
            raise ValueError
        except ValueError:
            raise HTTPException(detail="Некорректный формат времени. Введите время в формате 'ЧЧ:ММ:CC'", status_code=400)