import locale

from projeto_ped.despesa import GestorDespesas
from projeto_ped.gestores import GestaoCredor, GestorCategoriasDespesas, GestorOrgs
from projeto_ped.utils import DatasetInfo, Stats

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
        print("(p) Consultar despesa")
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
            case "s":
                self._running = False
                print("\nSaindo...")
            case _:
                print("\nOpção Inválida! Por favor tente novamente.")

    def run(self):
        while self._running:
            self._mostra_menu()
            user_input = input("Opção: ").strip()
            self._handle_input(user_input)

            if self._running:
                input("\nPressione Enter para continuar.")
