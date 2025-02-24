from datetime import datetime


class Despesa:
    def __init__(self, codigo_lancamento: int, data_lancamento: datetime, valor: float):
        self.data_lancamento = data_lancamento
        self.valor = valor
        self.codigo_lancamento = codigo_lancamento

    def __str__(self):
        return f'{self.codigo_lancamento}: {self.data_lancamento.strftime("%d/%m/%Y")}. - R$ {self.valor:5.2f}'

    def __lt__(self, other):  # <
        return self.codigo_lancamento < other.codigo_lancamento

    def __gt__(self, other):  # >
        return self.codigo_lancamento > other.codigo_lancamento

    def __eq__(self, other):  # ==
        return self.codigo_lancamento == other.codigo_lancamento
