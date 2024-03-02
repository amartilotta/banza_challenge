from fastapi import APIRouter, Depends
from sqlmodel import Session
from dependencies import get_db
from managers.movimiento_manager import MovimientoManager
from managers.cliente_manager import ClienteManager
from db.models.movimiento_model import MovimientoBody, Movimiento


router = APIRouter()
movimiento_manager = MovimientoManager()
cliente_manager = ClienteManager()


@router.post("/movimiento/ingreso/{id_cuenta}")
def registrar_movimiento_ingreso(
    id_cuenta: int, body: MovimientoBody, session: Session = Depends(get_db)
):

    response = movimiento_manager.registrar_movimiento(
        session, id_cuenta, "Ingreso", body.importe
    )
    return {"response": response}


@router.post("/movimiento/egreso/{id_cuenta}")
def registrar_movimiento_egreso(
    id_cuenta: int, body: MovimientoBody, session: Session = Depends(get_db)
):

    try:
        saldo = cliente_manager.consultar_saldo_cliente(session, id_cuenta)
    except ValueError as error:
        return {"response": error.args[0]}
    if float(body.importe) > float(saldo):
        return {"response": "Saldo insuficiente en la cuenta"}
    response = movimiento_manager.registrar_movimiento(
        session, id_cuenta, "Egreso", body.importe
    )
    return {"response": response}


@router.delete("/movimiento/{id}")
def eliminar_movimiento(id: int, session: Session = Depends(get_db)):

    response = movimiento_manager.eliminar_movimiento(session, id)
    return {"response": response}


@router.get("/movimiento/{id}")
def consultar_movimiento(id: int, session: Session = Depends(get_db)):

    response = movimiento_manager.consultar_movimiento(session, id)
    return {"response": response}
