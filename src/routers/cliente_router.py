from fastapi import APIRouter, Depends
from sqlmodel import Session
from dependencies import get_db
from managers.cliente_manager import ClienteManager
from db.models.cliente_model import Cliente


router = APIRouter()
cliente_manager = ClienteManager()


@router.post("/cliente/")
def crear_cliente(cliente_data: Cliente, session: Session = Depends(get_db)):

    response = cliente_manager.crear_cliente(session, cliente_data)
    return {"response": response}


@router.post("/cliente/{id_cliente}/categoria/{id_categoria}")
def agregar_cliente_a_categoria(
    id_cliente: int, id_categoria: int, session: Session = Depends(get_db)
):

    response = cliente_manager.agregar_cliente_a_categoria(
        session, id_cliente, id_categoria
    )
    return {"response": response}


@router.put("/cliente/{id}")
def editar_cliente(id: int, cliente_data: Cliente, session: Session = Depends(get_db)):

    response = cliente_manager.editar_cliente(session, id, cliente_data)
    return {"response": response}


@router.delete("/cliente/{id}")
def eliminar_cliente(id: int, session: Session = Depends(get_db)):

    response = cliente_manager.eliminar_cliente(session, id)
    return {"response": response}


@router.get("/cliente/")
def listar_clientes(session: Session = Depends(get_db)):

    response = cliente_manager.listar_clientes(session)
    return {"response": response}


@router.get("/cliente/{id}")
def consultar_cliente(id: int, session: Session = Depends(get_db)):

    response = cliente_manager.consultar_cliente(session, id)
    return {"response": response}


@router.get("/cliente/{id}/cuentas")
def consultar_cuentas_cliente(id: int, session: Session = Depends(get_db)):

    response = cliente_manager.consultar_cuentas_cliente(session, id)
    if response == []:
        return {"response": "El cliente no tiene cuentas asociadas"}
    return {"response": response}


@router.get("/cliente/{id}/categorias")
def consultar_categorias_cliente(id: int, session: Session = Depends(get_db)):

    response = cliente_manager.consultar_categorias_cliente(session, id)
    return {"response": response}


@router.get("/cliente/{id}/saldo")
def consultar_saldo_cliente(id: int, session: Session = Depends(get_db)):

    response = cliente_manager.consultar_saldo_cliente(session, id)
    return {"response": response}
