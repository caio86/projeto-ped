"""
Processa um arquivo CSV contendo informações de despesas.

A variável 'reader' lê o arquivo CSV utilizando `csv.reader`, garantindo que o delimitador (`;`)
e as aspas (`"`) sejam tratados corretamente, evitando problemas com vírgulas indevidas.

A versão anterior do código usava `split(';')`, o que causava erros ao quebrar
strings que continham vírgulas dentro de aspas. A solução implementada usa "csv.reader(delimiter=";")"
para manter a estrutura correta do CSV.
"""

import csv
from datetime import datetime

from projeto_ped.despesa import Despesa, GestorDespesas
from projeto_ped.gestores.categoria_despesa import GestorCategoriasDespesas
from projeto_ped.gestores.credor import Credor, GestaoCredor, desmascarar_cpf
from projeto_ped.gestores.organizacao_social import GestorOrgs, OrganizacaoSocial
from projeto_ped.utils import DatasetInfo, Logger, Stats

# Abertura do arquiuvo CSV
ficheiro = open("pagamentos_gestao_pactuada_2019_2024.csv", "r", encoding="latin-1")
reader = csv.reader(
    ficheiro, delimiter=";"
)  # Delimiter está substituindo o .split(";"), pois o split estava causando problemas.

# Criando logging e informações do dataset (linhas processadas, carregadas e descartas).
logger = Logger()
datasetinfo = DatasetInfo()

# Instanciando estruturas de dados
gestor_despesas = GestorDespesas()
gestor_credor = GestaoCredor()
gestor_categoria = GestorCategoriasDespesas()
gestor_organizacao_social = GestorOrgs()

organizacao_social = {}
stats = Stats()

for linha in reader:
    try:

        datasetinfo.update_processed()
        if datasetinfo.processed == 1:  # Descartando o cabeçalho
            datasetinfo.update_disregard()
            continue

        despesa = Despesa(
            str(linha[1].replace('"', "")),  # Coluna 2, COMPETENCIA
            int(linha[2].replace('"', "")),  # Coluna 3, CODIGO_ORGANIZACAO_SOCIAL
            int(linha[4].replace('"', "")),  # Coluna 5, CODIGO_LANCAMENTO
            datetime.strptime(
                linha[5].replace('"', ""), "%Y-%m-%d"
            ),  # Coluna 6, DATA_LANCAMENTO
            str(linha[9].replace('"', "")),  # Coluna 10, CODIGO_CATEGORIA_DESPESA
            str(linha[11].replace('"', "")),  # Coluna 12, CPFCNPJ_CREDOR
            float(linha[13].replace('"', "")),  # Coluna 14, VALOR_LANCAMENTO
            str(linha[14].replace('"', "")),  # Coluna 15, OBSERVACAO_LANCAMENTO
        )

        datasetinfo.update_loaded()  # Se o objeto foi instanciado sem problemas, incrementa quantidade de linhas que foram carregadas com sucesso

        # Adiciona na árvore binária
        gestor_despesas.adicionar_despesa(despesa)

        gestor_credor.adicionar_credor(
            Credor(
                desmascarar_cpf(despesa.cpf_cpnj_credor),
                str(linha[12].replace('"', "")),  # Coluna 13, NOME_CREDOR
            ),
            despesa.data_lancamento.strftime("%Y-%m-%d"),
            despesa.valor,
        )

        gestor_categoria.add(
            despesa.codigo_categoria_despesa,
            str(linha[12].replace('"', "")),  # Coluna 11, NOME_CATEGORIA
            despesa.data_lancamento,
            despesa.valor,
        )

        gestor_organizacao_social.adicionar_org(
            OrganizacaoSocial(
                despesa.codigo_organizacao_social,
                str(linha[3].replace('"', "")),  # Coluna 11, NOME_ORGANIZACAO_SOCIAL
            ),
            despesa.data_lancamento,
            despesa.valor,
        )

        # Exibe na tela o progresso a cada 1000 registros lidos
        datasetinfo.show_progress()

        # Montando uma hash table com o codigo e nome da organizacao social
        organizacao_social[int(linha[2].replace('"', ""))] = linha[3].replace('"', "")

        stats.acumular(
            despesa.valor,
            despesa.data_lancamento,
        )

    except Exception as _:
        """
        Se entrar aqui, houve algum problema na instanciação de alguma linha do csv,
        e então ela será descartada. O cabeçalho sempre é descartado."
        """
        logger.log_error(linha)
        datasetinfo.update_disregard
        # print('Erro:', e)
        # print(linha)
        # break

# Exibindo resultado final do processamento das linhas
print("=== Estatísticas de Processamento ===")
print("Total de processado:", datasetinfo.processed)
print("Total de carregados:", datasetinfo.loaded)
print("Total de descartados:", datasetinfo.disregard)
