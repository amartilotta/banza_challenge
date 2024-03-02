from db.models.categoria_model import Categoria


class CategoriaManager:

    @staticmethod
    def crear_categoria(session, categoria: Categoria) -> Categoria:
        """
        Propósito:
            Crea una nueva categoría.

        Args:
            categoria (Categoria): Objeto de tipo Categoria que representa la nueva categoría a crear.

        Returns:
            Categoria : La categoría creada.
        """

        session.add(categoria)
        session.commit()
        session.refresh(categoria)
        return categoria
