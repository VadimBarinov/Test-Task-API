from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import text

from app.dao.base import BaseDAO


class CityDAO(BaseDAO):
    __tablename__ = "cities"

    @classmethod
    async def add_city(cls, session:AsyncSession, city_name: str):
        query = text("""
            INSERT INTO "%s" (name) VALUES (:city_name) RETURNING id;
        """ % (cls.__tablename__, )).bindparams(city_name=city_name)
        result = await session.execute(query)

        try:
            await session.commit()
        except SQLAlchemyError as e:
            await session.rollback()
            raise e

        return result.scalar()