from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.deps import get_session
from app.routes.streets.dao import StreetDAO
from app.routes.streets.schemas import SStreetGet

router = APIRouter(
    prefix="/street",
    tags=["Улицы", ],
)


@router.get("/{city_id}/", summary="Получить все улицы указанного города")
async def get_all_streets_in_city(city_id: int, session: AsyncSession = Depends(get_session)) -> list[SStreetGet]:
    result = await StreetDAO.get_streets_in_city(session=session, city_id=city_id)
    if result is None or len(result) == 0:
        raise HTTPException(detail=f"Ошибка при получении улиц города с ID {city_id}", status_code=400)
    return result
