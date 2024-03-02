from typing import Optional
from sqlmodel import Field, SQLModel
from db.models.movimiento_model import Movimiento


class Cuenta(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    id_cliente: int = Field(foreign_key="cliente.id")
