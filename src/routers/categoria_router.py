from fastapi import APIRouter, Depends
from sqlmodel import Session
from dependencies import get_db
from managers.categoria_manager import CategoriaManager
from db.models.categoria_model import Categoria

router = APIRouter()
categoria_manager = CategoriaManager()


@router.post("/categoria/")
def crear_categoria(categoria_data: Categoria, session: Session = Depends(get_db)):

    response = categoria_manager.crear_categoria(session, categoria_data)
    return {"response": response}
