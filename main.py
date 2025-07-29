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


app = FastAPI()


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
async def create_city(city: schemas.City, db: Session = Depends(get_db)) -> Any:
    create_city_query = text("""
        INSERT INTO cities ("name")
        VALUES ('%s')
        RETURNING id;
    """ % (city.name, ))
    city_id = db.execute(create_city_query).scalar()
    db.commit()

    return city_id


@app.get("/city/", response_model=List[schemas.City])
async def get_all_cities(db: Session = Depends(get_db)) -> Any:
    get_cities_query = text("""
        SELECT * FROM cities;
    """)

    return db.execute(get_cities_query)


@app.post('/city//street/')
async def create_street(street: schemas.Street, db: Session = Depends(get_db)) -> Any:
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

        return street_id


@app.get('/city//street/', response_model=List[schemas.Street])
async def get_all_streets_in_this_city(city_id: int, db: Session = Depends(get_db)) -> Any:
    get_cities_query = text("""
        SELECT COUNT(*) FROM cities 
        WHERE id = %s;
    """ % (city_id, ))
    city_is_exists = db.execute(get_cities_query)

    if city_is_exists.scalar() < 1:
        raise HTTPException(status_code=400, detail="There is no city with such an ID.")

    else:
        get_streets_query = text("""
            SELECT * FROM streets
            WHERE city_id = %s;
        """ % (city_id, ))
        response_data = db.execute(get_streets_query)

        return response_data


@app.post('/shop/')
async def create_shop(shop: schemas.Shop, db: Session = Depends(get_db)) -> Any:
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

    return shop_id


@app.get('/shop/', response_model=List[schemas.ShopGet])
async def get_all_shops_with_param(
        street: int = None, city: int = None, open: int = None, db:Session = Depends(get_db)
) -> Any:
    if street and city and open and (street < 0 or city < 0 or open < 0 or open > 1):
        raise HTTPException(status_code=400, detail="Incorrect data has been entered.")

    else:

        if street:
            get_streets_query = text("""
                SELECT COUNT(*) FROM streets 
                WHERE id = %s;
            """ % (street, ))
            street_is_exists = db.execute(get_streets_query)
            if street_is_exists.scalar() < 1:
                raise HTTPException(status_code=400, detail="There is no street with such an ID.")

        if city:
            get_cities_query = text("""
                SELECT COUNT(*) FROM cities 
                WHERE id = %s;
            """ % (city, ))
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
            ("AND shops.city_id = %s" % (city, ))if city else "",
            ("AND shops.street_id = %s" % (street, )) if street else "",
            "AND CURRENT_TIME BETWEEN shops.opening_time AND shops.closing_time" if open == 1 else "",
            "AND CURRENT_TIME NOT BETWEEN shops.opening_time AND shops.closing_time" if open == 0 else "",
        ))

        return db.execute(get_shops_query)