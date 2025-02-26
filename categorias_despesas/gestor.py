from categorias_despesas.categorias import CategoriasDespesas


class GestorCategoriasDespesas:
    def __init__(self) -> None:
        self.__categorias: list[CategoriasDespesas] = []

    def __len__(self):
        return len(self.__categorias)
