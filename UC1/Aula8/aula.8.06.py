import random # Sempre no topo do arquivo!
def gerar_dados(qtd, min_val, max_val):
    """
    Gera uma LISTA de números aleatórios.
    - qtd: quantos números queremos na lista
    - min_val: o valor mínimo (inclusivo)
     - max_val: o valor máximo (inclusivo)
     """   
 
 # A estrutura a seguir se chama "List Comprehension".
 # É um jeito rápido de criar uma lista usando um loop.
    lista_de_dados = [random.randint(min_val, max_val) for _ in range(qtd)]
 
    return lista_de_dados
# Testando a função
dados_aleatorios = gerar_dados(5, 1, 100) # Gera 5 números entre 1 e 100
print(f"Dados gerados: {dados_aleatorios}")
def somar(a, b):
     return a + b
def subtrair(a, b):
    return a - b
def multiplicar(a, b):
    return a * b
def dividir(a, b):
    # Precisamos tratar a divisão por zero!
    # Este é um ótimo exemplo de lógica dentro de uma função.
    if b == 0:
        print("Erro: Divisão por zero não é permitida.")
        return 0 # Podemos retornar 0 ou None, ou uma string de erro
    else:
        return a / b

import random
# --- Nossas Definições de Funções (Etapa 1 e 2) ---
def gerar_dados(qtd, min_val, max_val):
    """Gera uma lista de 'qtd' números aleatórios entre 'min_val' e 'max_val'."""
    return [random.randint(min_val, max_val) for _ in range(qtd)]
def somar(a, b):
    return a + b
def subtrair(a, b):
    return a - b
def multiplicar(a, b):
    return a * b
def dividir(a, b):
    """Divide a por b, com tratamento para divisão por zero."""
    if b == 0:
        return "Erro (div/0)"
    else:
        return round(a / b, 2)

    # Arredondando para 2 casas decimais para ficar bonito
    
    # --- Nossa Integração ---

QTD_DE_DADOS = 5 # Quantos pares de números queremos testar
print("Gerando dados...")
    # Geramos duas listas de dados independentes
lista1 = gerar_dados(QTD_DE_DADOS, 1, 20)
lista2 = gerar_dados(QTD_DE_DADOS, 0, 10) # Permitindo 0 na lista 2 para testar a divisão
print(f"Lista 1: {lista1}")
print(f"Lista 2: {lista2}")
print("-"*40)
print("Iniciando Cálculos (elemento a elemento):")
    # Vamos usar um loop 'for' para "caminhar" pelas listas
    # A função 'zip' é usada para parear elementos de duas listas
for num1, num2 in zip(lista1, lista2):
    print(f"\nPar: ({num1}, {num2})")
 
     # Agora, chamamos nossas funções de cálculo com esses números
    print(f"Soma: {num1} + {num2} = {somar(num1, num2)}")
    print(f"Subtração: {num1} - {num2} = {subtrair(num1, num2)}")
    print(f"Multipl.: {num1} * {num2} = {multiplicar(num1, num2)}")
    print(f"Divisão: {num1} / {num2} = {dividir(num1, num2)}")