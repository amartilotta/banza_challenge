from sqlmodel import Field, SQLModel


class Categoria(SQLModel, table=True):
    id: int = Field(primary_key=True)
    nombre: str
