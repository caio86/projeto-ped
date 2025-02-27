import locale
from datetime import datetime

locale.setlocale(locale.LC_ALL, "pt_BR")


class CategoriasDespesas:
    def __init__(
        self,
        cod_lancamento: int,
        cod_categoria: str,
        data_lancamento: datetime,
        valor: float,
    ) -> None:
        self.__codigo_lancamento = cod_lancamento
        self.__codigo_categoria = cod_categoria
        self.__data_lancamento = data_lancamento
        self.__valor = valor

    @property
    def codigo_lancamento(self) -> int:
        return self.__codigo_lancamento

    @property
    def codigo_categoria(self) -> str:
        return self.__codigo_categoria

    @property
    def data_lancamento(self) -> datetime:
        return self.__data_lancamento

    @property
    def valor(self) -> float:
        return self.__valor

    def __str__(self):
        return f'{self.codigo_lancamento}: {self.data_lancamento.strftime("%d/%m/%Y")} - {self.codigo_categoria} - R$ {locale.format_string("%5.2f", self.valor, True)}'

    def __lt__(self, other):  # <
        return self.codigo_lancamento < other.codigo_lancamento

    def __gt__(self, other):  # >
        return self.codigo_lancamento > other.codigo_lancamento

    def __eq__(self, other):  # ==
        return self.codigo_lancamento == other.codigo_lancamento
