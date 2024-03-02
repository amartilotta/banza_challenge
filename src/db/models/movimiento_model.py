from typing import Optional
from sqlmodel import Field, SQLModel
from datetime import datetime


class Movimiento(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    id_cuenta: int = Field(foreign_key="cuenta.id")
    tipo: str
    importe: int
    fecha: datetime = Field(default=datetime.now())


class MovimientoBody(SQLModel):
    importe: int
