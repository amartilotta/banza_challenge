from db.models.movimiento_model import Movimiento
from db.models.cuenta_model import Cuenta


class MovimientoManager:

    @staticmethod
    def registrar_movimiento(
        session, cuenta_id: int, tipo: str, importe: int
    ) -> Movimiento:
        """
        Propósito:
            Registra un movimiento en la cuenta especificada.

        Args:
            cuenta_id (int): ID de la cuenta donde se registrará el movimiento.
            tipo (str): Tipo de movimiento ("Ingreso" o "Egreso").
            importe (int): Importe del movimiento.

        Returns:
            Movimiento : El movimiento registrado.
        """

        query = session.query(Cuenta).filter(Cuenta.id == cuenta_id)
        cuenta = query.first()  # firts()
        if not cuenta:
            raise ValueError(f"No existe una cuenta registrada con el id {cuenta_id}")
        movimiento_data = Movimiento(id_cuenta=cuenta_id, tipo=tipo, importe=importe)
        session.add(movimiento_data)
        session.commit()
        session.refresh(movimiento_data)
        return movimiento_data

    @staticmethod
    def eliminar_movimiento(session, movimiento_id: int) -> Movimiento:
        """
        Propósito:
            Elimina un movimiento por su ID.

        Args:
            movimiento_id (int): ID del movimiento a eliminar.

        Returns:
            Movimiento: El movimiento eliminado si se encontró.
        """
        movimiento = session.query(Movimiento).filter(Movimiento.id == movimiento_id)
        movimiento_borrado = movimiento.first()
        movimiento.delete()
        session.commit()
        return movimiento_borrado

    @staticmethod
    def consultar_movimiento(session, movimiento_id: int) -> Movimiento:
        """
        Propósito:
            Consulta un movimiento por su ID.

        Args:
            movimiento_id (int): ID del movimiento a consultar.

        Returns:
            Movimiento : El movimiento consultado.
        """

        query = session.query(Movimiento).filter(Movimiento.id == movimiento_id)
        movimiento = query.first()
        return movimiento
