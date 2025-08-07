from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.deps import get_session
from app.routes.cities.dao import CityDAO
from app.routes.cities.schemas import SCityGet, SCityAdd


router = APIRouter(
    prefix="/city",
    tags=["Города",],
)


@router.get("/", summary="Получить все города")
async def get_all_cities(session: AsyncSession = Depends(get_session)) -> list[SCityGet]:
    """
    # Получить все города
    ---
        :param session: AsyncSession - Сессия БД
    ---
        :return: [{
            id: "ID города",
            name: "Название города",
        },] - Список всех городов (JSON)
    """
    result = await CityDAO.get_all(session=session)
    if result is None or len(result) == 0:
        raise HTTPException(detail="Города не найдены!", status_code=400)
    return result


@router.get("/get_by_id/{city_id}/", summary="Получить город по ID")
async def get_city_by_id(city_id: int, session: AsyncSession = Depends(get_session)) -> SCityGet:
    """
    # Получить город по ID
    ---
        :param city_id: int - ID города

        :param session: AsyncSession - Сессия БД
    ---
        :return: {
            id: "ID города",
            name: "Название города",
        } - Город с переданным ID (JSON)
    """
    result = await CityDAO.get_by_id(session=session, data_id=city_id)
    if result is None:
        raise HTTPException(detail=f"Город c ID {city_id} не найден!", status_code=400)
    return result


@router.post("/add/", summary="Добавить новый город")
async def add_new_city(city: SCityAdd, session: AsyncSession = Depends(get_session)) -> dict:
    """
    # Добавить новый город
    ---
        :param city: SCityAdd {
            name: "Название города",
        } - Город (JSON)

        :param session: AsyncSession - Сессия БД
    ---
        :return: {"message": "Город с ID ... добавлен!"} - ID добавленного города (JSON)
    """
    result = await CityDAO.add_city(session=session, city_name=city.name)
    if result is None:
        raise HTTPException(detail="Ошибка при добавлении города", status_code=400)
    return {"message": f"Город с ID {result} добавлен!"}