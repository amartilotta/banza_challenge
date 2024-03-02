import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from sqlmodel import SQLModel

from app import app
from dependencies import get_db

SQLALCHEMY_DATABASE_URL = "sqlite://"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
SQLModel.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


def test_registrar_movimiento_ingreso():
    client.post("/cliente/", json={"nombre": "Facu"})
    client.post("/cuenta/1")
    response = client.post("/movimiento/ingreso/1", json={"importe": 100})
    # assert response.status_code == 200
    assert response.json()["response"]["tipo"] == "Ingreso"


def test_registrar_movimiento_egreso_saldo_suficiente():
    client.post("/cuenta/", json={"id_cliente": 1})
    client.post("/movimiento/ingreso/1", json={"importe": 200})
    response = client.post("/movimiento/egreso/1", json={"importe": 100})
    assert response.status_code == 200
    assert response.json()["response"]["tipo"] == "Egreso"


def test_registrar_movimiento_egreso_saldo_insuficiente():
    client.post("/cuenta/", json={"id_cliente": 1})

    response = client.post("/movimiento/egreso/1", json={"importe": 10000})

    assert response.json()["response"] == "Saldo insuficiente en la cuenta"


def test_eliminar_movimiento():
    client.post("/cuenta/", json={"id_cliente": 1})
    ingreso = client.post("/movimiento/ingreso/1", json={"importe": 100}).json()[
        "response"
    ]
    response = client.delete(f"/movimiento/{ingreso['id']}")
    assert response.status_code == 200
    assert response.json()["response"]["id"] == ingreso["id"]


def test_consultar_movimiento():
    client.post("/cuenta/", json={"id_cliente": 1})
    ingreso = client.post("/movimiento/ingreso/1", json={"importe": 100}).json()[
        "response"
    ]
    response = client.get(f"/movimiento/{ingreso['id']}")
    assert response.status_code == 200
    assert response.json()["response"]["id"] == ingreso["id"]
