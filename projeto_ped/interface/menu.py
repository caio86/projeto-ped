import locale
from datetime import datetime

from projeto_ped.despesa import Despesa, GestorDespesas
from projeto_ped.gestores import GestaoCredor, GestorCategoriasDespesas, GestorOrgs
from projeto_ped.utils import DatasetInfo, Stats, topn_cnpj, topn_cpf

locale.setlocale(locale.LC_ALL, "pt_BR.UTF-8")


class Menu:
    def __init__(
        self,
        datasetinfo: DatasetInfo,
        gestor_despesas: GestorDespesas,
        gestor_credor: GestaoCredor,
        gestor_categoria: GestorCategoriasDespesas,
        gestor_organizacao_social: GestorOrgs,
        stats: Stats,
    ):
        self._running = True
        self.__datasetinfo = datasetinfo
        self.__gestor_despesas = gestor_despesas
        self.__gestor_credor = gestor_credor
        self.__gestor_categoria = gestor_categoria
        self.__gestor_organizacao_social = gestor_organizacao_social
        self.__stats = stats

    def _show_value_with_locale(self, value: float) -> str:
        return locale.format_string("%5.2f", value, True)

    def _mostra_menu(self) -> None:
        print("\n============= Menu Principal ==============")
        print("(c) Pesquisar Credor")
        print("(p) Pesquisar Categoria da Despesa")
        print("(o) Pesquisar Organização Social")
        print("(g) Consultar gasto por ano de lançamento")
        print("(d) Consultar despesa")
        print("(l) Listar")
        print("\tOrganização Social")
        print("\tCredores")
        print("\tCategoria de Despesa")
        print("(t) Top n")
        print("\tCPF")
        print("\tCNPJ")
        print("(e) Estatísticas")
        print("(s) sair")
        print("===========================================")

    def _handle_input(self, user_input: str):
        user_input = user_input.lower()

        match user_input:
            case "c":
                self._handle_query_credor()
            case "p":
                self._handle_query_categorias()
            case "o":
                self._handle_query_organizacao()
            case "g":
                self._handle_query_gasto_ano()
            case "d":
                self._handle_query_despesa()
            case "l":
                pass
            case "t":
                self._handle_topn()
            case "e":
                pass
            case "s":
                self._running = False
                print("\nSaindo...")
            case _:
                print("\nOpção Inválida! Por favor tente novamente.")

    def _handle_query_credor(self):
        cpf_cnpj = input("Digite o CPF/CNPJ do credor: ").strip()
        credor = self.__gestor_credor.buscar_credor(cpf_cnpj)

        if credor is None:
            print("\nCredor não existe!")
            return

        print(f"\nCredor: {credor.nome_credor}")
        print(f"{'Ano':<18} {'Total':<15}")
        print("=" * 18, "=" * 15)
        for ano, valor in credor.receitas.items():
            print(f"{ano:<18} R$ {self._show_value_with_locale(valor):>12}")

    def _handle_query_categorias(self):
        cod_cat = input("Digite o código da categoria: ").strip()
        try:
            categoria = self.__gestor_categoria.busca_categoria(cod_cat)
        except KeyError:
            print("\nCategoria não existe!")
            return

        print(f"\nCategoria: {categoria.categoria}")
        print(f"{'Ano':<18} {'Total':<15}")
        print("=" * 18, "=" * 15)
        for ano, valor in categoria.ocorrencias.items():
            print(f"{ano:<18} R$ {self._show_value_with_locale(valor):>12}")

    def _handle_query_organizacao(self):
        cod_org = int(input("Digite o código da organização: ").strip())

        try:
            nome = self.__gestor_organizacao_social.get_nome_organizacao(cod_org)
            receitas = self.__gestor_organizacao_social.get_receitas(cod_org)
        except KeyError:
            print("\nOrganização não existe!")
            return

        print(f"\nOrganizacao: {nome}")
        print(f"{'Ano':<18} {'Total':<15}")
        print("=" * 18, "=" * 15)
        for ano, valor in receitas.items():
            print(f"{ano:<18} R$ {self._show_value_with_locale(valor):>12}")

    def _handle_query_gasto_ano(self):
        ano = int(input("Digite o ano: ").strip())

        try:
            gasto_ano = self.__stats.get_total_por_mes(ano)
        except AssertionError:
            print(f"\nAno: {ano}, não possui gastos.")
            return

        print(f"\n{'Mês/Ano':<18} {'Total':<15}")
        print("=" * 18, "=" * 15)
        for mes, valor in gasto_ano:
            mes_ano = mes + "/" + str(ano)
            print(f"{mes_ano:<18} R$ {self._show_value_with_locale(valor):>12}")

    def _handle_query_despesa(self):
        cod_despesa = int(input("Digite o codigo do lançamento: ").strip())
        res = self.__gestor_despesas.busca(
            Despesa("", 0, cod_despesa, datetime(1999, 1, 1), "", "", 0, "")
        )

        if res is None:
            print("\nDespesa não existe!")
            return

        nome_os = self.__gestor_organizacao_social.get_nome_organizacao(
            res.codigo_organizacao_social
        )
        nome_categoria = self.__gestor_categoria.busca_categoria(
            res.codigo_categoria_despesa
        ).categoria

        credor = self.__gestor_credor.buscar_credor(res.cpf_cpnj_credor)

        if credor is None:
            return

        nome_credor = credor.nome_credor

        print(f"\nCredor: [{res.codigo_organizacao_social}] {nome_os}")
        print(f"Data de lançamento: {res.data_lancamento.date()}")
        print(
            f"Categoria da Despesa: [{res.codigo_categoria_despesa}] {nome_categoria}"
        )
        print(f"Credor: [{res.cpf_cpnj_credor}] {nome_credor}")
        print(f"Valor: R$ {self._show_value_with_locale(res.valor)}")

    def _handle_topn(self):
        tipo_credor = input("Digite o tipo do credor [CPF,CNPJ]: ").strip().upper()

        if tipo_credor not in ["CPF", "CNPJ"]:
            print("\nTipo de credor inválido!")
            return

        n = int(input("Digite quantos credores serção mostrados: ").strip())

        ano = int(input("Digite o ano: ").strip())

        credores_dict = {}

        for cod, credor in self.__gestor_credor.credores.items():
            for ano, valor in credor.receitas.items():
                if ano not in credores_dict:
                    credores_dict[ano] = {}
                credores_dict[ano][cod] = valor

        if tipo_credor == "CPF":
            topn = topn_cpf(credores_dict, n, ano)  # type: ignore
            chave = "CPFs"
        else:
            topn = topn_cnpj(credores_dict, n, ano)  # type: ignore
            chave = "CNPJs"

        if ano not in topn or chave not in topn[ano]:
            print(f"\nNenhum dado encontrado para o ano {ano}!")
            return

        print(f"\n{chave:<18} {'Total':<15}")
        print("=" * 18, "=" * 15)
        for chave, valor in topn[ano][chave]:
            print(f"{chave:<18} R$ {self._show_value_with_locale(valor):>12}")

    def run(self):
        while self._running:
            self._mostra_menu()
            user_input = input("Opção: ").strip()
            self._handle_input(user_input)

            if self._running:
                input("\nPressione Enter para continuar.")
