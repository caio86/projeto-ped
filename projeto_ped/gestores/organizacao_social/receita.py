class Receita:
    def __init__(self):
        self.ano_valor = {}

    def adicionar_receita(self, ano: int, valor: float):
        try:
            # self.ano_valor.get(ano)
            self.ano_valor[ano] += valor
        except KeyError:
            self.ano_valor[ano] = valor

    def __str__(self):
        return str(self.ano_valor)

