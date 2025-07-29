import sqlalchemy.exc
from typing import List, Any
from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import PlainTextResponse
from fastapi.params import Depends
from sqlalchemy import text
from sqlalchemy.orm import Session
from database import get_db
import schemas


app = FastAPI(
    title="Тестовое задание MediaSoft",
)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return PlainTextResponse(str(exc), status_code=400)

@app.exception_handler(HTTPException)
async def validation_exception_handler(request, exc):
    return PlainTextResponse(str(exc), status_code=400)

@app.exception_handler(sqlalchemy.exc.SQLAlchemyError)
async def validation_exception_handler(request, exc):
    return PlainTextResponse(str(exc), status_code=400)


@app.post('/city/')
async def create_city(city: schemas.City, db: Session = Depends(get_db)) -> PlainTextResponse:
    """
        # Создание города

        ## Args:

            city:
                id: int
                name: str

            db: Сессия базы данных

        ## Returns:

            ID созданного города
    """
    create_city_query = text("""
        INSERT INTO cities ("name")
        VALUES ('%s')
        RETURNING id;
    """ % (city.name, ))
    city_id = db.execute(create_city_query).scalar()
    db.commit()

    return PlainTextResponse(("ID of the created object: " + str(city_id)), status_code=200)


@app.get("/city/", response_model=List[schemas.City])
async def get_all_cities(db: Session = Depends(get_db)) -> Any:
    """
        # Получение всех городов

        ## Args:

            db: Сессия базы данных

        ## Returns:

            Список всех городов
    """
    get_cities_query = text("""
        SELECT * FROM cities;
    """)

    return db.execute(get_cities_query)


@app.post('/city//street/')
async def create_street(street: schemas.Street, db: Session = Depends(get_db)) -> PlainTextResponse:
    """
        # Создание улицы в указанном города

        ## Args:

            street:
                id: int
                name: str
                city_id: int

            db: Сессия базы данных

        ## Returns:

            ID созданной улицы
    """
    get_cities_query = text("""
        SELECT COUNT(*) FROM cities 
        WHERE id = %s;
    """ % (street.city_id, ))
    city_is_exists = db.execute(get_cities_query)

    if city_is_exists.scalar() < 1:
        raise HTTPException(status_code=400, detail="There is no city with such an ID.")

    else:
        create_street_query = text("""
            INSERT INTO streets (
                name,
                city_id
            )
            VALUES (
                '%s',
                %s
            )
            RETURNING id;
        """ % (street.name, street.city_id,))
        street_id = db.execute(create_street_query).scalar()
        db.commit()

        return PlainTextResponse(("ID of the created object: " + str(street_id)), status_code=200)


@app.get('/city//street/', response_model=List[schemas.StreetGet])
async def get_all_streets_of_the_city(city_id: int, db: Session = Depends(get_db)) -> Any:
    """
        # Получение всех улиц города

        ## Args:

            city_id: int

            db: Сессия базы данных

        ## Returns:

            Список всех улиц города
    """
    get_cities_query = text("""
        SELECT COUNT(*) FROM cities 
        WHERE id = %s;
    """ % (city_id, ))
    city_is_exists = db.execute(get_cities_query)

    if city_is_exists.scalar() < 1:
        raise HTTPException(status_code=400, detail="There is no city with such an ID.")

    else:
        get_streets_query = text("""
            SELECT 
            streets.id as "id",
            streets.name as "name",
            cities.name as "city"
            FROM streets, cities
            WHERE streets.city_id = cities.id
            AND streets.city_id = %s;
        """ % (city_id, ))
        response_data = db.execute(get_streets_query)

        return response_data


@app.post('/shop/')
async def create_shop(shop: schemas.Shop, db: Session = Depends(get_db)) -> PlainTextResponse:
    """
        # Создание магазина

        ## Args:

            shop:
                id: int
                name: str
                city_id: int
                street_id: int
                house: int
                opening_time: str (00:00:00)
                closing_time: str (23:59:59)

            db: Сессия базы данных

        ## Returns:

            ID созданного магазина
    """
    create_shop_query = text("""
        INSERT INTO shops (
            name,
            city_id,
            street_id,
            house,
            opening_time,
            closing_time
        )
        VALUES (
            '%s', %s, %s, %s, '%s', '%s'
        )
        RETURNING id;
    """ % (
        shop.name,
        shop.city_id,
        shop.street_id,
        shop.house,
        shop.opening_time,
        shop.closing_time
    ))

    shop_id = db.execute(create_shop_query).scalar()
    db.commit()

    return PlainTextResponse(("ID of the created object: " + str(shop_id)), status_code=200)


@app.get('/shop/', response_model=List[schemas.ShopGet])
async def get_all_shops_with_param(
        street_id: int = None, city_id: int = None, is_open: int = None, db:Session = Depends(get_db)
) -> Any:
    """
        # Получение списка магазинов
        Метод принимает параметры для фильтрации. Параметры не обязательны. В случае отсутствия параметров выводятся все магазины, если хоть один параметр есть, то по нему выполняется фильтрация.

        ## Args:

            street_id: int
            city_id: int
            is_open: int (0 - закрыт, 1 - открыт)
            (Данный статус определяется исходя из параметров
            «Время открытия», «Время закрытия» и текущего
            времени сервера)

            db: Сессия базы данных

        ## Returns:

            Список магазинов удовлетворяющих параметрам
    """
    if (is_open and (is_open < 0 or is_open > 1)) or (city_id and city_id < 0) or (street_id and street_id < 0):
        raise HTTPException(status_code=400, detail="Incorrect data has been entered.")

    else:

        if street_id:
            get_streets_query = text("""
                SELECT COUNT(*) FROM streets 
                WHERE id = %s;
            """ % (street_id,))
            street_is_exists = db.execute(get_streets_query)
            if street_is_exists.scalar() < 1:
                raise HTTPException(status_code=400, detail="There is no street with such an ID.")

        if city_id:
            get_cities_query = text("""
                SELECT COUNT(*) FROM cities 
                WHERE id = %s;
            """ % (city_id,))
            city_is_exists = db.execute(get_cities_query)
            if city_is_exists.scalar() < 1:
                raise HTTPException(status_code=400, detail="There is no city with such an ID.")

        get_shops_query = text("""
            SELECT shops.id AS "id",
                shops.name AS "name",
                cities.name AS "city",
                streets.name AS "street",
                shops.house AS "house",
                shops.opening_time AS "opening_time",
                shops.closing_time AS "closing_time"
            FROM shops, streets, cities
            WHERE shops.city_id = cities.id
                AND shops.street_id = streets.id
                AND streets.city_id = cities.id
                %s %s %s %s;
        """ % (
            ("AND shops.city_id = %s" % (city_id,))if city_id else "",
            ("AND shops.street_id = %s" % (street_id,)) if street_id else "",
            "AND CURRENT_TIME BETWEEN shops.opening_time AND shops.closing_time" if is_open == 1 else "",
            "AND CURRENT_TIME NOT BETWEEN shops.opening_time AND shops.closing_time" if is_open == 0 else "",
        ))

        return db.execute(get_shops_query)