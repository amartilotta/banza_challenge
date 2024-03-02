from fastapi import APIRouter, Depends
from sqlmodel import Session
from dependencies import get_db
from managers.cuenta_manager import CuentaManager
from db.models.cuenta_model import Cuenta


router = APIRouter()
cuenta_manager = CuentaManager()


@router.post("/cuenta/{id_cliente}")
def crear_cuenta(id_cliente: int, session: Session = Depends(get_db)):

    response = cuenta_manager.crear_cuenta(session, id_cliente)
    return {"response": response}


@router.get("/cuenta/{id_cuenta}")
def get_saldo_usd(id_cuenta: int, session: Session = Depends(get_db)):

    response = CuentaManager.get_saldo_usd(session, id_cuenta)
    return {"response": response}
