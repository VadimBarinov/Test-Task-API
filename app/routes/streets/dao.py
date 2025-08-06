from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import text

from app.dao.base import BaseDAO
from app.routes.cities.dao import CityDAO


class StreetDAO(BaseDAO):
    __tablename__ = "streets"

    @classmethod
    async def get_streets_in_city(cls, session: AsyncSession, city_id: int):
        query = text("""
                SELECT * FROM "%s" s
                INNER JOIN (
                    SELECT id as city_id, name as city_name 
                    FROM "%s"
                ) c
                ON s.city_id = c.city_id
                WHERE s.city_id = :city_id;
            """ % (cls.__tablename__, CityDAO.__tablename__, )).bindparams(city_id=city_id)
        result = await session.execute(query)
        streets_data = result.all()

        streets_result = []
        for street in streets_data:
            street_dict = {
                "id": street.id,
                "name": street.name,
                "city": {
                    "id": street.city_id,
                    "name": street.city_name,
                }
            }
            streets_result.append(street_dict)

        return streets_result