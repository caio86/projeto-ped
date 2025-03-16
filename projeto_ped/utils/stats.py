import locale
from datetime import datetime

locale.setlocale(locale.LC_ALL, "pt_BR.UTF-8")


class Mes:
    """
    Classe responsável por armazenar e gerenciar o total de um mês específico.

    Attributes
    ----------
    __mes : int
        Número do mês.
    __total : float
        Total acumulado das despesas do mês.
    """

    def __init__(self, mes: int):
        """
        Inicializa um objeto Mes.

        Parameters
        ----------
        mes : int
            Número do mês.
        """
        self.__mes = mes
        self.__total = 0

    @property
    def total(self) -> float:
        """
        Retorna o total acumulado das despesas do mês.

        Returns
        -------
        float
            Total acumulado das despesas do mês.
        """
        return self.__total

    @property
    def mes(self) -> int:
        """
        Retorna o número do mês.

        Returns
        -------
        int
            Número do mês.
        """
        return self.__mes

    @property
    def sigla(self) -> str:
        """
        Retorna a sigla do mês.

        Returns
        -------
        str
            Sigla do mês correspondente.
        """
        try:
            meses_str = "jan fev mar abr mai jun jul ago set out nov dec"
            return meses_str.split()[self.__mes - 1]
        except IndexError:
            raise ValueError("Mês inválido.")

    def acumular(self, valor: float):
        """
        Adiciona um valor ao total acumulado das despesas do mês.

        Parameters
        ----------
        valor : float
            Valor a ser adicionado ao total acumulado.
        """
        self.__total += valor

    def __lt__(self, other):
        return self.__mes < other

    def __gt__(self, other):
        return self.__mes > other

    def __eq__(self, other):
        return self.__mes == other


class Ano:
    """
    Classe responsável por armazenar e gerenciar as estatísticas de um ano específico.

    Attributes
    ----------
    __ano : int
        Número do ano.
    __meses : list
        Lista de objetos Mes representando os meses do ano.
    __total : float
        Total acumulado das despesas do ano.
    """

    def __init__(self, ano: int):
        """
        Inicializa um objeto Ano.

        Parameters
        ----------
        ano : int
            Número do ano.
        """
        self.__ano = ano
        self.__meses = [Mes(i) for i in range(1, 13)]
        self.__total = 0

    @property
    def ano(self):
        """
        Retorna o número do ano.

        Returns
        -------
        int
            Número do ano.
        """
        return self.__ano

    @property
    def meses(self):
        """
        Retorna a lista de meses do ano.

        Returns
        -------
        list
            Lista de objetos Mes representando os meses do ano.
        """
        return self.__meses[:]

    @property
    def total(self):
        """
        Retorna o total acumulado das despesas do ano.

        Returns
        -------
        float
            Total acumulado das despesas do ano.
        """
        return self.__total

    def acumular(self, valor: float, data: datetime):
        """
        Adiciona um valor ao total acumulado das despesas do ano e do mês correspondente.

        Parameters
        ----------
        valor : float
            Valor a ser adicionado ao total acumulado.
        data : datetime
            Data da despesa, usada para determinar o mês correspondente.

        Raises
        ------
        ValueError
            Se o mês da data for inválido.
        """
        # self.__meses.index(data.month).acumular(valor)
        # self.__total += valor

        for m in self.__meses:
            if m.mes == data.month:
                m.acumular(valor)
                self.__total += valor

    def __lt__(self, other):
        return self.__ano < other

    def __gt__(self, other):
        return self.__ano > other

    def __eq__(self, other):
        return self.__ano == other


class Stats:
    """
    Classe responsável por armazenar e gerenciar as estatísticas de todos os anos.

    Attributes
    ----------
    __anos : list
        Lista de objetos Ano representando os anos.
    __total : float
        Total acumulado de todas as despesas.
    """

    def __init__(self):
        """
        Inicializa um objeto Stats.
        """
        self.__anos = []  # Lista de objetos Ano
        self.__total = 0

    @property
    def total(self):
        """
        Retorna o total acumulado de todas as despesas.

        Returns
        -------
        float
            Total acumulado de todas as despesas.
        """
        return self.__total

    def acumular(self, valor: float, data: datetime):
        """
        Adiciona um valor ao total acumulado das despesas, conforme
        mês e ano do lançamento.

        Parameters
        ----------
        valor : float
            Valor a ser acumulado.
        data : datetime
            Data da despesa.
        """

        if data.year not in self.__anos:
            self.__anos.append(Ano(data.year))
            self.__anos.sort()

        for ano in self.__anos:
            if ano.ano == data.year:
                ano.acumular(valor, data)
                self.__total += valor
                break

    def get_ano(self, ano_informado: int) -> Ano | None:
        """
        Retorna o objeto Ano correspondente ao ano especificado.

        Parameters
        ----------
        ano : int
            Número do ano.

        Returns
        -------
        Ano
            Objeto Ano correspondente ao ano especificado. None se não encontrado.
        """
        # ano_desejado = next((ano for ano in self.__anos if ano.valor == ano_informado), None)
        # return ano_desejado
        for a in self.__anos:
            if a == ano_informado:
                return a
        return None

    def get_total_por_ano(self) -> list:
        """
        Retorna uma lista de tuplas contendo o total acumulado em cada ano.

        Returns
        -------
        list
            Lista de tuplas no formato (ano, total).
        """
        return [(t.ano, t.total) for t in self.__anos]

    def get_total_por_mes(self, ano: int) -> list:
        """
        Retorna uma lista de tuplas contendo o total acumulado por mês no ano especificado.

        Parameters
        ----------
        ano : int
            Número do ano.

        Returns
        -------
        list
            Lista de tuplas no formato (sigla do mês, total).

        Raises
        ------
        AssertionError
            Se o ano especificado não possuir dados.
        """
        res = self.get_ano(ano)
        assert res is not None, "Este ano não possui dados."
        return [(t.sigla, t.total) for t in res.meses]

    def __str__(self):
        """
        Retorna uma representação em string das estatísticas.

        Returns
        -------
        str
            String formatada com o total acumulado e a porcentagem de cada ano.
        """
        r = "Estatísticas computadas:\n"
        lista_anos = [t for t in self.__anos]

        for t in lista_anos:
            r += f"{t.ano}: {locale.currency(t.total, grouping=True, symbol=True)} ({(t.total/self.__total)*100:.2f}%)\n"
        r += (
            f"Total Geral : {locale.currency(self.__total, grouping=True, symbol=True)}"
        )
        return r
