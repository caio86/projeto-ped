import locale

from categorias_despesas.categorias import CategoriasDespesas

locale.setlocale(locale.LC_ALL, "pt_BR.UTF-8")


class GestorCategoriasDespesas:
    def __init__(self) -> None:
        self.__categorias: dict[int, list[CategoriasDespesas]] = {}
        self._anos: list[int] = []
        self._categorias: list[str] = []

    @property
    def anos(self):
        return self._anos

    @property
    def categorias(self):
        return self._categorias

    @staticmethod
    def show_value_with_locale(value: float) -> str:
        return locale.format_string("%5.2f", value, True)

    def add(self, despesa: CategoriasDespesas):
        ano = despesa.data_lancamento.year
        if ano in self.__categorias:
            self.__categorias[ano].append(despesa)
        else:
            self.__categorias[ano] = [despesa]

        if ano not in self._anos:
            self._anos.append(ano)

    def pesquisar_ano(self, ano: int):
        total = 0
        for categoria in self.__categorias[ano]:
            total += categoria.valor
            print(categoria)

        print(f"Total {ano}: R${self.show_value_with_locale(total)}")

    def mostrar_anos(self):
        total = 0
        for ano in self.__categorias:
            total_ano = 0
            for categoria in self.__categorias[ano]:
                total += categoria.valor
                total_ano += categoria.valor
                print(categoria)
            print(f"Total {ano}: R${self.show_value_with_locale(total_ano)}")
        print(f"Total: R${self.show_value_with_locale(total)}")

    def pesquisar_categoria(self, categoria: str): ...

    def __len__(self):
        qtd = 0
        for ano in self.__categorias.keys():
            qtd += len(self.__categorias[ano])
        return qtd
