from datetime import datetime

from .LinearProbingLoadFactor import HashTable
from .organizacao_social import OrganizacaoSocial
from .receita import Receita


class GestorOrgs:
    def __init__(self):
        self.orgs = (
            HashTable()
        )  # de organizacao social    <id> id: <value> OrganizacoesSociais

    def adicionar_org(self, org: OrganizacaoSocial, data: datetime, valor: float):
        """
        Adiciona uma organização à HashTable e registra sua receita.
        ----------
        Recebe o objeto organização, o ano e o valor
        """
        try:
            org, receita = self.orgs.get(org.id)  # Obtendo a tupla
        except KeyError:
            receita = Receita()
            self.orgs.put(org.id, (org, receita))  # Armazena a tupla

        receita.adicionar_receita(data.year, valor)

    def remover_org(self, id: int):
        """
        Remove uma organização da hash table.
        ---------
        Recebe a id como argumento.
        """
        try:
            # Verifica se a organização existe na hash table
            if self.orgs.get(id):
                # Remove a organização da hash table
                carga = self.orgs.remove(id)
                return carga
            else:
                return None
        except KeyError:
            # Trata erros caso a id não seja encontrada
            print(f"Erro: Organização com id {id} não encontrada.")

    def get_nome_organizacao(self, id: int) -> str:
        """
        Retorna o nome da organização.
        ----------
        Recebe a id como argumento.
        Retorna o nome da organização ou None se não for encontrada.
        """
        try:
            # Tenta acessar a id da hash table
            org, _ = self.orgs.get(id)
            return org.nome
        except KeyError:
            raise KeyError(f"Organização com id {id} não encontrada.")

    def get_organizacoes(self) -> dict:
        """
        Retorna um dicionário com o código (chave) e o nome das organizações sociais.
        """
        orgs = {}
        for id, (org, _) in self.orgs.items():
            orgs[id] = org.nome
        return orgs

    def get_receitas(self, id: int) -> dict:
        """
        Retorna um dicionario com as receitas por ano da organizacao passada como argumento
        """
        receitas = {}
        try:
            _, receita = self.orgs.get(id)
            receitas = receita.ano_valor
            return receitas.copy()
        except KeyError:
            raise KeyError(f"Organização com id {id} não encontrada.")

        # for id, (org, receita) in self.orgs.items():  # Desempacotando a tupla
        #     print(f"id: {id} - Nome: {org.nome}")
        #     # Verifica se há receitas registradas
        #     if receita.ano_valor:  # Acessa o dicionário de receitas
        #         for ano, valor in receita.ano_valor.items():
        #             print(f"   🗓️  {ano}: R${valor:,.2f}")
        #     else:
        #         print("   Nenhuma receita registrada.")

    def listar_receita_org(self, id: int):
        """
        Lista as receitas de uma organização específica, se existir.
        ----------
        Recebe o id como argumento.
        """
        try:
            # Tenta acessar o id da hash table
            org_receita = self.orgs.get(id)  # Obtém a tupla (org, receita)
            if org_receita:
                org, receita = org_receita  # Desempacota a tupla
                print(f"Receitas da organização {id} ({org.nome}):")
                if receita.ano_valor:  # Verifica se há receitas registradas
                    for ano, valor in receita.ano_valor.items():
                        print(f" 🗓️ {ano}: R${valor:,.2f}")
                else:
                    print("   Nenhuma receita registrada.")
            else:
                print(f"Organização com id {id} não encontrada.")
        except KeyError:
            print(f"Organização com id {id} não encontrada.")

    def __len__(self):
        return len(self.orgs)

    def __str__(self):
        return f"{str(list(self.orgs.items()))}"
