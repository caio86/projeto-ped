class Credor:
    """
    Classe que representa o objeto Credor.

    Attributes
    ----------
    identificador : str
            Recebe um CPF ou CNPJ.

    nome_credor : str
            Recebe o nome do Credor.

    Methods
    -------
    __str__ :
            Exibe o CPF/CNPJ e o Nome do Credor.


    """

    def __init__(self, identificador: str, nome_credor: str):
        """
        Parameters
        ----------
        identificador : str
            Recebe um CPF ou CNPJ.

        nome_credor : str
            Recebe o nome do Credor.

        Raises
        ------
        TypeError: Se o parâmetro estiver com o tipo errado.
        """

        if type(identificador) is str and type(nome_credor) is str:
            self.identificador = identificador
            self.nome_credor = nome_credor
            self.receitas = {}  # Dicionário de Receitas. Chave: ano, Valor: float

        else:
            raise TypeError("Objeto Credor declarado com parâmetro do tipo errado.")

    def __str__(self):
        """
        Retorna uma representação em str do objeto Credor.

        Returns
        ------
        Formato: "CPF/CNPJ - Nome"
        """
        return f"{self.identificador} - {self.nome_credor}"

    def __lt__(self, other):
        return self.identificador < other.identificador

    def __eq__(self, other):
        return self.identificador == other.identificador

    def __gt__(self, other):
        return self.identificador > other.identificador
