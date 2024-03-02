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


def test_crear_cliente():
    response = client.post("/cliente/", json={"nombre": "Facu"})
    assert response.status_code == 200
    assert response.json()["response"]["nombre"] == "Facu"


def test_consultar_cliente():
    response = client.get(f"/cliente/{1}")
    assert response.status_code == 200
    assert response.json()["response"]["nombre"] == "Facu"


def test_listar_clientes():
    response = client.get("/cliente/")
    assert response.status_code == 200
    assert isinstance(response.json()["response"], list)


def test_agregar_cliente_a_categoria_existente():
    client.post("/categoria/", json={"nombre": "Categoria 1"})
    response = client.post("/cliente/1/categoria/1")
    assert response.status_code == 200
    assert response.json()["response"]["id"] == 1
    assert response.json()["response"]["nombre"] == "Facu"


def test_editar_cliente_existente():
    response = client.put("/cliente/1", json={"nombre": "NuevoNombre"})
    assert response.status_code == 200
    assert response.json()["response"]["id"] == 1
    assert response.json()["response"]["nombre"] == "NuevoNombre"


def test_consultar_cuentas_cliente_existente():
    response = client.get("/cliente/1/cuentas")
    assert "El cliente no tiene cuentas asociadas" in response.json()["response"]


def test_consultar_categorias_cliente_existente():
    response = client.get("/cliente/1/categorias")
    assert isinstance(response.json()["response"], list)


def test_consultar_saldo_cliente_existente_con_cuentas_asociadas():
    client.post("/cuenta/1")

    response = client.get("/cliente/1/saldo")
    assert response.json()["response"] == 0


def test_eliminar_cliente_existente():
    response = client.delete("/cliente/1")
    assert response.json()["response"]["message"] == "Cliente eliminado"
    assert response.json()["response"]["cliente"]["id"] == 1
    assert response.json()["response"]["cliente"]["nombre"] == "NuevoNombre"


def test_listar_clientes_sin_clientes():
    response = client.get("/cliente/")
    assert isinstance(response.json()["response"], list)
    assert len(response.json()["response"]) == 0
