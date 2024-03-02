from typing import Optional
from sqlmodel import Field, SQLModel
from db.models.categoria_cliente_model import CategoriaCliente


class Cliente(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
