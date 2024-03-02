from db.models.movimiento_model import Movimiento
from db.models.cliente_model import Cliente
from db.models.cuenta_model import Cuenta
import requests


class CuentaManager:

    @staticmethod
    def crear_cuenta(session, id_cliente: int) -> Cuenta:
        """
        Propósito:
            Crea una nueva cuenta en la base de datos.

        Args:
            cuenta (Cuenta): Instancia de la cuenta a crear.

        Returns:
            Cuenta : La cuenta creada.
        """

        cuenta = Cuenta(id_cliente=id_cliente)
        session.add(cuenta)
        session.commit()
        session.refresh(cuenta)
        return cuenta

    @staticmethod
    def consultar_saldo_disponible(session, cuenta_id: int) -> dict:
        """
        Propósito:
            Consulta el saldo disponible de una cuenta por su ID.

        Args:
            cuenta_id (int): ID de la cuenta cuyo saldo se desea consultar.

        Returns:
            dict : Diccionario con el id de la cuenta y saldo total de dicha cuenta.
        """

        query = session.query(Movimiento).filter(Movimiento.id_cuenta == cuenta_id)
        movimientos = query.all()
        monto_movimientos_egreso = 0
        monto_movimientos_ingreso = 0
        for resultado in movimientos:
            if resultado.tipo == "Egreso":
                monto_movimientos_egreso += resultado.importe
            else:
                monto_movimientos_ingreso += resultado.importe
        saldo_total = monto_movimientos_ingreso - monto_movimientos_egreso
        return {"cuenta_id": cuenta_id, "saldo_total": saldo_total}

    @staticmethod
    def consultar_cuenta(session, cuenta_id: int) -> Cuenta:
        """
        Propósito:
            Consulta una cuenta por su ID.

        Args:
            cuenta_id (int): ID de la cuenta a consultar.

        Returns:
            Cuenta : La cuenta consultada.
        """

        query = session.query(Cuenta).filter(Cuenta.id == cuenta_id)
        cuenta = query.first()
        return cuenta

    @staticmethod
    def get_usd_exchange_rate() -> float:
        """
        Propósito:
            Obtiene la cotización del dólar en el mercado.

        Returns:
            float : La cotización del dólar.
        """
        url = "https://dolarapi.com/v1/dolares/bolsa"
        response = requests.get(url)

        cotizacion = response.json()
        return cotizacion["compra"]

    @staticmethod
    def get_saldo_usd(session, cuenta_id: int) -> float:
        """
        Propósito:
            Obtiene el saldo disponible en dólares de una cuenta por su ID.

        Args:
            cuenta_id (int): ID de la cuenta cuyo saldo se desea consultar.

        Returns:
            float: El saldo disponible en dólares.
        """

        cotizacion = CuentaManager.get_usd_exchange_rate()

        cuenta = CuentaManager.consultar_saldo_disponible(cuenta_id)
        saldo_usd = cuenta["saldo_total"] / float(cotizacion)
        return saldo_usd

    @staticmethod
    def eliminar_cuentas_cliente(session, cliente_id: int) -> str:
        """
        Propósito:
            Elimina todas las cuentas asociadas al ID del cliente dado.

        Args:
            cliente_id (int): ID del cliente de las cuentas a eliminar.

        Returns:
            str: str con mensaje de confirmación de eliminación.
        """
        deleted = session.query(Cuenta).filter(Cuenta.id_cliente == cliente_id).delete()
        session.commit()
        return deleted
