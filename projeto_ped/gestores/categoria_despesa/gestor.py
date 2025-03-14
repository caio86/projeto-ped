"""Módulo para gestão de categorias de despesas e análise de registros financeiros."""

from datetime import datetime

from .categoria import CategoriaDespesa


class GestorCategoriasDespesas:
    """Gerencia categorias de despesas.

    Attributes:
        categorias: Lista de tuplas contendo códigos e nomes de categorias
    """

    def __init__(self) -> None:
        self.__categorias: dict[str, CategoriaDespesa] = {}

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
            self.__categorias[cod_cat] = CategoriaDespesa(cod_cat, cat)

        self.__categorias[cod_cat].add_receita(
            date,
            valor,
        )

    def busca_categoria(self, cod: str) -> CategoriaDespesa:
        """Retorna o objeto CodigoCategoria especificado como argumento.

        Args:
            cod: Código da categoria a consultar

        Returns:
            Objeto CategoriaDespesa associado à chave, ou None caso o
            o código não exista

        Raises:
            KeyError: Se o código não existir
        """
        return self.__categorias[cod]

    def receitas(self, cod: str) -> dict[int, float]:
        """Obtém o histórico completo de ocorrências de anos e totais registrados
           para a categoria especificada.

        Args:
            cod (str): Código da categoria a consultar

        Returns:
            dict[int, float]
                - Dicionário com a chave correspondente ao ano
                - Os valores correspondentes ao total por ano
        """
        return self.__categorias[cod]._ocorrencias.copy()

    def total_receitas(self, cod: str) -> float:
        """Retorna o total de de valores acumulados em todos os anos de uma categoria.

        Args:
            cod: Código da categoria a consultar

        Returns:
            Dicionário no formato {ano: valor_total}
        """
        return sum(self.__categorias[cod]._ocorrencias.values())

    def receitas_em_um_ano(self, cod: str, year: int) -> float:
        """Obtém o total acumulado em uma categoria específica durante um ano.

        Args:
            cod: Código da categoria a consultar
            year: Ano de referência

        Returns:
            Valor total acumulado no ano especificado

        Errors:
            KeyError: Se o ano especificado não existir na categoria
        """
        return self.__categorias[cod]._ocorrencias[year]

    def __len__(self):
        return len(self.__categorias)
