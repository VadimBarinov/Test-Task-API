from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import init_db
from app.deps import get_session
from app.routes.cities.router import router as router_cities
from app.routes.streets.router import router as router_streets
from app.routes.shops.router import router as router_shops


app = FastAPI()

# НУЖНО НАПИСАТЬ
# @app.on_event("startup")
# async def on_startup(session: AsyncSession = Depends(get_session)):
#     await init_db(session=session)
# --------------------------------------------------------------------
# ИСПОЛЬЗОАТЬ lifespan!!!


@app.get("/", summary="Начальная страница")
def home() -> dict:
    return {"message": "Тестовое задание"}


app.include_router(router_cities)
app.include_router(router_streets)
app.include_router(router_shops)