
# Função para calcular os "top n" credores (CPFs e CNPJs) para um determinado ano
from collections import defaultdict

def topn_cpf(credores_dict:defaultdict, n:int, ano:int)->defaultdict:
    '''
    Função para calcular os "top n" credores (CPFs) para um determinado ano.
    O CPF deve estar formatado, totalizando 14 caracteres (xxx.xxx.xxx-xx)

    Parâmetros:
    credores_dict (defaultdict) - Dicionário com as despesas agrupadas por
    ano e credor. Cada credor tem um totalizador referente ao ano

    n (int): Quantidade de credores a serem recuperados
    ano (int): Ano de referencia

    Retorno:
    defaultdict - Dicionário com os "top n" credores (CPF) relativos
    ao ano passado como argumento
    '''
    resultado = defaultdict(lambda: defaultdict(list))

    if ano in credores_dict:
        credores = credores_dict[ano]
        cpfs = {c: v for c, v in credores.items() if len(c) == 14}  #Vai pegar o codigo de felipe para desmascarar o CPF/CNPJ e alterar o codigo depois.

        top_n_cpfs = sorted(cpfs.items(), key=lambda x: x[1], reverse=True)[:n]

        resultado[ano]['CPFs'] = top_n_cpfs
    
    return resultado

def topn_cnpj(credores_dict:defaultdict, n:int, ano:int)->defaultdict:
    '''
    Função para calcular os "top n" credores (CNPJs) para um determinado ano.
    O CNPJ deve estar formatado, totalizando 18 caracteres (xx.xxx.xxx/xxxx-xx")

    Parâmetros:
    credores_dict (defaultdict) - Dicionário com as despesas agrupadas por
    ano e credor. Cada credor tem um totalizador referente ao ano

    n (int): Quantidade de credores a serem recuperados
    ano (int): Ano de referencia

    Retorno:
    defaultdict - Dicionário com os "top n" credores (CNPJ) relativos
    ao ano passado como argumento
    '''
    resultado = defaultdict(lambda: defaultdict(list))

    if ano in credores_dict:
        credores = credores_dict[ano]
        cnpjs = {c: v for c, v in credores.items() if len(c) > 14}  

        top_n_cnpjs = sorted(cnpjs.items(), key=lambda x: x[1], reverse=True)[:n]

        resultado[ano]['CPFs'] = top_n_cnpjs
    
    return resultado


# Função para exibir os "top n" credores de um determinado ano
def prints(topn:defaultdict, chave:str, ano):
    '''
    Função para exibir os top credores de um determinado ano.

    Parâmetros:
    topn (defaultdict) - Dicionário com os top credores
    chave (str) - use 'CPFs' para listar os CPFs, e 'CNPJs' para listar os CNPJs
    ano (int) - Ano de referencia
    '''
    if chave not in ['CPFs', 'CNPJs']:
        raise ValueError(f"Chave inválida: {chave}")
        return
    
    for chave, valor in topn[ano]['CPFs']:
        print(f"{chave}: R$ {valor:14,.2f}")
    
    # print(f"Top {n} CNPJs:")
    # for cnpj, valor in topns[ano]['CNPJs']:
    #     print(f"{cnpj}: R$ {valor:,.2f}")
    print("-" * 50)




