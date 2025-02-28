import locale
from datetime import datetime

from categorias_despesas.categorias import CategoriasDespesas

locale.setlocale(locale.LC_ALL, "pt_BR.UTF-8")


class GestorCategoriasDespesas:
    categorias = {}

    def __init__(self) -> None:
        self.__categorias: dict[str, CategoriasDespesas] = {}

    def add(
        self,
        cod_cat: str,
        cat: str,
        date: datetime,
        valor: float,
    ):
        if cod_cat not in self.__categorias:
            self.__categorias[cod_cat] = CategoriasDespesas(cod_cat, cat)
            self.categorias[cod_cat] = cat

        self.__categorias[cod_cat].new_record(
            date,
            valor,
        )

    def get_total_cat(self, cod: str):
        return self.__categorias[cod]._ocorrencias

    def get_year_cat(self, cod: str, year: int):
        return self.__categorias[cod]._ocorrencias[year]

    def __len__(self):
        return len(self.__categorias)
