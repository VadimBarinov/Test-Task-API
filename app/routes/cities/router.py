from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.deps import get_session
from app.routes.cities.dao import CityDAO
from app.routes.cities.schemas import SCityGet
from app.routes.streets.router import router as router_streets


router = APIRouter(
    prefix="/city",
    tags=["Города",],
)

router.include_router(router_streets)


@router.get("/", summary="Получить все города")
async def get_all_cities(session: AsyncSession = Depends(get_session)) -> list[SCityGet]:
    result = await CityDAO.get_all(session=session)
    if result is None or len(result) == 0:
        raise HTTPException(detail="Города не найдены!", status_code=400)
    return result


@router.get("/get_by_id/{city_id}/", summary="Получить город по ID")
async def get_city_by_id(city_id: int, session: AsyncSession = Depends(get_session)) -> SCityGet:
    result = await CityDAO.get_by_id(session=session, data_id=city_id)
    if result is None:
        raise HTTPException(detail=f"Город c ID {city_id} не найден!", status_code=400)
    return result
