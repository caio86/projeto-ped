"""Módulo para representação de categorias de despesas e gestão de registros financeiros."""

from datetime import datetime


class CategoriasDespesas:
    """Representa uma categoria de despesas com histórico de valores acumulados por ano.

    Attributes:
        codigo_categoria: Código único identificador da categoria
        categoria: Nome descritivo da categoria
        ocorrencias: Dicionário dos anos em que a categoria aparece com o valor gasto no ano
    """

    def __init__(
        self,
        cod_categoria: str,
        categoria: str,
    ) -> None:
        self._codigo_categoria = cod_categoria
        self._categoria = categoria
        self._ocorrencias: dict[int, float] = {}

    def add_receita(self, data_lancamento: datetime, valor: float) -> None:
        """Adiciona um novo valor à categoria no ano especificado.

        Args:
            data_lancamento: Data do registro financeiro
            valor: Valor monetário a ser adicionado
        """
        ano = data_lancamento.year
        if ano not in self._ocorrencias:
            self._ocorrencias[ano] = valor
        else:
            self._ocorrencias[ano] += valor

    @property
    def codigo_categoria(self) -> str:
        """Código único identificador da categoria."""

        return self._codigo_categoria

    @property
    def categoria(self) -> str:
        """Nome descritivo da categoria."""

        return self._categoria

    @property
    def ocorrencias(self) -> dict[int, float]:
        return self._ocorrencias.copy()

    def __str__(self):
        return f"{self._categoria}: {self._ocorrencias}"

    def __lt__(self, other):  # <
        return self.codigo_categoria < other.codigo_categoria

    def __gt__(self, other):  # >
        return self.codigo_categoria > other.codigo_categoria

    def __eq__(self, other):  # ==
        return self.codigo_categoria == other.codigo_categoria
