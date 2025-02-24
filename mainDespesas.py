import csv
import logging
from datetime import datetime

from AVLTree import AVLTree
from despesa import Despesa
from gestor_despesas import GestorDespesas

# abertura do arquiuvo
ficheiro = open("pagamentos_gestao_pactuada_2019_2024.csv", "r")
reader = csv.reader(ficheiro)

# Configuração do logging
# Configuração do logging
logging.basicConfig(
    filename="erros_processamento_despesa.log",  # Nome do arquivo de log
    level=logging.ERROR,  # Nível mínimo de mensagens registradas
    format="%(asctime)s \t %(levelname)s \t %(message)s",  # Formato das mensagens
    datefmt="%Y-%m-%d",  # Formato da data/hora
    # datefmt="%Y-%m-%d %H:%M:%S"  # Formato da data/hora
)


arvore_despesas = AVLTree()
gd = GestorDespesas()
organizacao_social = {}

processed = 0
loaded = 0
disregard = 0
for linha in reader:
    try:
        linha = linha[0].split(";")

        processed += 1
        if processed == 1:  # descartando o cabecalho
            disregard += 1
            continue

        loaded += 1
        #         Despesa(           codigo             , data, valor)
        despesa = Despesa(
            int(linha[4].replace('"', "")),
            datetime.strptime(linha[5].replace('"', ""), "%Y-%m-%d"),
            float(linha[13].replace('"', "")),
        )

        # adiciona na arvore binaria
        arvore_despesas.add(despesa)
        # adicionada no objeto "GestorDespesas"
        gd.adicionar_despesa(despesa)

        # mostra na tela o progresso a cada 1000 registros lidos
        if processed % 1000 == 0:
            print("progress:", processed)

        # Montando um hash table com o codigo e nome da organizacao social
        organizacao_social[int(linha[2].replace('"', ""))] = linha[3].replace('"', "")

        # if cont > 10:
        #     break
    except Exception as e:
        # se entrar aqui, houve algum problema na conversão dos dados
        # e então ele será descartado
        # print('Erro:', e)
        logging.error(linha)
        # print(linha)
        disregard += 1
print(despesa.data_lancamento)
print()
print("Total de registros processado:", processed)
print("Total de Válidos:", loaded)
print("Descartados:", disregard)
print("Len (arvore):", len(arvore_despesas))
print("Len (gd):", len(gd))

for codigo, os in organizacao_social.items():
    print(codigo, os)
# for despesa in repositorio_despesas:
#     print(despesa)

# key = Despesa(1681572,'','')
# print('busca:', repositorio_despesas.search(key))
