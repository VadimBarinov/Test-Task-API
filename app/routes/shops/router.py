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

@router.post("/add/", summary="Добавить новый магазин")
async def add_new_shop(shop: SShopAdd, session: AsyncSession = Depends(get_session)) -> dict:
    result = await ShopDAO.add_shop(session=session, **shop.model_dump())
    if result is None:
        raise HTTPException(detail="Ошибка при создании магазина", status_code=400)
    return {"message": f"ID созданного магазина: {result}"}


@router.get("/get_by_filter/", summary="Получить список магазинов по фильтрам")
async def get_shops_by_filter(shop: RBShop = Depends(), session: AsyncSession = Depends(get_session)) -> list[SShopGet] | dict:
    result = await ShopDAO.get_full_data(session=session, **shop.to_dict())
    if result is None or len(result) == 0:
        raise HTTPException(detail="Магазинов нет!", status_code=400)
    return result