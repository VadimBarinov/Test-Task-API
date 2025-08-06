from sqlalchemy.sql import text
from sqlalchemy.ext.asyncio import AsyncSession


class BaseDAO:
    __tablename__: str | None = None

    @classmethod
    async def get_all(cls, session: AsyncSession):
        query = text("""
            SELECT * FROM "%s";
        """ % cls.__tablename__)
        result = await session.execute(query)
        return result.all()


    @classmethod
    async def get_by_id(cls, session: AsyncSession, data_id):
        query = text("""
            SELECT * FROM "%s"
            WHERE id = :data_id
        """ % cls.__tablename__).bindparams(data_id=data_id)
        result = await session.execute(query)
        return result.first()
