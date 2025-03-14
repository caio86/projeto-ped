from .despesa import Despesa


class GestorDespesas:
    """
    Classe responsável por gerenciar uma lista de despesas.

    Atributos:
        despesas (list): Lista que armazena objetos do tipo Despesa.
    """

    def __init__(self):
        """
        Inicializa uma instância da classe GestorDespesas.

        Cria uma lista vazia para armazenar objetos do tipo Despesa.
        """
        self.despesas = []

    def adicionar_despesa(self, despesa: Despesa):
        """
        Adiciona uma despesa à lista de despesas.

        Args:
            despesa (Despesa): Objeto do tipo Despesa a ser adicionado à lista.
        """
        self.despesas.append(despesa)

    def busca(self, despesa: Despesa):
        """
        Busca uma despesa na lista com base em um objeto de referência.

        Args:
            despesa (Despesa): Objeto do tipo Despesa usado como referência para a busca.

        Returns:
            Despesa: O objeto Despesa encontrado na lista, ou None se não for encontrado.
        """
        for d in self.despesas:
            if d == despesa:
                return d
        return None

    def __len__(self):
        """
        Retorna o número de despesas armazenadas na lista.

        Returns:
            int: Número de despesas na lista.
        """
        return len(self.despesas)
