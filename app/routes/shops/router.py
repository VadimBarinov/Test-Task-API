from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.deps import get_session
from app.routes.shops.dao import ShopDAO
from app.routes.shops.rb import RBShop
from app.routes.shops.schemas import SShopAdd, SShopGet

router = APIRouter(
    prefix="/shop",
    tags=["Магазины", ],
)

@router.get("/get_by_filter/", summary="Получить список магазинов по фильтрам")
async def get_shops_by_filter(shop: RBShop = Depends(), session: AsyncSession = Depends(get_session)) -> list[SShopGet] | dict:
    """
    # Получить список магазинов по фильтрам
    ---
        :param street_id: int - ID улицы

        :param street_name: str - Название улицы

        :param city_id: int - ID города

        :param city_name: str - Название города

        :param is_open: int(1|0) - Открыт|Закрыт магазин

        :param session: AsyncSession - Сессия БД
    ---
        :return: [{
            id: "ID магазина",
            name: "Название магазина",
            city: {
                id: "ID города",
                name: "Название города",
            },
            street: {
                id: "ID улицы",
                name: "Название улицы",
                city: {
                    id: "ID города",
                    name: "Название города",
                },
            },
            house: "Номер дома в формате 'НОМЕРбуква'",
            opening_time: "Время открытия магазина в формате 'ЧЧ:ММ:СС'",
            closing_time: "Время закрытия магазина в формате 'ЧЧ:ММ:СС'",
        },] - Список магазинов удовлетворяющих фильтрам (JSON)
    """
    result = await ShopDAO.get_full_data(session=session, **shop.to_dict())
    if result is None or len(result) == 0:
        raise HTTPException(detail="Магазинов нет!", status_code=400)
    return result


@router.post("/add/", summary="Добавить новый магазин")
async def add_new_shop(shop: SShopAdd, session: AsyncSession = Depends(get_session)) -> dict:
    """
    # Добавить новый магазин
    ---
        :param shop: SShopAdd {
            name: "Название магазина",
            city_id: "ID города",
            street_id: "ID улицы",
            house: "Номер дома в формате 'НОМЕРбуква'",
            opening_time: "Время открытия магазина в формате 'ЧЧ:ММ:СС'",
            closing_time: "Время закрытия магазина в формате 'ЧЧ:ММ:СС'",
        } - Магазин (JSON)

        :param session: AsyncSession - Сессия БД
    ---
        :return: {"message": "ID созданного магазина: ..."} - ID добавленного магазина (JSON)
    """
    result = await ShopDAO.add_shop(session=session, **shop.model_dump())
    if result is None:
        raise HTTPException(detail="Ошибка при создании магазина", status_code=400)
    return {"message": f"ID созданного магазина: {result}"}