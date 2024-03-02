from db.models.cliente_model import Cliente
from db.models.categoria_model import Categoria
from db.models.categoria_cliente_model import CategoriaCliente
from db.models.movimiento_model import Movimiento
from db.models.cuenta_model import Cuenta
from managers.cuenta_manager import CuentaManager

cuenta_manager = CuentaManager()


class ClienteManager:

    @staticmethod
    def crear_cliente(session, cliente: Cliente) -> Cliente:
        """
        Propósito:
            Crea un nuevo cliente en la base de datos.

        Args:
            cliente (Cliente): Datos del cliente a crear.

        Returns:
            Cliente : El cliente creado si se realiza correctamente.
        """

        session.add(cliente)
        session.commit()
        session.refresh(cliente)
        return cliente

    @staticmethod
    def consultar_cliente(session, cliente_id: int) -> Cliente:
        """
        Propósito:
            Consulta un cliente por su ID en la base de datos.

        Args:
            cliente_id (int): ID del cliente a consultar.

        Returns:
            Cliente : El cliente consultado si se encuentra.
        """

        query = session.query(Cliente).filter(Cliente.id == cliente_id)
        cliente = query.first()
        return cliente

    @staticmethod
    def consultar_cuentas_cliente(session, cliente_id: int) -> list:
        """
        Propósito:
            Consulta las cuentas de un cliente por su ID en la base de datos.

        Args:
            cliente_id (int): ID del cliente cuyas cuentas se desean consultar.

        Returns:
            list : La lista de cuentas del cliente si se encuentran.
        """

        cliente = ClienteManager.consultar_cliente(session, cliente_id)
        if type(cliente) != Cliente:
            return "El id no pertenece a ningun cliente registrado"

        query = session.query(Cuenta).filter(Cuenta.id_cliente == cliente_id)
        cuentas = query.all()
        return cuentas

    @staticmethod
    def consultar_categorias_cliente(session, cliente_id: int) -> list:
        """
        Propósito:
            Consulta las categorías asociadas a un cliente por su ID.

        Args:
            cliente_id (int): ID del cliente cuyas categorías se desean consultar.

        Returns:
            list : Lista de categorías asociadas al cliente.
        """

        cliente = ClienteManager.consultar_cliente(session, cliente_id)
        if type(cliente) != Cliente:
            return "El id no pertenece a ningun cliente registrado"

        categorias = (
            session.query(Categoria)
            .join(CategoriaCliente)
            .filter(CategoriaCliente.id_cliente == cliente_id)
        )
        resultados = categorias.all()
        if not resultados:
            return "El cliente no tiene categorias asociadas"
        return resultados

    @staticmethod
    def consultar_saldos_cuentas_cliente(session, cliente_id: int) -> list:
        """
        Propósito:
            Consulta el saldo disponible de un cliente por su ID.

        Args:
            cliente_id (int): ID del cliente cuyo saldo se desea consultar.

        Returns:
            list : Lista de saldos disponibles por cuenta del cliente en formato JSON.
        """

        cliente = ClienteManager.consultar_cliente(session, cliente_id)
        if type(cliente) != Cliente:
            raise ValueError("El cliente no existe")

        cuentas = ClienteManager.consultar_cuentas_cliente(session, cliente_id)
        if len(cuentas) == 0:
            raise ValueError("El cliente no tiene cuentas asociadas")

        json_final = [
            cuenta_manager.consultar_saldo_disponible(session, cuenta.id)
            for cuenta in cuentas
        ]

        return json_final

    @staticmethod
    def editar_cliente(session, cliente_id: int, cliente: Cliente) -> Cliente:
        """
        Propósito:
            Edita un cliente por su ID.

        Args:
            cliente_id (int): ID del cliente a editar.
            cliente (Cliente): Instancia del cliente con los nuevos datos.

        Returns:
            Cliente : Instancia del cliente editado.
        """

        cliente_a_modificar = ClienteManager.consultar_cliente(session, cliente_id)
        if type(cliente_a_modificar) != Cliente:
            return "El cliente no existe"
        for key, value in cliente.model_dump().items():
            if value is not None:
                setattr(cliente_a_modificar, key, value)
        session.commit()
        session.refresh(cliente_a_modificar)
        return cliente_a_modificar

    @staticmethod
    def eliminar_cliente(session, cliente_id: int) -> dict:
        """
        Propósito:
            Elimina un cliente por su ID.

        Args:
            cliente_id (int): ID del cliente a eliminar.

        Returns:
            dict : dict con mensaje de confirmación de eliminación y el cliente eliminado en formato JSON.
        """

        cliente_a_eliminar = ClienteManager.consultar_cliente(session, cliente_id)
        if type(cliente_a_eliminar) != Cliente:
            return "El cliente no existe"

        cliente_borrado = cliente_a_eliminar.model_dump()

        if ClienteManager.consultar_cuentas_cliente != []:
            cuenta_manager.eliminar_cuentas_cliente(session, cliente_id)

        session.query(Cliente).filter(Cliente.id == cliente_id).delete()
        session.commit()
        return {"message": "Cliente eliminado", "cliente": cliente_borrado}

    @staticmethod
    def listar_clientes(session) -> list:
        """
        Propósito:
            Lista todos los clientes de la base de datos.

        Returns:
            list : Lista de clientes.
        """

        resultados = session.query(Cliente)

        clientes = [cliente for cliente in resultados]

        return clientes

    @staticmethod
    def agregar_cliente_a_categoria(
        session, cliente_id: int, categoria_id: int
    ) -> Cliente:
        """
        Propósito:
            Agrega un cliente a una categoría.

        Args:
            cliente_id (int): ID del cliente a agregar.
            categoria_id (int): ID de la categoría a la que se desea agregar el cliente.

        Returns:
            Cliente: el cliente al cual se le ha agregado la categoria
        """

        cliente = ClienteManager.consultar_cliente(session, cliente_id)
        if type(cliente) != Cliente:
            return "El cliente no existe"

        query = session.query(Categoria).filter(Categoria.id == categoria_id)

        relacion_cliente_categoria = CategoriaCliente(
            id_cliente=cliente_id, id_categoria=categoria_id
        )
        query = session.query(CategoriaCliente).filter(
            CategoriaCliente.id_cliente == cliente_id,
            CategoriaCliente.id_categoria == categoria_id,
        )
        existe_combinacion = query.first()

        if existe_combinacion:
            return "El cliente ya está asociado a esta categoría."
        session.add(relacion_cliente_categoria)
        session.commit()
        session.refresh(cliente)
        return cliente

    @staticmethod
    def consultar_saldo_cliente(session, cliente_id: int) -> int:
        """
        Propósito:
            Realiza la sumatoria de los saldos de todas las cuentas del cliente del id dado.

        Args:
            cliente_id (int): ID del cliente.

        Returns:
            int - el saldo total.
        """

        saldo_total = 0

        cuentas = ClienteManager.consultar_saldos_cuentas_cliente(session, cliente_id)

        for cuenta in cuentas:
            saldo_total += cuenta["saldo_total"]
        return saldo_total
