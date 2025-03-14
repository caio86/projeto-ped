from datetime import datetime

from .credor import Credor


class GestaoCredor:
    """
    Classe que representa o objeto GestaoCredor.

    Attributes
    ----------
    self.credores : Lista()
        Lista que possui os credores sem repetição.

    self.receitas : Lista()
        Lista que possui as receitas anuais dos credores.


    Methods
    -------
    adicionar_credor:
        Adiciona um credor na lista de credores.

        Adiciona uma receita na lista de receitas.

    buscar_credor:
        Busca um credor na lista de credores.

    tamanho_credores:
        Mostra o tamanho da lista de credores.

    consultar_valor_total:
        Exibe o valor total lançado pelo credor.

    mostrar_credores:
        Mostra cada credor da lista de credores.

    buscar_receita:
        Busca uma receita na lista de receitas.

    mostrar_receitas_individual:
        Exibe as receitas anuais individuais de um Credor.

    mostrar_receitas:
        Mostra todas as receitas da lista de receitas.

    tamanho_receitas:
        Exibe o tamanho da lista de receitas.

    mostrar_receitas_anuais:
        Mostra todas as receitas de um determinado ano.

    """

    def __init__(self):
        """
        Classe que representa o objeto GestaoCredor.

        Attributes
        ----------
        self.credores : Lista()
            Lista que possui os credores sem repetição.

        self.receitas : Lista()
            Lista que possui as receitas anuais dos credores.

        """
        self.credores = {}  # chave: identificador, valor: Credor

    def adicionar_credor(
        self, credor: Credor, data_lancamento: str, valor_lancamento: float
    ):
        """
        Método que adiciona um Credor na lista de Credores.

        Método que adiciona uma Receita anual na lista de receitas.

        Parameters
        ----------
        credor : Credor
            Objeto Credor(Identificador + Nome do Credor)

        data_lancamento : str
            Data lançada pelo Credor.

        valor_lancamento : float
            Valor lançado pelo Credor.

        """

        data = datetime.strptime(data_lancamento, "%Y-%m-%d")

        try:
            credor_recuperado = self.credores[credor.identificador]
            try:
                credor_recuperado.receitas[data.year] += valor_lancamento
            except KeyError:
                credor_recuperado.receitas[data.year] = valor_lancamento
        except KeyError:
            self.credores[credor.identificador] = credor
            credor.receitas[data.year] = valor_lancamento

        # try:
        #     posicao = self.credores.busca(credor)
        #     receita_recuperada = self.buscar_receita(data.year, credor.identificador)
        #     if receita_recuperada is None:
        #         self.receitas.append(ReceitaAnual(
        #             data.year, credor.identificador, valor_lancamento))
        #     else:
        #         receita_recuperada.valor_lancamento += valor_lancamento

        # except KeyError:
        #     self.credores.append(credor)
        #     self.receitas.append(ReceitaAnual(
        #         data.year, credor.identificador, valor_lancamento))

        # if len(credor.identificador) > 14:
        #     id = self.buscar_credor(credor.identificador)
        #     if id == None:
        #         self.credores.append(credor)
        #         self.receitas.append(ReceitaAnual(
        #             data.year, credor.identificador, valor_lancamento))

        #     elif self.buscar_receita(data.year, credor.identificador) == None:
        #         self.receitas.append(ReceitaAnual(
        #             data.year, credor.identificador, valor_lancamento))

        #     else:
        #         self.alterar_receita(
        #             data.year, credor.identificador, valor_lancamento)

        # else:
        #     busca = self.buscar_credor(credor.desmascarar_cpf())
        #     if busca == None:
        #         credor.identificador = credor.desmascarar_cpf()
        #         self.credores.append(credor)
        #         self.receitas.append(ReceitaAnual(
        #             data.year, credor.identificador, valor_lancamento))

        #     elif self.buscar_receita(data.year, busca.identificador) == None:
        #         self.receitas.append(ReceitaAnual(
        #             data.year, busca.identificador, valor_lancamento))

        #     else:
        #         self.alterar_receita(
        #             data.year, busca.identificador, valor_lancamento)

    def buscar_credor(self, identificador: str) -> Credor | None:
        """
        Método para buscar um credor na lista de credores.

        Parameters
        ----------
        identificador : str
            Recebe um CPF ou CNPJ.

        Returns
        ----------
        Credor | None: Retorna o objeto Credor se encontrado, senão retorna None.

        Raises
        ----------
        TypeError: Se o identificador não for do tipo str.
        """
        try:
            return self.credores[identificador]
        except KeyError:
            return None
        # if type(identificador) == str:
        #     for credor in self.credores:
        #         if credor.identificador == identificador:
        #             return credor
        #     return None
        # else:
        #     raise TypeError(
        #         'O valor fornecido para o identificador não é do tipo necessário.')

    def __len__(self):
        """
        Returns
        ----------
        Retorna o tamanho da lista de credores.
        """
        return self.credores.__len__()

    def obter_valor_total(self, identificador: str):
        """
        Método para consultar o valor total (de todos os anos) lançado pelo Credor.

        Parameters
        ----------
        identificador : str
            Recebe um CPF ou CNPJ.

        Returns
        ----------
        Valor | None: Retorna o valor total do objeto Credor se encontrado, senão retorna None.

        Raises
        ----------
        KeyError: Se o identificador não existir
        """
        try:
            return sum(self.credores[identificador].receitas.values())
        except KeyError:
            raise KeyError(f"id {identificador} não está cadastrado")

        # if type(identificador) == str:
        #     valor_total = 0
        #     busca = self.buscar_credor(identificador)
        #     if busca == None:
        #         return None
        #     for receita in self.receitas:
        #         if receita.identificador == identificador:
        #             valor_total += receita.valor_lancamento

        #     return valor_total

        # else:
        #     raise TypeError(
        #         'O valor fornecido para o identificador não é do tipo necessário.')

    def listar_credores(self):
        """
        Mostra na tela a relação de credores, por cpf/cnpj e nome.

        Returns
        ----------
        Formato : Identificador - Nome do Credor
        """
        for id in sorted(self.credores.keys()):
            print(f"{id} - {self.credores[id].nome_credor}")

    def obter_receita_anual(self, identificador: str, ano: int) -> float:
        """
        Retorna o total de receitas do ano passado como parâmetro.

        Parameters
        ----------
        identificador : str
            Recebe um CPF ou CNPJ.
        ano : int
            Recebe um ano

        Returns
        ----------
        o total de receitas do ano passado como parâmetro.

        Raises
        ----------
        KeyError: Se o ano não existir
        ValueError: Se o ano for menor ou igual a zero

        """
        try:
            assert ano > 0
            return self.credores[identificador].receitas[ano]
        except KeyError:
            raise KeyError(f"Ano {ano} não está cadastrado")
        except AssertionError:
            raise ValueError("O ano deve ser maior que zero")

        # if type(ano) == int:
        #     for receita in self.receitas:
        #         if receita.ano == ano:
        #             print(receita)

        # else:
        #     raise TypeError(
        #         'O valor fornecido para o ano não é do tipo necessário.')

    def obter_receitas_todos_os_anos(self, identificador: str) -> dict:
        """
        Retorna todas as receitas de um determinado credor.

        Parameters
        ----------
        identificador : str
            Recebe um CPF ou CNPJ.

        Returns
        ----------
        dict: Retorna um dicionário com todas as receitas do credor, por ano.
              chave: ano, valor: total de receitas

              Raises
        ----------
        KeyError: Se o identificador não existir
        """
        return self.credores[identificador].receitas.copy()

