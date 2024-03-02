from fastapi import FastAPI
from sqlmodel import SQLModel
from db.seeding import seed_database
from routers.cliente_router import router as client_router
from routers.cuenta_router import router as cuenta_router
from routers.categoria_router import router as categoria_router
from routers.movimiento_router import router as movimiento_router
from db.configDB import engine

app = FastAPI()


app.include_router(client_router)
app.include_router(cuenta_router)
app.include_router(categoria_router)
app.include_router(movimiento_router)


async def initialize_database():
    seed_database()
    SQLModel.metadata.create_all(engine)


app.add_event_handler("startup", initialize_database)
