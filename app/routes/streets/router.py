from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.deps import get_session
from app.routes.streets.dao import StreetDAO
from app.routes.streets.schemas import SStreetGet, SStreetAdd

router = APIRouter(
    prefix="/city/street",
    tags=["Улицы", ],
)


@router.get("/{city_id}/", summary="Получить все улицы указанного города")
async def get_all_streets_in_city(city_id: int, session: AsyncSession = Depends(get_session)) -> list[SStreetGet]:
    """
    # Получить все улицы указанного города
    ---
        :param city_id: int - ID города

        :param session: AsyncSession - Сессия БД
    ---
        :return: [{
            id: "ID улицы",
            name: "Название улицы",
            city: {
                id: "ID города",
                name: "Название города",
            },
        },] - Список улиц указанного города (JSON)
    """
    result = await StreetDAO.get_streets_in_city(session=session, city_id=city_id)
    if result is None or len(result) == 0:
        raise HTTPException(detail=f"Ошибка при получении улиц города с ID {city_id}", status_code=400)
    return result


@router.post("/add/", summary="Добавить новую улицу")
async def add_new_city(street: SStreetAdd, session: AsyncSession = Depends(get_session)) -> dict:
    """
    # Добавить новую улицу
    ---
        :param street: SStreetAdd {
            name: "Название улицы",
            city_id: "ID города",
        } - Улица (JSON)

        :param session: AsyncSession - Сессия БД
    ---
        :return: {"message": "Улица с ID ... добавлена!"} - ID добавленной улицы (JSON)
    """
    result = await StreetDAO.add_street(session=session, **street.model_dump())
    if result is None:
        raise HTTPException(detail="Ошибка при добавлении улицы", status_code=400)
    return {"message": f"Улица с ID {result} добавлена!"}