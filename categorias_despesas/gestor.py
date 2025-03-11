"""Módulo para gestão de categorias de despesas e análise de registros financeiros."""

from datetime import datetime

from categorias_despesas.categorias import CategoriasDespesas


class GestorCategoriasDespesas:
    """Gerencia categorias de despesas.

    Attributes:
        categorias: Lista de tuplas contendo códigos e nomes de categorias
    """

    def __init__(self) -> None:
        self.__categorias: dict[str, CategoriasDespesas] = {}

    @property
    def categorias(self) -> list[tuple[str, str]]:
        """Lista de categorias registradas no formato (código, nome).

        Returns:
            Pares de código/nome das categorias existentes
        """

        lista: list[tuple[str, str]] = []
        for k, v in self.__categorias.items():
            lista.append((k, v.categoria))

        return lista

    def add(
        self,
        cod_cat: str,
        cat: str,
        date: datetime,
        valor: float,
    ) -> None:
        """Adiciona um novo registro financeiro à categoria especificada.

        Se a categoria já existir, adiciona o valor à categoria existente

        Args:
            cod_cat: Código único da categoria
            cat: Nome descritivo da categoria
            date: Data do registro financeiro
            valor: Valor monetário da transação
        """

        if cod_cat not in self.__categorias:
            self.__categorias[cod_cat] = CategoriasDespesas(cod_cat, cat)

        self.__categorias[cod_cat].add_receita(
            date,
            valor,
        )

    def get_cat_ocurrencies(self, cod: str) -> tuple[dict[int, float], list[int]]:
        """Obtém o histórico completo de ocorrências e anos registrados para uma categoria.

        Args:
            cod: Código da categoria a consultar

        Returns:
            tuple[dict[int, float], list[int]]: Tupla contendo:
                - Dicionário com valores por ano
                - Lista ordenada de anos com registros
        """

        years: list[int] = []
        for year in self.__categorias[cod]._ocorrencias:
            years.append(year)
        return (self.__categorias[cod]._ocorrencias, years)

    def get_total_cat(self, cod: str):
        """Retorna todo o histórico de valores acumulados por ano de uma categoria.

        Args:
            cod: Código da categoria a consultar

        Returns:
            Dicionário no formato {ano: valor_total}
        """

        return self.__categorias[cod]._ocorrencias

    def get_year_cat(self, cod: str, year: int):
        """Obtém o total acumulado em uma categoria específica durante um ano.

        Args:
            cod: Código da categoria a consultar
            year: Ano de referência

        Returns:
            Valor total acumulado no ano especificado
        """

        return self.__categorias[cod]._ocorrencias[year]

    def __len__(self):
        return len(self.__categorias)
