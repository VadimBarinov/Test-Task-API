from pydantic import BaseModel, Field


class SCityGet(BaseModel):
    id: int = Field(..., description="ID города")
    name: str = Field(..., description="Название города")


class SCityAdd(BaseModel):
    name: str = Field(..., description="Название города")