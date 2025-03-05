from datetime import datetime


class CategoriasDespesas:
    def __init__(
        self,
        cod_categoria: str,
        categoria: str,
    ) -> None:
        self._codigo_categoria = cod_categoria
        self._categoria = categoria
        self._ocorrencias: dict[int, float] = {}

    def new_record(self, data_lancamento: datetime, valor: float):
        ano = data_lancamento.year
        if ano not in self._ocorrencias:
            self._ocorrencias[ano] = valor
        else:
            self._ocorrencias[ano] += valor

    @property
    def codigo_categoria(self) -> str:
        return self._codigo_categoria

    @property
    def categoria(self) -> str:
        return self._categoria

    def __str__(self):
        return f"{self._categoria}: {self._ocorrencias}"

    def __lt__(self, other):  # <
        return self.codigo_categoria < other.codigo_categoria

    def __gt__(self, other):  # >
        return self.codigo_categoria > other.codigo_categoria

    def __eq__(self, other):  # ==
        return self.codigo_categoria == other.codigo_categoria
