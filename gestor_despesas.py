from despesa import Despesa


class GestorDespesas:
    def __init__(self):
        self.despesas = []

    def adicionar_despesa(self, despesa: Despesa):
        self.despesas.append(despesa)

    def busca(self, despesa: Despesa):
        for d in self.despesas:
            if d == despesa:
                return d
        return None

    def __len__(self):
        return len(self.despesas)
