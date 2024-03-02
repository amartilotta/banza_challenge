from db.models.categoria_model import Categoria
from sqlmodel import Field, SQLModel


class CategoriaCliente(SQLModel, table=True):
    id_categoria: int = Field(foreign_key="categoria.id", primary_key=True)
    id_cliente: int = Field(foreign_key="cliente.id", primary_key=True)
