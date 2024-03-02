from sqlalchemy import event
from db.models.categoria_model import Categoria
from db.models.cliente_model import Cliente
from db.models.cuenta_model import Cuenta

# Database initial data
INITIAL_DATA = {
    "categoria": [
        {
            "id": "1",
            "nombre": "Categoria 1",
        },
        {
            "id": "2",
            "nombre": "Categoria 2",
        },
        {
            "id": "3",
            "nombre": "Categoria 3",
        },
        {
            "id": "4",
            "nombre": "Categoria 4",
        },
        {
            "id": "5",
            "nombre": "Categoria 5",
        },
    ],
    "cliente": [
        {
            "id": "1",
            "nombre": "Banza Root",
        },
        {
            "id": "2",
            "nombre": "Viviana",
        },
        {
            "id": "3",
            "nombre": "Estaban",
        },
        {
            "id": "4",
            "nombre": "Nero",
        },
    ],
    "cuenta": [
        {
            "id": "1",
            "id_cliente": "1",
        },
        {
            "id": "2",
            "id_cliente": "1",
        },
        {
            "id": "3",
            "id_cliente": "2",
        },
        {
            "id": "4",
            "id_cliente": "2",
        },
        {
            "id": "5",
            "id_cliente": "3",
        },
        {
            "id": "6",
            "id_cliente": "4",
        },
        {
            "id": "7",
            "id_cliente": "4",
        },
    ],
}


def initialize_table(target, connection, **kw):
    tablename = str(target)
    if tablename in INITIAL_DATA and len(INITIAL_DATA[tablename]) > 0:
        connection.execute(target.insert(), INITIAL_DATA[tablename])


def seed_database():
    event.listen(Categoria.__table__, "after_create", initialize_table)
    event.listen(Cliente.__table__, "after_create", initialize_table)
    event.listen(Cuenta.__table__, "after_create", initialize_table)
