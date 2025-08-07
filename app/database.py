from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.sql import text

from app.config import get_db_url

DATABASE_URL = get_db_url()


engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


async def init_db(session: AsyncSession) -> None:
    add_cities_query = text("""
        INSERT INTO "cities" (name) 
        VALUES
            ('Ульяновск'),
            ('Москва'),
            ('Казань'),
            ('Пермь'),
            ('Волгоград');
    """)
    add_streets_query = text("""
        INSERT INTO "streets" (name, city_id) 
        VALUES
            ('Кирова', 1),
            ('Соборная', 2),
            ('Рябикова', 1),
            ('Набережная', 1);
    """)
    add_shops_query = text("""
        INSERT INTO "shops" (name, city_id, street_id, house, opening_time, closing_time) 
        VALUES
            ('Продукты', 1, 1, '22б', '10:00:00', '22:00:00'),
            ('Электроника',	1, 3, '10а', '08:00:00', '21:00:00'),
            ('Продукты', 2, 2, '13', '08:00:00', '22:00:00');
    """)

    await session.execute(add_cities_query)
    await session.execute(add_streets_query)
    await session.execute(add_shops_query)

    try:
        await session.commit()
    except SQLAlchemyError as e:
        await session.rollback()
        raise e
