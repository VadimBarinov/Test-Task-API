from fastapi import FastAPI
from app.routes.cities.router import router as router_cities
from app.routes.streets.router import router as router_streets
from app.routes.shops.router import router as router_shops


app = FastAPI()


@app.get("/", summary="Начальная страница")
def home() -> dict:
    return {"message": "Тестовое задание"}


app.include_router(router_cities)
app.include_router(router_streets)
app.include_router(router_shops)