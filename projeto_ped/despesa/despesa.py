from datetime import datetime


class Despesa:
    """
    Classe que representa uma despesa, com base nos dados extraídos de um arquivo .csv.

    Atributos:
        competencia (str): Competência da despesa (coluna 1 do arquivo .csv).
        codigo_organizacao_social (int): Código da organização social (coluna 2 do arquivo .csv).
        codigo_lancamento (int): Código do lançamento (coluna 4 do arquivo .csv).
        data_lancamento (datetime): Data do lançamento (coluna 5 do arquivo .csv).
        codigo_categoria_despesa (str): Código da categoria da despesa (coluna 9 do arquivo .csv).
        cpf_cpnj_credor (str): CPF ou CNPJ do credor (coluna 11 do arquivo .csv).
        valor (float): Valor do lançamento (coluna 13 do arquivo .csv).
        observacao_lancamento (str): Observação do lançamento (coluna 14 do arquivo .csv).
    """

    def __init__(
        self,
        competencia: str,
        codigo_organizacao_social: int,
        codigo_lancamento: int,
        data_lancamento: datetime,
        codigo_categoria_despesa: str,
        cpf_cpnj_credor: str,
        valor_lancamento: float,
        observacao_lancamento: str,
    ):
        """
        competecnia (str) = coluna[1];
        codigo_organizacao_social (int) = coluna[2];
        codigo_lancamento (int) = coluna[4];
        data_lancamento (datetime) = coluna[5];
        codigo_categoria_despesa (str) = coluna[9];
        cpf_cpnj_credor (str) = coulna[11];
        valor (float) = coluna[13];
        observacao_lancamento (str) = coluna[14].
        """
        self.competencia = competencia
        self.codigo_organizacao_social = codigo_organizacao_social
        self.codigo_lancamento = codigo_lancamento
        self.data_lancamento = data_lancamento
        self.codigo_categoria_despesa = codigo_categoria_despesa
        self.cpf_cpnj_credor = cpf_cpnj_credor
        self.valor = valor_lancamento
        self.observacao_lancamento = observacao_lancamento

    def __str__(self):
        """
        Retorna uma representação legível da despesa.

        Returns:
            #str: String formatada com o código do lançamento, data e valor.
        """
        return f'{self.codigo_lancamento}: {self.data_lancamento.strftime("%d/%m/%Y")} - R$ {self.valor:5.2f}'

    # Método __str__ alternativo, retornando todos os atributos do objeto despesa
    """
    def __str__(self):
        return (f"Competência: {self.competencia}\n"
                f"Código da Organização Social: {self.codigo_organizacao_social}\n"
                f"Código do Lançamento: {self.codigo_lancamento}\n"
                f"Data do Lançamento: {self.data_lancamento.strftime('%d/%m/%Y')}\n"
                f"Código da Categoria da Despesa: {self.codigo_categoria_despesa}\n"
                f"CPF/CNPJ do Credor: {self.cpf_cpnj_credor}\n"
                f"Valor do Lançamento: R$ {self.valor:.2f}\n"
                f"Observação do Lançamento: {self.observacao_lancamento}")
    """

    def __lt__(self, other):  # <
        """
        Método especial para comparar se uma despesa é menor que outra (operador <).

        Args:
            other (Despesa): Outra instância da classe Despesa.

        Returns:
            bool: True se o código do lançamento desta despesa for menor que o da outra.
        """
        return self.codigo_lancamento < other.codigo_lancamento

    def __gt__(self, other):  # >
        """
        Método especial para comparar se uma despesa é maior que outra (operador >).

        Args:
            other (Despesa): Outra instância da classe Despesa.

        Returns:
            bool: True se o código do lançamento desta despesa for maior que o da outra.
        """
        return self.codigo_lancamento > other.codigo_lancamento

    def __eq__(self, other):  # ==
        """
        Método especial para comparar se uma despesa é igual a outra (operador ==).

        Args:
            other (Despesa): Outra instância da classe Despesa.

        Returns:
            bool: True se o código do lançamento desta despesa for igual ao da outra.
        """
        return self.codigo_lancamento == other.codigo_lancamento
