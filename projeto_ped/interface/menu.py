import locale
import os
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

    def _show_value_with_locale(self, value: float, decimals: int = 2) -> str:
        return locale.format_string(f"%5.{decimals}f", value, True)

    def _limpa_tela(self):
        os.system("cls" if os.name == "nt" else "clear")

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
                self._handle_listar()
            case "t":
                self._handle_topn()
            case "e":
                self._handle_estatisticas()
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
            print("\nCredor não existe!")

        print(f"\nCredor: [{res.codigo_organizacao_social}] {nome_os}")
        print(f"Data de lançamento: {res.data_lancamento.date()}")
        print(
            f"Categoria da Despesa: [{res.codigo_categoria_despesa}] {nome_categoria}"
        )
        if credor is not None:
            nome_credor = credor.nome_credor
            print(f"Credor: [{res.cpf_cpnj_credor}] {nome_credor}")
        print(f"Valor: R$ {self._show_value_with_locale(res.valor)}")

    def _handle_listar(self):
        print("(c) Credor")
        print("(p) Categoria")
        print("(o) Organização Social")
        escolha = input("Escolha o tipo: ").strip().lower()

        if escolha not in "cop":
            print("\nTipo inválido!")
            return

        match escolha:
            case "c":
                self._listar_credor()
            case "p":
                self._listar_categoria()
            case "o":
                self._listar_organizacao()

    def _listar_credor(self):
        credores = [x for x in self.__gestor_credor.credores.values()][:5]

        print(f"{'Credor':<18} {'Total':<16}")
        print("=" * 18, "=" * 16)
        for credor in credores:
            if credor is None:
                print("\nCredor não existe!")
                return

            total = sum(credor.receitas.values())
            print(
                f"{credor.identificador:<18} R$ {self._show_value_with_locale(total):>13}"
            )

    def _listar_categoria(self):
        categorias = [x for x in self.__gestor_categoria.categorias][:5]

        lc = 9
        mc = max(len(s[1]) for s in categorias)
        rc = 16

        print(f"{'Categoria':<{lc}} {'Nome':<{mc}} {'Total':<{rc}}")
        print("=" * lc, "=" * mc, "=" * rc)
        for cod_cat, cat in categorias:
            try:
                total = self.__gestor_categoria.total_receitas(cod_cat)
            except KeyError:
                print("\nCategoria não existe!")
                return

            print(
                f"{cod_cat:^{lc}} {cat:<{mc}} R$ {self._show_value_with_locale(total):>{rc-3}}"
            )

    def _listar_organizacao(self):
        organizacoes = [
            x for x in self.__gestor_organizacao_social.get_organizacoes().items()
        ][:5]

        lc = 11
        mc = max(len(s[1]) for s in organizacoes)
        rc = 16

        print(f"{'Organização':<{lc}} {'Nome':<{mc}} {'Total':<{rc}}")
        print("=" * lc, "=" * mc, "=" * rc)
        for cod_org, nome in organizacoes:
            try:
                receitas = self.__gestor_organizacao_social.get_receitas(cod_org)
            except KeyError:
                print("\nOrganização não existe!")
                return

            total = sum(receitas.values())
            print(
                f"{cod_org:^{lc}} {nome:<{mc}} R$ {self._show_value_with_locale(total):>{rc-3}}"
            )

    def _handle_topn(self):
        tipo_credor = input("Digite o tipo do credor [CPF,CNPJ]: ").strip().upper()

        if tipo_credor not in ["CPF", "CNPJ"]:
            print("\nTipo de credor inválido!")
            return

        n = int(input("Digite quantos credores serção mostrados: ").strip())

        ano = int(input("Digite o ano: ").strip())

        credores_dict = {}

        for cod, credor in self.__gestor_credor.credores.items():
            for ano_receita, valor in credor.receitas.items():
                if ano_receita not in credores_dict:
                    credores_dict[ano_receita] = {}
                credores_dict[ano_receita][cod] = valor

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

    def _handle_estatisticas(self):
        anos: list[tuple[int, float]] = self.__stats.get_total_por_ano()
        total = self.__stats.total

        maior_cpf = None
        maior_cpf_valor = 0.0

        maior_cnpj = None
        maior_cnpj_valor = 0.0

        for credor in self.__gestor_credor.credores.values():
            valor = sum(credor.receitas.values())
            if len(credor.identificador) == 14:
                if valor > maior_cpf_valor:
                    maior_cpf = credor
                    maior_cpf_valor = valor
            else:
                if valor > maior_cnpj_valor:
                    maior_cnpj = credor
                    maior_cnpj_valor = valor

        if maior_cpf is None:
            print("\nNenhum CPF cadastrado\n")

        if maior_cnpj is None:
            print("\nNenhum CNPJ cadastrado\n")

        print(
            f"\nQuantidade de lançamentos de despesas processadas: {self.__datasetinfo.loaded}"
        )

        print("Despesas por ano encontrados:")
        for ano, valor in anos:
            porcentagem = (float(valor) / float(total)) * 100
            print(
                f"\t{ano}: R$ {self._show_value_with_locale(valor, 0):>11} ({porcentagem:.0f}%)"
            )
        print(
            f"Acumulado ao longo dos anos: R$ {self._show_value_with_locale(total, 0)} (100%)"
        )

        if maior_cnpj is not None:
            print("CNPJ que recebeu mais recursos:")
            print(f"\t{maior_cnpj.identificador}")
            print(f"\t{maior_cnpj.nome_credor}")
            print(f"\tValor: R$ {self._show_value_with_locale(maior_cnpj_valor)}")

        if maior_cpf is not None:
            print("CPF que mais recebeu recursos")
            print(f"\t{maior_cpf.identificador}")
            print(f"\t{maior_cpf.nome_credor}")
            print(f"\tValor: R$ {self._show_value_with_locale(maior_cpf_valor)}")

    def run(self):
        while self._running:
            self._mostra_menu()
            user_input = input("Opção: ").strip()
            self._handle_input(user_input)

            if self._running:
                input("\nPressione Enter para continuar.")
                self._limpa_tela()
