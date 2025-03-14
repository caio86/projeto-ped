import re


def calcular_digito_verificador(cpf_base: str) -> str:
    """
    Calcula os dígitos verificadores de um CPF com 9 dígitos.
    """

    def calcular_digito(cpf_parcial, pesos):
        soma = sum(int(digito) * peso for digito, peso in zip(cpf_parcial, pesos))
        resto = soma % 11
        return str(0 if resto < 2 else 11 - resto)

    primeiro_dv = calcular_digito(cpf_base, range(10, 1, -1))
    segundo_dv = calcular_digito(cpf_base + primeiro_dv, range(11, 1, -1))

    return primeiro_dv + segundo_dv


def desmascarar_cpf(cpf_mascarado: str) -> str:
    """
    Substitui os asteriscos em um CPF mascarado pelo cálculo correto dos dígitos verificadores.
    """
    if len(cpf_mascarado) != 14:
        return cpf_mascarado
    if not re.match(r"\*{3}\.\d{3}\.\d{3}-\*{2}", cpf_mascarado):
        raise ValueError("Formato inválido de CPF mascarado")

    cpf_base = "000" + cpf_mascarado[4:7] + cpf_mascarado[8:11]
    digitos_verificadores = calcular_digito_verificador(cpf_base)

    return f"000.{cpf_base[3:6]}.{cpf_base[6:9]}-{digitos_verificadores}"
