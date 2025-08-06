from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.dao.base import BaseDAO
from app.routes.cities.dao import CityDAO
from app.routes.streets.dao import StreetDAO


class ShopDAO(BaseDAO):
    __tablename__ = "shops"

    @classmethod
    async def get_full_data(cls, session: AsyncSession, **shop_data):
        query = text("""
            SELECT * FROM "%s" shop
            INNER JOIN (
                SELECT id as city_id, name as city_name
                FROM "%s"
            ) city
            ON shop.city_id = city.city_id
            INNER JOIN (
                SELECT id as street_id, name as street_name
                FROM "%s"
            ) street
            ON shop.street_id = street.street_id
            WHERE ((:street_id)::INTEGER IS NULL OR shop.street_id = (:street_id)::INTEGER)
                AND ((:street_name)::VARCHAR IS NULL OR street.street_name = (:street_name)::VARCHAR)
                AND ((:city_id)::INTEGER IS NULL OR shop.city_id = (:city_id)::INTEGER)
                AND ((:city_name)::VARCHAR IS NULL OR city.city_name = (:city_name)::VARCHAR)
                AND ((:is_open)::INTEGER IS NULL OR (:is_open)::INTEGER = 1 
                        OR CURRENT_TIME NOT BETWEEN shop.opening_time AND shop.closing_time)
                AND ((:is_open)::INTEGER IS NULL OR (:is_open)::INTEGER = 0 
                        OR CURRENT_TIME BETWEEN shop.opening_time AND shop.closing_time);
        """ % (cls.__tablename__, CityDAO.__tablename__, StreetDAO.__tablename__)).bindparams(**shop_data)
        result = await session.execute(query)
        shops_data = result.all()

        shops_result = []
        for shop in shops_data:
            shop_dict = {
                "id": shop.id,
                "name": shop.name,
                "city": {
                    "id": shop.city_id,
                    "name": shop.city_name,
                },
                "street": {
                    "id": shop.street_id,
                    "name": shop.street_name,
                    "city": {
                        "id": shop.city_id,
                        "name": shop.city_name,
                    },
                },
                "house": shop.house,
                "opening_time": shop.opening_time,
                "closing_time": shop.closing_time,
            }
            shops_result.append(shop_dict)

        return shops_result

    @classmethod
    async def add_shop(cls, session: AsyncSession, **shop_data):
        query = text("""
            INSERT INTO "%s" (
                name, 
                city_id, 
                street_id,
                house,
                opening_time,
                closing_time
                )
            VALUES (
                :name, 
                :city_id, 
                :street_id,
                :house,
                :opening_time,
                :closing_time
            )
            RETURNING id;
        """ % (cls.__tablename__, )).bindparams(**shop_data)
        result = await session.execute(query)

        try:
            await session.commit()
        except SQLAlchemyError as e:
            await session.rollback()
            raise e

        return result.scalar()