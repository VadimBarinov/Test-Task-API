from pydantic import BaseModel, Field

from app.routes.cities.schemas import SCityGet


class SStreetGet(BaseModel):
    id: int = Field(..., description="ID улицы")
    name: str = Field(..., description="Название улицы")
    city: SCityGet = Field(..., description="Город")


class SStreetAdd(BaseModel):
    name: str = Field(..., description="Название улицы")
    city_id: int = Field(..., description="ID города")